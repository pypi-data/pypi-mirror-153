:notoc:

.. _software-envs:

=====================
Software Environments
=====================

.. currentmodule:: coiled

.. toctree::
   :maxdepth: 1
   :hidden:

   software_environment_creation
   software_environment_management
   software_environment_local
   software_environment_cli


A crucial part of doing your work is making sure you have the software packages
you need. Coiled helps you manage software environments by building Docker
images from `pip <https://pip.pypa.io/en/stable/>`_ and
`conda <https://docs.conda.io/en/latest/>`_ environment files for you. You can
then use these environments locally, remotely in a Dask cluster, and can share
them with your friends and colleagues.

The video below will walk you through the process of creating and managing
software environments.

.. raw:: html

   <div style="display: flex; justify-content: center;">
       <iframe 
          width="560"
          height="315"
          src="https://youtube.com/embed/GfD40sn3h5E"
          title="YouTube video player" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        >
        </iframe>
   </div>


Supported software specifications
---------------------------------

Coiled supports publicly accessible conda packages, pip packages, and/or Docker
images for creating software environments. You can also compose these steps by,
for example, conda installing packages into a custom Docker image.


Design
------

Coiled uses packaging conventions you're already familiar with. You can point
Coiled to a list of conda or pip packages:

.. code-block:: python

    import coiled

    coiled.create_software_environment(
        name="my-software-env",
        conda=["dask", "xarray=0.15.1", "numba"],
    )

or to a local conda ``environment.yml`` or pip ``requirements.txt`` file:

.. code-block:: python

    coiled.create_software_environment(
        name="my-software-env",
        conda="environment.yml",
    )

to have custom Docker images built and stored for later use. Note that you do
not need to have Docker installed for Coiled to build Docker images for you!

Usage
-----

Coiled software environments can be used both locally by :ref:`installing the
software environment on your machine <local-software>` and on remote Dask
clusters (e.g. running on AWS):

.. code-block:: python

    import coiled

    # Create a cluster that uses the custom "my-software-env" software environment
    cluster = coiled.Cluster(software="my-software-env")

You can also collaborate with your friends and colleagues by easily sharing
software environments.

.. _coiled-runtime:

Coiled-runtime
--------------

Coiled maintains a number of software environments, found on the `Coiled software environments page <https://cloud.coiled.io/coiled/software>`_. For default coiled environments (e.g. ``coiled/default``) you'll notice ``coiled-runtime`` as one of the dependencies:

.. code:: yaml

    channels:
      - conda-forge
    dependencies:
      - python=<x.x>
      - coiled-runtime=<x.x.x>

``coiled-runtime`` is a `conda metapackage <https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html#metapackages>`_ that contains the recommended version of Dask and associated packages to make it easy to get started with Dask and Coiled (see `the recipe <https://github.com/coiled/coiled-runtime/blob/36df51243273b060407c93242333775ede840358/recipe/meta.yaml>`_ file for the complete list of included packages and versions). The tutorial on :doc:`setting up a custom software environment <tutorials/matching_coiled_senvs>` walks through how to use ``coiled-runtime`` to create a custom software environment.
