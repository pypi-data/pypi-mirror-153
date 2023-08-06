# If this was checked out from a git tag, this version number may not match.
# Refer to the git tag for the correct version number
__version__ = "0.4.12"

from geodesic.oauth import AuthManager
from geodesic.stac import Item, Feature, FeatureCollection, Asset, STACAPI, search
from geodesic.client import Client, get_client, raise_on_error
from geodesic.raster import Raster, RasterCollection


from geodesic.entanglement.dataset import Dataset, DatasetList, list_datasets, get_dataset
from geodesic.entanglement.object import get_objects
from geodesic.boson.boson import BosonConfig
from geodesic.account.projects import create_project, get_project, get_projects, set_active_project, \
    get_active_project, Project
from geodesic.account.user import myself

__all__ = [
    "authenticate",
    "Item",
    "Feature",
    "FeatureCollection",
    "Asset",
    "BosonConfig",
    "Client",
    "get_client",
    "raise_on_error",
    "Raster",
    "RasterCollection",
    "Dataset",
    "DatasetList",
    "list_datasets",
    "get_dataset",
    "get_objects",
    "Project",
    "create_project",
    "get_project",
    "get_projects",
    "set_active_project",
    "get_active_project",
    "myself",
    "STACAPI",
    "search"
]


def authenticate():
    auth = AuthManager()
    auth.authenticate()
