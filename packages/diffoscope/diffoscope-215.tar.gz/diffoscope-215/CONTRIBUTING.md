# Contributing

The preferred way to report bugs about *diffoscope*, as well as suggest
fixes and requests for improvements is to submit reports to the issue
tracker at:

    https://salsa.debian.org/reproducible-builds/diffoscope/issues

You can also submit patches via *Merge Request* on Salsa, Debian's
Gitlab instance. Start by forking the
[`diffoscope` Git repository](https://salsa.debian.org/reproducible-builds/diffoscope)
(see [documentation](https://salsa.debian.org/help/gitlab-basics/fork-project.md)),
make your changes and commit them as you normally would. You can then push your
changes and submit a *merge request* via Salsa. See:
[Gitlab documentation](https://salsa.debian.org/help/gitlab-basics/add-merge-request.md)
about *Merge Requests*.

You can also submit bugs about Debian specific issues to the Debian bug
tracker.

## Testing

diffoscope's test suite relies on [pytest](https://docs.pytest.org/);
to run all tests use `pytest[-3]`, appending `-n 4` or similar to enable
running tests concurrently. For faster interactive development here's
an example of how to run a (much) smaller subset of tests:

    $ pytest -v --exitfirst -k lib tests/comparators/test_elf.pyc [-pdb]

More options are available at `[pytest -h]`.

## Git setup

diffoscope's codebase adheres to the output
[Black](https://black.readthedocs.io/) source code reformatter. Since this was
not always the case, the default output of `git-blame(1)` is not useful due to
large changes made when it was adopted.

As an optional step, you can ignore these commits using:

    $ git config blame.ignoreRevsFile .git-blame-ignore-revs

## Common development topics

### Adding a comparator

Diffoscope doesn't support a specific file type? Please contribute to
the project! Each file type is handled by a comparator, and writing a
new one is usually very easy. Here are the steps to add a new
comparator:

* Add the new comparator in `diffoscope/comparators`.

* Declare the comparator File class in `ComparatorManager` in
  `diffoscope/comparators/__init__.py`

* Add a test under `tests/comparators/`

* If required:

  - Update the `Build-Depends` list in `debian/control` and regenerate
    `debian/tests/control` by following the instructions in that file.

  - Update the `EXTERNAL_TOOLS` list in
   `diffoscope/external_tools.py`

### Adding a new option

Please try and refrain from adding new command-line options. A brief rationale
may be found here:

  https://salsa.debian.org/reproducible-builds/diffoscope/-/issues/18#note_183040


## Release process

### Uploading to Debian

When uploading diffoscope to the Debian archive, please take extra care
to make sure the uploaded source package is correct, that is it includes
the files tests/data/test(1o) which in some cases are removed by
dpkg-dev when building the package.

See [#834315](https://bugs.debian.org/834315) for an example FTBFS bug
caused by this. (See [#735377](https://bugs.debian.org/735377#44)
and followups to learn how this happened and how to prevent it)

### Signed tarballs

Please also release a signed tarball:

    $ VERSION=FIXME
    $ git archive --format=tar --prefix=diffoscope-${VERSION}/ ${VERSION} | bzip2 -9 > diffoscope-${VERSION}.tar.bz2
    $ gpg --detach-sig --armor --output=diffoscope-${VERSION}.tar.bz2.asc < diffoscope-${VERSION}.tar.bz2

And commit them to our LFS repository at:

    https://salsa.debian.org/reproducible-builds/reproducible-lfs

### PyPI

You can update the version on PyPI using:

    $ python3 setup.py sdist upload --sign

### Docker image

Update the Docker image using:

    $ docker build --force-rm --no-cache --pull -t registry.salsa.debian.org/reproducible-builds/diffoscope .
    $ docker push registry.salsa.debian.org/reproducible-builds/diffoscope

### Publicity

To announce the package on the `diffoscope.org` homepage, use the `update`
script in that repository.

Once live entry appears, consider tweeting the release using the release from
the `@reprobuilds` Twitter account.
