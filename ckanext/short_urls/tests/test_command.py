from unittest import mock
from ckan.tests import factories
from ckanext.short_urls.logic import get_short_url_from_object_id
from ckanext.short_urls.command import migrate_data

dataset_or_resource_after_create_action = \
    'ckanext.short_urls.plugin.ShortUrlsPlugin.after_create'


class TestCommand(object):

    def test_assigning_short_urls_to_all_existing_datasets_command(self):
        with mock.patch(dataset_or_resource_after_create_action):
            dataset = factories.Dataset()
        short_url = get_short_url_from_object_id(dataset['id'])
        assert not short_url
        migrate_data()
        short_url = get_short_url_from_object_id(dataset['id'])
        assert short_url

    def test_assigning_short_urls_to_all_existing_resource_command(self):
        with mock.patch(dataset_or_resource_after_create_action):
            dataset = factories.Dataset()
            resource = factories.Resource(package_id=dataset['id'])
        short_url = get_short_url_from_object_id(resource['id'])
        assert not short_url
        migrate_data()
        short_url = get_short_url_from_object_id(resource['id'])
        assert short_url
