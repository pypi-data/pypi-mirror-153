# This is your Project Root
import pkg_resources

CONFIG_PATH = pkg_resources.resource_filename("atlaspyapi", "config/config.ini")

TEMPLATE_FOLDER_PATH = pkg_resources.resource_filename(
    "atlaspyapi", "entity_source_generation/template"
)
