.. _saytex-implementation:


Development Notes
=================

This section should be of little interest to everyone who is not
a maintainer of SayTeX.

Deploying
---------

Update the version number in ``setup.py``.

Remember to update the documentation, as per the instructions below.

Commit with the message ``version x.x.x``.

Build the package: ``python3 setup.py sdist bdist_wheel``.

Upload it to PyPI: ``twine upload --skip-existing dist/*``.

Then, make a new release on GitHub, where the binaries from ``dist/`` are uploaded.

Documentation
-------------

Install sphinx: ``pip3 install sphinx``

Install theme: ``pip3 install sphinx_rtd_theme``

To update the docs, first update the local installation of saytex by running ``pip3 install -e .`` from the project directory. Then go to the ``docs`` directory and run ``sphinx-apidoc -o . ../saytex -f``, then ``rm -rf _build`` followed by ``make html``.