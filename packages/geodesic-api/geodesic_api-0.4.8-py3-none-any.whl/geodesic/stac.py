
import os
import json
import uuid
from urllib.parse import unquote
from collections import defaultdict
from datetime import datetime as pydt
from typing import TYPE_CHECKING, Any, Tuple, List, Optional, Union

from dateutil.parser import ParserError, parse
import geodesic
from shapely.geometry import shape

from geodesic.bases import APIObject
from geodesic.client import get_client, raise_on_error
from geodesic.descriptors import BBoxDescr, BaseDescr, DatetimeDescr, DictDescr, GeometryDescr, ListDescr, StringDescr
from geodesic.utils.downloader import download
from geodesic.utils.gdal_utils import lookup_dtype, get_spatial_reference
from geodesic.utils.exif import get_image_geometry
from geodesic.raster import Raster
from geodesic.widgets import get_template_env, jinja_available
from geodesic.utils import DeferredImport, datetime_to_utc

arcgis = DeferredImport('arcgis')
pd = DeferredImport('pandas')
gpd = DeferredImport('geopandas')
gdal = DeferredImport('osgeo', 'gdal')
osr = DeferredImport('osgeo', 'osr')

if TYPE_CHECKING:
    gpd.GeoDataFrame = object
    pd.DataFrame = object
    gdal.Dataset = object
    osr.SpatialReference = object

    from geodesic.entanglement import Dataset
    import numpy as np


class Feature(APIObject):
    """A Geospatial feature

    Feature object, represented as an RFC7946 (https://datatracker.ietf.org/doc/html/rfc7946)
    GeoJSON Feature. Can be initialized using any compliant GeoJSON Feature.
    """
    id = StringDescr()
    bbox = BBoxDescr()
    geometry = GeometryDescr(bbox=bbox)
    properties = DictDescr()
    links = ListDescr(dict)

    def __init__(self, **obj) -> None:
        """
        Initialize the Feature by setting it's attributes
        """
        self._set_item('type', 'Feature')
        self.update(obj)

    @property
    def type(self):
        """
        the type is always Feature. This fills in for improperly constructed GeoJSON that
        doesn't have the "type" field set.
        """
        return 'Feature'

    @property
    def __geo_interface__(self) -> dict:
        """
        The Geo Interface convention (https://gist.github.com/sgillies/2217756)
        """
        return dict(**self)

    def _repr_svg_(self) -> str:
        """
        Represent this feature as an SVG to be rendered in Jupyter or similar. This
        returns an SVG representation of the geometry of this Feature
        """
        try:
            return self.geometry._repr_svg_()
        except Exception:
            return None


class FeatureListDescr(BaseDescr):
    """
    ListDescr is a list of Feature items, this sets/returns a list no matter what,
    it doesn't raise an attribute error.

    __get__ returns the list, creating it on the base object if necessary
    __set__ sets the list after validating that it is a list
    """

    def _get(self, obj: object, objtype=None) -> list:
        # Try to get the private attribute by name (e.g. '_features')
        f = getattr(obj, self.private_name, None)
        if f is not None:
            # Return it if it exists
            return f

        try:
            value = self._get_object(obj)

            # If this was set by other means, make sure the data inside are features/items
            if len(value) > 0:
                if not isinstance(value[-1], Feature):
                    dataset = getattr(obj, 'dataset', None)

                    is_stac = False
                    if 'assets' in value[0]:
                        is_stac = True
                    if is_stac:
                        self._set_object(obj, [Item(**f, dataset=dataset) for f in value])
                    else:
                        self._set_object(obj, [Feature(**f) for f in value])
        except KeyError:
            value = []
            self._set_object(obj, value)
        setattr(obj, self.private_name, value)
        return value

    def _set(self, obj: object, value: object) -> list:
        # Reset the private attribute
        setattr(obj, self.private_name, None)
        # return STAC items if a feature has an assets
        is_stac = False

        if len(value) > 0:
            f = value[0]
            if 'assets' in f:
                is_stac = True

        dataset = getattr(obj, 'dataset', None)

        if is_stac:
            self._set_object(obj, [Item(**f, dataset=dataset) for f in value])
        else:
            self._set_object(obj, [Feature(**f) for f in value])

    def _validate(self, obj: object, value: object) -> None:
        if not isinstance(value, (list, tuple)):
            raise ValueError(f"'{self.public_name}' must be a tuple or list")
        if len(value) > 0:
            if not isinstance(value[0], dict):
                raise ValueError(f"each value must be a dict/Feature/Item, not '{type(value[0])}'")
            if 'type' not in value[0]:
                raise ValueError('features are not valid GeoJSON Features')


class FeatureCollection(APIObject):
    """
    A collection of Features that is represented by a GeoJSON FeatureCollection in accordance with
    RFC7946 (https://datatracker.ietf.org/doc/html/rfc7946)

    Args:
        dataset: a `geodesic.entanglement.Dataset` associated with the FeatureCollection.
        query: a query, if any, used to initialize this from a request to Spacetime or Boson
        **obj: the underyling JSON data of the FeatureCollection to specify
    """
    features = FeatureListDescr(doc="this FeatureCollection's Feature/Item objects")
    links = ListDescr(dict, doc="links associated with this collection")

    def __init__(self, dataset: 'Dataset' = None, query: dict = None, **obj) -> None:
        # From GeoJSON
        if isinstance(obj, dict):
            self.update(obj)

        # Cache the GeoDataframe, Dataframe, and OGR layer
        self._gdf = None
        self._sedf = None
        self._ogr = None
        self._features = None

        # Query used to
        self.query = query
        self.dataset = dataset
        if self.dataset is not None:
            self._ds_type = self.dataset.data_api
            self._ds_subtype = self.dataset.item_type

        self._provenance = None

    @property
    def type(self):
        """
        the type is always FeatureCollection. This fills in for improperly constructed GeoJSON that
        doesn't have the "type" field set.
        """
        return 'FeatureCollection'

    def _repr_html_(self) -> str:
        """
        Represent this FeatureCollection as HTML, for example in a Jupyter Notebook.

        Returns:
            a str of HTML for this object
        """
        if not jinja_available():
            return self.__repr__()

        template = get_template_env().get_template("feature_collection_template.html.jinja")
        vals = defaultdict(None)
        vals['n_feats'] = len(self.features)
        return template.render(fc=self, vals=vals)

    @property
    def gdf(self) -> 'gpd.GeoDataFrame':
        """
        Return a geopandas.GeoDataFrame representation of this FeatureCollection

        Returns:
            a Geopandas GeoDataFrame of this object
        """
        if self._gdf is not None:
            return self._gdf

        df = pd.DataFrame([f.properties for f in self.features])

        geo = [f.geometry for f in self.features]
        self._gdf = gpd.GeoDataFrame(df, geometry=geo, crs="EPSG:4326")
        return self._gdf

    @property
    def sedf(self) -> 'pd.DataFrame':
        """
        Return an ArcGIS API for Python representation of this feature collection as a spatially
        enabled Pandas DataFrame

        Returns:
            a Pandas DataFrame of this object with a arcgis.features.GeoAccessor attached.
        """
        if self._sedf is not None:
            return self._sedf

        # Patch a bug in arcgis==2.0.0
        try:
            arcgis.geometry.Geometry({})
        except NameError:
            arcgis.geometry._type._HASSHAPELY = True

        df = pd.DataFrame([f.properties for f in self.features])
        geo = [arcgis.geometry.Geometry.from_shapely(f.geometry) for f in self.features]
        df.spatial.set_geometry(geo)
        self._sedf = df
        return self._sedf

    @property
    def ogr(self) -> 'gdal.Dataset':
        """
        Return an GDAL Dataset with an OGR Layer for this feature collection

        Returns:
            a gdal.Dataset for this object
        """
        if self._ogr is not None:
            return self._ogr

        feats = json.dumps(self)
        ds = gdal.OpenEx(feats, allowed_drivers=['GeoJSON'])
        self._ogr = ds
        return ds

    @property
    def __geo_interface__(self) -> dict:
        """
        Return this as a GeoJSON dictionary

        Returns:
            a dictionary of this object representing GeoJSON
        """
        return dict(self)

    @property
    def _next_link(self):
        """
        Get the link with relation "next" if any.

        Returns:
            the link if it exists, None otherwise
        """
        for link in self.links:
            if link.get("rel", None) == "next":
                return link

    @property
    def _next_page(self) -> Union[None, dict]:
        link = self._next_link
        if link is None:
            return
        href = link.get('href')
        if href is None:
            return

        href = unquote(href)

        method = link.get('method', 'GET')

        if method.lower() == 'get':
            return raise_on_error(get_client().get(href)).json()
        else:
            body = link.get('body', {})
            if link.get('merge', False):
                body.update(self.query)

            return raise_on_error(get_client().post(href, **body)).json()

    def next_page(self) -> 'FeatureCollection':
        fc = self._next_page
        if fc is None:
            return FeatureCollection()
        return FeatureCollection(**fc)

    def get_all(self) -> None:
        # Reset derived properties
        self._gdf = None
        self._sedf = None
        self._ogr = None

        next_page = self._next_page

        # Get features
        features = self.features

        while next_page is not None:
            if len(next_page.get('features', [])) == 0:
                self.features = features
                return

            features.extend(next_page["features"])
            self.links = next_page.get('links', [])
            next_page = self._next_page

        # Set features
        self.features = features

    def rasterize(
            self,
            property_name: str = None,
            dtype: 'np.dtype' = None,
            reference_dataset: 'gdal.Dataset' = None,
            shape: tuple = None,
            geo_transform: tuple = None,
            spatial_reference: Union[str, int, 'osr.SpatialReference'] = None,
            return_dataset: bool = True) -> Union['np.ndarray', 'gdal.Dataset']:
        """
        Rasterize this FeatureCollection given requirements on the input image

        Args:
            property_name: the name of the property to rasterize
            dtype: the numpy datatype you'd like for the output
            reference_dataset: a gdal.Dataset (image) that we would like to use as reference.
                Output will have the same shape, geo_transform, and spatial_reference
            shape: a tuple of ints representing the output shape (if reference_dataset is None)
            geo_transform: a tuple of affine transformation (if reference_dataset is None)
            spatial_reference: the spatial reference of the output (if reference_dataset is None)
            return_dataset: return the gdal.Dataset instead of a numpy array.
        """

        if reference_dataset is not None:
            driver = reference_dataset.GetDriver()
            gt = reference_dataset.GetGeoTransform()
            spatial_reference = reference_dataset.GetSpatialRef()
            xsize = reference_dataset.RasterXSize
            ysize = reference_dataset.RasterYSize
        else:
            driver = gdal.GetDriverByName("GTiff")
            gt = geo_transform
            ysize, xsize = shape
            spatial_reference = get_spatial_reference(spatial_reference)

        datatype = lookup_dtype(dtype)

        fname = f'/vsimem/{str(uuid.uuid4())}.tif'

        target_ds = driver.Create(fname, xsize, ysize, 1, datatype)
        target_ds.SetGeoTransform((gt[0], gt[1], 0, gt[3], 0, gt[5]))
        target_ds.SetSpatialRef(spatial_reference)

        options = gdal.RasterizeOptions(attribute=property_name)
        _ = gdal.Rasterize(target_ds, self.ogr, options=options)
        if return_dataset:
            return target_ds

        return target_ds.ReadAsArray()


class Asset(APIObject):
    """
    A STAC Asset object. Basically contains links and metadata for a STAC Asset

    Args:
        **obj: the attributes of this Asset
    """
    href = StringDescr()
    title = StringDescr()
    description = StringDescr()
    type = StringDescr()
    roles = ListDescr(str)

    def __init__(self, **obj) -> None:
        super().__init__(**obj)
        self._local = None

    def has_role(self, role: str) -> bool:
        """
        Does this have a requested role?

        Returns:
            True if yes, False if no
        """
        for r in self.roles:
            if role == r:
                return True
        return False

    @property
    def local(self) -> str:
        """
        Get the local path to this asset, if any

        Returns:
            a local path to this asset if downloaded, '' otherwise
        """
        if self._local is not None:
            return self._local

        self._local = self.get('local', '')
        return self._local

    @local.setter
    def local(self, local: str) -> None:
        """
        Set the local path to this asset after downloading

        Args:
            local: the local path
        """
        self._local = local
        self._set_item('local', local)

    @local.deleter
    def local(self) -> None:
        """
        Delete the local attribute and the underlying file in the file system.
        """
        path = self.pop('local')
        self._local = None
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def new() -> 'Asset':
        """
        Returns a new asset with all the fields empty
        """
        return Asset(
            **{
                "href": '',
                "title": '',
                "type": '',
                "description": '',
                "roles": [],
            }
        )

    def download(self, out_dir: str = None) -> str:
        """
        Download the asset to a local directory, returns the full path to the asset.

        Args:
            out_dir: The directory to download the asset too. A temp dir will be used instead

        Returns:
            the path that was actually used
        """

        if self._local is not None and self._local != '':
            return self._local

        path = download(self.href, out_dir)
        self.local = path
        return path


class AssetsDescr(BaseDescr):
    """
    A dictionary of Asset objects

    __get__ returns the dictionary, ensuring they are indeed Assets, not plain dicts
    __set__ sets the Assets, coercing to Assets if they are dicts

    """

    def _get(self, obj: object, objtype=None) -> dict:
        # Try to get the private attribute by name (e.g. '_assets')
        assets = getattr(obj, self.private_name, None)
        if assets is not None:
            # Return it if it exists
            return assets

        try:
            assets = self._get_object(obj)
            setattr(obj, self.private_name, assets)
        except KeyError:
            assets = {}
            self._set_object(obj, assets)
        return assets

    def _set(self, obj: object, value: object) -> None:
        self._set_object(obj, {
            asset_name: Asset(**asset) for asset_name, asset in value.items()
        })

    def _validate(self, obj: object, value: object) -> None:
        if not isinstance(value, dict):
            raise ValueError(f"'{self.public_name}' must be a dict of dicts/Assets")

        for asset_name, asset in value.items():
            if not isinstance(asset_name, str):
                raise ValueError("asset name must be a string")
            if not isinstance(asset, dict):
                raise ValueError("asset must be a dict/Asset")


class Item(Feature):
    """Class representing a STAC item.

    Implements additional STAC properties on top of a :class:`geodesic.stac.feature`

    Args:
        obj: A python object representing a STAC item.
        dataset: The dataset object this Item belongs to.

    """
    id = StringDescr(doc="the string id for this item")
    collection = StringDescr(doc="what collection this item belongs to")
    assets = AssetsDescr(doc="the assets for this item")
    datetime = DatetimeDescr(nested='properties', doc="the timestamp of this item")
    start_datetime = DatetimeDescr(nested='properties', doc="the start timestamp of this item")
    end_datetime = DatetimeDescr(nested='properties', doc="the end timestamp of this item")
    stac_extensions = ListDescr(str)

    def __init__(self, dataset: 'Dataset' = None, **obj) -> None:
        super().__init__(**obj)
        self.item_type = 'unknown'
        if dataset is not None:
            self.item_type = dataset.item_type
            self.dataset = dataset

    def _repr_html_(self) -> str:
        """
        Represent this Item as HTML

        Returns:
            a str of the HTML representation
        """

        if "thumbnail" in self.assets:
            href = self.assets["thumbnail"]["href"]
            width = 500
            if href == "https://seerai.space/images/Logo.svg":
                width = 100

            return f'<img src="{href}" style="width: {width}px;"></img>'
        else:
            try:
                svg = self._repr_svg_()
                if svg is None:
                    raise Exception()
            except Exception:
                href = "https://seerai.space/images/Logo.svg"
                width = 100
                return f'<img src="{href}" style="width: {width}px;"></img>'

    @property
    def pfs(self) -> dict:
        """Get information about this item from PFS

        If this item was produced by running in a Pachyderm pipeline, all of the relevant Pachyderm
        info will be stored in here. This allows the provenance of an item to be traced.
        """
        return {
            "pfs:repo": self.properties.get("pfs:repo", None),
            "pfs:commit": self.properties.get("pfs:commit", None),
            "pfs:path": self.properties.get("pfs:path", None),
        }

    def set_pfs(self, repo: str = None, commit: str = None, path: str = None) -> None:
        if repo is not None:
            self.properties["pfs:repo"] = repo
        if commit is not None:
            self.properties["pfs:commit"] = commit
        if path is not None:
            self.properties["pfs:path"] = path

    @property
    def raster(self) -> Raster:
        """
        Returns a Raster item associated with this. Allows for local image processing
        without explicity GDAL calls in some small number of instances
        """
        if self.item_type != "raster":
            raise ValueError(
                "item must be of raster type, is: '{0}'".format(self.item_type)
            )
        return Raster(self, dataset=self.dataset)

    @staticmethod
    def new(dataset: 'Dataset' = None) -> 'Item':
        """
        Create a new Item with blank fields
        """
        return Item(
            **{
                "type": "Feature",
                "id": '',
                "collection": '',
                "stac_extensions": [],
                "properties": {},
                "assets": {},
                "links": [],
            },
            dataset=dataset,
        )

    @staticmethod
    def from_image(path: str, **item):
        """
        Creates a new Item using the EXIF header to locate the image. This is useful
        when an asset is derived from a photolog of similar

        Args:
            path: a path to the file
            **item: any additional parameters to pass to the Item constructor
        """
        try:
            g = get_image_geometry(path)
        except Exception as e:
            raise ValueError("unable to extract geometry from image") from e

        # create a new asset
        i = Item(**item)

        # Set some basic parameters
        i.geometry = g
        i.id = item.pop('id', path)

        # Create the asset for this image
        img = Asset.new()
        img.href = path
        img.title = path
        img.description = "local image"

        # And a thumbnail asset
        thumb = Asset.new()
        thumb.href = path
        thumb.title = path
        thumb.description = "thumbnail"
        thumb.roles = ["thumbnail"]

        # Set the Assets
        i.assets['image'] = img
        i.assets['thumbnail'] = thumb

        return i


def search(
    bbox: Optional[Union[List, Tuple]] = None,
    datetime: Union[List, Tuple, str, pydt] = None,
    intersects=None,
    collections: List[str] = None,
    ids: List[str] = None,
    limit: int = 10,
    page_size: int = 500,
    query: dict = None,
    filter: dict = None,
    fields: dict = None,
    sortby: dict = None,
    method: str = 'POST',
    project: str = None
) -> FeatureCollection:
    """Search through the SeerAI STAC catalogue.

    Use the search function on the STAC catalogue using the STAC API version of search.
    The STAC api is described [here](https://stacspec.org/STAC-api.html#operation/postSearchSTAC).

    Args:
        bbox: list or tuple of coordinates describing a bounding box. Should have length should be either 4 or 6.
        datetime: Either a datetime or interval expressed as a string. Open ended intervals can be expressed using
                  double-dots '..'. If given as a string datetimes must be in RFC3339 format. See examples below
                  for different formats.
        intersects: Only items that intersect this geometry will be included in the results. Can be either geojson or
                    object that has  `__geo_interface__`.
        collections: List of strings with collection IDs to include in search results.
        ids: List of item IDs to return. All other filter parameters that further restrict the search are ignored.
        limit: The maximum number of results to return.
        query: a STAC query in the format of the STAC query extension
               filter: a CQL2 JSON filter
        fields: a list of fields to invlude/exclude. Included fields should be prefixed by '+' and excluded
                fields by '-'. Alernatively, a dict with a 'include'/'exclude' lists may be provided
        sortby: a list of sortby objects, with are dicts containing 'field' and 'direction'
        method: Request method to use. Valid options are 'POST' (default) and 'GET'. Normally you should not have to
                change this from the default.
        project: the project to search in.

    Examples:
        An example search.

        >>> from geodesic.stac import search
        >>> search(
        ...    bbox=[(-122.80058577975704, 40.72377233124292, -122.7906160884923, 40.726188159862616)],
        ...    datetime="2021-06-15T00:00:00",
        ...    collections: ['sentinel-2-l2a]
        ... )

        Datetimes can be passed as either python datetime objects or as strings. The following are valid arguments.

        >>> from datetime import datetime
        >>> dt = [datetime(2021, 1, 1), datetime(2021, 1, 2)]
        >>> dt = datetime(2021, 1, 1)
        >>> dt = ["2021-01-01T00:00:00", "2021-01-02T00:00:00"]
        >>> dt = "2021-01-01T00:00:00/2021-01-02T00:00:00"
        >>> dt = "2021-01-01T00:00:00"

        Datetimes may also be passed as open intervals using double-dot notation.

        >>> dt = "../2021-05-10T00:00:00"
        >>> dt = "2021-05-10T00:00:00/.."

    """
    stac_api = STACAPI('/spacetime/api/v1/stac')

    if limit is not None:
        page_size = limit

    if project is None:
        project = geodesic.get_active_project()
    elif isinstance(project, str):
        project = geodesic.get_project(project)

    extra_params = {
        'project': project.uid
    }

    fc = stac_api.search(
        bbox=bbox,
        datetime=datetime,
        intersects=intersects,
        collections=collections,
        ids=ids,
        limit=page_size,
        method=method,
        fields=fields,
        sortby=sortby,
        query=query,
        filter=filter,
        extra_params=extra_params
    )

    if limit is None:
        fc.get_all()
    return fc


def _parse_date(dt, index=0):

    if isinstance(dt, str):
        try:
            return datetime_to_utc(parse(dt)).isoformat()
        except ParserError as e:
            if dt == '..' or dt == '':
                if index == 0:
                    return '0001-01-01T00:00:00+00:00'
                else:
                    return '9999-01-01T00:00:00+00:00'
            else:
                raise e
    elif isinstance(dt, pydt):
        return datetime_to_utc(dt).isoformat()
    else:
        raise ValueError("could not parse datetime. unknown type.")


class STACAPI:
    def __init__(self, root: str):
        self.root = root
        if root.endswith('/'):
            self.root = self.root[:-1]

    def collections(self) -> dict:
        req_url = f'{self.root}/collections'

        c = get_client()

        res = raise_on_error(c.get(req_url))
        return res.json()

    def collection(self, collection_id: str) -> dict:
        req_url = f'{self.root}/collections/{collection_id}'

        c = get_client()

        res = raise_on_error(c.get(req_url))
        return res.json()

    def search(
        self,
        bbox: Optional[list] = None,
        datetime: Union[list, tuple] = None,
        limit: Union[None, int] = 10,
        intersects: Any = None,
        collections: List[str] = None,
        ids: List[str] = None,
        query: dict = None,
        filter: dict = None,
        fields: dict = None,
        sortby: dict = None,
        method: str = 'POST',
        extra_params: dict = {}
    ) -> FeatureCollection:
        """ Query the search endpoint for items.

        Query this service's OGC Features or STAC API.

        Args:
            bbox: The spatial extent for the query as a bounding box. Example: [-180, -90, 180, 90]
            datetime: The temporal extent for the query formatted as a list: [start, end].
            limit: The maximum number of items to return in the query.
            intersects: a geometry to filter results by geospatial intersection
            collections: a list of collections to query
            ids: a list of item/feature IDs to return
            query: a STAC query in the format of the STAC query extension
            filter: a CQL2 JSON filter
            fields: a list of fields to invlude/exclude. Included fields should be prefixed by '+' and excluded
                    fields by '-'. Alernatively, a dict with a 'include'/'exclude' lists may be provided
            sortby: a list of sortby objects, with are dicts containing 'field' and 'direction'
            method: GET or POST (default)
            extra_params: dictionary of extra parameters to pass to the STAC search API

        Returns:
            A :class:`geodesic.stac.FeatureCollection` with all items in the dataset matching the query.

        Examples:
            A query on the `sentinel-2-l2a` dataset with a given bouding box and time range. Additionally it
            you can apply filters on the parameters in the items.

            >>> bbox = geom.bounds
            >>> date_range = (datetime.datetime(2020, 12,1), datetime.datetime.now())
            >>> api.search(
            ...          bbox=bbox,
            ...          collections=['sentinel-2-l2a'],
            ...          datetime=date_range,
            ...          query={'properties.eo:cloud_cover': {'lte': 10}}
            ... )
        """
        if method.lower() not in ['post', 'get']:
            raise ValueError("request method must be 'GET' or 'POST'")

        req_url = f'{self.root}/search'

        # STAC client for Spacetime or external STAC apis.
        client = get_client()

        # Request query/body
        body = {"limit": limit}

        if collections is not None:
            if not isinstance(collections, list):
                raise TypeError('collections must be a list of strings')
            body["collections"] = collections

        # Parse geospatial aspect of this query (bbox and intersects)
        body = self._query_parse_geometry(body, 'stac', bbox, intersects, method=method)

        # Parse STAC search specific query/filtering
        params = self._query_parse_stac_query(
            params=body,
            ids=ids,
            filter=filter,
            query=query,
            fields=fields,
            sortby=sortby,
            method=method
        )

        if datetime is not None:
            if isinstance(datetime, (str, pydt)):
                params['datetime'] = _parse_date(datetime)
            else:
                params["datetime"] = "/".join([_parse_date(d, index=i) for i, d in enumerate(datetime)])

        params.update(extra_params)

        if method.lower() == 'post':
            res = raise_on_error(client.post(req_url, **params))
        else:
            res = raise_on_error(client.get(req_url, **params))

        # Wrap the results in a FeatureCollection
        collection = FeatureCollection(query=params, **res.json())

        return collection

    def collection_items(
            self,
            collection_id: str,
            bbox: Optional[list] = None,
            datetime: Union[list, tuple] = None,
            limit: Union[None, int] = 10,
            extra_params: dict = {}) -> FeatureCollection:
        """ Query the collections/<collection_id>/items endpoint for items.

        Query this service's OGC Features or STAC API.

        Args:
            collection_id: the collection to query
            bbox: The spatial extent for the query as a bounding box. Example: [-180, -90, 180, 90]
            datetime: The temporal extent for the query formatted as a list: [start, end].
            limit: The maximum number of items to return in the query.
            extra_params: extra query parameters to pass to the api
        """

        req_url = f'{self.root}/collections/{collection_id}/items'

        # STAC client for Spacetime or external STAC apis.
        client = get_client()

        # Request query/body
        params = {"limit": limit}

        # Parse geospatial aspect of this query (bbox and intersects)
        params = self._query_parse_geometry(params, 'features', bbox, None, method='GET')

        if datetime is not None:
            if isinstance(datetime, (str, pydt)):
                params['datetime'] = _parse_date(datetime)
            else:
                params["datetime"] = "/".join([_parse_date(d, index=i) for i, d in enumerate(datetime)])

        params.update(extra_params)
        res = raise_on_error(client.get(req_url, **params))

        # Wrap the results in a FeatureCollection
        collection = FeatureCollection(query=params, **res.json())

        return collection

    def collection_item(
            self,
            collection_id: str,
            feature_id: str,
            extra_params: dict = {}) -> Feature:
        """ Get a specific feature from collections/<collection_id>/items/feature_id endpoint

        Get a specific feature

        Args:
            collection_id: the collection to get the item from
            feature_id: The id of the feature
            extra_params: extra query parameters to pass
        """

        req_url = f'{self.root}/collections/{collection_id}/items/{feature_id}'

        # STAC client for Spacetime or external STAC apis.
        client = get_client()

        res = raise_on_error(client.get(req_url, **extra_params))

        # Wrap the results in a FeatureCollection
        feature = Feature(**res.json())

        return feature

    def _query_parse_geometry(
            self, params: dict, api: str, bbox: Optional[list],
            intersects: object, method: str = 'POST') -> dict:

        # If the bounding box only provided.
        if bbox is not None and intersects is None:
            if len(bbox) != 4 and len(bbox) != 6:
                raise ValueError("bbox must be length 4 or 6")
            if method == 'POST':
                params["bbox"] = bbox
            else:
                params["bbox"] = ",".join([str(x) for x in bbox])
            return params

        # If a intersection geometry was provided
        if intersects is not None:
            # Geojson geometry OR feature
            if isinstance(intersects, dict):
                try:
                    g = shape(intersects)
                except (ValueError, AttributeError):
                    try:
                        g = shape(intersects['geometry'])
                    except Exception as e:
                        raise ValueError('could not determine type of intersection geometry') from e

            elif hasattr(intersects, "__geo_interface__"):
                g = intersects

            else:
                raise ValueError("intersection geometry must be either geojson or object with __geo_interface__")

            # If STAC, use the geojson
            if api == "stac":
                params["intersects"] = g.__geo_interface__
            # Bounding box is all that's supported for OAFeat
            else:
                try:
                    # Shapely
                    params["bbox"] = ','.join([str(x) for x in g.bounds])
                except AttributeError:
                    # ArcGIS
                    params["bbox"] = ','.join([str(x) for x in g.extent])
        return params

    def _query_parse_stac_query(
            self,
            params: dict,
            ids: list = None,
            filter: dict = None,
            query: dict = None,
            fields: dict = None,
            sortby: dict = None,
            method: str = 'POST') -> dict:

        # Individual item ids to get
        if ids is not None:
            if not isinstance(ids, (list, tuple)):
                raise TypeError('ids must be a list or tuple of strings')
            params["ids"] = ids

        # Parse the original STAC Query object, this will go away soon now that
        # The core STAC spec adopted CQL. This is still supported by many STAC APIs
        # in the wild, including the ubiquitous sat-api.
        if query is not None:
            params["query"] = query

        if filter is not None:
            params['filter'] = filter

        # Sortby object, see STAC sort spec
        if sortby is not None:
            params["sortby"] = sortby

        # Fields to include/exclude.
        if fields is not None:
            fieldsObj = defaultdict(list)
            # fields with +/-
            if isinstance(fields, list):
                for field in fields:
                    if field.startswith("+"):
                        fieldsObj["include"].append(field[1:])
                    elif field.startswith("-"):
                        fieldsObj["exclude"].append(field[1:])
                    else:
                        fieldsObj["include"].append(field)
            else:
                fieldsObj = fields
            params["fields"] = fieldsObj

        return params
