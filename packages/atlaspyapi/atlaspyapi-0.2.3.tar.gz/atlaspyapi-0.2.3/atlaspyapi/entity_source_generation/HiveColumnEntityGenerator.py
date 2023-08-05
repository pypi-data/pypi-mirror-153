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
from atlaspyapi.entity_source_generation.utile import current_milli_time, init_config, populate_template


class HiveColumnEntityGenerator:
    __config = init_config(CONFIG_PATH)

    # get s3_bucket attributes list
    @staticmethod
    def get_hive_column_all_supported_attributes():
        return {
            "entity_type": "hive_column",
            "column_name": "Required attribute. "
                           "The name of the hive column, Example, studentId",
            "column_type": "Required attribute"
                           "The data type of the hive column. Example, int, string, bool, etc.",
            "column_qualified_name": "Required attribute. "
                                     " Fully qualified name of the hive column. It must be unique"
                                     " Example, insee.org@insee-data.students.studentId ",
            "table_qualified_name": "Required attribute. "
                                    " The hive table name that contains the column."
                                    " Example, insee.org@insee-data.students",
            "description": "The description of the entity",
            "createdBy": "User id of the entity creator",
            "updatedBy": "User id of the entity updater",
            "create_time": "Creation time of the entity",
            "update_time": "Last modification time of the entity ",
            "owner": "User id of the entity provider",
        }

    @staticmethod
    def generate_hive_column_json_source(
            column_name: str,
            column_type: str,
            table_qualified_name: str,
            description: str,
            **kwargs,
    ) -> str:
        # get hive_column
        entity_type = "hive_column"
        default_config = HiveColumnEntityGenerator.__config
        # build required attributes: name, cluster_name, qualified_name
        column_qualified_name = f"{table_qualified_name}.{column_name}"
        # build template file path
        template_path = (
            f"{TEMPLATE_FOLDER_PATH}/{default_config.get(entity_type, 'template_name')}"
        )
        # generate default value for optional empty attributes
        creator_id = kwargs.get(
            "creator_id", default_config.get(entity_type, "createdBy")
        )
        updator_id = kwargs.get(
            "updator_id", default_config.get(entity_type, "updatedBy")
        )
        create_time = kwargs.get("create_time", current_milli_time())
        update_time = kwargs.get("update_time", current_milli_time())
        owner = kwargs.get("owner", default_config.get(entity_type, "owner"))

        # populate the template with attributes
        context = {
            # required attributes
            "column_name": column_name,
            "column_type": column_type,
            "column_qualified_name": column_qualified_name,
            "table_qualified_name": table_qualified_name,
            "description": description,
            # optional attributes
            "created_by": creator_id,
            "updated_by": updator_id,
            "create_time": create_time,
            "update_time": update_time,
            "owner": owner,
            "display_name": column_name,
        }
        entity_source = populate_template(template_path, context)
        return entity_source
