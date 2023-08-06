.. -*- coding: utf-8 -*-

.. _SetUpEnv:

Install a *CubicWeb* environment
================================

.. _`CubicWeb.org forge`: https://forge.extranet.logilab.fr/cubicweb/cubicweb

Official releases are available from the `CubicWeb.org forge`_ and from
`PyPI <http://pypi.python.org/pypi?%3Aaction=search&term=cubicweb&submit=search>`_. Since CubicWeb is developed using `Agile software development
<http://en.wikipedia.org/wiki/Agile_software_development>`_ techniques, releases
happen frequently. In a version numbered X.Y.Z, X changes after a few years when
the API breaks, Y changes after a few weeks when features are added and Z
changes after a few days when bugs are fixed.

There are several ways to install |cubicweb| depending on your needs:

- :ref:`Using Docker <DockerInstallation>`
- :ref:`In a virtualenv <VirtualenvInstallation>`
- :ref:`Using Pip <PipInstallation>`

If you are a power-user and need the very latest features, you can choose the following methods:

- :ref:`Downloading the source <SourceInstallation>`
- :ref:`Using mercurial <MercurialInstallation>`

Additional configuration can be found in the section :ref:`ConfigEnv` for better control
and advanced features of |cubicweb|.


.. _InstallDependencies:

Installing Dependencies
-----------------------

No matter your installation method, you will need to install the following Debian packages::

   apt install gettext graphviz

``gettext`` is used for translations (see :ref:`internationalization`), and ``graphviz`` to display relation schemas within the website.

Installing |cubicweb|
---------------------

.. _DockerInstallation:

Docker install
~~~~~~~~~~~~~~

Detailed instructions on how to deploy CubicWeb using docker can be found
on the `docker hub <https://hub.docker.com/r/logilab/cubicweb>`_.

Images are built using the source code available in the
`docker-cubicweb <https://forge.extranet.logilab.fr/cubicweb/docker-cubicweb/>`_ repository.

.. _VirtualenvInstallation:

`Virtualenv` install
~~~~~~~~~~~~~~~~~~~~

|cubicweb| can be safely installed, used and contained inside a
`virtualenv`_. To create and activate a `virtualenv`_, use the following commands::

   pip install --user virtualenv
   virtualenv venv
   source venv/bin/activate

Then you can use either :ref:`pip <PipInstallation>` or
:ref:`easy_install <EasyInstallInstallation>` to install |cubicweb|
inside an activated virtual environment.

.. _PipInstallation:

`pip` install
~~~~~~~~~~~~~

`pip <https://pip.pypa.io/>`_ is a python tool that helps downloading,
building, installing, and managing Python packages and their dependencies. It
is fully compatible with `virtualenv`_ and installs the packages from sources
published on the `The Python Package Index <https://pypi.org/>`_.

.. _`virtualenv`: https://virtualenv.pypa.io

A working compilation chain is needed to build modules which include C
extensions. If you really do not want to compile anything, installing `lxml <http://lxml.de/>`_,
and `libgecode <http://www.gecode.org/>`_ will help.

For Debian, these minimal dependencies can be obtained by doing::

  apt install gcc python3-pip python3-dev python3-lxml

or, if you prefer to get as much as possible from pip::

  apt install gcc python3-pip python3-dev libxslt1-dev libxml2-dev

For Windows, you can install pre-built packages (possible `source
<http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_). For a minimal setup, install:

- pip http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip
- setuptools http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools
- libxml-python http://www.lfd.uci.edu/~gohlke/pythonlibs/#libxml-python>
- lxml http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

Make sure to choose the correct architecture and version of Python.

Finally, install |cubicweb| and its dependencies by running::

  pip install cubicweb



.. _SourceInstallation:

Install from source
~~~~~~~~~~~~~~~~~~~

You can download the archive containing the sources from
`CubicWeb forge downloads section <https://forge.extranet.logilab.fr/cubicweb/cubicweb/-/archive/branch/default/cubicweb-branch-default.zip>`_.

Make sure you also have all the :ref:`dependencies installed <InstallSourceDependencies>`.

Once uncompressed, you can install the framework from inside the uncompressed
folder with::

  python3 setup.py install

Or you can run |cubicweb| directly from the source directory by
setting the :ref:`resource mode <ResourcesConfiguration>` to `user`. This will
ease the development with the framework.

.. _MercurialInstallation:

Install from version control system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To keep-up with on-going development, clone the :ref:`Mercurial
<MercurialPresentation>` repository::

  hg clone -u 'last(tag())' https://forge.extranet.logilab.fr/cubicweb/cubicweb # stable version
  hg clone https://forge.extranet.logilab.fr/cubicweb/cubicweb # development branch

Make sure you also have all the :ref:`InstallSourceDependencies`.

Installing `cubes`
------------------

Many other :ref:`cubes <AvailableCubes>` are available. Those cubes can help expanding the functionalities offered by |cubicweb|. A list is available at
`PyPI <http://pypi.python.org/pypi?%3Aaction=search&term=cubicweb&submit=search>`_
or at the `CubicWeb.org forge`_.

For example the `blog cube <https://forge.extranet.logilab.fr/cubicweb/cubes/blog>`_ can be installed using::

  pip install cubicweb-blog
