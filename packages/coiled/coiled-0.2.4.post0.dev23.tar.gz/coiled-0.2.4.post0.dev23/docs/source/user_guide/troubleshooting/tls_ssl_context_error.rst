.. _tls_ssl_context_error:

===============================
TLS expects a ssl_context error
===============================

TLS errors might show up when a ``Client`` attempts to connect to a scheduler
that's using TLS but doesn't pass the required TLS information. Occasionally,
you might see this error if there are any version mismatches between your local
Dask version and the Dask version installed on Coiled's software environment.

.. code::

    TypeError: TLS expects a `ssl_context` argument of type ssl.SSLContext (perhaps check your TLS configuration?)  Instead got None

Check your versions
-------------------

The first step in trying to debug why you have seen this error, is to confirm
that you are running the same version locally and on Coiled. If you are using
conda to manage your environment, you can run the command
``coiled install <account>/<software environment name>`` in your terminal to 
create a new conda environment with the same dependencies and versions as the
ones installed on Coiled.

If you want to check the version of your local dependencies quickly, you can run
the following command on your ipython session:

.. code:: python

    import coiled

    coiled.list_local_versions()

If you see a version mismatch between Dask and Distributed, it's a good idea to update
your local versions as well. You can do this by running the command 
``pip install dask distributed --upgrade`` if you are using pip or by running the command
``conda update dask distributed`` if you are using conda.

Check the logs
--------------

It's always good to look at the scheduler and worker logs to see if we can gather
any useful information. If you see a failure to deserialize a task, this might
give you some idea as to why you got that final TLS error.


Check your code
---------------

If the issue wasn't a version mismatch and the log don't show any useful information. 
It's time to look at your code to see if something might be causing Dask to throw this
TLS error. A common occurrence is when we call ``.compute()`` inside a
``.map_partitions()``, it might be worth checking if your code might be doing this.

Note that even if calling compute inside a map partitions
isn't causing the error, this practice is discouraged as the code will run slow. There
might be different ways to do the computation that could be more performant.

Reach out for help
------------------

If you are still having issues with this TLS error and you need help, please reach
out to us by `opening a support ticket <https://support.coiled.io/hc/en-us/requests/new>`_ or by joining
our
`community on slack <https://join.slack.com/t/coiled-users/shared_invite/zt-hx1fnr7k-In~Q8ui3XkQfvQon0yN5WQ>`_
we are always happy to help.
