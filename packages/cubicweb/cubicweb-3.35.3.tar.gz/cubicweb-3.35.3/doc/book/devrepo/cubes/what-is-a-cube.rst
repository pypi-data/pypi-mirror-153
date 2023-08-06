What is a Cube?
---------------

A cube is the equivalent of a module or a component but for CubicWeb.
A website made with CubicWeb is generally an instance based on a cube that is
just an assembly of already existing cubes with some domain specific logics.
If you need a functionality that is not available, then you write a new Cube for
it (and hopefully share it with the community).

A cube is made of mainly four parts:

- its :ref:`data model <datamodel_definition>` stored in `schema.py`,
- its logic added to the :ref:`data <book/devrepo/entityclasses/>` stored in `entities`
- its logic concerning :ref:`dataflow <book/devrepo/repo/hooks/>` stored in `hooks`,
- its :ref:`user interface <book/devweb/>` stored in `views`.

A cube can also define:

- its :ref:`internationalization <book/devweb/internationalization/>` stored in the `i18n/`,
- new :ref:`cubicweb commands <book/admin/cubicweb-ctl/>` stored in `ccplugin.py`.

A cube can use other cubes as building blocks and assemble them to provide a
whole with richer functionnalities than its parts. The cubes `cubicweb-blog`_ and
`cubicweb-comment`_ could be used to make a cube named *myblog* with commentable
blog entries.


The `CubicWeb.org Forge`_ offers a large number of cubes developed by the community
and available under a free software license.
They are designed with the `KISS principle <https://en.wikipedia.org/wiki/KISS_principle>`_
as each cube usually adds a single functionality.
Usually an application is an instance based on a regular cube that is just an
assembly of existing cubes with some specific logics.


.. note::

   The command :command:`cubicweb-ctl list` displays the list of available cubes.

.. _`CubicWeb.org Forge`: https://forge.extranet.logilab.fr/cubicweb/cubicweb
.. _`cubicweb-blog`: https://forge.extranet.logilab.fr/cubicweb/cubes/blog
.. _`cubicweb-comment`: https://forge.extranet.logilab.fr/cubicweb/cubes/comment
