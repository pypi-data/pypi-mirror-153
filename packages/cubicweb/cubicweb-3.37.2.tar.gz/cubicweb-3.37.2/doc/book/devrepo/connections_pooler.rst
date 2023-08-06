.. -*- coding: utf-8 -*-

.. _connection_poller:

Source connections pooler
=========================

*CubicWeb* comes with a connections pool for it's datasource (typically sqlite
or postgresql), it is a dynamic pool meaning that:

* it will keep a minimum number of connections open (by default 0)
* when load increase it will open new connections
* if a max number of connections is set it will stop once it's reached
* if the max number of connections is zero, it is considered to be unlimited
* after some idle time (`connections-pool-idle-timeout`), if no new connections needed to be open
  on a new request, the pool will close one unused connection if the queue isn't empty
* if no connection are available after some time and the max number of connections has been
  reached, the connections pool will raise. To fix this, you can either increase the value of
  `connections-pool-max-size` or set it to 0 for an unlimited number of connections. A minimum of
  5 connections per process is recommended if you want to set a max number.

Note that the connections pool won't be activated in some "quick start" situations
like database dump/restore.

Configuration
-------------

The values used by the connections pool are fully configurable *in your instance
configuration file* (usually the `all-in-one.conf`), here is the list:

* **connections-pooler-enabled**: enable the connections pooler, default: true. You want to disable
  the pool if you are using another external pooling system like pgbouncer.
* **connections-pool-max-size**: max size of the connections pool. 0 means unlimited. Each source
  supporting multiple connections will have this maximum number of opened connections, default: 0
* **connections-pool-min-size**: min size of the connections pool. Each source
  supporting multiple connections will have this minimum number of opened
  connections, default: 0
* **connections-pool-idle-timeout**: the delay, in seconds, after the last opened connection before
  which the pool will start closing unused connections. A connection is only closed on a request
  that didn't need to create a new connection, default: 600
