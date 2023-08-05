.. _cluster-management:

=================
Managing clusters
=================

.. currentmodule:: coiled

You can manage your Coiled clusters in two ways: using the ``coiled`` Python
package or via Coiled's `web interface <https://cloud.coiled.io/clusters>`_.

The video below will walk you through creating custom Coiled clusters and managing your running clusters.

.. raw:: html

   <div style="display: flex; justify-content: center;">
       <iframe width="560" height="315" src="https://youtube.com/embed/neZVurbbBvA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   </div>


Listing and deleting clusters
-----------------------------

The :meth:`coiled.list_clusters` method will list all active clusters:

.. code-block:: python

    coiled.list_clusters()

Note that when a cluster is created, by default, a unique name for the cluster
is automatically generated. You can provide your own cluster name using the
``name=`` keyword argument for ``coiled.Cluster``.

:meth:`coiled.delete_cluster` can be used to delete individual clusters.
For example:

.. code-block:: python

    coiled.delete_cluster(name="my-cluster")

deletes the cluster named "my-cluster".

.. note::
    Listing and deleting only work for active clusters. Your account dashboard
    will show all the clusters that have been created, but their status will
    show as stopped.



Web interface
-------------

Coiled maintains a web interface where you can, among other things, view your
recently created Dask cluster along with other information like how many workers
are in the cluster, how much has running the cluster cost, etc. For more
information, see https://cloud.coiled.io/clusters.

.. figure:: images/clusters-table.png

The video below walks you through the Coiled dashboard:

.. raw:: html

   <div style="display: flex; justify-content: center;">
       <iframe width="560" height="315" src="https://www.youtube.com/embed/gSlUbo8TAqk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   </div>
