import pytest

from ckanext.short_urls.tests import short_urls_db_setup


@pytest.fixture(autouse=True)
def short_urls_setup(clean_db):
    short_urls_db_setup()
