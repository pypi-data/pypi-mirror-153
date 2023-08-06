from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('event_participant_fee')
class EventParticipantFee(Entity):
    LIST_URL = '/event/v1/participants/{id}/fees'
    CREATE_URL = '/event/v1/participants/{id}/fees'
    GET_URL = '/event/v1/participants/{parent_id}/fees/{id}'
    UPDATE_URL = '/event/v1/participants/{parent_id}/fees/{id}'
    DELETE_URL = '/event/v1/participants/{parent_id}/fees/{id}'
