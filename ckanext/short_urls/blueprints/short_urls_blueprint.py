from flask import Blueprint
import ckan.plugins.toolkit as toolkit
from ckan.lib import helpers as h
from ckanext.short_urls.model import ObjectType
from ckanext.short_urls.logic import short_url_get


short_urls_blueprint = Blueprint(
    u'short_urls_blueprint',
    __name__
)


def short_url_redirect(short_url_code):
    short_url = short_url_get(short_url_code)
    object_type = short_url['object_type']
    if short_url['object_state'] == 'active':
        if object_type == ObjectType.DATASET:
            url = toolkit.url_for(
                'dataset.read',
                id=short_url['object_id']
            )
        elif object_type == ObjectType.RESOURCE:
            url = toolkit.url_for(
                'resource.read',
                id=short_url['object_id']
            )
        else:
            raise BaseException(
                f'object_type {object_type} unrecognized'
            )
    else:
        # TODO: what do we do if the object.state != active??
        url = '#'
    return h.redirect_to(url)


short_urls_blueprint.add_url_rule(
    u'/link/<short_url_code>',
    view_func=short_url_redirect
)
