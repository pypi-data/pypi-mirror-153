from sky_api_client.entity.base import Entity


class WebhookSubscription(Entity):
    LIST_URL = '/webhook/v1/subscriptions/'
    CREATE_URL = '/webhook/v1/subscriptions/'
    GET_URL = '/webhook/v1/subscriptions/{id}/'
    DELETE_URL = '/webhook/v1/subscriptions/{id}/'
