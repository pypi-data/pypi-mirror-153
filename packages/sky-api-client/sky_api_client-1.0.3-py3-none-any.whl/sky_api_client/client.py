import time
from typing import Dict
import requests
from sky_api_client.entity.base import Entity
from sky_api_client.entity.address import Address
from sky_api_client.entity.constituent import Constituent
from sky_api_client.entity.education import Education
from sky_api_client.entity.online_presence import OnlinePresence
from sky_api_client.entity.phone import Phone
from sky_api_client.entity.relationship import Relationship
from sky_api_client.entity.email_addresses import EmailAddress
from sky_api_client.entity.custom_field import CustomField
from sky_api_client.entity.custom_field_categories import CustomFieldCategory
from sky_api_client.entity.code_table import CodeTable
from sky_api_client.entity.table_entry import TableEntry
from sky_api_client.entity.webhook_subscription import WebhookSubscription
from sky_api_client.exceptions.exception import GeneralError

BASE_URL = 'https://api.sky.blackbaud.com'
DEFAULT_TIMEOUT = 300

PROPERTIES = {
    'constituent': Constituent,
    'education': Education,
    'phone': Phone,
    'address': Address,
    'relationship': Relationship,
    'email_addresses': EmailAddress,
    'custom_fields': CustomField,
    'custom_field_category': CustomFieldCategory,
    'code_table': CodeTable,
    'table_entry': TableEntry,
    'subscription_webhook': WebhookSubscription,
    'online_presence': OnlinePresence,
}


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
        if PROPERTIES[attr]:
            return PROPERTIES[attr](api=self._api)
