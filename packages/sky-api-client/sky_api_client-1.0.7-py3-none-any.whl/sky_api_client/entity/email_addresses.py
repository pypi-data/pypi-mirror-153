from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('email_addresses')
class EmailAddress(Entity):
    LIST_URL = '/constituent/v1/emailaddresses/'
    CREATE_URL = '/constituent/v1/emailaddresses/'
    UPDATE_URL = '/constituent/v1/emailaddresses/{id}'
    DELETE_URL = '/constituent/v1/emailaddresses/{id}'
    TYPES_URL = 'constituent/v1/emailaddresstypes'
