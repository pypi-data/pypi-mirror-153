from sky_api_client.entity.base import Entity


class Address(Entity):
    LIST_URL = '/constituent/v1/addresses/'
    CREATE_URL = '/constituent/v1/addresses/'
    GET_URL = '/constituent/v1/constituents/addresses/{id}'
    LIST_FOR_CONSTITUENT_URL = '/constituent/v1/constituents/{constituent_id}/addresses?include_inactive=true'
    UPDATE_URL = '/constituent/v1/addresses/{id}'
    DELETE_URL = '/constituent/v1/addresses/{id}'
    TYPES_URL = 'constituent/v1/addresstypes'
