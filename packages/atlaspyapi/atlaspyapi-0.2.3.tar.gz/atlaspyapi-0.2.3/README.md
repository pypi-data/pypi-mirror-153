# Apache Atlas Client in Python

This python client is only compatible with Apache Atlas REST API v2. 

In this repository, we develop a python api to generate atlas entities and import them into atlas instances.

## Quick start

### Create a client to connect to an Atlas instance

```python
from atlaspyapi.client import Atlas
# login with your token
hostname = "https://atlas.lab.sspcloud.fr"
port = 443
oidc_token = "<your_token>"
atlas_client = Atlas(hostname, port, oidc_token=oidc_token)

# login with your username and password
atlas_client = Atlas(hostname, port, username='',password='')
```
### Search entity and return entity's guid

```python
from atlaspyapi.entity_search.EntityFinder import EntityFinder

finder = EntityFinder(atlas_client)
search_result = finder.search_full_text("aws_s3_bucket", "test")

EntityFinder.show_search_results(search_result)
entity_number = EntityFinder.get_entity_number(search_result)
print("Find " + str(entity_number) + " result in total")

guid_list = EntityFinder.get_result_entity_guid_list(search_result)

for guid in guid_list:
    print("result:" + guid)


```

### Atlas entities CRUD

#### S3 entities

```python
from atlaspyapi.entity_management.s3.S3BucketManager import S3BucketManager

s3_bucket_manager = S3BucketManager(atlas_client)

# creat s3 bucket in atlas
name = "test"
domain = "s3://test.org"
qualified_name = "s3://test.org/test1"
description = "test for me"
s3_bucket_manager.create_entity(name, domain, qualified_name, description)
# get s3 bucket via guid
guid = "9642d134-4d0e-467c-8b36-ca73902d4c14"
e = s3_bucket_manager.get_entity(guid)
s3_bucket_manager.show_entity_attributes(e)
e_attributes = s3_bucket_manager.get_entity_attributes(e)
e_attributes_key_list = s3_bucket_manager.get_s3_attributes_key_list(e)
print(e_attributes_key_list)
print(e_attributes['description'])

# update s3 bucket attributes
s3_bucket_manager.update_entity(guid, 'description', 'update description from api')

# delete s3 bucket
s3_bucket_manager.delete_entity(guid)

``` 

#### Hive entities

```python
hive_db = HiveDBManager(atlas_client)
hive_table = HiveTableManager(atlas_client)
hive_column = HiveColumnManager(atlas_client)

# insert hive tables
hive_db.create_entity("pengfei-stock", "pengfei.org", "database for my stock market",owner="pliu",location="pengfei.org")
hive_table.create_entity("favorite", "pengfei.org@pengfei-stock", "favorite stock")
hive_column.create_entity("stock_id", "int", "pengfei.org@pengfei-stock.favorite", "id of the stock")
hive_column.create_entity("stock_name", "string", "pengfei.org@pengfei-stock.favorite", "name of the stock")

```

### Generate atlas entity json file
If you want to use the Atlas rest api by yourself, we also provide you the support of json file generation

```python
from atlaspyapi.entity_source_generation.S3BucketEntityGenerator import S3BucketEntityGenerator
name = "test"
domain = "s3://test.org"
qualified_name = "s3://test.org/test1"
description = "test for me"

s3_bucket_json_source = S3BucketEntityGenerator.generate_s3_bucket_json_source(name, domain,qualified_name,description
                                                                               , creator_id="toto")
print(s3_bucket_json_source)

```

## Package organization

### entity_source_generation

In the entity_source_generation folder, you can find various templates and generators for generating atlas entities.

### entity_search

In the entity_search folder, you can find EntityFinder which help you to find entity in an Atlas instance

### entity_management

In the entity_management folder, you can find various rest client to upload entities into atlas

### docs

In the docs folder, you can find helper function which shows which entity type and attributes are supported by this api


## Prerequisites

This tool only requires python 3.7 or above

## Supported OS

Windows XP/7/8/10

Linux  

MacOS


## Authors

* **Pengfei Liu** 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgement

This package was created by using [verdan/pyatlasclient](<https://github.com/verdan/pyatlasclient>) project