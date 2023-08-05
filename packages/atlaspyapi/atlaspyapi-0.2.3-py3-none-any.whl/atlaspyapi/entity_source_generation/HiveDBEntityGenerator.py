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

from atlaspyapi.definition import CONFIG_PATH
from atlaspyapi.definition import TEMPLATE_FOLDER_PATH
from atlaspyapi.entity_source_generation.utile import init_config, populate_template, current_milli_time


class HiveDBEntityGenerator:
    __config = init_config(CONFIG_PATH)

    # get s3_bucket attributes list
    @staticmethod
    def get_hive_db_all_supported_attributes():
        return {
            "entity_type": "hive_db",
            "name": "Required attribute. "
                    "The name of the hive db, Example, insee-data",
            "clusterName": "Required attribute. "
                           " The cluster name of your hive db. Example, insee.org",
            "qualified_name": "Required attribute. "
                              " Fully qualified name of the hive db. It must be unique"
                              " Example, insee.org@insee-data ",
            "description": "The description of the entity",
            "createdBy": "User id of the entity creator",
            "updatedBy": "User id of the entity updater",
            "create_time": "Creation time of the entity",
            "update_time": "Last modification time of the entity ",
            "owner": "User id of the entity provider",
            "ownerType": "The type of the owner user",
        }

    @staticmethod
    def generate_hive_db_json_source(
            name: str, cluster_name: str, description: str, **kwargs
    ):
        # get hive_db
        entity_type = "hive_db"
        # build required attributes: name, cluster_name, qualified_name
        qualified_name = f"{cluster_name}@{name}"
        # build template file path
        template_file_path = f"{TEMPLATE_FOLDER_PATH}/{HiveDBEntityGenerator.__config.get(entity_type, 'template_name')}"
        # generate default value for optional empty attributes
        creator_id = kwargs.get(
            "creator_id", HiveDBEntityGenerator.__config.get(entity_type, "createdBy")
        )
        updator_id = kwargs.get(
            "updator_id", HiveDBEntityGenerator.__config.get(entity_type, "updatedBy")
        )
        create_time = kwargs.get("create_time", current_milli_time())
        update_time = kwargs.get("update_time", current_milli_time())
        owner = kwargs.get(
            "owner", HiveDBEntityGenerator.__config.get(entity_type, "owner")
        )
        location = kwargs.get("location")

        # populate the template with attributes
        context = {
            # required attributes
            "qualified_name": qualified_name,
            "description": description,
            "cluster_name": cluster_name,
            "name": name,
            # optional attributes
            "created_by": creator_id,
            "updated_by": updator_id,
            "create_time": create_time,
            "update_time": update_time,
            "owner": owner,
            "display_name": name,
            "location": location,
        }
        entity_source = populate_template(template_file_path, context)
        return entity_source
