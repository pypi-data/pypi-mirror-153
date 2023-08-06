from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('constituent')
class Constituent(Entity):
    LIST_URL = '/constituent/v1/constituents/'
    CREATE_URL = '/constituent/v1/constituents/'
    GET_URL = '/constituent/v1/constituents/{id}'
    UPDATE_URL = '/constituent/v1/constituents/{id}'
    DELETE_URL = '/constituent/v1/constituents/{id}'
    SEARCH_URL = '/constituent/v1/constituents/search?search_text={search_text}'
