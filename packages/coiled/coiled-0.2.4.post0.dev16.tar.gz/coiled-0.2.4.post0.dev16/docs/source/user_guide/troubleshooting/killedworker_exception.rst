.. _killedworker_exception:

======================
KilledWorker Exception
======================

This article aims to help you diagnose and understand a bit better what the ``KilledWorker`` exception means. 
To get us started, let's first show you how you can diagnose this error, then I will explain briefly why 
this error can happen and finally, how you might mitigate against it.

Diagnose the error
------------------

The best way to understand what went wrong is to check the worker logs. You might find a traceback with 
some exception or some other information about what happened with that worker.

You can head over to your dashboard and click the 'View logs' button on Coiled's affected cluster. 
You can see both the scheduler and workers' logs, open a worker log, and scroll down to see the last 
thing logged in that worker.

On Dask, logs will use **standard error** by default, which means that if you are using Dask, you need 
to check your terminal for any information as to what happened.

Example
^^^^^^^

Once I forgot to add the ``s3fs`` dependency when creating a software environment. I opened a notebook 
and started working through an example. All worked fine until I tried to run ``df.head()`` and got the 
following error:

.. code-block::

    KilledWorker: ("('read-csv-c075100a8373a0cab23cd3671871aeb7', 470)", <Worker 'tls://10.2.1.52:44429', name: fabiorosado-3880-worker-5-afdae8, memory: 0, processing: 179>)


Heading over to my Coiled dashboard to check the cluster logs, I have noticed that I was missing 
the ``s3fs`` dependency from the exception there.

.. code-block::

    ModuleNotFoundError: No module named 's3fs'


Understanding the error
-----------------------

We have already seen a possible cause of this error, but there are many other reasons why we might 
get a ``KilledWorker`` exception:

* Caused by a segmentation fault
* Too much memory allocated to the worker
* Using a library that is not threadsafe
* The worker died unexpectedly

When a Task dies on a worker, it might be sent to a different worker. If the same tasks kill that 
worker, then Dask decides to blame the task itself. This behaviour is a way to protect the cluster
against tasks that kill workers (like throwing a memory error, for example.)

Because there are various reasons you might get this ``KilledWorker`` exception, it's important to 
reiterate that checking the logs is the best way to gather information and figure out why something 
went wrong.

Mitigate the error
------------------

When it comes to mitigating an exception such as this, it's hard to point to specific things, because
there are many reasons why you might get this error. A few things that I can suggest is to:

- Increase the number of allowed failures before a worker is killed
- Make sure you allocate the right memory to your workers
- Watch the diagnostic dashboard for memory spikes (only possible while the worker is active)
- Make sure you are running the same package version on your client and worker.

Increase the number of allowed failures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When creating a cluster with coiled, you can use the `scheduler_options` keyword to increase the number 
of allowed failures. For example:

.. code-block:: python

    cluster = coiled.Cluster(scheduler_options={"allowed_failures": 4})


**Reference:** :meth:`coiled.Cluster`

On dask, you can use the config key ``distributed.scheduler.allowed-failures`` to change the number of 
allowed failures. You can also edit the file ``~/.config/dask/distributed.yaml`` and find the line 
``allowed-failures``.


Allocate the correct memory to your workers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With coiled, you can choose how much memory your workers should have when you create your cluster. 
If you don't want to decide, we will allocate 8 GiB by default per worker.

You can allocate more memory to your workers with the keyword ``worker_memory`` that you can pass to
both ``coiled.Cluster``. For example:

.. code-block:: python

    cluster = coiled.Cluster(worker_memory="16GiB")


Use the same dependencies versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the coiled CLI, you can run the command ``coiled install <software environment name>`` to create 
a new conda environment with the same dependencies and versions we used when creating your software 
environment.

Doing this will also help fix the version mismatch between the client and the scheduler/workers
running in the cluster. 

Note that the above command creates a new conda environment, so you will need to activate it before 
starting your work on your cluster.
