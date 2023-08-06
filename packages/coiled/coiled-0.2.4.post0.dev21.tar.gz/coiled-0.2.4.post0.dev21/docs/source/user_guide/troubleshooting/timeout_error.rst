.. _timeout-error:

=============
Timeout error
=============

A timed out error can have different reasons as to why it happened. Usually, the
manifestation of this error is by an ``IOError`` exception that Dask Distributed 
raises. The message usually contains information as to where the time out happened.

If you look at the logs, you should see this error message followed by a traceback.

.. code-block::

    distributed.worker - ERROR - Worker stream died during communication

It's important to attempt to diagnose this problem, perhaps you are transferring large
dependencies between workers, and you get a time out error. Or there might be a different
reason. 

Looking at the logs and the dask dashboard might give you valuable information about why 
this error happened.

Increasing the default timeout time
-----------------------------------

If you have a long-running task, you might need to increase the TCP comm connection 
timeout - the default timeout time is 10 seconds. 

In this example, we will increase the timeout time - to 60 seconds, but you might 
need to adapt it depending on your use case.

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(environ={"DASK_DISTRIBUTED__COMM_TIMEOUTS__CONNECT": "60s"})
