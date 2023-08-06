from os import path
from setuptools import find_namespace_packages, setup

from huscy.project_documents import __version__


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='huscy.project_documents',
    version=__version__,
    license='AGPLv3+',

    description='Managing document files for projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Alexander Tyapkov, Mathias Goldau, Stefan Bunde',
    author_email='tyapkov@gmail.com, goldau@cbs.mpg.de, stefanbunde+git@posteo.de',

    url='https://bitbucket.org/huscy/project_documents',

    packages=find_namespace_packages(include=['huscy.*']),

    install_requires=[
        'huscy.projects',
    ],
    extras_require={
        'development': [
            'psycopg2-binary',
        ],
        'testing': [
            'tox',
            'watchdog==0.9',
        ],
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
    ],
)
