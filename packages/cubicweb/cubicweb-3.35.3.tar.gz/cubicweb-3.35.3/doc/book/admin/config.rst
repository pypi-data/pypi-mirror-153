.. -*- coding: utf-8 -*-

.. _ConfigEnv:

Set-up of a *CubicWeb* environment
==================================

You can `configure the database`_ system of your choice:

  - `PostgreSQL configuration`_
  - `SQLite configuration`_

For advanced features, have a look to:

  - `Cubicweb resources configuration`_

.. _`configure the database`: DatabaseInstallation_
.. _`PostgreSQL configuration`: PostgresqlConfiguration_
.. _`SQLite configuration`: SQLiteConfiguration_
.. _`Cubicweb resources configuration`: RessourcesConfiguration_



.. _RessourcesConfiguration:

Cubicweb resources configuration
--------------------------------

.. automodule:: cubicweb.cwconfig


.. _DatabaseInstallation:

Databases configuration
-----------------------

Each instance can be configured with its own database connection information,
that will be stored in the instance's :file:`sources` file. The database to use
will be chosen when creating the instance. CubicWeb is known to run with
Postgresql (recommended) and SQLite.

Other possible sources of data include CubicWeb, LDAP and Mercurial,
but at least one relational database is required for CubicWeb to work. You do
not need to install a backend that you do not intend to use for one of your
instances. SQLite is not fit for production use, but it works well for testing
and ships with Python, which saves installation time when you want to get
started quickly.

.. _PostgresqlConfiguration:

PostgreSQL
~~~~~~~~~~

Many Linux distributions ship with the appropriate PostgreSQL packages.
Basically, you need to install the following packages:

* `postgresql` and `postgresql-client`, which will pull the respective
  versioned packages (e.g. `postgresql-9.1` and `postgresql-client-9.1`) and,
  optionally,
* a `postgresql-plpython-X.Y` package with a version corresponding to that of
  the aforementioned packages (e.g. `postgresql-plpython-9.1`).
  (Not needed now by default)

If you run postgres on another host than the |cubicweb| repository, you should
install the `postgresql-client` package on the |cubicweb| host, and others on the
database host.

For extra details concerning installation, please refer to the `PostgreSQL
project online documentation`_.

.. _`PostgreSQL project online documentation`: http://www.postgresql.org/docs


Database cluster
++++++++++++++++

If you already have an existing cluster and PostgreSQL server running, you do
not need to execute the initilization step of your PostgreSQL database unless
you want a specific cluster for |cubicweb| databases or if your existing
cluster doesn't use the UTF8 encoding (see note below).

To initialize a PostgreSQL cluster, use the command ``initdb``::

    $ initdb -E UTF8 -D /path/to/pgsql

Note: ``initdb`` might not be in the PATH, so you may have to use its
absolute path instead (usually something like
``/usr/lib/postgresql/9.4/bin/initdb``).

Notice the encoding specification. This is necessary since |cubicweb| usually
want UTF8 encoded database. If you use a cluster with the wrong encoding, you'll
get error like::

  new encoding (UTF8) is incompatible with the encoding of the template database (SQL_ASCII)
  HINT:  Use the same encoding as in the template database, or use template0 as template.

Once initialized, start the database server PostgreSQL with the command::

  $ postgres -D /path/to/psql

If you cannot execute this command due to permission issues, please make sure
that your username has write access on the database.  ::

  $ chown username /path/to/pgsql


Database authentication
+++++++++++++++++++++++

The database authentication is configured in `pg_hba.conf`. It can be either set
to `ident sameuser` or `md5`.  If set to `md5`, make sure to use an existing
user of your database.  If set to `ident sameuser`, make sure that your client's
operating system user name has a matching user in the database. If not, please
do as follow to create a user::

  $ su
  $ su - postgres
  $ createuser -s -P <dbuser>

The option `-P` (for password prompt), will encrypt the password with the
method set in the configuration file :file:`pg_hba.conf`.  If you do not use this
option `-P`, then the default value will be null and you will need to set it
with::

  $ su postgres -c "echo ALTER USER <dbuser> WITH PASSWORD '<dbpassword>' | psql"

The above login/password will be requested when you will create an instance with
`cubicweb-ctl create` to initialize the database of your instance.


Database creation
+++++++++++++++++

If you create the database by hand (instead of using the `cubicweb-ctl
db-create` tool), you may want to make sure that the local settings are
properly set. For example, if you need to handle french accents
properly for indexing and sorting, you may need to create the database
with something like::

  $ createdb --encoding=UTF-8 --locale=fr_FR.UTF-8 -t template0 -O <owner> <dbname>

Notice that the `cubicweb-ctl db-create` does database initialization that
may requires a postgres superuser. That's why a login/password is explicitly asked
at this step, so you can use there a superuser without using this user when running
the instance. Things that require special privileges at this step:

* database creation, require the 'create database' permission

Where `pgadmin` is a postgres superuser.

.. _SQLiteConfiguration:

SQLite
~~~~~~

SQLite has the great advantage of requiring almost no configuration. Simply
use 'sqlite' as db-driver, and set path to the dabase as db-name. Don't specify
anything for db-user and db-password, they will be ignore anyway.

.. Note::
  SQLite is great for testing and to play with cubicweb but is not suited for
  production environments.
