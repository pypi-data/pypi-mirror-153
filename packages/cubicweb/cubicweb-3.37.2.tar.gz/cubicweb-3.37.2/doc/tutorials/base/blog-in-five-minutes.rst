.. -*- coding: utf-8 -*-

.. _TutosBaseBlogFiveMinutes:

Get a blog running in five minutes!
-----------------------------------

First choose and follow :ref:`the installation method <SetUpEnv>` of your choice.

Once you have |cubicweb| setup, install the `blog cube <https://forge.extranet.logilab.fr/cubicweb/cubes/blog>`_
using the following command::

    pip install cubicweb-blog

Then you can create and initialize your blog instance::

    cubicweb-ctl create blog myblog

Here the ``blog`` argument tells the command to use the blog
cube as a base for your instance named ``myblog``.

.. Note::

   If you get a permission error of the kind ``OSError: [Errno 13] Permission denied: '/etc/cubicweb.d/myblog'``
   , read the :ref:`next section <AboutFileSystemPermissions>`.

This command will ask you a series of question. The first one is about the database engine to use (SQLite or PostgreSQL).
For this tutorial, we will use SQLite as it is easier to setup and does not need a database server.
In production environments, PostgreSQL is recommended as it offers better performances. More information on
database configuration can be found :ref:`here <DatabaseInstallation>`.

The command will also create a user used to manage your instance, for which you will be asked to give a name and password.

You can leave the remaining questions to their default by simply pressing ``Enter``.

.. Note::
    If you get errors during installation such as::

        while handling language es: [Errno 2] No such file or directory: 'msgcat': 'msgcat'
        while handling language en: [Errno 2] No such file or directory: 'msgcat': 'msgcat'
        while handling language fr: [Errno 2] No such file or directory: 'msgcat': 'msgcat'

    This means you are missing the ``gettext`` dependency. To fix this, follow the instructions in the section :ref:`InstallDependencies`.
    Then either restart the installation process or run ``cubicweb-ctl i18ncubicweb && cubicweb-ctl i18ncube blog`` after installation. More information in :ref:`internationalization`.

.. Then you need to setup the CubicWeb Pyramid interface as document in the section
.. :ref:`pyramid_settings`.

Then you need to tell |cubicweb| your instance is going to run on the localhost by editing :file:`~/etc/cubicweb.d/myblog/all-in-one.conf`.
In this file under the ``[MAIN]`` section, replace the line ``#host=` by `host=localhost``.

Once this process is complete (including database initialisation), you can start
your instance by using::

    cubicweb-ctl pyramid -D myblog

The ``-D`` option activates the debugging mode. Removing it will launch the instance
as a daemon in the background.

This is it, your blog is functional and running at `http://localhost:8080 <http://localhost:8080>`_!

.. _AboutFileSystemPermissions:

About file system permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unless you :ref:`installed from source <SourceInstallation>`, the above commands will initialize your instance as a regular user in your home directory (under `~/etc/cubicweb.d/`).
If you installed from source, your instance will be created in system directories and thus will require root privileges.
To change this behavior, please have a look at the :ref:`ResourceMode` section.


Instance parameters
~~~~~~~~~~~~~~~~~~~

If you would like to change database parameters such as the database host or the
user name used to connect to the database, edit the ``sources`` file located in the
:file:`/etc/cubicweb.d/myblog` directory.

Then relaunch the database creation::

     cubicweb-ctl db-create myblog

Other parameters, like web server or emails parameters, can be modified in the
:file:`/etc/cubicweb.d/myblog/all-in-one.conf` file (or :file:`~/etc/cubicweb.d/myblog/all-in-one.conf` depending on your configuration.)

You'll have to restart the instance after modification in one of those files.

