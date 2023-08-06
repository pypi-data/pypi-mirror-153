.. -*- coding: utf-8 -*-

.. _TutosBaseCustomizingTheApplication:

Customizing your application
----------------------------

Usually you won't get enough by assembling cubes out-of-the-box.
You will want to customize them to get personal look and
feel, add your own data model and so on. Or maybe start from scratch?

So let's get a bit deeper and start coding our own cube. In our case, we want
to customize the blog we created to add more features to it.


Creating your own cube
~~~~~~~~~~~~~~~~~~~~~~

Once your |cubicweb| development environment is set up, you can create a new
cube::

  cubicweb-ctl newcube mycube

This will create a a directory named :file:`cubicweb-mycube` reflecting the
structure described in :ref:`cubelayout`.

To install your new cube on the virtual environment created previously, run
the following command in :file:`cubicweb-mycube` directory::

  pip install -e .

All `cubicweb-ctl` commands are described in details in
:ref:`cubicweb-ctl`.

Cube metadata
~~~~~~~~~~~~~

The folder :file:`cubicweb_mycube/` contains the actual code and metadata for your cube.
In this folder, a simple set of metadata about your cube are stored in the :file:`__pkginfo__.py`
file. In our case, we want to extend the blog cube, so we have to tell that our
cube depends on this cube by modifying the ``__depends__`` dictionary in that
file:

.. sourcecode:: python

   __depends__ =  {"cubicweb": ">= 3.35.0", "cubicweb-blog": None}

where ``None`` means we do not depend on a particular version of the cube.

.. _TutosBaseCustomizingTheApplicationDataModel:

Extending the data model
~~~~~~~~~~~~~~~~~~~~~~~~

The data model or schema is the core of your |cubicweb| application. It defines
the type of content your application will handle. It is defined in the file
:file:`schema.py` of the cube.


Defining our model
^^^^^^^^^^^^^^^^^^

Let's say we want a new entity type named `Community`
with a name and a description. A `Community` will hold several blogs.

We can edit the :file:`schema.py` as follows:

.. sourcecode:: python

  from yams.buildobjs import EntityType, RelationDefinition, String, RichString

  class Community(EntityType):
      name = String(maxsize=50, required=True)
      description = RichString()

  class community_blog(RelationDefinition):
      subject = 'Community'
      object = 'Blog'
      cardinality = '*?'
      composite = 'subject'


The import from the :mod:`yams` package provides necessary classes to build the schema.

This file defines the following:

* a `Community` has a name and a description as attributes

  - the name is a string which is required and cannot be longer than 50 characters

  - the description is an unconstrained string and may contains rich
    content such as HTML or Restructured text.

* a `Community` may be linked to a `Blog` using the `community_blog` relation

  - ``*`` means a community may be linked from 0 to N blog, ``?`` means a blog may
    be linked to 0 to 1 community. For completeness, you can also use ``+`` for
    1 to N, and ``1`` for a single mandatory relation (e.g. one to one);

  - this is a composite relation where `Community` (e.g. the subject of the
    relation) is the composite. That means that if you delete a community, its
    blog will be deleted as well.

Of course, there are a lot of other data types and relations such as constraints,
permissions, etc, that may be defined in the schema but those will not be covered
in this tutorial.

Notice that our schema refers to the `Blog` entity type which is not defined
here.  But we know this type is available since we depend on the `blog` cube defining it.


Applying changes from the model into our instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The problem is that we created an instance using the ``blog`` cube, not our
`mycube` cube. If we do not do anything there is no way we'll see anything
changing in the ``myblog`` instance.

As we do not have any really valuable data in the instance, an easy way would be to trash it and recreated it.
First stop the running instance by pressing ``Ctrl-C`` in the terminal running the server in debug mode.
Then run the following commands::

  cubicweb-ctl delete myblog
  cubicweb-ctl create mycube myblog
  cubicweb-ctl pyramid -D myblog

Another way is to add our cube to the instance using the ``cubicweb-ctl shell``
facility. It is a python shell connected to the instance with some special
commands available to manipulate it (the same as you'll have in migration
scripts, which are not covered in this tutorial). In that case, we are interested
in the ``add_cube`` command. First stop the instance by pressing ``Ctrl-C`` in the terminal running the server in debug mode
and enter the shell using the following command::

  cubicweb-ctl shell myblog

Then in the python shell, type the ``add_cube`` command::

  add_cube('mycube')

Press ``Ctrl-D`` to exit then restart your instance::

  cubicweb-ctl pyramid -D myblog

The ``add_cube`` command is enough since it automatically updates our
application to the cube's schema. There are plenty of other migration
commands of a more finer grain. They are described in :ref:`migration`

If you take another look at the schema on your instance, you will see that changes to the data model have
actually been applied (meaning database schema updates and all necessary actions have been done).

.. image:: ../../images/tutos-base_myblog-schema_en.png
   :alt: the instance schema after adding our cube

If you follow the ``Site information`` link in the home page, you will also see that the
instance is using blog and mycube cubes (sioc is a dependency of the blog cube).

.. image:: ../../images/tutos-base_myblog-siteinfo_en.png
   :alt: the instance schema after adding our cube

You can now add some communities and link them to a blog. You will see that the
framework provides default views for this entity type (we have not yet defined any
view for it!), and also that the blog primary view will show the community it is
linked to if any. All this thanks to the model driven interface provided by the
framework.

We will now see how to redefine each of them according to your needs
and preferences.

.. _TutosBaseCustomizingTheApplicationCustomViews:

Defining your views
~~~~~~~~~~~~~~~~~~~

|cubicweb| provides a lot of standard views in the directory
:file:`cubicweb/web/views/`. We already talked about `primary` and `list` views,
which are views applying to one or more entities.

A view is defined by a python class which includes:

- an identifier: all objects used to build the user interface in |cubicweb| are
  recorded in a registry and this identifier will be used as a key in that
  registry to store the view. There may be multiple views for the same identifier.

- a *selector*, which is a kind of filter telling how well a view suits to a
  particular context. When looking for a particular view (e.g. given an
  identifier), |cubicweb| computes for each available view with that identifier
  a score which is returned by the selector. Then the view with the highest
  score is used. The standard library of predicates is in :mod:`cubicweb.predicates`.

A view has a set of methods inherited from the :class:`cubicweb.view.View` class,
though you do not usually derive directly from this class but from one of its more
specific child class.

Last but not least, |cubicweb| provides a set of default views accepting any kind
of entities.

To illustrate this, we will create a community as we already have done for other entity types
through the index page. You will get a screen similar to this:

.. image:: ../../images/tutos-base_myblog-community-default-primary_en.png
   :alt: the default primary view for our community entity type


Changing the layout of the application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The layout is the general organization of the pages in the website. Views generating
the layout are sometimes referred to as `templates`. They are implemented by the
framework in the module :mod:`cubicweb.web.views.basetemplates`. By overriding
classes in this module, you can customize whatever part you wish of the default
layout.

|cubicweb| provides many other ways to customize the
interface thanks to actions and components (which you can individually
(de)activate, control their location, customize their look...) as well as
"simple" CSS customization. You should first try to achieve your goal using such
fine grained parametrization rather then overriding a whole template, which usually
embeds customisation access points that you may loose in the process.

But for the sake of example, let's say we want to change the generic page
footer. We can simply add in the file :file:`cubicweb_mycube/views.py` the code below:

.. sourcecode:: python

  from cubicweb.web.views import basetemplates


  class MyHTMLPageFooter(basetemplates.HTMLPageFooter):

      def footer_content(self):
          self.w(u'This website has been created with <a href="http://cubicweb.org">CubicWeb</a>.')


  def registration_callback(vreg):
      vreg.register_all(globals().values(), __name__, (MyHTMLPageFooter,))
      vreg.register_and_replace(MyHTMLPageFooter, basetemplates.HTMLPageFooter)


* Our class inherits from the default page footer to ease getting things right,
  but this is not mandatory.

* When we want to write something to the output stream, we simply call `self.w`,
  which *must be passed a unicode string*.

* Since both :class:`HTMLPageFooter` and :class:`MyHTMLPageFooter` have the same selector, hence the same
  score the framework would not be able to choose which footer to use.
  In this case we want our footer to replace the default one, so we have
  to define a :func:`registration_callback` function to control object
  registration. The first instruction tells to register everything in the module
  but the :class:`MyHTMLPageFooter` class, then the second to register it instead
  of :class:`HTMLPageFooter`. Without this function, everything in the module is
  registered blindly.

.. Note::

  When a view is modified while running in debug mode, it is not required to
  restart the instance server. Save the Python file and reload the page in your
  web browser to view the changes.

You will now see this simple footer on every page of the website.


Primary view customization
~~~~~~~~~~~~~~~~~~~~~~~~~~

The `primary` view (i.e. any view with the identifier set to `primary`) is the one used to
display all the information about a single entity. The standard primary view is one
of the most sophisticated views of all. It has several customisation points, but
its power comes with `uicfg` allowing you to control it without having to
subclass it.

However this is a bit off-topic for this first tutorial. Let's say we simply want a
custom primary view for the ``Community`` entity type, using directly the view
interface without trying to benefit from the default implementation (you should
do that though if you're rewriting reusable cubes; everything is described in more
details in :ref:`primary_view`).


here is the code that we will put in the file :file:`cubicweb_mycube/views.py` of our cube:

.. sourcecode:: python

  from cubicweb.predicates import is_instance
  from cubicweb.web.views import primary


  class CommunityPrimaryView(primary.PrimaryView):
      __select__ = is_instance('Community')

      def cell_call(self, row, col):
          entity = self.cw_rset.get_entity(row, col)
          self.w(u'<h1>Welcome to the "%s" community</h1>' % entity.printable_value('name'))

          if entity.description:
              self.w(u'<p>%s</p>' % entity.printable_value('description'))

What's going on here?

* Our class inherits from the default primary view, here mainly to get the correct
  view identifier, since we do not use any of its features.

* We set on it a selector telling that it only applies when trying to display
  some entity of the `Community` type. This is enough to get an higher score than
  the default view for entities of this type.

* A view that applies to an entity usually has to define the method
  ``cell_call`` as an entry point. This receives the arguments
  ``row`` and ``col`` telling to which entity in the result set the view is
  applied. We can then get this entity from the result set (``self.cw_rset``) by
  using the ``get_entity`` method.

* To ease thing, we access our entity's attribute to display using its
  ``printable_value`` method, which will handle formatting and escaping when
  necessary. As you can see, you can also access attributes by their name on the
  entity to get the raw value.


You can now reload the page of the community we just created and see the changes.

.. image:: ../../images/tutos-base_myblog-community-custom-primary_en.png
   :alt: the custom primary view for our community entity type

We have seen here a lot of thing you will have to deal with to write views in
|cubicweb|. The good news is that this is almost everything that is used to
build higher level layers.

.. Note::

  As things get complicated and the volume of code in your cube increases, you can
  of course still split your views module into a python package with subpackages.

You can find more details about views and selectors in :ref:`Views`.


Write entities to add logic in your data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|cubicweb| provides an ORM (Object-Relational Mapper) to programmatically manipulate
entities (just like the one we have fetched earlier by calling
``get_entity`` on a result set). By default, entity
types are instances of the :class:`AnyEntity` class, which holds a set of
predefined methods as well as properties automatically generated for
attributes/relations of the type it represents.

You can redefine each entity to provide additional methods or whatever you want
to help you write your application. Customizing an entity requires that your
entity:

- inherits from :class:`cubicweb.entities.AnyEntity` or any subclass

- defines a :attr:`__regid__` linked to the corresponding data type of your schema

You may then want to add your own methods, override default implementation of some
method, etc... To do so, write this code in :file:`mycube/entities.py`:

.. sourcecode:: python

    from cubicweb.entities import AnyEntity, fetch_config


    class Community(AnyEntity):
        """customized class for Community entities"""
        __regid__ = 'Community'

        fetch_attrs, cw_fetch_order = fetch_config(['name'])

        def dc_title(self):
            return self.name

        def display_cw_logo(self):
            return 'CubicWeb' in self.name

In this example:

* we used the :func:`fetch_config` convenience function to tell which attributes
  should be prefetched by the ORM when looking for some related entities of this
  type, and how they should be ordered

* we overrode the standard :meth:`dc_title` method, used in various place in the interface
  to display the entity (though in this case the default implementation would
  have had the same result)

* we implemented here a method :meth:`display_cw_logo` which tests if the
  community title contains `CubicWeb`. It can then be used when you are writing
  code involving `Community` entities in your views, hooks, etc. For instance,
  you can modify your previous views as follows:

.. sourcecode:: python


  class CommunityPrimaryView(primary.PrimaryView):
      __select__ = is_instance('Community')

      def cell_call(self, row, col):
          entity = self.cw_rset.get_entity(row, col)
          self.w(u'<h1>Welcome to the "%s" community</h1>' % entity.printable_value('name'))

          if entity.display_cw_logo():
              self.w(u'<img src="https://docs.cubicweb.org/_static/logo-cubicweb.svg"/>')

          if entity.description:
              self.w(u'<p>%s</p>' % entity.printable_value('description'))

Then each community whose description contains 'CW' is shown with the |cubicweb|
logo in front of it.

.. Note::

  As for view, you don't have to restart your instance when modifying some entity
  classes while your server is running in debug mode, the code will be
  automatically reloaded.


Extending the application by using more cubes!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the goals of the |cubicweb| framework is to have truly reusable
components. To do so they must behave nicely when plugged into the
application and be easily customisable, from the data model to the user
interface. Thanks to systems such as the selection mechanism and the choice
to write views as python code, we can build our pages using true object oriented
programming techniques to achieve this goal.


A library of standard cubes is available at the `CubicWeb Forge <https://forge.extranet.logilab.fr/cubicweb/cubes>`_
to address a lot of common problems such as manipulating files, people, todos, etc. In
our community blog case, we could be interested for instance in functionalities
provided by the `comment <https://forge.extranet.logilab.fr/cubicweb/cubes/comment>`_ and
`tag <https://forge.extranet.logilab.fr/cubicweb/cubes/tag>`_ cubes. ``comment`` provides threaded
discussion functionalities and ``tag`` a simple tag mechanism to classify content.
We will first modify our cube's :file:`__pkginfo__.py` file to add those cubes as dependencies:

.. sourcecode:: python

   __depends__ =  {'cubicweb': '>= 3.35.0',
                   'cubicweb-blog': None,
                   'cubicweb-comment': None,
                   'cubicweb-tag': None}

Now we will simply tell on which entity types we want to activate the ``comment``
and ``tag`` cubes by adding respectively the ``comments`` and ``tags`` relations on
them in our schema (:file:`schema.py`).

.. sourcecode:: python

  class comments(RelationDefinition):
      subject = 'Comment'
      object = 'BlogEntry'
      cardinality = '1*'
      composite = 'object'


  class tags(RelationDefinition):
      subject = 'Tag'
      object = ('Community', 'BlogEntry')


In the above code we activated comments on ``BlogEntry`` entities and tags on
both ``Community`` and ``BlogEntry``. Various views from both ``comment`` and ``tag``
cubes will then be automatically displayed when one of those relations is supported.

Let's install the cubes and synchronize the data model as we've done earlier. So first install the cubes::

    pip install cubicweb-comment cubicweb-tag

Stop the instance by pressing ``Ctrl-C`` in the terminal running the server in debug mode and enter the migration shell::

  cubicweb-ctl shell myblog

Add the new cubes and exit with ``Ctrl-D``::

  add_cubes(('comment', 'tag'))

Then restart the instance with ``cubicweb-ctl pyramid -D myblog`` and open a blog entry:

.. image:: ../../images/tutos-base_myblog-blogentry-taggable-commentable-primary_en.png
   :alt: the primary view for a blog entry with comments and tags activated

As you can see, we now have a box displaying tags and a section proposing to add
a comment and displaying existing one below the post. All this without changing
anything in our views, thanks to the design of generic views provided by the
framework. Though if we take a look at a community, we will not see the tags box!
This is because by default this box tries to locate itself in the right column within
the white frame, and this column is handled by the primary view we overrode.
Let's change our view to make it more extensible, by keeping both our
custom rendering but also extension points provided by the default
implementation.

Add the following code in :file:`cubicweb_mycube/views.py`:


.. sourcecode:: python

  class CommunityPrimaryView(primary.PrimaryView):
      __select__ = is_instance('Community')

      def render_entity_title(self, entity):
          self.w(u'<h1>Welcome to the "%s" community</h1>' % entity.printable_value('name'))

      def render_entity_attributes(self, entity):
          if entity.display_cw_logo():
              self.w(u'<img src="https://docs.cubicweb.org/_static/logo-cubicweb.svg"/>')

          if entity.description:
              self.w(u'<p>%s</p>' % entity.printable_value('description'))

By reloading the Community page, it will now appear properly:

.. image:: ../../images/tutos-base_myblog-community-taggable-primary_en.png
   :alt: the custom primary view for a community entry with tags activated

You can control part of the interface independently from each others, piece by
piece.
