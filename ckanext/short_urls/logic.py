import logging
import string
import random
from ckan import model
from ckanext.short_urls.model import (
    ShortUrl,
    ObjectType
)
log = logging.getLogger(__name__)


def _get_short_url_object_state(object_type, object_id):
    if object_type == ObjectType.DATASET:
        # TODO: replace with db request
        return 'active'
    elif object_type == ObjectType.RESOURCE:
        # TODO: replace with db request
        return 'deleted'
    else:
        raise BaseException(
            f'object_type {object_type} unrecognized'
        )


def _get_short_url_from_code(code):
    short_url = model.Session.query(ShortUrl)\
        .filter(ShortUrl.code == code)\
        .one_or_none()
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
    new_short_url = ShortUrl(
        code=_generate_unique_short_url_code(),
        object_type=object_type,
        object_id=object_id,
    )
    model.Session.add(new_short_url)
    model.repo.commit()
    return _get_short_url_from_code(new_short_url['code'])


def short_url_get(code):
    return _get_short_url_from_code(code)
