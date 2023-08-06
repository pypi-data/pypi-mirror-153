from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('event_fee')
class EventFee(Entity):
    LIST_URL = '/event/v1/events/{event_id}/eventfees'
    CREATE_URL = '/event/v1/events/{event_id}/eventfees'
    GET_URL = '/event/v1/events/{event_id}/eventfees/{id}/'
    UPDATE_URL = '/event/v1/events/{event_id}/eventfees/{id}/'
    DELETE_URL = '/event/v1/events/{event_id}/eventfees/{id}/'
