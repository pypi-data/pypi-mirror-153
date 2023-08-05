# -*- coding: utf-8 -*-
"""
This module contains the tool of redturtle.bandi
"""
import os
from setuptools import setup, find_packages

version = "1.4.0"

setup(
    name="redturtle.bandi",
    version=version,
    description="A product for announcements management based on rer.bandi",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Addon",
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python",
    ],
    keywords="redturtle bandi announcements",
    author="RedTurtle Technology",
    author_email="sviluppoplone@redturtle.it",
    url="https://github.com/PloneGov-IT/redturtle.bandi",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/redturtle.bandi",
        "Source": "https://github.com/RedTurtle/redturtle.bandi",
        "Tracker": "https://github.com/RedTurtle/redturtle.bandi/issues",
        # 'Documentation': 'https://redturtle.bandi.readthedocs.io/en/latest/',
    },
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["redturtle"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "lxml",
        "plone.restapi",
        "collective.tiles.collection",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ]
    },
    test_suite="redturtle.bandi.tests.test_docs.test_suite",
    entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
        [console_scripts]
        update_locale = redturtle.bandi.locales.update:update_locale
      """,
)
