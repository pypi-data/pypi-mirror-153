from typing import Dict
from sky_api_client.exceptions.exception import MethodNotDefined, InvalidArguments
from sky_api_client import client


class Entity(object):
    CREATE_URL = None
    UPDATE_URL = None
    GET_URL = None
    LIST_URL = None
    DELETE_URL = None
    SEARCH_URL = None
    TYPES_URL = None

    def __init__(self, api: client) -> None:
        self._api = api

    def list(self, id=None, parent_id=None):
        if self.LIST_URL:
            if 'id' in self.LIST_URL and id is None:
                raise InvalidArguments()
            elif 'parent_id' in self.LIST_URL and parent_id is None:
                raise InvalidArguments()
            else:
                return self._api.request(method='GET', path=self.LIST_URL.format(id=id))
        raise MethodNotDefined('List')

    def types(self):
        if self.TYPES_URL:
            return self._api.request(method='GET', path=self.TYPES_URL).get('value', [])
        raise MethodNotDefined('Types')

    def get(self, id: str, parent_id=''):
        if self.GET_URL:
            return self._api.request(method='GET', path=self.GET_URL.format(id=id, parent_id=parent_id))
        raise MethodNotDefined('Get')

    def create(self, data: Dict[str, str], id=''):
        if self.CREATE_URL:
            return self._api.request(method='POST', path=self.CREATE_URL.format(id=id), data=data)
        raise MethodNotDefined('Create')

    def update(self, id: str, data: Dict[str, str], parent_id=''):
        if self.UPDATE_URL:
            return self._api.request(method='PATCH', path=self.UPDATE_URL.format(id=id, parent_id=parent_id), data=data)
        raise MethodNotDefined('Update')

    def delete(self, id: str, parent_id=''):
        if self.DELETE_URL:
            return self.api.request(method='DELETE', path=self.DELETE_URL.format(id=id, parent_id=parent_id))
        raise MethodNotDefined('Delete')

    def search(self, search_text: str):
        if self.SEARCH_URL:
            return self._api.request(method='GET', path=self.SEARCH_URL.format(search_text=search_text))
        raise MethodNotDefined('Search')
