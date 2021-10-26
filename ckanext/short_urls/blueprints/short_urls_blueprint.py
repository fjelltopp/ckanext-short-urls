from flask import Blueprint
from flask.views import MethodView
import ckan.plugins.toolkit as toolkit
from ckan.lib import helpers as h
from ckanext.short_urls.model import ObjectType
from ckanext.short_urls.logic import get_short_url_from_code


short_urls_blueprint = Blueprint(
    u'short_urls',
    __name__,
    url_prefix=u'/link'
)


@short_urls_blueprint.route('/<code>', methods=['GET'])
def redirect(code):
    short_url = get_short_url_from_code(code)
    object_type = short_url['object_type']
    if object_type == ObjectType.DATASET:
        url = toolkit.url_for(
            'dataset.read',
            id=short_url['object_id']
        )
    elif object_type == ObjectType.RESOURCE:
        resource = toolkit.get_action('resource_show')(
            {'ignore_auth': True}, {'id': short_url['object_id']}
        )
        url = toolkit.url_for(
            'resource.read',
            id=resource['package_id'],
            resource_id=resource['id']
        )
    else:
        raise TypeError(
            f'object_type {object_type} unrecognized'
        )
    return h.redirect_to(url)
