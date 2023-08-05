# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atlaspyapi',
 'atlaspyapi.docs',
 'atlaspyapi.entity_management',
 'atlaspyapi.entity_management.hive',
 'atlaspyapi.entity_management.s3',
 'atlaspyapi.entity_search',
 'atlaspyapi.entity_source_generation']

package_data = \
{'': ['*'],
 'atlaspyapi': ['config/*'],
 'atlaspyapi.entity_source_generation': ['template/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'click>=8.1.2,<9.0.0',
 'requests>=2.27.1,<3.0.0',
 'six>=1.16.0,<2.0.0']

setup_kwargs = {
    'name': 'atlaspyapi',
    'version': '0.2.3',
    'description': '',
    'long_description': '# Apache Atlas Client in Python\n\nThis python client is only compatible with Apache Atlas REST API v2. \n\nIn this repository, we develop a python api to generate atlas entities and import them into atlas instances.\n\n## Quick start\n\n### Create a client to connect to an Atlas instance\n\n```python\nfrom atlaspyapi.client import Atlas\n# login with your token\nhostname = "https://atlas.lab.sspcloud.fr"\nport = 443\noidc_token = "<your_token>"\natlas_client = Atlas(hostname, port, oidc_token=oidc_token)\n\n# login with your username and password\natlas_client = Atlas(hostname, port, username=\'\',password=\'\')\n```\n### Search entity and return entity\'s guid\n\n```python\nfrom atlaspyapi.entity_search.EntityFinder import EntityFinder\n\nfinder = EntityFinder(atlas_client)\nsearch_result = finder.search_full_text("aws_s3_bucket", "test")\n\nEntityFinder.show_search_results(search_result)\nentity_number = EntityFinder.get_entity_number(search_result)\nprint("Find " + str(entity_number) + " result in total")\n\nguid_list = EntityFinder.get_result_entity_guid_list(search_result)\n\nfor guid in guid_list:\n    print("result:" + guid)\n\n\n```\n\n### Atlas entities CRUD\n\n#### S3 entities\n\n```python\nfrom atlaspyapi.entity_management.s3.S3BucketManager import S3BucketManager\n\ns3_bucket_manager = S3BucketManager(atlas_client)\n\n# creat s3 bucket in atlas\nname = "test"\ndomain = "s3://test.org"\nqualified_name = "s3://test.org/test1"\ndescription = "test for me"\ns3_bucket_manager.create_entity(name, domain, qualified_name, description)\n# get s3 bucket via guid\nguid = "9642d134-4d0e-467c-8b36-ca73902d4c14"\ne = s3_bucket_manager.get_entity(guid)\ns3_bucket_manager.show_entity_attributes(e)\ne_attributes = s3_bucket_manager.get_entity_attributes(e)\ne_attributes_key_list = s3_bucket_manager.get_s3_attributes_key_list(e)\nprint(e_attributes_key_list)\nprint(e_attributes[\'description\'])\n\n# update s3 bucket attributes\ns3_bucket_manager.update_entity(guid, \'description\', \'update description from api\')\n\n# delete s3 bucket\ns3_bucket_manager.delete_entity(guid)\n\n``` \n\n#### Hive entities\n\n```python\nhive_db = HiveDBManager(atlas_client)\nhive_table = HiveTableManager(atlas_client)\nhive_column = HiveColumnManager(atlas_client)\n\n# insert hive tables\nhive_db.create_entity("pengfei-stock", "pengfei.org", "database for my stock market",owner="pliu",location="pengfei.org")\nhive_table.create_entity("favorite", "pengfei.org@pengfei-stock", "favorite stock")\nhive_column.create_entity("stock_id", "int", "pengfei.org@pengfei-stock.favorite", "id of the stock")\nhive_column.create_entity("stock_name", "string", "pengfei.org@pengfei-stock.favorite", "name of the stock")\n\n```\n\n### Generate atlas entity json file\nIf you want to use the Atlas rest api by yourself, we also provide you the support of json file generation\n\n```python\nfrom atlaspyapi.entity_source_generation.S3BucketEntityGenerator import S3BucketEntityGenerator\nname = "test"\ndomain = "s3://test.org"\nqualified_name = "s3://test.org/test1"\ndescription = "test for me"\n\ns3_bucket_json_source = S3BucketEntityGenerator.generate_s3_bucket_json_source(name, domain,qualified_name,description\n                                                                               , creator_id="toto")\nprint(s3_bucket_json_source)\n\n```\n\n## Package organization\n\n### entity_source_generation\n\nIn the entity_source_generation folder, you can find various templates and generators for generating atlas entities.\n\n### entity_search\n\nIn the entity_search folder, you can find EntityFinder which help you to find entity in an Atlas instance\n\n### entity_management\n\nIn the entity_management folder, you can find various rest client to upload entities into atlas\n\n### docs\n\nIn the docs folder, you can find helper function which shows which entity type and attributes are supported by this api\n\n\n## Prerequisites\n\nThis tool only requires python 3.7 or above\n\n## Supported OS\n\nWindows XP/7/8/10\n\nLinux  \n\nMacOS\n\n\n## Authors\n\n* **Pengfei Liu** \n\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n\n## Acknowledgement\n\nThis package was created by using [verdan/pyatlasclient](<https://github.com/verdan/pyatlasclient>) project',
    'author': 'pengfei',
    'author_email': 'liu.pengfei@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pengfei99/AtlasPyApi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
