<!-- Local IspellDict: en -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2020-2022 Jens Lechtenbörger -->

# Changelog
Changelog information is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
where version numbers adhere to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2022-06-06
### Added
- Optional parameter attributes in FDSet.key()
### Fixed
- Previously, attributes of a relation schema were largely ignored,
  potentially leading to incorrect keys and synthesis results.
  Make sure in RelSchema.synthesize() that also attributes that do not
  occur in any FD are implied by the key (see doctest with nokeyschema).

## [1.2.1] - 2021-01-05
### Fixed
- Remove cyclic module import for doctest

## [1.2.0] - 2020-12-30
### Added
- Gitlab CI/CD
### Changed
- Use project_urls in setup.py

## [1.1.0] - 2020-12-28
### Added
- Parameter minimize in RelSchema.synthesize().
- Sample notebook with 3NF example by Codd, also at mybinder.org.
### Fixed
- Import in __init__.py.
- Project URL in docstring.
- Raw URL for coverage badge in setup.py.
- URL for REUSE badge in README.md.

## [1.0.1] - 2020-12-22
### Fixed
- Package URL and coverage badge in setup.py.

## [1.0.0] - 2020-12-22
No change in functionality.

## [1.0.0-rc.1] - 2020-12-22
Initial release.  Code from
[there](https://gitlab.com/oer/cs/programming/-/blob/master/functional_dependencies.py)
packaged for independent distribution.

<!-- Remember -->
<!-- - Change types: Added, Changed, Deprecated, Removed, Fixed, Security -->
<!-- - Versions: Major.Minor.Patch -->
<!--   - Major for incompatible changes -->
<!--   - Minor for backwards compatible changes -->
<!--   - Patch for backwards compatible bug fixes -->
<!-- - Might use Ma.Mi.P-alpha < Ma.Mi.P-alpha.1 < Ma.Mi.P-beta -->
