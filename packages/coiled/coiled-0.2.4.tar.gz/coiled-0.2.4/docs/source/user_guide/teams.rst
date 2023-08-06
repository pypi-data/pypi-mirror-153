:notoc:

=====
Teams
=====

Coiled helps individuals and teams manage their resources, control costs, and
collaborate with one another. Team members within an account can create software
environments, etc. within that account to easily share
resources and consolidate billing.

Accounts & Teams
----------------

`Upon signing up for Coiled <https://cloud.coiled.io/signup>`_, an account is
automatically created for your user, and the name of the account is the same as
your username. For example, if you sign up with the username ``awesome-dev``,
then we create an account for you named ``awesome-dev``.

If you want to work with a team of two or more users as part of Coiled
Pay As You Go or Coiled Enterprise, you can either:

1. Add other Coiled users to your existing account by using the Team page at
   https://cloud.coiled.io/<YOUR-ACCOUNT-NAME>/team

2. Reach out to us at support@coiled.io to create an additional account to use
   for your team such as https://cloud.coiled.io/<YOUR-COMPANY-NAME>/team

Taking the screenshot below as an example, note that this user Kris (seen in the
avatar on the top right) is viewing the Team page of the Coiled account (seen in
the dropdown on the left).

.. figure:: images/team-management.png

Working with other accounts
---------------------------

If you are a team member of another account, you can create clusters or any
other resources in the other account by using the ``account=`` keyword argument
that most of our :doc:`API commands <api>` accept, or by specifying
``my-team-account-name/`` as a prefix in the ``name=`` keyword argument.

For example, to create a cluster in the other account:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(n_workers=10, account="my-team-account-name")

Or, to create a software environment in the other account:

.. code-block:: python

   import coiled

   coiled.create_software_environment(
       name="my-team-account-name/my-pip-env",
       pip=["dask[complete]", "xarray==0.15.1", "numba"],
   )

You can also configure a different account to act as your default account via
your :doc:`local coiled configuration file <configuration>`.


Sharing
-------

Software environments which belong to an account are
visible and accessible to all account members. This allows team members to
easily control, share, and collaborate on their teams's resources.


Resource limits & tracking costs
--------------------------------

Administrators for each Coiled account can set resource limits for account
members like the number of cores a user can allocate at one time or whether or
not to grant access to GPUs (which can be expensive). Additionally, you can
track each cluster's cost over time.

.. figure:: images/clusters-table.png
