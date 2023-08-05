import base64
from typing import Union, Any
from getpass import getpass
from geodesic.bases import APIObject
import json
from geodesic import raise_on_error
from geodesic.service import ServiceClient
from geodesic.descriptors import StringDescr

# Credentials client
credentials_client = ServiceClient("krampus", 1, "credentials")

SERVICE_ACCOUNT_KEY = 'SERVICE_ACCOUNT_KEY'
AWS_KEY_PAIR = 'AWS_KEY_PAIR'
AZURE_ACCESS_KEY = 'AZURE_ACCESS_KEY'
JWT = 'JWT'
OAUTH2_CLIENT_CREDENTIALS = 'OAUTH2_CLIENT_CREDENTIALS'
OAUTH2_REFRESH_TOKEN = 'OAUTH2_REFRESH_TOKEN'
BASIC_AUTH = 'BASIC_AUTH'

valid_types = [
    SERVICE_ACCOUNT_KEY,
    AWS_KEY_PAIR,
    AZURE_ACCESS_KEY,
    JWT,
    OAUTH2_CLIENT_CREDENTIALS,
    OAUTH2_REFRESH_TOKEN,
    BASIC_AUTH
]


def get_credential(name_or_uid: str = None):
    """
    Gets the uid/name/type of requested credential, or None if it doesn't exist

    Args:
        name_or_uid: Name or UID of the credential to access
    """
    res = raise_on_error(credentials_client.get(name_or_uid))
    c = res.json()['credential']
    if c is None:
        return None
    return Credential(**c)


def get_credentials():
    """
    Returns all of your user's credentials
    """
    res = raise_on_error(credentials_client.get(''))
    return [Credential(**p) for p in res.json()['credentials']]


class Credential(APIObject):
    """
    Credentials to access secure resources such as a cloud storage bucket. Credentials have
    a name, type and data. Credentials can be created or deleted but not accessed again
    except by internal services. This is for security reasons. Credentials are stored using
    symmetric PGP encryption at rest.
    """
    uid = StringDescr(doc="the unique ID for this credential. Set automatically")
    name = StringDescr(doc="the name of this credential. Unique to the user and how a user will typically reference it")
    type = StringDescr(
        one_of=valid_types,
        doc=f"the type of the credential. Supported types are {', '.join(valid_types)}")

    _limit_setitem = [
        "name",
        "type",
        "data"
    ]

    def __init__(self, **credential):
        self._name = None
        self._type = None
        self.__data = bytes()
        self._client = credentials_client
        for k, v in credential.items():
            setattr(self, k, v)

    def create(self):
        """
        Creates a new Credentials. Encodes the data to be sent.
        """

        data = self.__data
        if isinstance(data, bytes):
            enc_data = base64.b64encode(data).decode()
        elif isinstance(data, dict):
            enc_data = base64.b64encode(json.dumps(data).encode()).decode()
        elif isinstance(data, str):
            enc_data = base64.b64encode(data.encode()).decode()

        raise_on_error(self._client.post("", name=self.name, type=self.type, data=enc_data))

    def delete(self):
        raise_on_error(self._client.delete(self.name))

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, v: Any):
        self.__data = v

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'data':
            self.__data = value
        return super().__setattr__(name, value)

    @staticmethod
    def from_gcp_service_account(*, name: str, key: Union[str, dict] = None) -> 'Credential':
        """creates new GCP Service Account Credential

        Creates a new Credential object for a GCP Service Account (e.g. Google Earth Engine,
        BigQuery, etc)

        Arguments:
            name: the name of the Credential to create
            key: the full service account, either a string or dict. If `None`, user will
                 be prompted via stdin

        Returns:
            a new Credential object that can be saved to backend
        """
        if key is None:
            key = getpass(prompt='Paste Complete Google Cloud Service Account Key: ')
        if isinstance(key, str):
            key = json.loads(key)

        return Credential(
            name=name,
            type=SERVICE_ACCOUNT_KEY,
            data=key
        )

    @staticmethod
    def from_aws_key_pair(*, name: str, aws_access_key_id: str, aws_secret_access_key: str = None) -> 'Credential':
        """creates new AWS Key Pair Credential

        Creates a new Credential object for an AWS Key Pair (such as from an IAM User)

        Arguments:
            name: the name of the Credential to create
            aws_access_key_id: the access key id
            aws_secret_access_key: the secret key.  If `None`, user will
                 be prompted via stdin.

        Returns:
            a new Credential object that can be saved to backend
        """

        if aws_secret_access_key is None:
            aws_secret_access_key = getpass(prompt='AWS Secret Access Key: ')

        return Credential(
            name=name,
            type=AWS_KEY_PAIR,
            data={
                'aws_access_key_id': aws_access_key_id,
                'aws_secret_access_key': aws_secret_access_key
            }
        )

    @staticmethod
    def from_azure_storage_account(*, name: str, account_name: str, account_key: str = None) -> 'Credential':
        """creates new Azure Storage Account Credential

        Creates a new Credential object for an Azure Storage Account (e.g. Blob storage)

        Arguments:
            name: the name of the Credential to create
            account_name: the Azure account name
            account_key: the secret key for the account.  If `None`, user will
                 be prompted via stdin.

        Returns:
            a new Credential object that can be saved to backend
        """
        if account_key is None:
            account_key = getpass(prompt='Azure Storage Account Key: ')

        return Credential(
            name=name,
            type=AZURE_ACCESS_KEY,
            data={
                'account_name': account_name,
                'account_key': account_key
            }
        )

    @staticmethod
    def from_jwt(*, name: str, jwt: str = None) -> 'Credential':
        """creates new JSON Web Token Credential

        Creates a new Credential object for an arbitrary JWT

        Arguments:
            name: the name of the Credential to create
            jwt: the string/encoded JWT. If `None`, user will
                 be prompted via stdin.

        Returns:
            a new Credential object that can be saved to backend
        """
        if jwt is None:
            jwt = getpass(prompt='Paste Complete JSON Web Token: ')

        return Credential(
            name=name,
            type=JWT,
            data=jwt
        )

    @staticmethod
    def from_oauth2_client_credentials(
        *,
        name: str,
        client_id: str,
        client_secret: str = None,
        token_url: str = None,
        authorization_url: str = None,
        audience: str = None,
            scope: str = None) -> 'Credential':
        """creates new OAuth2 Client Credentials Credential

        Creates a new Credential object for an OAuth2 Application

        Arguments:
            name: the name of the Credential to create
            client_id: the client_id of the oauth2 app
            client_secret: the client secret of the oauth2 app. If `None`, user will
                 be prompted via stdin.
            token_url: the token url/uri to request an access token
            authorization_url: the authorization url for certain auth flows
            audience: (optional) the audience of the access_token
            scope: (optional) custom scope to be requested with the token

        Returns:
            a new Credential object that can be saved to backend
        """

        if token_url is None:
            raise ValueError('must provide token_url')
        if authorization_url is None:
            raise ValueError('must provide authorization_url')
        if client_secret is None:
            client_secret = getpass(prompt='Client Secret: ')

        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'token_url': token_url,
            'authorization_url': authorization_url,
        }

        if audience is not None:
            data['audience'] = audience
        if scope is not None:
            data['scope'] = scope

        return Credential(
            name=name,
            type=OAUTH2_CLIENT_CREDENTIALS,
            data=data
        )

    @staticmethod
    def from_basic_auth(*, name: str, username: str, password: str = None) -> 'Credential':
        """creates new Basic Auth Credential

        Creates a new Credential object for a username/password

        Arguments:
            name: the name of the Credential to create
            username: the username
            password: the password. If `None`, user will
                 be prompted via stdin.

        Returns:
            a new Credential object that can be saved to backend
        """
        if password is None:
            password = getpass()

        return Credential(
            name=name,
            type=BASIC_AUTH,
            data={
                'username': username,
                'password': password
            }
        )
