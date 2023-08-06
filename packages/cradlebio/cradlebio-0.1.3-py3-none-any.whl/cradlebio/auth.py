"""Helper functions for authenticating users to Google Services such as Firebase or GCS """
import json
import logging
from datetime import datetime, timedelta
from typing import Union, List

from google.auth.credentials import Credentials, Scoped
from google.auth import transport, jwt
from google.cloud import firestore


class IdentityPlatformTokenCredentials(Credentials):
    """A refreshable Identity Platform JWT ID Token.

    See: https://cloud.google.com/identity-platform/docs/use-rest-api#section-refresh-token for details
    Can be loaded from a JSON file available at https://auth.internal.cradle.bio

    In addition to parent attributes provides:
    uid: A string with the Identity Platform specific user ID
    """

    def __init__(self, refresh_token: str, token: str, api_key: str):
        """Initialize directly from token values.

        :param refresh_token: Signed token used to fetch new ID tokens from the secure token service
        :param token: JWT used to access resources.
        :param api_key: Key used to identify this application to the identity platform
        """
        super().__init__()
        self.refresh_token = refresh_token
        self.token = token
        self.api_key = api_key

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value: str):
        """Decode the JWT and populate necessary values for the parent class."""
        if value:
            data = jwt.decode(value, verify=False)
            self._quota_project_id = data['aud']
            self.project_id = data['aud']
            self.expiry = datetime.utcfromtimestamp(int(data['exp']))
            self.uid = data['sub']
        self._token = value

    def refresh(self, request: transport.Request):
        logging.debug(self.token)
        resp = request(
            f'https://securetoken.googleapis.com/v1/token?key={self.api_key}',
            method='POST',
            json={'grant_type': 'refresh_token', 'refresh_token': self.refresh_token})
        data = json.loads(resp.data.decode('utf-8'))
        if 'access_token' not in data:
            raise RuntimeError(f'JWT token retrieval failed: response {str(data)}')

        self.token = data['access_token']

    @classmethod
    def from_file(cls, filepath: str):
        with open(filepath, 'r') as f:
            return cls(**json.load(f))

    def as_access_token_credentials(self, scopes: List[str] = None):
        """Get credentials that use an access token obtained via Workload Identity (see STSCredentials)."""
        return WorkloadIdentityCredential(self, scopes=scopes)


class WorkloadIdentityCredential(Credentials, Scoped):
    """Fetches access tokens for a Workload Identity Principal using a JWT from the Identity Platform

    See https://cloud.google.com/iam/docs/configuring-workload-identity-federation for details on how this works
    """

    def __init__(self, jwt_creds: IdentityPlatformTokenCredentials,
                 scopes: List[str] = None,
                 default_scopes: List[str] = None):
        super().__init__()
        self.jwt_creds = jwt_creds
        self.token = None
        self.expiry = datetime.fromtimestamp(0)
        self._quota_project_id = self.jwt_creds.quota_project_id
        self.project_id = self.jwt_creds.project_id
        self._scopes = scopes
        self._default_scopes = default_scopes

    @property
    def requires_scopes(self):
        return True

    def with_scopes(self, scopes, default_scopes=None):
        return WorkloadIdentityCredential(self.jwt_creds, scopes, default_scopes)

    def refresh(self, request: transport.Request):
        # Make sure the identity platform JWT token is fresh
        if not self.jwt_creds.valid:
            self.jwt_creds.refresh(request)

        resp = request(
            'https://sts.googleapis.com/v1/token',
            method='POST',
            json={
                "audience": "//iam.googleapis.com/projects/473699240866/locations/global/workloadIdentityPools/firebase/providers/firebase",
                "grantType": "urn:ietf:params:oauth:grant-type:token-exchange",
                "requestedTokenType": "urn:ietf:params:oauth:token-type:access_token",
                "scope": " ".join(self.scopes or self.default_scopes),
                "subjectTokenType": "urn:ietf:params:oauth:token-type:jwt",
                "subjectToken": self.jwt_creds.token
            }
        )
        data = json.loads(resp.data.decode('utf-8'))
        if 'access_token' not in data:
            raise RuntimeError(f'Access token retrieval failed: response {str(data)}')
        self.expiry = datetime.utcnow() + timedelta(seconds=int(data['expires_in']))
        self.token = data['access_token']


def get_client(credentials: Union[IdentityPlatformTokenCredentials, str]) -> firestore.Client:
    if isinstance(credentials, str):
        credentials = IdentityPlatformTokenCredentials.from_file(credentials)

    return firestore.Client(
        credentials=credentials,
        project=credentials.quota_project_id)


def get_user_document(credentials: Union[IdentityPlatformTokenCredentials, str] = None,
                      client: firestore.Client = None) -> firestore.DocumentReference:
    """
    Fetch (or create if it doesn't exist) a user scoped document from Firebase Credentials or a filepath to credentials.
    """
    if client is None:
        if credentials is None:
            raise ValueError('At least one of `client` and `credentials` must be specified')
        client = get_client(credentials)

    user_doc = client.document(f'users/{credentials.uid}').get()
    if not user_doc.exists:
        user_doc.reference.create({})
    return user_doc.reference

