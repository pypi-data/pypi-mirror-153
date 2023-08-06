from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('webhook_subscription')
class WebhookSubscription(Entity):
    LIST_URL = '/webhook/v1/subscriptions/'
    CREATE_URL = '/webhook/v1/subscriptions/'
    GET_URL = '/webhook/v1/subscriptions/{id}/'
    DELETE_URL = '/webhook/v1/subscriptions/{id}/'
