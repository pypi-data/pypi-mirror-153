from sky_api_client.entity.base import Entity


class Education(Entity):
    LIST_URL = '/constituent/v1/educations/'
    CREATE_URL = '/constituent/v1/educations/'
    GET_URL = '/constituent/v1/constituents/educations/{id}'
    UPDATE_URL = '/constituent/v1/educations/{id}'
    DELETE_URL = '/constituent/v1/educations/{id}'
