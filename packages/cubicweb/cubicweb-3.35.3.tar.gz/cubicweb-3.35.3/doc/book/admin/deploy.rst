.. -*- coding: utf-8 -*-

Deploy a *CubicWeb* application
===============================

.. _deploy_python:

Deployment with uwsgi
---------------------

`uWSGI <https://uwsgi-docs.readthedocs.io/>`_ is often used to deploy CubicWeb
applications.

Short version is install `uwsgi`:

.. sourcecode:: console

  apt install uwsgi

Deploy a configuration file for your application
`/etc/uwsgi/apps-enabled/example.ini`. Don't forget to replace `example` with
the instance name to deploy:

.. sourcecode:: ini

    [uwsgi]
    master = true
    http = 0.0.0.0:8080
    env = CW_INSTANCE=example
    module = cubicweb.pyramid:wsgi_application()
    processes = 2
    threads = 8
    plugins = http,python3
    auto-procname = true
    lazy-apps = true
    log-master = true
    disable-logging = true

You can run it manualliy with:

.. sourcecode:: console

    uwsgi --ini /etc/uwsgi/apps-enabled/example.ini

Apache configuration
````````````````````
It is possible to use apache (for example) as proxy in front of uwsgi.

For this to work you have to activate the following apache modules :

* rewrite
* proxy
* http_proxy

The command on Debian based systems for that is ::

  a2enmod rewrite http_proxy proxy
  /etc/init.d/apache2 restart

:Example:

   For an apache redirection of a site accessible via `http://localhost/demo` while cubicweb is
   actually running on port 8080:::

     ProxyPreserveHost On
     RewriteEngine On
     RewriteCond %{REQUEST_URI} ^/demo
     RewriteRule ^/demo$ /demo/
     RewriteRule ^/demo/(.*) http://127.0.0.1:8080/$1 [L,P]


   and we will configure the `base-url` in the `all-in-one.conf` of the instance:::

     base-url = http://localhost/demo

Deployment with SaltStack
-------------------------

To deploy with SaltStack one can refer themselves to the
`cubicweb-formula <https://hg.logilab.org/master/salt/cubicweb-formula/>`_.

.. _deploy_docker:

Deployment with Docker
----------------------

To deploy in a docker container cluster, you should use our
`docker image <https://hub.docker.com/r/logilab/cubicweb>`_. The source code is
also in the `forge <https://forge.extranet.logilab.fr/cubicweb/docker-cubicweb>`_.
For a standard cube with no `apt` dependencies, the following dockerfile is fine:

.. sourcecode:: Docker

    FROM logilab/cubicweb:3.29
    USER root
    COPY . /src
    RUN pip install -e /src
    USER cubicweb
    RUN docker-cubicweb-helper create-instance

To run your instance, don't forget the port redirection and change the image
name:

.. sourcecode:: console

    docker run --rm -it -p 8080:8080 example:latest

If you need to customize the variables in the files `all-in-one.conf` or
`sources`, you should pass them as environnement variables. For example, the
database name is read from `CW_DB_NAME`. The admin password is read from `CW_PASSWORD`.
Also if the database is on the host, it has to be accessible from the container:

.. sourcecode:: console

    docker run --rm -it -p 8080:8080 --env-file ./.env -v /var/run/postgresql:/var/run/postgresql example:latest

If your instance needs a scheduler, it has to be run in a separate container
from the same image:

.. sourcecode:: console

    docker run --rm -it --env-file ./.env -v /var/run/postgresql:/var/run/postgresql example:latest cubicweb-ctl scheduler instance

Don't forget to change the image name `example:latest` and the instance name `name`.

.. _deploy_kubernetes:

Deployment with Kubernetes
--------------------------

To deploy in a Kubernetes cluster, you can take inspiration from the
`deploy instructions <https://forge.extranet.logilab.fr/cubicweb/cubes/fresh/-/blob/branch/default/deploy/deployment.yaml>`_
included in `the fresh cube  <https://forge.extranet.logilab.fr/cubicweb/cubes/fresh>`_.
It includes nginx to serve static files, one container for the application and
one for the scheduler and also an `initContainer <https://kubernetes.io/docs/concepts/workloads/pods/init-containers/>`_ to automatically upgrade the
database in case of new version.
