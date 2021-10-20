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


def get_short_url_from_code(code):
    short_url = model.Session.query(ShortUrl)\
        .filter(ShortUrl.code == code)\
        .one_or_none()
    return short_url.to_dict()


def get_short_url_from_object_id(object_id):
    short_url = model.Session.query(ShortUrl)\
        .filter(ShortUrl.object_id == object_id)\
        .one_or_none()
    return short_url.to_dict()


def _generate_random_string(length=8):
    # taken from https://bit.ly/3nxGSMo
    alphanumeric_chars = string.ascii_lowercase + string.digits
    return ''.join(
        random.SystemRandom().choice(alphanumeric_chars)
        for _ in range(length)
    )


def _generate_unique_short_url_code():
    def _short_url_code_exists(code):
        short_urls_using_code = model.Session.query(ShortUrl)\
            .filter(ShortUrl.code == code)\
            .count()
        return short_urls_using_code > 0
    code = _generate_random_string()
    while _short_url_code_exists(code):
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
    return get_short_url_from_code(new_short_url.code)
