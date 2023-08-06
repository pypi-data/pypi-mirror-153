from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('address')
class Address(Entity):
    LIST_URL = '/constituent/v1/addresses/'
    CREATE_URL = '/constituent/v1/addresses/'
    GET_URL = '/constituent/v1/constituents/addresses/{id}'
    UPDATE_URL = '/constituent/v1/addresses/{id}'
    DELETE_URL = '/constituent/v1/addresses/{id}'
    TYPES_URL = 'constituent/v1/addresstypes'
