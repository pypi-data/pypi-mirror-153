.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: 📕 Guides

    book/intro/index
    tutorials/index

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: ⚙ Setup and Usage

    book/admin/index
    book/devrepo/index
    book/devweb/index
    book/pyramid/index
    book/additionnal_services/index

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: ➕ More

    book/annexes/index

    changes/index

    api/index


*****************************************************
|cubicweb| - The Semantic Web is a construction game!
*****************************************************


|cubicweb| is a semantic web application framework, licensed under the LGPL,
empowering developers to efficiently build web applications by reusing
components (called `cubes`) and following the well known object-oriented design
principles.

Main Features
=============

* an engine driven by the explicit :ref:`data model
  <datamodel_definition>` of the application,

* a query language named :ref:`RQL <RQL>` similar to W3C's SPARQL,

* a :ref:`selection+view <TutosBaseCustomizingTheApplicationCustomViews>`
  mechanism for semi-automatic XHTML/XML/JSON/text generation,

* a library of reusable :ref:`components <Cube>` (data model and views) that
  fulfill common needs,

* the power and flexibility of the Python_ programming language,
* the reliability of SQL databases, LDAP directories and Mercurial
  for storage backends.

Created in early 2000s from an R&D effort and still maintained, supporting 100,000s of
daily visits at some production sites, |cubicweb| is a proven end to end solution
for semantic web application development promoting quality, reusability and
efficiency.

First steps
===========

* **From scratch:**

  - :ref:`SetUpEnv`

  - :ref:`ConfigEnv`

  - :ref:`DeployEnv`

* **Guides:**

  - :ref:`CubicWebIntro`

  - Basics: :ref:`TutosBase`

  - Advanced: :ref:`TutosPhotoWebSite`


Cubicweb core principle
=======================

* **Why cubicweb?**

  - :ref:`Concepts`

* **Cubes:**

  - :ref:`WhatIsACube`

  - :ref:`CreatingACube`

  - :ref:`cubelayout`

* **Registries:**

  - :ref:`What are registries <VRegistryIntro>`

  - :ref:`How to use registries <Registries>`

* **Data-centric framework:**

  - :ref:`Data schema with YAMS <datamodel_definition>`

  - :ref:`RQLChapter`



Routing
=======

|cubicweb| offers two different ways of routing : one internal to CubicWeb and a one with the `pyramid framework <https://trypyramid.com/>`_.

* **Principle:**

  - :doc:`cubicweb and pyramid <>`

  - :doc:`the CW request object <>`

  - :doc:`the pyramid request object <book/pyramid/index>`

  - :doc:`encapsulation of the CW request in the pyramid request <>`

  - :doc:`bw_compat and the options to use, fallback when CW doesn't find anything <>`

* **CubicWeb routing:**

  - :doc:`url publishers <book/devweb/publisher>`

  - :doc:`url rewriters <book/devweb/views/urlpublish>`

* **Pyramid routing:**

  - :doc:`general principles <>`

  - :doc:`predicates <>`

  - :doc:`tweens <>`

  - :doc:`content negociation <>`


Front development
=================

* **With Javascript / Typescript (using React):**

  - :doc:`general principle <>`

  - :doc:`how to install and integrate js tooling into CW <>`

  - :doc:`cwelements <>`

  - :doc:`rql browser <>`

* **With Pyramid:**

  - :doc:`general integration with CubicWeb <>`

  - `The renderers <https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/renderers.html>`_

  - `Jinja2 templates <https://jinja.palletsprojects.com/>`_

  - :doc:`example of usages with CW <>`

* **With CubicWeb Views:**

  - :ref:`Introduction <ViewSystem>`

  - :ref:`Select a view with registers <object_selection>`

  - :doc:`Facets <>`

  - :doc:`How to use javascript inside CW views <>`

  - :doc:`Customize CSS <>`

* **RDF:**

  - :doc:`the RDF adaptator <>`

  - :doc:`RDFLib integration into CW <>`

Data model and management
=========================

* **Data in CubicWeb:**

  - :ref:`DataModel`

  - :ref:`DataAsObjects`

* **Data Import:**

  - :ref:`Standard Import <dataimport>`

  - :doc:`massive store <>`


Security
========

* **Security:**

  - :ref:`securitymodel`

  - :doc:`Permissions management with Pyramid <>`

  - :ref:`csrf_protection`

Migrate your schema
===================

Each time the schema is updated, two action are needed : update the underlying tables and update the corresponding data.

* **Migrations:**

  - :ref:`Execute and write migration script <migration>`

  - :doc:`Debug script migration <>`


Cubicweb configuration files
============================

* **Base configuration:**

  - :ref:`The all-in-one.conf <WebServerConfig>`

  - :ref:`The Pyramid configuration <cubicweb_settings>`

* **Advanced configuration:**

  - :ref:`The database connection pooler <connection_poller>`



Common Web application tools
=============================

* **Test**

  - :ref:`CubicWeb <Tests>`

  - :doc:`Pyramid <>`

* **Caching**

  - :ref:`HttpCaching`

* **Internationalization**

  - :ref:`Localize your application <internationalization>`

* **Full text indexation**

  - :ref:`searchbar`




Development
===========

* **Command line tool:**

  - :ref:`cubicweb-ctl`

* **Performances:**

  - :ref:`Profiling your application <PROFILING>`

* **Debugging:**

  - :doc:`Command line options for debugging <>`

  - :doc:`Debugging configuration directly in the code <>`

  - :doc:`Pyramid debug toolbar <>`

  - :doc:`Debug channels <>`

* **Good practices:**

  - :doc:`tox<>`

  - :doc:`check-manifest<>`

  - :doc:`mypy<>`

  - :doc:`flake8 et black<>`

* **CI:**

  - :doc:`Gitlab-ci integration <>`



System administration
=====================

* **Deployment:**

  - :ref:`Raw python deployment <deploy_python>`

  - :ref:`Working with Docker <deploy_docker>`

  - :ref:`Working with Kubernetes <deploy_kubernetes>`

* **Administration:**

  - :ref:`Cubicweb-ctl tool <cubicweb-ctl>`

  - :doc:`Sources configuration <>`

  - :ref:`Backup <Backups>`


CubicWeb's ecosystem
====================

CubicWeb is based on different libraries, in which you may be interested :

* `YAMS <https://yams.readthedocs.io/>`_
* `RQL <https://rql.readthedocs.io/>`_
* `logilab-common <https://logilab-common.readthedocs.io/>`_
* `logilab-database <https://logilab-database.readthedocs.io/>`_
* `logilab-constraints <https://forge.extranet.logilab.fr/open-source/logilab-constraint>`_
* `logilab-mtconverter <https://forge.extranet.logilab.fr/open-source/logilab-mtconverter>`_

How to contribute
=================

* Chat on the `matrix room`_ `#cubicweb:matrix.logilab.org`
* Visio Weekly meeting every **Tuesday** afternoon (UTC+1). The link is shared in the `matrix room`_
* Discuss on the `mailing-list`_
* Discover on the `blog`_
* Contribute on the forge_
* Find published python modules on `pypi <https://pypi.org/search/?q=cubicweb>`_
* Find published npm modules on `npm <https://www.npmjs.com/search?q=keywords:cubicweb>`_
* :ref:`Changelog`

.. _forge: https://forge.extranet.logilab.fr/cubicweb/cubicweb
.. _Python: http://www.python.org/
.. _`matrix room`: https://matrix.to/#/#cubicweb:matrix.logilab.org
.. _`mailing-list`: http://lists.cubicweb.org/mailman/listinfo/cubicweb
.. _blog: http://www.cubicweb.org/blog/1238
