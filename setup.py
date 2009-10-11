import os
import sys
from setuptools import setup, find_packages

setup(
    name = 'django-metafeed',
    version = '0.1.0',
    description = '''Django feed aggregator, to merge few feeds into the one.''',
    keywords = 'django apps',
    license = 'New BSD License',
    author = 'Alexander Artemenko',
    author_email = 'svetlyak.40wt@gmail.com',
    url = 'http://github.com/svetlyak40wt/django-metafeed/',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    #package_dir = {'': 'src'},
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
)

