#!/usr/bin/env python
# coding: utf-8

from setuptools import find_packages, setup

from __pkginfo__ import numversion

distname = "release-new"
version = ".".join(str(num) for num in numversion)
license = "LGPL"
description = ""
author = "Logilab"
author_email = "contact@logilab.fr"
requires = {
    "redbaron": ">=0.9.2,<0.10",
    "jinja2": None,
    "mercurial": ">=5.4.2,<5.5.0",
}

install_requires = ["{0} {1}".format(d, v or "").strip() for d, v in requires.items()]

setup(
    name=distname,
    version=version,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    url="https://forge.extranet.logilab.fr/open-source/release-new",
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    entry_points={"console_scripts": ["release-new = release_new.main:main"]},
)
