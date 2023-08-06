====================================
Set up a custom software environment
====================================

This tutorial will go through creating a custom local software environment that is in sync with a Coiled software environment. It is important that the software installed in the user environment (often a local computer) is the same as in the cloud computing environment where the Dask clusters are created (see :doc:`../software_environment_local` for more information).

.. figure:: ../images/coiled-architecture.png
   :width: 100%
   :alt: Coiled Architecture

   Coiled Architecture (click image to enlarge)

Installing software can be challenging due to the combinations of various requirements, dependencies, and configurations. To simplify this process, we can use the `coiled-runtime metapackage <https://github.com/coiled/coiled-runtime>`_ with the recommended versions of Dask and associated packages to get started (see the :ref:`overview on coiled-runtime <coiled-runtime>` for more information).

Create the environment locally
------------------------------

In the :doc:`Getting Started page <../getting_started>`, you created the ``coiled/default`` environment locally. Though this is a great way to get started quickly, as a next step we recommend creating a custom environment specific to the needs of your project. One way to do this is using an ``environment.yml`` file and conda.

Start by copying and pasting the following into a file named ``environment.yml``, replacing ``<x.x.x>`` with the versions you would like to use and optionally including any other packages you need in the list of dependencies. You can get most up-to-date version of coiled-runtime from the latest `tag <https://github.com/coiled/coiled-runtime/tags>`_ in the public coiled-runtime repository. Python versions 3.7, 3.8, and 3.9 are currently supported (see `software environments yaml file <https://github.com/coiled/coiled-runtime/blob/304ae9db862e23d38f17d73ce7a3f7ca965eeff2/.github/workflows/software-environments.yml#L16>`_ in the coiled-runtime repository).

.. code:: yaml

    channels:
      - conda-forge
    dependencies:
      - coiled-runtime=<x.x.x>
      - python=<x.x.x>

If you wanted to include XGBoost, use Python version 3.9, and coiled-runtime version 0.0.3, the ``environment.yml`` file would look like the following example. In case you would like to include packages that are not available on conda-forge, you can also use pip.

.. code:: yaml

    channels:
      - conda-forge
    dependencies:
      - coiled-runtime=0.0.3
      - python=3.9
      - xgboost=1.5.1
      # uncomment the lines below for installing packages with pip
      # - pip
      # - pip:
        # - <pip-only-installable-package>

Run the code snippet below in your terminal to create and activate the same environment locally. In this example, the environment is named ``my-env-py39`` (set with the ``-n`` flag). The environment name should only contain ASCII letters, hyphens, and underscores and be something that will help you remember which project it will be used for. It is conventional to include the python version at the end, but not required.

.. code:: bash

    $ conda env create -f environment.yml -n my-env-py39
    $ conda activate my-env-py39

Create the environment on the cloud
-----------------------------------

Next create this same environment to be used in the cloud computing environment using the ``coiled env create`` command line tool:

.. code:: bash

    $ coiled env create -n my-env-py39 --conda environment.yml

This is one of many ways Coiled supports creating software environments on the cloud computing environment. For a comprehensive overview see the documentation on :doc:`creating software environments </user_guide/software_environment_creation>`.

Now you can launch a Dask cluster with this environment, replacing ``software="my-env-py39"`` with the name of your software environment:

.. code:: python

    import coiled

    cluster = coiled.Cluster(software="my-env-py39")

    cluster.close()

Key takeaways
-------------

In this tutorial, you created a custom software environment by relying on the `coiled-runtime metapackage <https://github.com/coiled/coiled-runtime>`_. As you create more custom software environments for other projects, keep the following guidelines in mind:

#. **Pin a specific Python version.** This is an important first step and will determine which package versions to pin.
#. **Pin specific package versions.** Using specific package versions is good practice for visibility and replicability, with the added benefit of making the environment much faster to build. When using Coiled, pinning specific versions reduces the possibility of version mismatches between the user and cloud environments (see the :ref:`FAQ on version mismatch warnings <faq-version-mismatch>`).
#. **Use the conda-forge channel.** `conda-forge <https://conda-forge.org/docs/user/introduction.html#a-brief-introduction>`_ is maintained by the maintainers of the packages themselves and can be more up-to-date, has more packages available, and can reduce inter-package compatibility.

Now that you have your custom environment set up, you may want to check out the documentation on :doc:`creating and managing Dask clusters </user_guide/cluster>`.
