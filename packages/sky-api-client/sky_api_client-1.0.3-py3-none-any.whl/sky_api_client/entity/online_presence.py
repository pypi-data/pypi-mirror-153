from sky_api_client.entity.base import Entity


class OnlinePresence(Entity):
    LIST_URL = '/constituent/v1/onlinepresences?include_inactive=true'
    CREATE_URL = '/constituent/v1/onlinepresences/'
    GET_URL = '/constituent/v1/constituents/onlinepresences/{id}'
    LIST_FOR_CONSTITUENT_URL = '/constituent/v1/constituents/{constituent_id}/onlinepresences?include_inactive=true'
    UPDATE_URL = '/constituent/v1/onlinepresences/{id}'
    DELETE_URL = '/constituent/v1/onlinepresences/{id}'
    TYPES_URL = 'constituent/v1/onlinepresencetypes'
