=============================
How to set threads per worker
=============================

By default, a Worker will use as many threads as your node has cores. This
allows the Worker to run many computations in parallel. But you might want
to limit the number of threads that the Worker can use. If you set the
number of threads to one, it will allow the Worker to run computations 
mostly synchronously.

If you want to set the number of threads that a Worker has access to, you can
do it by using the ``worker_options`` keyword argument from the
``coiled.Cluster`` constructor.

.. code:: python

    import coiled

    cluster = coiled.Cluster(worker_options={"nthreads": 1})
