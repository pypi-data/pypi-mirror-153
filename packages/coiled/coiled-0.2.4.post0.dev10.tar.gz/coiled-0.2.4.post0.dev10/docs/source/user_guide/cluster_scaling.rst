.. _cluster-scaling:

================
Scaling clusters
================

.. currentmodule:: coiled

Using the scale method
----------------------

.. _scaling-clusters:

After you're created a cluster with Coiled, you can scale it up or down using
the :meth:`coiled.Cluster.scale()` functionality. You can input the number of
desired worker nodes to scale up or down to as an integer, as in:

.. code-block:: python

   cluster.scale(20)

For example, to create a cluster with 10 workers and then scale it up to 15
workers, you would run the following commands:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(n_workers=10)
   cluster.scale(15)

You'll see the new desired cluster size reflected in the Coiled dashboard, and
the new worker nodes will be added and ready to receive work after they are
provisioned and join the Dask cluster.

.. note::

   When scaling a cluster up or down with ``cluster.scale()``, the operation
   will return asynchronously after the scaling request is acknowledged but
   before the desired cluster size is reached.

   If you need to wait for the cluster to reach a specific number of workers
   before continuing, then you can use the
   `client.wait_for_workers() <https://distributed.dask.org/en/latest/api.html#distributed.Client.wait_for_workers>`_
   functionality in the Dask client.

.. important::

   If you're configured Coiled with a backend that
   :doc:`runs on your own cloud account <backends>`, make sure that you've
   requested a sufficient number of instances per your quota/limits to support
   the desired amount of compute resources that you are requesting. Otherwise,
   Coiled will encounter quota limits when requesting additional compute
   resources, and your clusters will not be able to scale up to the desired
   sizes.

Using the adapt method
----------------------

You can also use the :meth:`coiled.Cluster.adapt()` method to let the scheduler
decide on how many workers it should create/destroy depending on the workload.
Adapt allows you to specify a range between the ``minimum`` and ``maximum``
number of workers, then Coiled will then handle scaling the cluster up or down
for you.

For example, to create a cluster and set the adaptive scaling between 2 workers
and 40, you would run the following commands:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster()

   cluster.adapt(minimum=2, maximum=40)

The ``maximum`` keyword argument is related to your core limits, if your account has a
limit of 150 cores and you request 100 workers bringing your core limit count above the
allowed number, Coiled will use all the available quota and stop creating workers if the
limit is reached.

.. seealso::

   You might be intestested on reading more about 
   `Adaptive Deployments in the Dask docs <https://docs.dask.org/en/latest/setup/adaptive.html>`_.

