Developer Guide
===============

Thank you for your interest in developing SatNOGS!
There are always bugs to file; bugs to fix in code; improvements to be made to the documentation; and more.

The below instructions are for software developers who want to work on `satnogs-db code <http://gitlab.com/librespacefoundation/satnogs/satnogs-db>`_.


Workflow
--------

When you want to start developing for SatNOGS, you should :doc:`follow the installation instructions <installation>`, then...

#. Read CONTRIBUTING.md file carefully.

#. Fork the `upstream repository <https://gitlab.com/librespacefoundation/satnogs/satnogs-db/forks/new>`_ in GitLab.

#. Code!

#. Test the changes and fix any errors by running `tox <https://tox.readthedocs.io/en/latest/>`_.

#. Commit changes to the code!

#. When you're done, push your changes to your fork.

#. Issue a merge request on Gitlab.

#. Wait to hear from one of the core developers.

If you're asked to change your commit message or code, you can amend or rebase and then force push.

If you need more Git expertise, a good resource is the `Git book <http://git-scm.com/book>`_.


Templates
---------

satnogs-db uses `Django's template engine <https://docs.djangoproject.com/en/dev/topics/templates/>`_ templates.


Frontend development
--------------------

Third-party static assets are not included in this repository.
The frontend dependencies are managed with ``npm``.
Development tasks like the copying of assets, code linting and tests are managed with ``gulp``.

To download third-party static assets:

#. Install dependencies with ``npm``::

     $ npm install

#. Test and copy the newly downlodaded static assets::

     $ ./node_modules/.bin/gulp

To add new or remove existing third-party static assets:

#. Install a new dependency::

     $ npm install <package>

#. Uninstall an existing dependency::

     $ npm uninstall <package>

#. Copy the newly downlodaded static assets::

     $ ./node_modules/.bin/gulp assets


Documentation
-------------

The documentation can be generated locally with sphinx::

     $ cd docs
     $ virtualenv -p python3 env
     $ source env/bin/activate
     $ pip install sphinx_rtd_theme
     $ make html SPHINXOPTS="-W"


Coding Style
------------

Follow the `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_ and `PEP257 <http://www.python.org/dev/peps/pep-0257/#multi-line-docstrings>`_ Style Guides.


What to work on
---------------
You can check `open issues <https://gitlab.com/librespacefoundation/satnogs/satnogs-db/issues>`_.
We regurarly open issues for tracking new features. You pick one and start coding.
