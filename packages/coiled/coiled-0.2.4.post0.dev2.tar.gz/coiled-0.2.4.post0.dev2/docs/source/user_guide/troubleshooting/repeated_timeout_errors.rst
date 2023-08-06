.. _cluser-timeout-errors:

===============================
Repeated cluster timeout errors
===============================

Problem
-------

Affected versions: Dask 2021.10.0

When creating or working with a Dask cluster in Coiled, you might see repeated
messages with ``asyncio.exceptions.TimeoutError`` or
``asyncio.exceptions.CancelledError`` in your Jupyter Notebooks or Python shell,
which will appear similar to the following errors:

.. code-block::

   tornado.application - ERROR - Exception in callback functools.partial(<bound
   method IOLoop._discard_future_result of <zmq.eventloop.ioloop.ZMQIOLoop object
   at 0x1334d13d0>>, <Task finished name='Task-337' coro=<Cluster._sync_cluster_info()
   done, defined at /Users/username/dev/distributed/distributed/deploy/cluster.py:104>
   exception=OSError('Timed out trying to connect to tls://54.212.201.147:8786 after 5 s')>)
   Traceback (most recent call last):
     File "/Users/username/dev/distributed/distributed/comm/tcp.py", line 398, in connect
       stream = await self.client.connect(
     File "/Users/username/dev/dask-playground/env/lib/python3.9/site-packages/tornado/tcpclient.py", line 288, in connect
       stream = await stream.start_tls(
   asyncio.exceptions.CancelledError

   During handling of the above exception, another exception occurred:

   Traceback (most recent call last):
     File "/Users/username/.pyenv/versions/3.9.1/lib/python3.9/asyncio/tasks.py", line 489, in wait_for
       fut.result()
   asyncio.exceptions.CancelledError

   The above exception was the direct cause of the following exception:

   Traceback (most recent call last):
     File "/Users/username/dev/distributed/distributed/comm/core.py", line 284, in connect
       comm = await asyncio.wait_for(
     File "/Users/username/.pyenv/versions/3.9.1/lib/python3.9/asyncio/tasks.py", line 491, in wait_for
       raise exceptions.TimeoutError() from exc
   asyncio.exceptions.TimeoutError

   The above exception was the direct cause of the following exception:

   Traceback (most recent call last):
     File "/Users/username/dev/dask-playground/env/lib/python3.9/site-packages/tornado/ioloop.py", line 741, in _run_callback
       ret = callback()
     File "/Users/username/dev/dask-playground/env/lib/python3.9/site-packages/tornado/ioloop.py", line 765, in _discard_future_result
       future.result()
     File "/Users/username/dev/distributed/distributed/deploy/cluster.py", line 105, in _sync_cluster_info
       await self.scheduler_comm.set_metadata(
     File "/Users/username/dev/distributed/distributed/core.py", line 785, in send_recv_from_rpc
       comm = await self.live_comm()
     File "/Users/username/dev/distributed/distributed/core.py", line 742, in live_comm
       comm = await connect(
     File "/Users/username/dev/distributed/distributed/comm/core.py", line 308, in connect
       raise OSError(
   OSError: Timed out trying to connect to tls://54.212.201.147:8786 after 5 s


The repeated error messages were caused when a periodic callback encountered an
intermittent network connectivity issue and resulted in a frequently repeating
error condition, as described in the following Dask
`issue <https://github.com/dask/distributed/issues/5472>`_ and
`resolution <https://github.com/dask/distributed/pull/5488>`_.

Solution
--------

Upgrading to Dask 2021.11.0 or a newer version will resolve this issue and stop
the repeated error messages. You can upgrade to the latest version of Dask on
your local machine by running the following command in a terminal:

.. code-block::

    pip install dask distributed --upgrade

or

.. code-block::

    conda update dask distributed -c conda-forge

If you are using any custom software environments in Coiled, you'll need to
update the version of Dask in those environments and rebuild them by running the
following command with the desired version of Dask (or, you can omit the version
specifier to use the latest version of Dask):

.. code-block:: python

   coiled.create_software_environment(
       name="my-pip-env",
       pip=["dask==2021.11.0", "distributed==2021.11.0"],
   )
