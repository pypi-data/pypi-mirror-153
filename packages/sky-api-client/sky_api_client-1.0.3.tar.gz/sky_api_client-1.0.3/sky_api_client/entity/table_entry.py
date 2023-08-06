from sky_api_client.entity.base import Entity


class TableEntry(Entity):
    LIST_URL = '/nxt-data-integration/v1/re/codetables/{id}/tableentries/'
    CREATE_URL = '/nxt-data-integration/v1/re/codetables/{id}/tableentries/'
    GET_URL = '/nxt-data-integration/v1/re/codetables/{parent_id}/tableentries/{id}'
    UPDATE_URL = '/nxt-data-integration/v1/re/codetables/{parent_id}/tableentries/{id}/'
    DELETE_URL = '/nxt-data-integration/v1/re/codetables/{parent_id}/tableentries/{id}/'
