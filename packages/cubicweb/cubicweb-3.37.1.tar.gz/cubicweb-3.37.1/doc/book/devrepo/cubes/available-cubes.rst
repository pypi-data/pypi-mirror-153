.. _AvailableCubes:

Available cubes
---------------

An instance is made of several basic cubes. In the set of available
basic cubes we can find for example:

Base entity types
~~~~~~~~~~~~~~~~~
* addressbook_: PhoneNumber and PostalAddress
* card_: Card, generic documenting card
* event_: Event (define events, display them in calendars)
* file_: File (to allow users to upload and store binary or text files)
* link_: Link (to collect links to web resources)
* mailinglist_: MailingList (to reference a mailing-list and the URLs
  for its archives and its admin interface)
* person_: Person (easily mixed with addressbook)
* task_: Task (something to be done between start and stop date)
* zone_: Zone (to define places within larger places, for example a
  city in a state in a country)


Classification
~~~~~~~~~~~~~~
* folder_: Folder (to organize things by grouping them in folders)
* keyword_: Keyword (to define classification schemes)
* tag_: Tag (to tag anything)

Other features
~~~~~~~~~~~~~~
* basket_: Basket (like a shopping cart)
* blog_: a blogging system using Blog and BlogEntry entity types
* comment_: system to attach comment threads to entities)
* email_: archiving management for emails (`Email`, `Emailpart`,
  `Emailthread`), trigger action in cubicweb through email





.. _addressbook: https://forge.extranet.logilab.fr/cubicweb/cubes/addressbook
.. _basket: https://forge.extranet.logilab.fr/cubicweb/cubes/basket
.. _card: https://forge.extranet.logilab.fr/cubicweb/cubes/card
.. _blog: https://forge.extranet.logilab.fr/cubicweb/cubes/blog
.. _comment: https://forge.extranet.logilab.fr/cubicweb/cubes/comment
.. _email: https://forge.extranet.logilab.fr/cubicweb/cubes/email
.. _event: https://forge.extranet.logilab.fr/cubicweb/cubes/event
.. _file: https://forge.extranet.logilab.fr/cubicweb/cubes/file
.. _folder: https://forge.extranet.logilab.fr/cubicweb/cubes/folder
.. _keyword: https://forge.extranet.logilab.fr/cubicweb/cubes/keyword
.. _link: https://forge.extranet.logilab.fr/cubicweb/cubes/link
.. _mailinglist: https://forge.extranet.logilab.fr/cubicweb/cubes/mailinglist
.. _person: https://forge.extranet.logilab.fr/cubicweb/cubes/person
.. _tag: https://forge.extranet.logilab.fr/cubicweb/cubes/tag
.. _task: https://forge.extranet.logilab.fr/cubicweb/cubes/task
.. _zone: https://forge.extranet.logilab.fr/cubicweb/cubes/zone

To declare the use of a cube, once installed, add the name of the cube
and its dependency relation in the `__depends_cubes__` dictionary
defined in the file `__pkginfo__.py` of your own component.

.. _`CubicWeb's forge`: https://forge.extranet.logilab.fr/cubicweb/
