import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.short_urls.model import (
    ObjectType, tables_exists
)
from ckanext.short_urls.logic import (
    short_url_create, get_short_url_from_object_id
)
from ckanext.short_urls import command
from ckanext.short_urls.blueprints import blueprints

log = logging.getLogger(__name__)


def _data_dict_is_resource(data_dict):
    return not (
        u'creator_user_id' in data_dict
        or u'owner_org' in data_dict
        or u'resources' in data_dict
        or data_dict.get(u'type') == u'dataset'
    )


class ShortUrlsPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # IClick
    def get_commands(self):
        return command.get_commands()

    # IConfigurer
    def update_config(self, config_):
        if not tables_exists():
            log.critical(
                "The short_urls extension requires a database setup. Please run "
                "the following to create the database tables: \n"
                "ckan short_urls initdb"
            )
        else:
            log.debug('short_urls tables verified to exist')
        log.info('short_urls Plugin is enabled')
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'ckanext-short-urls')

    # IBlueprint
    def get_blueprint(self):
        return blueprints

    # IPackageController & IResourceController
    def after_create(self, context, data_dict):
        if _data_dict_is_resource(data_dict):
            short_url_create(ObjectType.RESOURCE, data_dict['id'])
        else:
            short_url_create(ObjectType.DATASET, data_dict['id'])

    # ITemplateHelpers
    def get_helpers(self):
        return {
            u'get_short_url_from_object_id': get_short_url_from_object_id,
        }
