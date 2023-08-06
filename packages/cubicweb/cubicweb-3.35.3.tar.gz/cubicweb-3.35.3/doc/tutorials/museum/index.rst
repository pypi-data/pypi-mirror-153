.. -*- coding: utf-8 -*-

.. _TutosMuseums:

Create a Website from scratch with CubicWeb
===========================================

Introduction
~~~~~~~~~~~~

This tutorial aims to demonstrate how to create a website using CubicWeb. This website will
present museums from French Ministry of Culture data, available here_.

.. _here: https://data.culture.gouv.fr/explore/dataset/liste-et-localisation-des-musees-de-france/export/

First, we will start with installation and creation of our website, and a short presentation of
out of the box CubicWeb functionalities. Then, we will see how to enhance our views using Jinja2
templates or React components to have a better looking site. Finally, we will see how to manage
more data, and how to serialize them in RDF.

At the end of this tutorial, you will have a website giving information about all France's
museums, describes them in RDF and present them on a map.

You can find the code of the finished tutorial in our forge, look for the cube tuto_.

.. _tuto: https://forge.extranet.logilab.fr/cubicweb/cubes/tuto/

.. toctree::
   :maxdepth: 2

   getting-started
   enhance-views
   data-management

