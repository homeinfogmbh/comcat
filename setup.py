#! /usr/bin/env python3
"""Install script."""

from setuptools import setup


setup(
    name='comcat',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info@homeinfo.de>',
    maintainer='Richard Neumann',
    maintainer_email='<r.neumann@homeinfo.de>',
    requires=[
        'authlib',
        'cmslib',
        'comcatlib',
        'damage_report',
        'flask',
        'hinews',
        'his',
        'hisfs',
        'lptlib',
        'mdb',
        'peewee',
        'qrcode',
        'setuptools',
        'tenant2tenant',
        'wsgilib'
    ],
    packages=[
        'comcat',
        'comcat.app',
        'comcat.app.damage_report',
        'comcat.his',
        'comcat.his.content'
    ],
    description='HOMEINFO ComCat.'
)
