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
    install_requires=[
        'authlib',
        'ccmessenger',
        'cmslib',
        'comcatlib',
        'damage_report',
        'filedb',
        'flask',
        'hinews',
        'hisfs',
        'lptlib',
        'marketplace',
        'mdb',
        'notificationlib',
        'peewee',
        'peeweeplus',
        'qrcode',
        'recaptcha',
        'reportlib',
        'tenantcalendar',
        'tenantforum',
        'wsgilib'
    ],
    packages=[
        'comcat',
        'comcat.damage_report'
    ],
    description='HOMEINFO ComCat.'
)
