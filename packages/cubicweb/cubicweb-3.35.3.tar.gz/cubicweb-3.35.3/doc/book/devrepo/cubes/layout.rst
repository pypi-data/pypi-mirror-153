
.. _foundationsCube:

.. _cubelayout:

Standard structure for a cube
-----------------------------

A cube named "mycube" is a Python package "cubicweb-mycube" structured as
follows:

::

  cubicweb-mycube/
  ├── cubicweb_mycube
  │   ├── data
  │   ├── entities.py
  │   ├── hooks.py
  │   ├── i18n
  │   │   ├── de.po
  │   │   ├── en.po
  │   │   ├── es.po
  │   │   └── fr.po
  │   ├── __init__.py
  │   ├── migration
  │   │   └── postcreate.py
  │   ├── __pkginfo__.py
  │   ├── schema.py
  │   └── views.py
  ├── cubicweb-mycube.spec
  ├── MANIFEST.in
  ├── README
  ├── setup.py
  ├── test
  │   ├── data
  │   │   └── bootstrap_cubes
  │   ├── __pycache__
  │   └── test_mycube.py
  └── tox.ini



We can use subpackages instead of Python modules for ``views.py``, ``entities.py``,
``schema.py`` or ``hooks.py``. For example, we could have:

::

  cubicweb-mycube/
  |
  |-- cubicweb_mycube/
  |   |
      |-- entities.py
  .   |-- hooks.py
  .   `-- views/
  .       |-- __init__.py
          |-- forms.py
          |-- primary.py
          `-- widgets.py


where :

* ``schema`` contains the schema definition (server side only)
* ``entities`` contains the entity definitions (server side and web interface)
* ``hooks`` contains hooks and/or views notifications (server side only)
* ``views`` contains the web interface components (web interface only)
* ``test`` contains tests related to the cube
* ``i18n`` contains message catalogs for supported languages (server side and
  web interface)
* ``data`` contains data files for static content (images, css,
  javascript code)...(web interface only)
* ``migration`` contains initialization files for new instances (``postcreate.py``)
  and a file containing dependencies of the component depending on the version
  (``depends.map``)
* file ``__pkginfo__.py`` provides component meta-data, especially the distribution
  and the current version (server side and web interface) or sub-cubes used by
  the cube.


At least you should have the file ``__pkginfo__.py``.


The :file:`site_cubicweb.py` files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It contains the definition of cube options that are customisable through
:ref:`all-in-one.conf <WebServerConfig>`. This should define the attribute
`options` :

::

  # -*- coding: utf-8 -*-
  # cubicweb-mycube/cubicweb_mycube/site_cubicweb.py


  options = (
      ('example-option-name-1',
       {'type': 'string',
        'default': 'Default value',
        'help': 'Some text explaining the usage of this option.',
        'group': 'cubicweb_mycube',
        'level': 2,
        }),
  )

The options format are defined in `logilab common <https://logilab-common.readthedocs.io/en/latest/logilab.common.html#module-logilab.common.configuration>`_.
The ``options`` attribute should be a list of ``('option-name', option-value)``.
The value should be ``dict`` with the following entries:

* ``type``: available types are : string, int, float, file, font, color, regexp,
  csv, yn (yes/no), bool, named, password, date, time, bytes, choice and multiple_choice.
* ``default``: the default value of the option.
* ``help``: the message to print as a help message.
* ``group``: the section where the option should be  stored in ``the all-in-one.conf``.
* ``level``: the verbosity at which the help should be displayed.

This is useful to add token configuration or endpoint, see for example
`sentry <https://forge.extranet.logilab.fr/cubicweb/cubes/sentry>`_ or
`seo <https://forge.extranet.logilab.fr/cubicweb/cubes/seo>`_.

When modifying this, don't forget to add a :ref:`migration script <migrationOption>`.

The :file:`__pkginfo__.py` file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It contains metadata describing your cube, mostly useful for packaging.

Two important attributes of this module are __depends__ and __recommends__
dictionaries that indicates what should be installed (and each version if
necessary) for the cube to work.

Dependency on other cubes are expected to be of the form 'cubicweb-<cubename>'.

When an instance is created, dependencies are automatically installed, while
recommends are not.

Recommends may be seen as a kind of 'weak dependency'. Eg, the most important
effect of recommending a cube is that, if cube A recommends cube B, the cube B
will be loaded before the cube A (same thing happend when A depends on B).

Having this behaviour is sometime desired: on schema creation, you may rely on
something defined in the other's schema; on database creation, on something
created by the other's postcreate, and so on.

The :file:`setup.py` file
-------------------------

This is standard setuptools based setup module which reads most of its data
from :file:`__pkginfo__.py`. In the ``setup`` function call, it should also
include an entry point definition under the ``cubicweb.cubes`` group so that
CubicWeb can discover cubes (in particular their custom ``cubicweb-ctl``
commands):

::

    setup(
      # ...
      entry_points={
          'cubicweb.cubes': [
              'mycube=cubicweb_mycube',
          ],
      },
      # ...
    )

The :file:`__init__.py` file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first purpose of this file is to define the cube as a python module.

Furthermore, this file is, by default, the starting point of pyramid
mechanism of inclusion for routes, views, predicates, etc.
During initialization, Pyramid will check for the `includeme` function
in this file. See `the documentation of pyramid
<https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/extconfig.html#adding-methods-to-the-configurator-via-add-directive>`_.

:file:`migration/precreate.py` and :file:`migration/postcreate.py`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The precreate script is executed at instance creation time or when
the cube is added to an existing instance, before the schema is serialized.
This is typically to create groups referenced by the cube'schema.

The postcreate script, executed at instance creation time or when
the cube is added to an existing instance.
You could setup site properties or a workflow here for example.

More information : :doc:`see migration description <book/devrepo/migration.rst>`_

External resources such as image, javascript and css files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. XXX naming convention external_resources file


Out-of the box testing
~~~~~~~~~~~~~~~~~~~~~~

.. XXX MANIFEST.in, __pkginfo__.include_dirs


Packaging and distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. XXX MANIFEST.in, __pkginfo__.include_dirs
