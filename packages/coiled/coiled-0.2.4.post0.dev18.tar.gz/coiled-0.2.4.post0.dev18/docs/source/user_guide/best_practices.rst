Best Practices
==============

When performing computations across a distributed cluster on the cloud, there
are a few things to keep in mind to help you be as effective as possible. This
page contains suggestions for some best practices when using Coiled.


Use the same software locally and on Coiled
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using Coiled you'll connect your local machine (e.g. your laptop) to a
remote Dask cluster. It's important that both your local and remote software
environments have the same libraries installed in them. Version mismatches
between these two environments can sometimes yield unexpected errors.

With this in mind, Coiled has a ``coiled install`` command line utility
(:ref:`documentation <coiled-install-api>`) which you can run locally to create
a conda environment on your machine with the same packages in a software
environment used locally. Run the following locally in a terminal:

.. code-block:: bash

   $ coiled install <software-environment-name>

where ``<software-environment-name>`` should be replaced with the name of the
Coiled software environment you want to install on your machine.

.. tip::

   You can check whether or not the version of a package you have locally is the
   same version that's being used remotely on a Coiled cluster using Dask's
   :meth:`distributed.Client.get_versions` method:

   .. code-block::

      import coiled
      from dask.distributed import Client

      # Create a Coiled cluster and connect a Dask Client to it
      cluster = coiled.Cluster(...)
      client = Client(cluster)

      # This will raise a ValueError if package versions do not match
      client.get_versions(packages=["xgboost", "numpy"], check=True)


Look at cluster logs
^^^^^^^^^^^^^^^^^^^^

Coiled clusters keep track of various events that happen throughout a cluster's
lifetime through maintaining a log on the scheduler and workers in the cluster.
These cluster logs provide insight into cluster activity and are particularly
useful when debugging tricky situations (e.g. when a ``KilledWorker``
`error is raised <https://distributed.dask.org/en/latest/killed.html>`_).
For more information see :doc:`logging`.

Use Dask best practices
^^^^^^^^^^^^^^^^^^^^^^^

The Dask community maintains a
`general Dask best practices page <https://docs.dask.org/en/latest/best-practices.html>`_,
as well as separate best practices pages for working with individual Dask
collections:

- `Dask Array best practices <https://docs.dask.org/en/latest/array-best-practices.html>`_
- `Dask DataFrame best practices <https://docs.dask.org/en/latest/dataframe-best-practices.html>`_
- `Dask Delayed best practices <https://docs.dask.org/en/latest/delayed-best-practices.html>`_

It's generally recommended to use Dask best practices with your Coiled
workloads.
