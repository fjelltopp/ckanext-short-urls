from ckan import model
from ckanext.short_urls.model import (
    OBJECT_TYPE_DATASET,
    OBJECT_TYPE_RESOURCE,
    ShortUrls
)


def _get_short_url_object_state(object_type, object_id):
    if object_type == OBJECT_TYPE_DATASET:
        # TODO: replace with db request
        return 'active'
    elif object_type == OBJECT_TYPE_RESOURCE:
        # TODO: replace with db request
        return 'deleted'
    else:
        raise BaseException(
            f'object_type {object_type} unrecognized'
        )


def _get_short_url_from_hash(hash):
    short_url = model.Session.query(ShortUrls)\
        .filter(ShortUrls.hash == hash)\
        .one()
    return_dict = short_url.to_dict()
    return_dict.update({
        'object_state': _get_short_url_object_state(
            object_type=short_url.object_type,
            object_id=short_url.object_id
        )
    })
    return return_dict


def short_url_create(object_type, object_id):
    new_short_url = ShortUrls(object_type, object_id)
    # TODO: retry on hash unique error
    # TODO: raise error on object_type/object_id unique error
    model.Session.add(new_short_url)
    model.repo.commit()
    return _get_short_url_from_hash(new_short_url['hash'])


def short_url_get(hash):
    return _get_short_url_from_hash(hash)
