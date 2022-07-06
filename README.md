[![Tests](https://github.com/fredericlam/ckanext-csutheme/workflows/Tests/badge.svg?branch=main)](https://github.com/fredericlam/ckanext-csutheme/actions)

# ckanext-csutheme

**TODO:** Put a description of your extension here:  What does it do? What features does it have? Consider including some screenshots or embedding a video!


## Requirements

**TODO:** For example, you might want to mention here which versions of CKAN this
extension works with.

If your extension works across different versions you can add the following table:

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | not tested    |

Suggested values:

* "yes"
* "not tested" - I can't think of a reason why it wouldn't work
* "not yet" - there is an intention to get it working
* "no"


## Installation

**TODO:** Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

Note ex: https://snyk.io/advisor/python/ckan/functions/ckan.plugins

To install ckanext-csutheme:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/fredericlam/ckanext-csutheme.git
    cd ckanext-csutheme
    pip install -e .
	pip install -r requirements.txt

3. Add `csutheme` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

None at present

**TODO:** Document any optional config settings here. For example:

	# The minimum number of hours to wait before re-checking a resource
	# (optional, default: 24).
	ckanext.csutheme.some_setting = some_default_value


## Developer installation

To install ckanext-csutheme for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/fredericlam/ckanext-csutheme.git
    cd ckanext-csutheme
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-csutheme

If ckanext-csutheme should be available on PyPI you can follow these steps to publish a new version:

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

## Custom

### Virtualenv
--------------
virtualenv --python=/usr/bin/python2.7 --no-site-packages /etc/ckan/default
. /etc/ckan/default/bin/activate

$ . ~/venv/bin/activate && cd ~/venv/src/ckanext-csutheme
$ python setup.py develop

### User managements
---------------

* add user
$ ckan user add LOGIN email=ADRESS_EMAIL name=LOGIN

* populate with test data
$ ckan -c /etc/ckan/production.ini seed basic
$ ckan -c /etc/ckan/production.ini seed family
$ ckan -c /etc/ckan/production.ini seed gov
$ ckan -c /etc/ckan/production.ini seed hierarchy
$ ckan -c /etc/ckan/production.ini seed search
$ ckan -c /etc/ckan/production.ini seed translations
$ ckan -c /etc/ckan/production.ini seed user
$ ckan -c /etc/ckan/production.ini seed vocabs

### Overide environments vars
use ckanext-envvars https://github.com/okfn/ckanext-envvars

### Known Issues
----------------

#### Option A : Accessing virtual machine using docker for mac
$ docker run -it --rm --privileged --pid=host justincormack/nsenter1
then 
$ cd /var/lib/docker/volumes/

#### Option B
$ docker run -it --rm --entrypoint sh ckan-csu_ckan-dev (name of images)

* Install ckan pages plugin
$ ckan pages initdb

### Install linux packages into container terminal
$ apk add --update util-linux

### i18ln translation
$ pip install --upgrade Babel

### ckanapi installation
For more features into ckan data portal data, install ckanapi from https://github.com/ckan/ckanapi

### scheming csu definition
Add into ckan.ini file
scheming.presets = ckanext.scheming:presets.json
scheming.group_schemas = ckanext.scheming:groups.json
scheming.organization_schemas = ckanext.scheming:organizations.json

## Rest API urls

Among Rest API urls found via documentation, stackoverflow, official github, or routing config (via ckan debugger) some of them are not working. This is a list of working and test urls. 

* /api/3/action/organization_list
* /api/3/action/group_list
* /api/3/action/tag_list

## Emails notifications

curl -X POST -H "Authorization:e7724f34-1f74-4f63-ad1b-718f29ae32f6" http://ckan:8084/api/3/action/send_email_notifications

## Routes update since 2.9

Routes use Flask and not Pylons anymore.

https://github.com/ckan/ckan/wiki/Migration-from-Pylons-to-Flask#flask-views-blueprints-and-routing

