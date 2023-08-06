from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('custom_field_category')
class CustomFieldCategory(Entity):
    LIST_URL = '/constituent/v1/constituents/customfields/categories/details/'
