<!--- Local IspellDict: en -->
<!--- SPDX-FileCopyrightText: 2020 Jens Lechtenbörger -->
<!--- SPDX-License-Identifier: CC0-1.0 -->

[![](https://img.shields.io/pypi/v/functional-dependencies.svg)](https://pypi.org/project/functional-dependencies/)
[![](https://gitlab.com/oer/cs/functional-dependencies/-/raw/master/coverage.svg)](https://pypi.org/project/coverage/)
[![REUSE status](https://api.reuse.software/badge/gitlab.com/oer/cs/functional-dependencies)](https://api.reuse.software/info/gitlab.com/oer/cs/functional-dependencies)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/oer%2Fcs%2Ffunctional-dependencies/HEAD?filepath=notebooks%2FCodd-3NF-ex.ipynb)

# Overview
This package provides an
[Open Educational Resource](https://en.wikipedia.org/wiki/Open_educational_resources)
(OER) to refresh prior knowledge about functional dependencies (FDs)
and normalization of relational database schemata.  Towards that goal,
the package implements algorithms for the manipulation of functional
dependencies; the package’s doc string explains the used vocabulary
and contains examples.

Selected algorithms:
- FD.rminimize(): Return a minimal cover of r-minimal FDs
- FDSet.closure(): Return closure of attributes under given FDs
- FDSet.lminimize(): Return minimum subset of lhs that determines rhs
- FDSet.key(): Return a key
- FDSet.basis(): Return non-redundant r- and l-minimal basis/cover
- RelSchema.synthesize(): Normalize via synthesis into set of 3NF schemata

# Installation and usage

This is [Python](https://www.python.org/) software.

A 3NF synthesis example is available as
[notebook on mybinder.org](https://mybinder.org/v2/gl/oer%2Fcs%2Ffunctional-dependencies/HEAD?filepath=notebooks%2FCodd-3NF-ex.ipynb);
you can use that notebook in your web browser (without the need to
install further software).

To normalize your own schemata, you may prefer to use the software
locally.  You can either clone the source repository
(`git clone https://gitlab.com/oer/cs/functional-dependencies.git`)
or install the [PyPI package](https://pypi.org/project/functional-dependencies/)
(`pip install functional-dependencies`).

The docstring for module `functional_dependencies` provides an
introduction and several examples.  See
[here for generated documentation](https://oer.gitlab.io/cs/functional-dependencies/functional_dependencies.html).

# Comments, feedback, improvements
Your feedback is highly appreciated.  Feel free to open issues or
merge requests in the
[source repository](https://gitlab.com/oer/cs/functional-dependencies).
For merge requests, make sure that pre-commit hooks are installed and
run successfully as indicated next.

# Side goal
Besides, the package may serve as sample Python code that respects
usual coding conventions, which are checked with
[pre-commit hooks](https://pre-commit.com).
The configuration file [.pre-commit-config.yaml](https://gitlab.com/oer/cs/functional-dependencies/-/blob/master/.pre-commit-config.yaml)
specifies test tools used here.

# Origin of code
The code here is based on
[that file](https://gitlab.com/oer/cs/programming/-/blob/master/functional_dependencies.py),
which will not be maintained any longer.
