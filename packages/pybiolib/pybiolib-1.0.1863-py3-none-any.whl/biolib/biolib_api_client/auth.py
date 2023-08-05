import requests
from requests.auth import AuthBase  # type: ignore

from biolib.biolib_api_client import BiolibApiClient
from biolib.biolib_api_client.api_client import UserTokens
from biolib.biolib_errors import BioLibError
from biolib.typing_utils import TypedDict, Literal


class BearerAuth(AuthBase):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def __call__(self, req):
        if self.access_token:
            req.headers['Authorization'] = 'Bearer ' + self.access_token
        return req


class AuthChallengeCreate(TypedDict):
    token: str


class _AuthChallengeStatus(TypedDict):
    state: Literal['awaiting', 'completed']


class AuthChallengeStatus(_AuthChallengeStatus, total=False):
    user_tokens: UserTokens


class BiolibAuthChallengeApi:

    @staticmethod
    def create_auth_challenge() -> AuthChallengeCreate:
        response = requests.post(
            url=f'{BiolibApiClient.get().base_url}/api/user/auth_challenges/',
            timeout=5,
        )

        if not response.ok:
            raise BioLibError(response.content.decode())

        response_dict: AuthChallengeCreate = response.json()
        return response_dict

    @staticmethod
    def get_auth_challenge_status(token: str) -> AuthChallengeStatus:
        response = requests.get(
            url=f'{BiolibApiClient.get().base_url}/api/user/auth_challenges/',
            headers={'Auth-Challenge-Token': token},
            timeout=5,
        )

        if not response.ok:
            raise BioLibError(response.content.decode())

        response_dict: AuthChallengeStatus = response.json()
        return response_dict
