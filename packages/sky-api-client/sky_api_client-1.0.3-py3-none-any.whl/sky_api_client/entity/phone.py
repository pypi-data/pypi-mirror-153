from sky_api_client.entity.base import Entity


class Phone(Entity):
    LIST_URL = '/constituent/v1/phones/'
    CREATE_URL = '/constituent/v1/phones/'
    GET_URL = '/constituent/v1/constituents/phones/{id}'
    LIST_FOR_CONSTITUENT_URL = '/constituent/v1/constituents/{constituent_id}/phones?include_inactive=true'
    UPDATE_URL = '/constituent/v1/phones/{id}'
    DELETE_URL = '/constituent/v1/phones/{id}'
    TYPES_URL = 'constituent/v1/phonetypes'
