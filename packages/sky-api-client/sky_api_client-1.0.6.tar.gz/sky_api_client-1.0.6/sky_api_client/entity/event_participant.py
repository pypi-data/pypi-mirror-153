from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('event_participant')
class EventParticipant(Entity):
    LIST_URL = '/event/v1/events/{event_id}/participants'
    CREATE_URL = '/event/v1/events/{event_id}/participants'
    GET_URL = '/event/v1/events/{event_id}/participants/{id}/'
    UPDATE_URL = '/event/v1/events/{event_id}/participants/{id}/'
    DELETE_URL = '/event/v1/events/{event_id}/participants/{id}/'
