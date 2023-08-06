.. -*- coding: utf-8 -*-


Configure an instance
=====================

While creating an instance, a configuration file is generated in::

    $ (CW_INSTANCES_DIR) / <instance> / <configuration name>.conf

For example::

    /etc/cubicweb.d/myblog/all-in-one.conf

It is a simple text file in the INI format
(http://en.wikipedia.org/wiki/INI_file). In the following description,
each option name is prefixed with its own section and followed by its
default value if necessary, e.g. "`<section>.<option>` [value]."

.. note:: At runtime, configuration options can be overriden by environments
    variables which name follows the option name with ``-`` replaced by ``_``
    and a ``CW_`` prefix. For instance ``CW_BASE_URL=https://www.example.com``
    would override the ``base-url`` configuration option.

.. _`WebServerConfig`:

Configuring the Web server
--------------------------
:`web.auth-model` [cookie]:
    authentication mode, cookie or http
:`web.realm`:
    realm of the instance in http authentication mode
:`web.http-session-time` [0]:
    period of inactivity of an HTTP session before it closes automatically.
    Duration in seconds, 0 meaning no expiration (or more exactly at the
    closing of the browser client)

:`main.anonymous-user`, `main.anonymous-password`:
    login and password to use to connect to the RQL server with
    HTTP anonymous connection. CWUser account should exist.

:`main.base-url`:
    url base site to be used to generate the urls of web pages


Setting up the web client
-------------------------
:`web.embed-allowed`:
    regular expression matching sites which could be "embedded" in
    the site (controllers 'embed')
:`web.submit-url`:
    url where the bugs encountered in the instance can be mailed to


RQL server configuration
------------------------
:`main.host`:
    host name if it can not be detected correctly
:`main.pid-file`:
    file where will be written the server pid
:`main.uid`:
    user account to use for launching the server when it is
    root launched by init
:`main.session-time [30*60]`:
    timeout of a RQL session
:`main.query-log-file`:
    file where all requests RQL executed by the server are written


Configuring e-mail
------------------
RQL and web server side:

:`email.mangle-mails [no]`:
    indicates whether the email addresses must be displayed as is or
    transformed

RQL server side:

:`email.smtp-host [mail]`:
    hostname hosting the SMTP server to use for outgoing mail
:`email.smtp-port [25]`:
    SMTP server port to use for outgoing mail
:`email.smtp-username`:
    SMTP server username for authenticated email sending
:`email.smtp-password`:
    SMTP server password for authenticated email sending
:`email.sender-name`:
    name to use for outgoing mail of the instance
:`email.sender-addr`:
    address for outgoing mail of the instance
:`email.default dest-addrs`:
    destination addresses by default, if used by the configuration of the
    dissemination of the model (separated by commas)
:`email.supervising-addrs`:
    destination addresses of e-mails of supervision (separated by
    commas)


Configuring logging
-------------------
:`main.log-threshold`:
    level of filtering messages (DEBUG, INFO, WARNING, ERROR)
:`main.log-file`:
    file to write messages


.. _PersistentProperties:

Configuring persistent properties
---------------------------------
Other configuration settings are in the form of entities `CWProperty`
in the database. It must be edited via the web interface or by
RQL queries.

:`ui.encoding`:
    Character encoding to use for the web
:`navigation.short-line-size`:
    number of characters for "short" display
:`navigation.page-size`:
    maximum number of entities to show per results page
:`navigation.related-limit`:
    number of related entities to show up on primary entity view
:`navigation.combobox-limit`:
    number of entities unrelated to show up on the drop-down lists of
    the sight on an editing entity view

Cross-Origin Resource Sharing
-----------------------------

CubicWeb's support for the CORS_ protocol is provided by the wsgicors_
middleware at the Pyramid level. For now, the provided implementation only
deals with access to a CubicWeb instance as a whole. Support for a finer
granularity may be considered in the future.

.. _wsgicors: https://pypi.org/project/wsgicors/

A few parameters can be set to configure the CORS_ capabilities of CubicWeb,
the values are passed to the `wsgicors.CORS()` middleware constructor, hence
the wsgicors documentation can be used for more details.

.. _CORS: http://www.w3.org/TR/cors/

:`access-control-allow-origin`:
   comma-separated list of allowed origin domains or "*" for any domain
:`access-control-allow-methods`:
   comma-separated list of allowed HTTP methods
:`access-control-allow-headers`:
   comma-separated list of allowed HTTP custom headers (used in simple requests)
:`access-control-expose-headers`:
   comma-separated list of allowed HTTP custom headers (used in preflight requests)
:`access-control-max-age`:
   maximum age of cross-origin resource sharing (in seconds)

`credentials` is always set to `true` and is not configurable.
