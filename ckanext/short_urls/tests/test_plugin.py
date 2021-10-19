import pytest
from unittest import mock
from ckan.model import core
from ckan.lib.helpers import url_for
from ckan.tests import factories
import ckan.plugins.toolkit as t
from ckanext.short_urls.logic import get_short_url_from_object_id
from sqlalchemy.orm.exc import MultipleResultsFound
from bs4 import BeautifulSoup

generate_unique_short_url_code_function = \
    'ckanext.short_urls.logic._generate_unique_short_url_code'


@pytest.mark.usefixtures('with_plugins')
class TestPlugin(object):

    def test_creating_multiple_dataset_short_urls_with_the_same_code(self):
        with mock.patch(generate_unique_short_url_code_function) as mocked_function:
            mocked_function.return_value = 'mocked_code'
            factories.Dataset()
            with pytest.raises(MultipleResultsFound):
                factories.Dataset()

    def test_creating_multiple_resource_short_urls_with_the_same_code(self):
        dataset = factories.Dataset()
        with mock.patch(generate_unique_short_url_code_function) as mocked_function:
            mocked_function.return_value = 'mocked_code'
            factories.Resource(package_id=dataset['id'])
            with pytest.raises(MultipleResultsFound):
                factories.Resource(package_id=dataset['id'])

    def test_short_url_object_state_for_a_active_dataset(self):
        dataset = factories.Dataset()
        short_url = get_short_url_from_object_id(dataset['id'])
        assert short_url['object_state'] == core.State.ACTIVE

    def test_short_url_object_state_for_a_active_resource(self):
        resource = factories.Resource()
        short_url = get_short_url_from_object_id(resource['id'])
        assert short_url['object_state'] == core.State.ACTIVE

    def test_short_url_object_state_for_a_deleted_dataset(self):
        dataset = factories.Dataset()
        t.get_action('package_delete')(
            {'user': factories.Sysadmin()['name']},
            {'id': dataset['id']}
        )
        short_url = get_short_url_from_object_id(dataset['id'])
        assert short_url['object_state'] == core.State.DELETED

    def test_short_url_object_state_for_a_deleted_resource(self):
        resource = factories.Resource()
        t.get_action('resource_delete')(
            {'user': factories.Sysadmin()['name']},
            {'id': resource['id']}
        )
        short_url = get_short_url_from_object_id(resource['id'])
        assert short_url['object_state'] == core.State.DELETED

    def test_short_url_on_dataset_page_is_correct(self, app):
        user = factories.User()
        dataset = dataset = factories.Dataset(user=user)
        short_url = get_short_url_from_object_id(dataset['id'])
        response = app.get(
            url=url_for(
                'dataset.read',
                id=dataset['name'],
            ),
            extra_environ={'REMOTE_USER': user['name']}
        )
        soup = BeautifulSoup(response.body)
        short_url_div = soup.find(id='ShortUrl')
        short_url_href = short_url_div.find('a')['href']
        assert f"link/{short_url['code']}" == short_url_href

    def test_short_url_on_resource_page_is_correct(self, app):
        user = factories.User()
        dataset = dataset = factories.Dataset(user=user)
        resource = factories.Resource(package_id=dataset['id'])
        short_url = get_short_url_from_object_id(resource['id'])
        response = app.get(
            url=url_for(
                'resource.read',
                id=dataset['id'],
                resource_id=resource['id']
            ),
            extra_environ={'REMOTE_USER': user['name']}
        )
        soup = BeautifulSoup(response.body)
        short_url_div = soup.find(id='ShortUrl')
        short_url_href = short_url_div.find('a')['href']
        assert f"link/{short_url['code']}" == short_url_href
