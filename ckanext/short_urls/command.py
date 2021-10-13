import click
from ckanext.short_urls.model import init_tables, tables_exists


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
        click.secho('ShortUrls tables already exist', fg="green")
        ctx.exit(0)

    init_tables()
    click.secho('ShortUrls tables created', fg="green")


def get_commands():
    return [short_urls]
