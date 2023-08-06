import time
from typing import Dict
import requests
from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry
from sky_api_client.exceptions.exception import GeneralError

BASE_URL = 'https://api.sky.blackbaud.com'
DEFAULT_TIMEOUT = 300


class SkyApiClient(object):
    def __init__(self, subscription_key: str, access_token: str) -> None:
        self.subscription_key = subscription_key
        self.access_token = access_token

    def request(self, method: str, path: str, data: Dict[str, str] = None):
        response = requests.request(
            method=method,
            url='{}/{}'.format(BASE_URL, path),
            timeout=DEFAULT_TIMEOUT,
            headers=self.get_headers(),
            json=data or {},
        )

        if response.status_code == 429:
            sleep_seconds = response.headers.get('Retry-After', 3)
            time.sleep(int(sleep_seconds))

            # retry the failed request. In the worst case, we'll exceed recursion limit and the job will fail
            return self.request(method, path, data=data)

        if response.ok:
            try:
                return response.json()
            except Exception:
                return 'Success'
        raise GeneralError(response.text)

    def get_headers(self):
        return {
            'Bb-Api-Subscription-Key': self.subscription_key,
            'Authorization': 'Bearer {access_token}'.format(access_token=self.access_token),
            'Content-Type': 'application/json',
        }


class SkyApi(object):
    def __init__(self, subscription_key: str, access_token: str) -> None:
        self._api = SkyApiClient(subscription_key, access_token)

    def __getattr__(self, attr: str) -> Entity:
        entity_class = EntityRegistry.get_class(attr)
        if entity_class:
            return entity_class(api=self._api)
