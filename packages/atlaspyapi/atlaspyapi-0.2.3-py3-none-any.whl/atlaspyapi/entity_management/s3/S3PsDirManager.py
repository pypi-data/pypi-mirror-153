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

import json
from atlaspyapi.client import Atlas
from atlaspyapi.entity_management.EntityManager import EntityManager
from atlaspyapi.entity_source_generation.S3PsDirEntityGenerator import (
    S3PsDirEntityGenerator,
)


class S3PsDirManager(EntityManager):
    def __init__(self, atlas_client: Atlas):
        super().__init__(atlas_client)

    def create_entity(
        self,
        name: str,
        qualified_name: str,
        bucket_qualified_name: str,
        object_prefix: str,
        **kwargs
    ) -> bool:
        s3_ps_dir_json_source = (
            S3PsDirEntityGenerator.generate_s3_ps_dir_entity_json_source(
                name, qualified_name, bucket_qualified_name, object_prefix, **kwargs
            )
        )

        s3_ps_dir_json_source = json.loads(s3_ps_dir_json_source)
        try:
            self.client.entity_post.create(data=s3_ps_dir_json_source)
        except Exception as e:
            print("atlas bucket entity creation failed. Origin exception: " + str(e))
            return False
        else:
            return True
