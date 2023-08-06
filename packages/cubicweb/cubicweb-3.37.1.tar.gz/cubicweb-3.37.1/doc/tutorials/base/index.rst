.. -*- coding: utf-8 -*-

.. _TutosBase:

Building a simple blog with |cubicweb|
======================================

|cubicweb| is a semantic web application framework which favors reuse and
object-oriented designs.

This tutorial is designed to help you make your very first steps with
|cubicweb|. It will guide you through basic concepts such as:

* getting an application running by using existing components
* discovering the default user interface
* extending and customizing the look and feel of that application

More advanced concepts are covered in :ref:`TutosPhotoWebSite`.


.. _TutosBaseVocab:

Some vocabulary
---------------

|cubicweb| comes with a few words of vocabulary that you should know to
understand what we're talking about. To follow this tutorial, you should at least
know that:

* a `cube` is a component that usually includes a model defining some data types
  and a set of views to display them. A cube can be built by assembling other
  cubes;

* an `instance` is a specific installation of one or more cubes and includes
  configuration files, a web server and a database.

Reading :ref:`Concepts` for more vocabulary will be required at some point.

Now, let's start the hot stuff!

.. toctree::
   :maxdepth: 2

   blog-in-five-minutes
   discovering-the-ui
   customizing-the-application
   conclusion
