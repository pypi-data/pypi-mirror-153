from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('custom_field')
class CustomField(Entity):
    LIST_URL = '/constituent/v1/constituents/customfields/'
    CREATE_URL = '/constituent/v1/constituents/customfields/'
    GET_URL = '/constituent/v1/constituents/{id}/customfields/'
    UPDATE_URL = '/constituent/v1/constituents/customfields/{id}/'
    DELETE_URL = '/constituent/v1/constituents/customfields/{id}/'
