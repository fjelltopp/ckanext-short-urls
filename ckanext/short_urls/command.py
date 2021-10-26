import click
from sqlalchemy.exc import IntegrityError

import ckan.model
from ckan.plugins import toolkit
from ckanext.short_urls.model import (
    init_tables, tables_exists, ObjectType
)
from ckanext.short_urls.logic import short_url_create


@click.group()
def short_urls():
    '''short_urls commands
    '''
    pass


@short_urls.command()
@click.pass_context
def initdb(ctx):
    """Creates the necessary tables for short_urls in the database.
    """
    if tables_exists():
        click.secho('ShortUrl tables already exist', fg="green")
        ctx.exit(0)

    init_tables()
    click.secho('ShortUrl tables created', fg="green")


@short_urls.command()
def migrate():
    datasets = toolkit.get_action('current_package_list_with_resources')(
        {
            'model': ckan.model,
            'session': ckan.model.Session,
            'user': None, # will exclude private datasets
            'ignore_auth': True
        }, {}
    )
    for dataset in datasets:
        try:
            short_url_create(ObjectType.DATASET, dataset['id'])
        except IntegrityError:
            # short url exists
            pass
        for resource in dataset['resources']:
            try:
                short_url_create(ObjectType.RESOURCE, resource['id'])
            except IntegrityError:
                # short url exists
                pass


def get_commands():
    return [short_urls]
