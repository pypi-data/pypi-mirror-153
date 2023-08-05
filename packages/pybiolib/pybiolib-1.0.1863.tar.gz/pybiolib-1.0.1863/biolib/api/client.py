from urllib.parse import urljoin

import requests
from requests import Response

from biolib.typing_utils import Dict, Optional
from biolib.biolib_api_client import BiolibApiClient as DeprecatedApiClient


class ApiClient:

    def get(self, url: str, params: Dict[str, str]) -> Response:
        deprecated_api_client = DeprecatedApiClient.get()

        access_token: Optional[str] = None
        if deprecated_api_client.is_signed_in:
            deprecated_api_client.refresh_access_token()
            access_token = deprecated_api_client.access_token

        base_api_url = urljoin(deprecated_api_client.base_url, '/api/')
        absolute_url = urljoin(base_api_url, url.strip('/') + '/')

        response = requests.get(
            headers={'Authorization': f'Bearer {access_token}'} if access_token else None,
            params=params,
            url=absolute_url,
        )
        response.raise_for_status()
        return response
