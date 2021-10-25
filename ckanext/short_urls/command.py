import click
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
#@click.pass_context
def assign_short_urls_to_existing_dataset():
    pass
    # datasets = toolkit.get_action('package_list')(
    #     {'ignore_auth': True}, {}
    # )
    # assert datasets
    # for dataset in datasets:
    #     short_url_create(ObjectType.DATASET, dataset['id'])


def get_commands():
    return [short_urls]
