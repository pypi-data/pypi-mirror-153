#!/usr/bin/python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2020-2022 Jens Lechtenbörger

"""Configure package setup.

Based on:
- https://packaging.python.org/tutorials/packaging-projects/
- https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

import io
import re
import setuptools

COMMENT_RE = re.compile("^<!--.*-->\n$", re.U)


def ignore_comment(line):
    """Return line if it is no comment; otherwise, return empty string."""
    if COMMENT_RE.match(line):
        return ""
    return line


def filter_comments(filename):
    """Return contents of filename without comment lines."""
    with io.open(filename, "r", encoding="utf-8") as handle:
        result = ""
        for line in handle.readlines():
            result += ignore_comment(line)
        return result


def long_desc():
    """Return long description.

    Contents of README and CHANGELOG without comments.
    """
    return "{0}\n\n{1}".format(filter_comments("README.md"),
                               filter_comments("CHANGELOG.md"))


setuptools.setup(
    name="functional_dependencies",
    version="1.3.0",
    author="Jens Lechtenbörger",
    author_email="lechten@wi.uni-muenster.de",
    license="GPL-3.0-or-later AND CC0-1.0 AND CC-BY-4.0",
    description="Compute functional dependencies for database schema design"
    " and normalization: implication, closure, synthesis",
    long_description=long_desc(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/oer/cs/functional-dependencies",
    project_urls={
        "Documentation": "https://oer.gitlab.io/cs/functional-dependencies/",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved ::"
        " GNU General Public License v3 or later (GPLv3+)",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Topic :: Database",
        "Topic :: Education",
    ],
)
