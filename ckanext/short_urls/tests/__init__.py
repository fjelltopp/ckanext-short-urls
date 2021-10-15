from ckan import model
from ckanext.short_urls.model import tables_exists, init_tables


def short_urls_db_setup():
    if not tables_exists():
        init_tables()


def get_context(user):
    return {
        'model': model,
        'user': user if isinstance(user, str) else user['name']
    }
