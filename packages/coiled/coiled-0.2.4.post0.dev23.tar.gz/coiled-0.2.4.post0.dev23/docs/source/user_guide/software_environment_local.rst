========================================
Installing software environments locally
========================================

Motivation
==========

When performing distributed computation with Dask, you’ll create a
:class:`distributed.Client` object to connect your local Python process (e.g.
your laptop) to your remote Dask cluster (e.g. running on AWS). Dask ``Client``
s are the user-facing entry point for submitting tasks to a Dask cluster. When
using a ``Client`` to submit tasks to your cluster, Dask will package up and
send data, functions, and other Python objects needed for your computations
*from* your local Python process where your ``Client`` is running *to* your
remote Dask cluster in order for them to be executed.

This means that if you want to run a function on your Dask cluster, for example
NumPy’s :func:`numpy.mean` function, then you must have NumPy installed in your
local Python process so Dask can send the ``numpy.mean`` function from your
local Dask ``Client`` to the workers in your Dask cluster. For this, and other
reasons, you must have the same libraries installed on both your
local machine and on the remote workers in your cluster.

As such, Coiled software environments can be installed locally to have a
consistent set of libraries and versions between your local environment and the environment
your cluster is running in.


Install Coiled software environments locally
============================================

You can install a Coiled software environment locally using the
``coiled install`` command line tool. ``coiled install`` installs an existing
Coiled software environment on your machine as a local conda environment. For
example, to install the ``coiled/default`` software environment locally:

.. code-block:: bash

    # Create local version of the coiled/default software environment
    $ coiled install coiled/default
    $ conda activate coiled-coiled-default

The ``coiled/default`` name after ``coiled install`` specifies which Coiled
software environment to install locally. Generally Coiled software environments
are specified in the form of
"<coiled-account-name>/<software-environment-name>". So in the above example
we're telling ``coiled install`` to create the Coiled software environment named
"default" in the "coiled" account locally.

Note that currently ``coiled install`` requires conda to be installed locally
and does not support software environments with custom Docker images.

.. dropdown:: For windows users
    :container: mb-2 border-0
    :title: bg-white text-left h6 mb-3
    :body: bg-white mb-3
    :animate: fade-in

    If you try something like ``coiled install coiled/default`` 
    from a Windows command prompt it will only return a list of
    dependencies for the selected environment. It is 
    straightforward to use that dependency list to create a
    ``environment.yml`` file, and with that use ``conda env create -f 
    environment.yml`` to create the desired software environment.
    
See our :doc:`tutorial<tutorials/matching_coiled_senvs>` for more on how to do this.
