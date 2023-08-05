=========
Analytics
=========


.. note::

    Coiled's analytics functionality is under active development and its features are still
    experimental. Please submit feedback to our :doc:`support team <support>`.

A key part of running distributed workloads at scale with Dask and Coiled
is understanding what is happening in your Coiled account, including

* How much data is being processed
* How much your Dask computations/clusters cost
* Dask adoption and usage within your team
* Where there are opportunities for greater speed and efficiency

To that end, Coiled collects usage data for your clusters and surfaces it to you
on `https://cloud.coiled.io <https://cloud.coiled.io>`_.


Account-level analytics
-----------------------

In addition to the cost and metrics shown on your account dashboard for recent clusters,
Coiled provides more detailed analytics and historical information for each account.
This page is at ``https://cloud.coiled.io/<your-account-name>/analytics``
and accessible using the `Analytics` item in the sidebar.
It shows account-level information, and allows you to answer questions
about where and how resources are being spent.


Account Statistics
^^^^^^^^^^^^^^^^^^

The account statistics panel shows some high-level values for Coiled usage
in your account, including total cluster time, memory processed, and tasks executed.

.. figure:: images/account-statistics.png


.. _member-compute-usage:

Member Compute Usage
^^^^^^^^^^^^^^^^^^^^

Coiled accounts can have many :doc:`members <teams>`.
The `Member Compute Usage` panel shows the activity of the account members over the last
several months, including total cluster time, total compute time, and total cluster cost,
broken into weekly bins.

By clicking on a particular bin, the :ref:`cluster-listing` will be filtered to show
only clusters for that user and time period. Double-clicking clears the selection.


.. _cluster-listing:

Cluster Listing
^^^^^^^^^^^^^^^

The clusters table shows statistics for clusters that have been run in your account.
It includes the user, start/stop time, cost, and compute statistics for the cluster.
By clicking on the eyeball icon, you will be taken to the :ref:`analytics page<cluster-analytics>`
for that cluster, allowing you to investigate the performance of specific computations.

By default, the listing shows the most recent 100 clusters from the account,
but it will show clusters from a specific time window and creator if you make a selection
in the :ref:`member-compute-usage` panel.


Performance Reports
^^^^^^^^^^^^^^^^^^^

Dask performance reports can be uploaded to ``cloud.coiled.io`` and viewed there.
Any reports that have been uploaded with to a Coiled account will be listed here,
and you can click through to view them.

For more information, see :doc:`performance_reports`.


.. _cluster-analytics:

Cluster-level analytics
-----------------------

In addition to account-level statistics, Coiled collects usage data for individual clusters.
This allows you to view the activity on a given cluster in your account,
including timing data, cost, and profiling information.

An individual cluster analytics page can be accessed by clicking through from the
:ref:`cluster-listing`.


Cluster Statistics
^^^^^^^^^^^^^^^^^^

The cluster statistics panel shows some high-level metrics for the given cluster
including total time, memory processed, and tasks executed, and tasks errored.

.. figure:: images/cluster-statistics.png


Task Prefixes
^^^^^^^^^^^^^

Tasks that are executed on Dask clusters are given names,
and the prefix of these names are typically descriptive of what kind of
operation that the task is performing (e.g., ``read_csv`` or ``groupby``).

The task prefix panel shows a histogram of the most common task prefixes
for your cluster, allowing you to view at-a-glance the kinds of operations
that a given cluster is performing.

.. figure:: images/task-prefixes.png


Computations
^^^^^^^^^^^^

A single ``perisist``, ``compute`` or ``submit`` call to a Dask cluster
is considered a "computation", and each computation is comprised of a number
of "task groups", which are related sets of tasks that are executed
(e.g., ``read_parquet-abc`` or ``shuffle-123``).

Coiled shows you information about specific computations in the `Computations`
listing, including the total number of tasks, timing information, whether any tasks errored,
You can click to expand a given computation to show more information:

**Code snippet**
    The code snippet that launched the computation.
**Task group graph**
    A graph showing the task groups that were executed in the computation and their
    dependencies.

    The arrows point from dependency to dependent, and the nodes
    show information about a specific task group. The size of each node scales with
    the amount of memory consumed by a task group. The background colors show whether
    the task group duration was dominated by compute, transfer, disk I/O, or deserialization
    (using the same color scheme as the `Dask Task Stream <https://distributed.dask.org/en/latest/diagnosing-performance.html#task-start-and-stop-times>`_).
    If tasks within the task group fail, the node is drawn with a red border.


Cluster Profiling
^^^^^^^^^^^^^^^^^

Dask includes a statistical profiler to help you identify bottlenecks and hot code paths
in your data analysis workflows. Coiled automatically ingests profiling data from your
Coiled clusters and renders it as a flame graph.

You can zoom in on various regions of interest in the flame graph to see what your
computations are doing, and how often different code paths are run. Click the
"Reset Zoom" button to reset the state of the flame graph.

.. figure:: images/cluster-profile.png
