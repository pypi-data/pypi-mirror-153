from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('constituent_phone')
class ConstituentPhone(Entity):
    LIST_URL = '/constituent/v1/constituents/{id}/phones?include_inactive=true'
