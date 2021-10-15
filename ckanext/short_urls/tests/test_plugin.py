import ckanext.short_urls.plugin as plugin
from ckanext.short_urls.logic import (
    short_url_create,
    short_url_get
)
from ckanext.short_urls.model import ObjectType


def _set_object_to_deleted(object_type, object_id):
    if object_type == ObjectType.DATASET:
        # TODO: set dataset to deleted
        pass
    elif object_type == ObjectType.RESOURCE:
        # TODO: set resource to deleted
        pass
    else:
        raise BaseException(
            f'Unhandled object_type: {object_type}'
        )


def test_creating_multiple_short_urls_for_the_same_dataset():
    short_url_create(ObjectType.DATASET, 1)
    # TODO: this should fail
    short_url_create(ObjectType.DATASET, 1)


def test_creating_multiple_short_urls_for_the_same_resource():
    short_url_create(ObjectType.RESOURCE, 1)
    # TODO: this should fail
    short_url_create(ObjectType.RESOURCE, 1)


def test_short_url_for_active_dataset():
    short_url = short_url_create(ObjectType.DATASET, 1)
    fetched_short_url = short_url_get(short_url['hash'])
    assert short_url['id'] == fetched_short_url['id']
    assert short_url['hash'] == fetched_short_url['hash']
    assert short_url['object_type'] == fetched_short_url['object_type']
    assert short_url['object_id'] == fetched_short_url['object_id']


def test_short_url_for_active_resource():
    short_url = short_url_create(ObjectType.RESOURCE, 1)
    fetched_short_url = short_url_get(short_url['hash'])
    assert short_url['id'] == fetched_short_url['id']
    assert short_url['hash'] == fetched_short_url['hash']
    assert short_url['object_type'] == fetched_short_url['object_type']
    assert short_url['object_id'] == fetched_short_url['object_id']


def test_short_url_for_deleted_dataset():
    short_url = short_url_create(ObjectType.DATASET, 1)
    _set_object_to_deleted(ObjectType.DATASET, 1)
    fetched_short_url = short_url_get(short_url['hash'])
    assert short_url['object_state'] == 'active'
    assert fetched_short_url['object_state'] == 'deleted'


def test_short_url_for_deleted_resource():
    short_url = short_url_create(ObjectType.RESOURCE, 1)
    _set_object_to_deleted(ObjectType.RESOURCE, 1)
    fetched_short_url = short_url_get(short_url['hash'])
    assert short_url['object_state'] == 'active'
    assert fetched_short_url['object_state'] == 'deleted'
