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


from atlaspyapi.definition import TEMPLATE_FOLDER_PATH, CONFIG_PATH
from atlaspyapi.entity_source_generation.utile import init_config, populate_template, current_milli_time


class S3ObjectEntityGenerator:
    config = init_config(CONFIG_PATH)
    template_folder_path = TEMPLATE_FOLDER_PATH

    # get s3_object attributes list
    @staticmethod
    def get_s3_object_all_supported_attributes():
        return {
            "entity_type": "aws_s3_object",
            # required attributes
            "name": "Required attribute. " "The name of the s3 object.",
            "qualified_name": "Required attribute. "
            " The fully qualified name of the s3 object. It must be unique"
            " Example, s3://minio.lab.sspcloud.fr/donnees-insee/RP/pengfei.csv  ",
            "description": "Required attribute. " "The description of the s3 object.",
            "ps_dir_qualified_name": "Required attribute. "
            " The fully qualified name of the pseudo dir which the s3 object belongs to. It must be unique"
            " Example, s3://minio.lab.sspcloud.fr/donnees-insee/RP/  ",
            "object_prefix": "Required attribute. "
            " The prefix of the pseudo dir. It must match the ps_dir_qualified_name "
            "Example, RP/",
            "data_type": "The data type of the s3 object",
            "owner": "The owner of the s3 object",
            # optional attributes
            "creator_id": "User id of the entity creator",
            "updator_id": "User id of the entity updater",
            "create_time": "Creation time of the entity",
            "update_time": "Last modification time of the entity ",
            "compression_type": "The compression type of the s3 object, if it exists",
            "size": "The size of the s3 object in bit",
            "replicated_to": "Indicate if this dir is replicated to other path. It takes an array of guids",
            "replicated_from": "Indicate if this dir is replicated from other path. It takes an array of guids",
        }

    @staticmethod
    def generate_s3_object_entity_json_source(
        name: str,
        qualified_name: str,
        ps_dir_qualified_name: str,
        object_prefix: str,
        data_type: str,
        owner: str,
        description: str,
        **kwargs
    ):
        # get s3_bucket default type
        entity_type = S3ObjectEntityGenerator.config.get("aws_s3_object", "entity_type")

        # need to be modified
        template_file_path = (
            S3ObjectEntityGenerator.template_folder_path
            + "/"
            + entity_type
            + ".json.j2"
        )

        # generate default value for optional empty attributes
        creator_id = kwargs.get(
            "creator_id", S3ObjectEntityGenerator.config.get(entity_type, "creator_id")
        )
        updator_id = kwargs.get(
            "updator_id", S3ObjectEntityGenerator.config.get(entity_type, "updator_id")
        )
        create_time = kwargs.get("create_time", current_milli_time())
        update_time = kwargs.get("update_time", current_milli_time())
        compression_type = kwargs.get(
            "compression_type",
            S3ObjectEntityGenerator.config.get(entity_type, "compression_type"),
        )
        size = kwargs.get(
            "size", S3ObjectEntityGenerator.config.get(entity_type, "size")
        )
        replicated_to = kwargs.get(
            "replicated_to",
            S3ObjectEntityGenerator.config.get(entity_type, "replicated_to"),
        )
        replicated_from = kwargs.get(
            "replicated_from",
            S3ObjectEntityGenerator.config.get(entity_type, "replicated_from"),
        )

        # populate the template with attributes
        context = {
            # required attributes
            "name": name,
            "qualified_name": qualified_name,
            "description": description,
            "ps_dir_qualified_name": ps_dir_qualified_name,
            "object_prefix": object_prefix,
            "data_type": data_type,
            "owner": owner,
            # optional attributes
            "created_by": creator_id,
            "updated_by": updator_id,
            "create_time": create_time,
            "update_time": update_time,
            "compression_type": compression_type,
            "size": size,
            "replicated_to": replicated_to,
            "replicated_from": replicated_from,
        }

        entity_source = populate_template(template_file_path, context)
        return entity_source
