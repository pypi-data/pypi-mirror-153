from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('phone')
class Phone(Entity):
    LIST_URL = '/constituent/v1/phones/'
    CREATE_URL = '/constituent/v1/phones/'
    GET_URL = '/constituent/v1/constituents/phones/{id}'
    UPDATE_URL = '/constituent/v1/phones/{id}'
    DELETE_URL = '/constituent/v1/phones/{id}'
    TYPES_URL = 'constituent/v1/phonetypes'
