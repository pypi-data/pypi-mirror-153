from urllib.parse import urljoin

import requests
from requests import Response

from biolib.typing_utils import Dict
from biolib.biolib_api_client import BiolibApiClient as DeprecatedApiClient


class ApiClient:

    def get(self, url: str, params: Dict[str, str]) -> Response:
        response = requests.get(
            headers=self._get_headers(),
            params=params,
            timeout=10,
            url=self._get_absolute_url(url),
        )
        response.raise_for_status()
        return response

    def post(self, path: str, data: Dict) -> Response:
        response = requests.post(
            headers=self._get_headers(),
            json=data,
            timeout=10,
            url=self._get_absolute_url(path),
        )
        response.raise_for_status()
        return response

    @staticmethod
    def _get_headers() -> Dict[str, str]:
        headers: Dict[str, str] = {}

        deprecated_api_client = DeprecatedApiClient.get()

        if deprecated_api_client.is_signed_in:
            deprecated_api_client.refresh_access_token()
            access_token = deprecated_api_client.access_token
            if access_token:
                headers['Authorization'] = f'Bearer {access_token}'

        return headers

    @staticmethod
    def _get_absolute_url(path: str) -> str:
        deprecated_api_client = DeprecatedApiClient.get()
        base_api_url = urljoin(deprecated_api_client.base_url, '/api/')
        return urljoin(base_api_url, path.strip('/') + '/')
