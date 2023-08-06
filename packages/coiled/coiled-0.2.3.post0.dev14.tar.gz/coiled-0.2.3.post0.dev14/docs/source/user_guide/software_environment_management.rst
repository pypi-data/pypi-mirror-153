.. _managing-software-environments:

==============================
Managing software environments
==============================

.. currentmodule:: coiled

Managing software environments involves four pieces of functionality: creating
new software environments, updating existing software environments, listing
available software environments, and deleting software environments.

Creating software environments is discussed in detail in the
:ref:`creating-software-environments` page. The other software management
operations are discussed here.


Updating software environments
------------------------------

You can update an existing software environment, for example to add a new conda
package, by calling ``coiled.create_software_environment`` with the name of the
software environment you want to update and the new specification for the
software environment.

If the inputs to ``coiled.create_software_environment`` have changed since the
last time it was called for a given software environment, the corresponding
software environment will be rebuilt using the new inputs and any future uses of
the software environment will use the updated version. Repeated calls to
``coiled.create_software_environment`` with the same inputs are a no-op.

You can't update the software environment being used on an already running
cluster. The cluster must first be closed and then restarted to use any updates
made to a software environment.


Listing software environments
-----------------------------

The :meth:`coiled.list_software_environments` function will list all available
software environments:

.. code-block:: python

    coiled.list_software_environments()

There is also a ``account=`` keyword argument which lets you specify the account
which you want to list software environments for.


Deleting software environments
------------------------------

The :meth:`coiled.delete_software_environment` function can be used to delete
individual software environments. For example:

.. code-block:: python

    coiled.delete_software_environment(name="alice/my-conda-env")

will delete the software environment named "my-conda-env" in the Coiled account
named "alice".
