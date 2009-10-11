import os.path

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/django.db'
INSTALLED_APPS = ['django_metafeed']
ROOT_URLCONF = ['django_metafeed.urls']

TEMPLATE_DIRS = [
    os.path.join(
        os.path.dirname(__file__),
        'testtemplates'
    ),
]

