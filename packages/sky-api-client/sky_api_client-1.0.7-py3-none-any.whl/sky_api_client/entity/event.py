from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('event')
class Event(Entity):
    LIST_URL = '/event/v1/events'
    CREATE_URL = '/event/v1/events'
    GET_URL = '/event/v1/events/{id}'
    UPDATE_URL = '/event/v1/events/{id}'
    DELETE_URL = '/event/v1/events/{id}'
