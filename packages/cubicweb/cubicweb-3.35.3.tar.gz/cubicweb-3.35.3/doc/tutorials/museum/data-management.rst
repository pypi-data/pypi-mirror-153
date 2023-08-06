.. -*- coding: utf-8 -*-

.. _TutosMuseumsDataManagement:

Data management with CubicWeb
=============================

Import data
~~~~~~~~~~~

With our application customized, let's see how to import more data.
There is several ways to import data in CubicWeb. In our tutorial, we want to import our
museums from a `csv` file. This file is provided by the France's Ministry of Culture, and is
available here_.

.. _here: https://data.culture.gouv.fr/explore/dataset/liste-et-localisation-des-musees-de-france/export/

There are several ways to import data in CubicWeb; in this tutorial, we will use one of them,
the others are described here: :ref:`dataimport`.

First of all, we define in :file:`tuto/cubicweb_tuto/dataimport.py` a function which will read a file
from a `filepath` and create the corresponding entities, using a `CubicWeb connection`:

.. sourcecode:: python

    import csv


    def import_museums(cnx, filepath):
        existing_cities = dict(cnx.execute("Any Z, C Where C is City, C zip_code Z"))
        existing_cities_nb = len(existing_cities)
        created_museum_nb = 0
        with open(filepath) as fileobj:
            reader = csv.DictReader(fileobj, delimiter=";")
            for record in reader:
                museum_name = record["NOM DU MUSEE"]
                street = record["ADR"]
                zip_code = record["CP"]
                city_name = record["VILLE"]
                try:
                    lat, lng = record["coordonnees_finales"].split(",")
                    lat_long = {
                        "latitude": lat,
                        "longitude": lng,
                    }
                except (AttributeError, ValueError):
                    lat_long = {}
                try:
                    city = existing_cities[zip_code]
                except KeyError:
                    city = cnx.create_entity("City", name=city_name, zip_code=zip_code)
                    existing_cities[zip_code] = city.eid
                cnx.create_entity(
                    "Museum",
                    name=museum_name,
                    postal_address=f"{street}, {zip_code} {city_name}",
                    is_in=city,
                    **lat_long,
                )
                created_museum_nb += 1

        print(
            "Import finished! {} existing cities, {} cities created, {} museums created.".format(
                existing_cities_nb,
                len(existing_cities) - existing_cities_nb,
                created_museum_nb,
            )
        )

To be sure we don't have several time the same city, we first query CubicWeb to ask for all
existing city. To do this, we use a specific language called **RQL**. As for SPARQL, it's a
query language designed to query linked data. See :ref:`rql_intro` for more information about it.

Then, we put existing cities in a dictionary, using zip code as key. In the real world, a zip code
can concern several cities, but it's not really an issue in this tutorial.

For each line of our `csv` file, we will check if we already have the city in our base.
If not, we create it. Then, we create our Museum entity with all needed arguments.

To create an entity, we use the `create_entity` method of the CubicWeb connection. This method takes
as first argument the type of the entity (ie: the name of the corresponding class previously
defined in :file:`tuto/cubicweb_tuto/schema.py`), and then all arguments of the entity type.

In our example, a city needs a name and a zip code. A museum needs a name, a postal address,
a latitude, a longitude and a city. As `is_in` is a relation, we give to the corresponding argument
the eid of the city.

.. Note::

    As we have defined Museum in the schema, we have to link each instance of Museum to a City,
    that's why we create the city before the museum, and give this city as argument of the museum.

    If the city wasn't mandatory, we could add it later, using:

    .. sourcecode:: python

        museum_entity.cw_set(is_in=city)

To use our function we need to create a CubicWeb command that will call it. First, we create a file
:file:`tuto/cubicweb_tuto/ccplugin.py` (the name doesn't matter, but it is commonly used for all new
CubicWeb commands). Then, we write the following code:

.. sourcecode:: python

    from cubicweb.cwctl import CWCTL
    from cubicweb.toolsutils import Command
    from cubicweb.utils import admincnx

    from cubicweb_tuto.dataimport import import_museums


    @CWCTL.register
    class ImportMuseums(Command):
        """
        Import Museums and Cities from a CSV from:
        https://data.culture.gouv.fr/explore/dataset/liste-et-localisation-des-musees-de-france/export/
        """

        arguments = "<instance> <csv_file>"
        name = "import-museums"
        min_args = max_args = 2

        def run(self, args):
            appid, csv_file = args[:2]

            with admincnx(appid) as cnx:
                import_museums(cnx, csv_file)
                cnx.commit()

* ``@CWCTL.register`` allows to register the command and then make it available with
  ``cubicweb-ctl`` command by its ``name``.
* ``arguments`` defines which arguments take our command.
* ``name`` defines the name of the command.
* ``with admincnx(appid) as cnx`` allows to have an admin access to our instance, and then
  be able to create new entities.

Thus, to execute our import command, we just have to enter in our shell (within our virtual env):

.. code-block:: console

    cubicweb-ctl import-museums tuto_instance <path_to_the_csv>

After this script, we should be able to see that we have much more cities and museums by
visiting the homepage of our CubicWeb instance:

.. image:: ../../images/tutos-museum_finished_import.png
   :alt: A CubicWeb instance with several cities and museums.

RDF serialisation
~~~~~~~~~~~~~~~~~

Content negotiation
~~~~~~~~~~~~~~~~~~~
