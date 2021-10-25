from ckanext.short_urls.logic import (
    short_url_create
)
import pytest
from unittest import mock
from ckan.model import core
from ckan.lib.helpers import url_for
from ckan.tests import factories
import ckan.plugins.toolkit as t
from ckanext.short_urls.logic import get_short_url_from_object_id
from ckanext.short_urls.model import ObjectType
from sqlalchemy.exc import IntegrityError
from bs4 import BeautifulSoup

generate_unique_short_url_code_function = \
    'ckanext.short_urls.logic._generate_unique_short_url_code'
dataset_or_resource_after_create_action = \
    'ckanext.short_urls.plugin.ShortUrlsPlugin.after_create'


@pytest.mark.usefixtures('with_plugins')
class TestPlugin(object):

    def test_short_url_is_created_on_dataset_create(self):
        dataset = factories.Dataset()
        short_url = get_short_url_from_object_id(dataset['id'])
        assert short_url['code']
        assert short_url['object_type'] == ObjectType.DATASET
        assert short_url['object_id'] == dataset['id']

    def test_short_url_is_created_on_resource_create(self):
        resource = factories.Resource()
        short_url = get_short_url_from_object_id(resource['id'])
        assert short_url['code']
        assert short_url['object_type'] == ObjectType.RESOURCE
        assert short_url['object_id'] == resource['id']

    def test_creating_multiple_dataset_short_urls_with_the_same_code(self):
        with mock.patch(
            generate_unique_short_url_code_function,
            return_value='duplicate_short_code'
        ):
            factories.Dataset()
            with pytest.raises(IntegrityError):
                factories.Dataset()

    def test_creating_multiple_resource_short_urls_with_the_same_code(self):
        dataset = factories.Dataset()
        with mock.patch(
            generate_unique_short_url_code_function,
            return_value='duplicate_short_code'
        ):
            factories.Resource(package_id=dataset['id'])
            with pytest.raises(IntegrityError):
                factories.Resource(package_id=dataset['id'])

    def test_creating_multiple_short_urls_for_the_same_dataset_gives_an_error(self):
        dataset = factories.Dataset()
        with pytest.raises(IntegrityError):
            short_url_create(ObjectType.DATASET, dataset['id'])

    def test_creating_multiple_short_urls_for_the_same_resource_gives_an_error(self):
        dataset = factories.Dataset()
        resource = factories.Resource(package_id=dataset['id'])
        with pytest.raises(IntegrityError):
            short_url_create(ObjectType.RESOURCE, resource['id'])

    def test_short_url_on_dataset_page_is_correct(self, app):
        user = factories.User()
        dataset = factories.Dataset(user=user)
        short_url = get_short_url_from_object_id(dataset['id'])
        expected_short_url_href = url_for(
            'short_urls.redirect',
            code=short_url['code'],
            _external=True
        )
        response = app.get(
            url=url_for(
                'dataset.read',
                id=dataset['name'],
            ),
            extra_environ={'REMOTE_USER': user['name']}
        )
        soup = BeautifulSoup(response.body)
        short_url_div = soup.find(id='DatasetPageShortUrlContainer')
        short_url_href = short_url_div.find('a')['href']
        assert short_url_href == expected_short_url_href

    def test_short_url_on_resource_page_is_correct(self, app):
        user = factories.User()
        dataset = factories.Dataset(user=user)
        resource = factories.Resource(package_id=dataset['id'])
        short_url = get_short_url_from_object_id(resource['id'])
        expected_short_url_href = url_for(
            'short_urls.redirect',
            code=short_url['code'],
            _external=True
        )
        response = app.get(
            url=url_for(
                'resource.read',
                id=dataset['id'],
                resource_id=resource['id']
            ),
            extra_environ={'REMOTE_USER': user['name']}
        )
        soup = BeautifulSoup(response.body)
        short_url_div = soup.find(id='ResourcePageShortUrlContainer')
        short_url_href = short_url_div.find('a')['href']
        assert short_url_href == expected_short_url_href

    def test_short_url_for_dataset_redirects_to_dataset_page(self, app):
        user = factories.User()
        dataset = factories.Dataset(user=user)
        short_url = get_short_url_from_object_id(dataset['id'])
        response = app.get(
            url=url_for(
                'short_urls.redirect',
                code=short_url['code']
            ),
            extra_environ={'REMOTE_USER': user['name']},
            status=302,
            follow_redirects=False
        )
        dataset_read_url = url_for(
            'dataset.read',
            id=dataset['id'],
            _external=True
        )
        assert response.headers['location'] == dataset_read_url

    def test_short_url_for_resource_redirects_to_resource_page(self, app):
        user = factories.User()
        dataset = factories.Dataset(user=user)
        resource = factories.Resource(package_id=dataset['id'])
        short_url = get_short_url_from_object_id(resource['id'])
        response = app.get(
            url=url_for(
                'short_urls.redirect',
                code=short_url['code']
            ),
            extra_environ={'REMOTE_USER': user['name']},
            status=302,
            follow_redirects=False
        )
        resource_read_url = url_for(
            'resource.read',
            id=dataset['id'],
            resource_id=resource['id'],
            _external=True
        )
        assert response.headers['location'] == resource_read_url

    def test_short_url_on_dataset_page_is_hidden_if_missing(self, app):
        user = factories.User()
        with mock.patch(dataset_or_resource_after_create_action):
            dataset = factories.Dataset(user=user)
        response = app.get(
            url=url_for(
                'dataset.read',
                id=dataset['name'],
            ),
            extra_environ={'REMOTE_USER': user['name']}
        )
        soup = BeautifulSoup(response.body)
        short_url_div = soup.find(id='DatasetPageShortUrlContainer')
        assert not short_url_div

    def test_short_url_on_resource_page_is_hidden_if_missing(self, app):
        user = factories.User()
        dataset = factories.Dataset(user=user)
        with mock.patch(dataset_or_resource_after_create_action):
            resource = factories.Resource(package_id=dataset['id'])
        response = app.get(
            url=url_for(
                'resource.read',
                id=dataset['id'],
                resource_id=resource['id']
            ),
            extra_environ={'REMOTE_USER': user['name']}
        )
        soup = BeautifulSoup(response.body)
        short_url_div = soup.find(id='ResourcePageShortUrlContainer')
        assert not short_url_div
