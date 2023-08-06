:notoc:

=============
Dask Clusters
=============

Coiled manages Dask clusters. It manages cloud resources, networking, software
environments, and everything you need to scale Python in the cloud robustly and
easily.

.. currentmodule:: coiled

.. toctree::
   :maxdepth: 1
   :hidden:

   cluster_creation
   cluster_scaling
   cluster_reuse
   cluster_management

Simple Example
--------------

The main entry point to launch a Coiled cluster is the ``coiled`` Python API. In
the simplest case you can run the following from anywhere that you can run
Python.

.. code-block:: python

   import coiled

   # Spin up a Dask cluster using Coiled
   cluster = coiled.Cluster()

And then you can connect to that cluster with Dask

.. code-block:: python

   from dask.distributed import Client

   client = Client(cluster)


Configuration
-------------

Though in real-world use cases there are many parameters that we may want to
control:

- The amount of RAM and number of CPUs in each worker
- The number of workers to use
- Whether or not to use GPUs
- The software used in each worker
- ...

These can also be specified when you create a Coiled cluster. For example:

.. code-block:: python

    import coiled

    # Spin up a Dask cluster using Coiled
    # where each worker has 4 CPUs and 16 GiB of RAM
    cluster = coiled.Cluster(
        worker_cpu=4,
        worker_memory="16 GiB",
    )

More details about creating Dask clusters with Coiled are discussed on the
:ref:`cluster-creation` documentation page.


Learn more
----------

In the next sections we'll learn more about how to configure and launch Dask
clusters.
