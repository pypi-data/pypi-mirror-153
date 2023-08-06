from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('constituent_online_presence')
class ConstituentOnlinePresence(Entity):
    LIST_URL = '/constituent/v1/constituents/{id}/onlinepresences?include_inactive=true'
