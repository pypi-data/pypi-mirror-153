# README

This package eases the creation of new releases for
a python package versioned with mercurial.
It assumes mercurial as vcs and semantic versioning.
Also, the version has to be managed by a variable
`numversion` inside a file `__pkginfo__.py`.

It takes care to :

- update the version in the file `__pkginfo__.py` (required)
- update the changelog
- create a commit with only this changes
- tag the commit.

The new version, `patch`, `minor` or `major`, depends on the option `-r`/`--release`
passed as parameter.
The `auto` option reads the commit message and determines the release type
according to conventional commit.

The primary use case is to have `release-new` inside a tox rules for cubicweb
cubes.

You can use `release-new --preview-changelog` or `release-new -c` to preview the
changelog that will be generated.

It does not:

- release to pypi

The release should be done by the CI, see the `.gitlab-ci.yml`.

It can be installed with `pip install release-new`.
