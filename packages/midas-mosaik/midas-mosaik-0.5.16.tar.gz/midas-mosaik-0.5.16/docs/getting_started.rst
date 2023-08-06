Getting started
===============

This guide describes how to use *midas* to run some simple simulations.

Prerequisites
-------------

It is assumed that you have already followed the instructions of the
:doc:`Installation <installation>` guide.

First start
-----------

To work properly, *midas* needs to perform some setup. First, a runtime
configuration file is required. This file stores information that are
necessary for *midas*, e.g., where the datasets are located on your machine.
The command line tool *midasctl* is able to create such a configuration file
for you:

.. code-block:: bash

    midasctl configure --autocfg

For most of the users, the default values should suffice. If you want to have
more control over the process, just leave out the *--autocfg* parameter and
you will be asked where to store the configuration file and the datasets.

The next step is to download the required datasets. *midasctl* has a command
for that, as well:

.. code-block:: bash

    midasctl download

This will download all required datasets to the download location specified in
the runtime configuration file.

Troubleshooting
###############

Even if the installation was successful, Windows users may get errors during
the *download* command. The most common error is that pytables could not be
imported although it is installed. Installing Visual Studio solved the issues
for some users (see :doc:`Installation <installation>`, a reinstallation of
the virtualenv might also be required).

Running a simple scenario
-------------------------

*midas* has a few preconfigured scenarios that run out-of-the-box. To test
your installation, type

.. code-block:: bash

    midasctl run demo

This will start the scenario *midasmv*, which consists of a CIGRE medium
voltage grid and household data attached to it. 

Congratulations! You have successfully run a co-simulation with 
*midas*. Now see :doc:`Configuration <configuration>` for a more in-depth look
at the scenario file and how to manipulate it.