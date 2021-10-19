import logging
import string
import random
from ckan.model import core
from ckan import model
import ckan.plugins.toolkit as t
from ckanext.short_urls.model import (
    ShortUrl,
    ObjectType
)
log = logging.getLogger(__name__)


def _get_short_url_object_state(object_type, object_id):
    if object_type == ObjectType.DATASET:
        dataset = t.get_action('package_show')(
            {'ignore_auth': True}, {'id': object_id}
        )
        return dataset['state']
    elif object_type == ObjectType.RESOURCE:
        try:
            # TODO: confirm it's safe to assume all
            # resource_show failures = deleted state
            resource = t.get_action('resource_show')(
                {'ignore_auth': True}, {'id': object_id}
            )
            return resource['state']
        except:
            return core.State.DELETED
    else:
        raise BaseException(
            f'object_type {object_type} unrecognized'
        )


def _format_short_url_dictionary(short_url):
    if short_url:
        return_dict = short_url.to_dict()
        return_dict.update({
            'object_state': _get_short_url_object_state(
                object_type=short_url.object_type,
                object_id=short_url.object_id
            )
        })
        return return_dict
    else:
        return None


def _get_short_url_from_code(code):
    short_url = model.Session.query(ShortUrl)\
        .filter(ShortUrl.code == code)\
        .one_or_none()
    return _format_short_url_dictionary(short_url)


def get_short_url_from_object_id(object_id):
    short_url = model.Session.query(ShortUrl)\
        .filter(ShortUrl.object_id == object_id)\
        .one_or_none()
    return _format_short_url_dictionary(short_url)


def _generate_random_string(length=8):
    # taken from https://bit.ly/3nxGSMo
    alphanumeric_chars = string.ascii_lowercase + string.digits
    return ''.join(
        random.SystemRandom().choice(alphanumeric_chars)
        for _ in range(length)
    )


def _generate_unique_short_url_code():
    code = _generate_random_string()
    while _get_short_url_from_code(code):
        log.info(f'ShortUrl Code {code} already taken. Retrying...')
        code = _generate_random_string()
    return code


def short_url_create(object_type, object_id):
    if object_type == ObjectType.DATASET:
        try:
            t.get_action('package_show')(
                {'ignore_auth': True}, {'id': object_id}
            )
        except:
            raise BaseException(
                f'Dataset {object_id} not found'
            )
    elif object_type == ObjectType.RESOURCE:
        try:
            t.get_action('resource_show')(
                {'ignore_auth': True}, {'id': object_id}
            )
        except:
            raise BaseException(
                f'Resource {object_id} not found'
            )
    else:
        raise BaseException(
            f'object_type {object_type} unrecognized'
        )
    new_short_url = ShortUrl(
        code=_generate_unique_short_url_code(),
        object_type=object_type,
        object_id=object_id,
    )
    model.Session.add(new_short_url)
    model.repo.commit()
    return _get_short_url_from_code(new_short_url.code)
