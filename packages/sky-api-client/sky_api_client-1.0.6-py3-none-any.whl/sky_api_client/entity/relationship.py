from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('relationship')
class Relationship(Entity):
    LIST_URL = '/constituent/v1/relationships/'
    CREATE_URL = '/constituent/v1/relationships/'
    GET_URL = '/constituent/v1/constituents/relationships/{id}'
    UPDATE_URL = '/constituent/v1/relationships/{id}'
    DELETE_URL = '/constituent/v1/relationships/{id}'
