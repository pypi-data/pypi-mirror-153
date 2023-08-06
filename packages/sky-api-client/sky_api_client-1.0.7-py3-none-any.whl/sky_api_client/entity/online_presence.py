from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('online_presence')
class OnlinePresence(Entity):
    LIST_URL = '/constituent/v1/onlinepresences?include_inactive=true'
    CREATE_URL = '/constituent/v1/onlinepresences/'
    GET_URL = '/constituent/v1/constituents/onlinepresences/{id}'
    UPDATE_URL = '/constituent/v1/onlinepresences/{id}'
    DELETE_URL = '/constituent/v1/onlinepresences/{id}'
    TYPES_URL = 'constituent/v1/onlinepresencetypes'
