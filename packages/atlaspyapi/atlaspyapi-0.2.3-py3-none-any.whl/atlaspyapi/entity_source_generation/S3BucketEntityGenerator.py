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


class S3BucketEntityGenerator:
    config = init_config(CONFIG_PATH)

    # get s3_bucket attributes list
    @staticmethod
    def get_s3_bucket_all_supported_attributes():
        return {
            "entity_type": "aws_s3_bucket",
            "name": "Required attribute. "
                    "The name of the s3 bucket, Example, donnees-insee",
            "domain": "Required attribute. "
                      " The domain of your s3. Example, minio.lab.sspcloud.fr",
            "qualified_name": "Required attribute. "
                              " Fully qualified name of the s3 bucket. It must be unique"
                              " Example, s3://minio.lab.sspcloud.fr/donnees-insee  ",
            "description": "Required attribute. " "The description of the entity",
            "creator_id": "User id of the entity creator",
            "updator_id": "User id of the entity updater",
            "create_time": "Creation time of the entity",
            "update_time": "Last modification time of the entity ",
            "owner": "User id of the entity provider",
            "encryptionType": "If data is encrypted, we specify the encryption algorithm here",
            "partner": "none",
            "isEncrypted": "Indicate if data is encrypted or not, only boolean value is accepted. Example, True, False",
            "region": "none",
        }

    @staticmethod
    def generate_s3_bucket_json_source(
            name: str, domain: str, qualified_name: str, description: str, **kwargs
    ):
        # get s3_bucket default type
        entity_type = S3BucketEntityGenerator.config.get("aws_s3_bucket", "entity_type")
        # need to be modified
        template_file_path = TEMPLATE_FOLDER_PATH + "/aws_s3_bucket.json.j2"
        # generate default value for optional empty attributes
        creator_id = kwargs.get(
            "creator_id", S3BucketEntityGenerator.config.get(entity_type, "creator_id")
        )
        updator_id = kwargs.get(
            "updator_id", S3BucketEntityGenerator.config.get(entity_type, "updator_id")
        )
        create_time = kwargs.get("create_time", current_milli_time())
        update_time = kwargs.get("update_time", current_milli_time())
        owner = kwargs.get(
            "owner", S3BucketEntityGenerator.config.get(entity_type, "owner")
        )
        is_encrypted = kwargs.get(
            "is_encrypted",
            S3BucketEntityGenerator.config.get(entity_type, "is_encrypted"),
        )
        encryption_type = kwargs.get(
            "encryption_type",
            S3BucketEntityGenerator.config.get(entity_type, "encryption_type"),
        )
        partner = kwargs.get(
            "partner", S3BucketEntityGenerator.config.get(entity_type, "partner")
        )
        region = kwargs.get(
            "region", S3BucketEntityGenerator.config.get(entity_type, "region")
        )

        # populate the template with attributes
        context = {
            # required attributes
            "qualified_name": qualified_name,
            "description": description,
            "domain": domain,
            "name": name,
            # optional attributes
            "created_by": creator_id,
            "updated_by": updator_id,
            "create_time": create_time,
            "update_time": update_time,
            "owner": owner,
            "is_encrypted": is_encrypted,
            "encryption_type": encryption_type,
            "partner": partner,
            "region": region,
        }
        entity_source = populate_template(template_file_path, context)
        return entity_source
