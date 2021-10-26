[![Tests](https://github.com/fjelltopp/ckanext-short-urls/workflows/Tests/badge.svg?branch=main)](https://github.com/fjelltopp/ckanext-short-urls/actions)

# ckanext-short-urls

This extensions creates a short permanent urls for datasets and resources
so they can be referenced in articles and other places.
https://yourckan.org/link/xxxx -> https://yourcan.org/dataset/my-dataset/resource/xyz


## Requirements

The extension has been developed and tested with CKAN 2.9 + python3

## Installation

To install ckanext-short-urls:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate
2. Install the extension

   pip install ckanext-short-urls
3. [optional] Or install from source:

    git clone https://github.com/fjelltopp/ckanext-short-urls.git
    cd ckanext-short-urls
    pip install -e .
    pip install -r requirements.txt
4. Add `short-urls` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).
5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:
   ```
   sudo service apache2 reload
   ``` 
7. Initialize the extensions db
   ```
   ckan -c ckan.ini short-urls initdb
   ```


## Migration of already existing datasets and resources

You can create short urls for all already existing datasets and resources with the command:
   ```bash
   ckan -c ckan.ini short-urls migrate
   ```



## Developer installation

To install ckanext-short-urls for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/fjelltopp/ckanext-short-urls.git
    cd ckanext-short-urls
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-short-urls

If ckanext-short-urls should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
