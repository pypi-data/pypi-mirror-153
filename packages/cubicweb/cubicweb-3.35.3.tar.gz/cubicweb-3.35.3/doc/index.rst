=====================================================
|cubicweb| - The Semantic Web is a construction game!
=====================================================


|cubicweb| is a semantic web application framework, licensed under the LGPL,
that empowers developers to efficiently build web applications by reusing
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

Built since 2000 from an R&D effort still continued, supporting 100,000s of
daily visits at some production sites, |cubicweb| is a proven end to end solution
for semantic web application development that promotes quality, reusability and
efficiency.

.. _index-first-steps:

First steps
===========

The impatient developer will move right away to :ref:`SetUpEnv` then to :ref:`ConfigEnv`.

* **From scratch:**
  :doc:`Introduction to CubicWeb <book/intro/history/>` |
  :doc:`Installation <book/admin/setup/>`

* **Tutorial:**
  :doc:`Part 1: Get a blog running in five minutes! <tutorials/base/blog-in-five-minutes/>` |
  :doc:`Part 2: Discovering the web interface <tutorials/base/discovering-the-ui/>` |
  :doc:`Part 3: Customizing your application <tutorials/base/customizing-the-application/>` |
  :doc:`Part 4: What’s next? <tutorials/base/conclusion/>`


Cubicweb core principle
=======================

* **Why cubicweb ?**
  :doc:`Concepts <book/intro/concepts>`

* **Cubes:**
  :doc:`What is a cube <book/devrepo/cubes/what-is-a-cube/>` |
  :doc:`How to create a cube <book/devrepo/cubes/cc-newcube/>` |
  :doc:`Cubes general structure <book/devrepo/cubes/layout/>`

* **The Registeries:**
  :ref:`What are registries <VRegistryIntro>` |
  :doc:`How to use registries <book/devrepo/vreg>` |
  :doc:`All available registries <>`

* **A Data-centric framework:**
  :ref:`Data schema with YAMS <datamodel_definition>` |
  :doc:`RQL <book/annexes/rql/index>`



Routing
=======

Cubicweb offers two different ways of rooting : one internal to CubicWeb and a new one with pyramid.

* **Principle:**
  :doc:`cubicweb and pyramid <>` |
  :doc:`the CW request object <>` |
  :doc:`the pyramid request object <book/pyramid/index>` |
  :doc:`encapsulation of the CW request in the pyramid request <>`
  :doc:`bw_compat and the options to use, fallback when CW doesn't find anything <>` |

* **CubicWeb routing:**
  :doc:`url publishers <book/devweb/publisher>` |
  :doc:`url rewriters <book/devweb/views/urlpublish>`

* **Pyramid routing:**
  :doc:`general principles <>` |
  :doc:`predicates <>` |
  :doc:`tweens <>` |
  :doc:`content negociation <>`


Front development
=================

* **With Javascript / Typescript (using React):**
  :doc:`general principle <>`
  :doc:`how to install and integrate js tooling into CW <>`
  :doc:`cwelements <>` |
  :doc:`rql browser <>`

* **With Pyramid:**
  :doc:`general integration with CubicWeb <>` |
  `the renderers
  <https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/renderers.html>`_ |
  `Jinja2 templates <https://jinja.palletsprojects.com/>`_ |
  :doc:`example of usages with CW <>`

* **With CubicWeb Views:**
  :doc:`Introduction <book/devweb/views/index>` |
  :ref:`How to select a views with registers <object_selection>` |
  :doc:`Facets <>` |
  :doc:`How to use javascript inside CW views <>` |
  :doc:`Customize CSS <>`

* **RDF:**
  :doc:`the RDF adaptator <>` |
  :doc:`RDFLib integration into CW <>`

Data model and management
=========================

* **Data in CubicWeb:**
  :doc:`The data modelization <book/devrepo/datamodel/index>` |
  :doc:`Data as objects <book/devrepo/entityclasses/index>`

* **Importation:**
  :doc:`standard import <book/devrepo/dataimport>` |
  :doc:`massive store <>`


Security
========

* **Security:**
  :ref:`The permission model <securitymodel>` |
  :doc:`Permissions management with Pyramid <>` |
  :ref:`CSRF protection <csrf_protection>`

Migrate your schema
===================

Each time the schema is updated, two action are needed : update the underlying tables and update the corresponding data.

* **Migrations:**
  :ref:`Execute and write script migration <migration>` |
  :doc:`Debug script migration <>`


Cubicweb configuration files
============================

* **Base configuration:**
  :ref:`The all-in-one.conf <WebServerConfig>` |
  :doc:`The Pyramid configuration <book/pyramid/settings/>`

* **Advanced configuration:**
  :doc:`The database connection pooler <book/devrepo/connections_pooler/>`



Common Web application tools
=============================

* **Test**
  :doc:`cubicweb <book/devrepo/testing>`
  :doc:`Test pyramid <>`

* **Caching**
  :doc:`Cache management <book/devweb/httpcaching>`

* **Internationalisation**
  :doc:`Localize your application <book/devweb/internationalization>`

* **Full text indexation**
  :doc:`The searchbar <book/devweb/searchbar>`




Development
===========

* **Command line tool:**
  :doc:`cubicweb-ctl <book/admin/cubicweb-ctl/>`

* **Performences:**
  :doc:`Profiling your application <book/devrepo/profiling/>`

* **Debugging:**
  :doc:`Command line options for debugging <>` |
  :doc:`Debugging configuration directly in the code <>` |
  :doc:`Pyramid debug toolbar <>` |
  :doc:`Debug channels <>`

* **Good pratices:**
  :doc:`tox<>` |
  :doc:`check-manifest<>` |
  :doc:`mypy<>` |
  :doc:`flake8 et black<>`

* **CI:**
  :doc:`Gitlab-ci integration <>` |



System administration
=====================

* **Deployment:**
  :ref:`Raw python deployment <deploy_python>` |
  :ref:`Working with Docker <deploy_docker>` |
  :ref:`Working with Kubernetes <deploy_kubernetes>` |

* **Administration:**
  :ref:`Cubicweb-ctl tool <cubicweb-ctl>` |
  :doc:`Sources configuration <>` |
  :ref:`Backup <Backups>`



Reference API
=============

.. toctree::
    :maxdepth: 1
    :glob:

    api/*


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
* :doc:`CHANGELOG <changes/changelog>`

.. _forge: https://forge.extranet.logilab.fr/cubicweb/cubicweb
.. _Python: http://www.python.org/
.. _`matrix room`: https://matrix.to/#/#cubicweb:matrix.logilab.org
.. _`mailing-list`: http://lists.cubicweb.org/mailman/listinfo/cubicweb
.. _blog: http://www.cubicweb.org/blog/1238
