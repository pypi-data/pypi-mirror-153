#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from abc import ABC, abstractmethod
from typing import KeysView
from requests.models import Response

from atlaspyapi.client import Atlas


class EntityManager(ABC):
    def __init__(self, atlas_client: Atlas):
        self.client = atlas_client

    @abstractmethod
    def create_entity(self, *args, **kwargs) -> bool:
        pass

    def get_entity(self, guid: str) -> dict:
        entity = self.client.entity_guid(guid)
        print("get_result" + str(entity._data))
        return entity.entity

    @staticmethod
    def get_entity_attributes(entity: dict) -> dict:
        return entity["attributes"]

    @staticmethod
    def show_entity_attributes(entity: dict) -> None:
        print(entity["attributes"])

    @staticmethod
    def get_s3_attributes_key_list(entity: dict) -> KeysView:
        return EntityManager.get_entity_attributes(entity).keys()

    def update_entity(
        self, guid: str, attribute_name: str, attribute_value: str
    ) -> Response:
        current_entity_obj = self.client.entity_guid(guid)
        current_entity_obj.entity["attributes"][attribute_name] = attribute_value
        return current_entity_obj.update(attribute=attribute_name)

    def delete_entity(self, guid: str) -> Response:
        current_entity_obj = self.client.entity_guid(guid)
        return current_entity_obj.delete()

    def purge_entity(self, guid: str) -> Response:
        return self.client.purge_entity_by_guid(guid)
