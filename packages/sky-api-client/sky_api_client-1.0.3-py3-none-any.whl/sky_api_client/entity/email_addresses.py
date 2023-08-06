from sky_api_client.entity.base import Entity


class EmailAddress(Entity):
    LIST_URL = '/constituent/v1/emailaddresses/'
    CREATE_URL = '/constituent/v1/emailaddresses/'
    LIST_FOR_CONSTITUENT_URL = '/constituent/v1/constituents/{constituent_id}/emailaddresses?include_inactive=true'
    UPDATE_URL = '/constituent/v1/emailaddresses/{id}'
    DELETE_URL = '/constituent/v1/emailaddresses/{id}'
    TYPES_URL = 'constituent/v1/emailaddresstypes'
