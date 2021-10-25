from ckanext.short_urls.logic import (
    short_url_create
)
from unittest import mock
from ckan.tests import factories
import ckan.plugins.toolkit as t
from ckanext.short_urls.logic import get_short_url_from_object_id
from ckanext.short_urls.model import ObjectType
#from ckanext.short_urls.command import assign_short_urls_to_existing_dataset_and_resources

dataset_or_resource_after_create_action = \
    'ckanext.short_urls.plugin.ShortUrlsPlugin.after_create'


class TestCommand(object):

    def assign_short_urls_to_existing_dataset_and_resources(self):
        # TODO: move this function into command.py
        import ckan.model
        from ckan.plugins import toolkit
        sysadmin_user = ckan.model.User.get('testsysadmin')
        datasets = toolkit.get_action('current_package_list_with_resources')(
            {
                'model': ckan.model,
                'session': ckan.model.Session,
                'user': sysadmin_user,
            }, {}
        )
        for dataset in datasets:
            short_url_create(ObjectType.DATASET, dataset['id'])
            for resource in dataset['resources']:
                short_url_create(ObjectType.RESOURCE, resource['id'])

    def test_assigning_short_urls_to_all_existing_datasets_command(self):
        with mock.patch(dataset_or_resource_after_create_action):
            dataset = factories.Dataset()
        short_url = get_short_url_from_object_id(dataset['id'])
        assert not short_url
        self.assign_short_urls_to_existing_dataset_and_resources()
        short_url = get_short_url_from_object_id(dataset['id'])
        assert short_url

    def test_assigning_short_urls_to_all_existing_resource_command(self):
        with mock.patch(dataset_or_resource_after_create_action):
            dataset = factories.Dataset()
            resource = factories.Resource(package_id=dataset['id'])
        short_url = get_short_url_from_object_id(resource['id'])
        assert not short_url
        self.assign_short_urls_to_existing_dataset_and_resources()
        short_url = get_short_url_from_object_id(resource['id'])
        assert short_url
