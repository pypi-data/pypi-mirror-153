from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('code_table')
class CodeTable(Entity):
    LIST_URL = '/nxt-data-integration/v1/re/codetables/'
    CREATE_URL = '/nxt-data-integration/v1/re/codetables/'
    GET_URL = '/nxt-data-integration/v1/re/codetables/{id}/'
    UPDATE_URL = '/nxt-data-integration/v1/re/codetables/{id}/'
    DELETE_URL = '/nxt-data-integration/v1/re/codetables/{id}/'
