# -*- coding: utf-8 -*-
"""Installer for the collective.easynewsletter-combined-send package."""

from setuptools import find_packages, setup

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.easynewsletter-combined-send',
    version='1.5.1',
    description="Extend EasyNewsletter to send languages combined one email.",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS',
    author='Maik Derstappen',
    author_email='md@derico.de',
    url='https://github.com/collective/collective.easynewsletter-combined-send',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.easynewsletter-combined-send',
        'Source': 'https://github.com/collective/collective.easynewsletter-combined-send',
        'Tracker': 'https://github.com/collective/collective.easynewsletter-combined-send/issues',
        # 'Documentation': 'https://collective.easynewsletter-combined-send.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*,!=3.6.*",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'z3c.jbot',
        'plone.api>=1.8.4',
        'plone.restapi',
        'plone.app.dexterity',
        'Products.EasyNewsletter>=5.0.7',
        'beautifulsoup4',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.easynewsletter_combined_send.locales.update:update_locale
    """,
)
