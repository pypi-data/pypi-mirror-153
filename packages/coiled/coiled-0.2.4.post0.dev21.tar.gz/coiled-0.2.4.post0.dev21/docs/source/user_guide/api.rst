=============
API Reference
=============

.. panels::
   :body: text-center

    :opticon:`file-code,size=24`

    .. link-button:: python-api
        :type: ref
        :text: Python API Reference
        :classes: btn-full btn-block stretched-link

    ---

    :opticon:`terminal,size=24`

    .. link-button:: command-line-api
        :type: ref
        :text: Command Line API Reference
        :classes: btn-full btn-block stretched-link


.. _python-api:

Python API Reference
====================

.. currentmodule:: coiled

.. autosummary::
   coiled.Cluster
   coiled.cluster_logs
   coiled.create_software_environment
   coiled.delete_cluster
   coiled.delete_software_environment
   coiled.diagnostics
   coiled.get_billing_activity
   coiled.get_notifications
   coiled.get_software_info
   coiled.install
   coiled.list_clusters
   coiled.list_core_usage
   coiled.list_gpu_types
   coiled.list_instance_types
   coiled.BackendOptions
   coiled.AWSOptions
   coiled.GCPOptions
   coiled.list_local_versions
   coiled.list_performance_reports
   coiled.list_software_environments
   coiled.list_user_information
   coiled.performance_report
   coiled.set_backend_options

Software Environments
---------------------
.. autofunction:: coiled.create_software_environment
.. autofunction:: coiled.delete_software_environment
.. autofunction:: coiled.get_software_info
.. autofunction:: coiled.inspect
.. autofunction:: coiled.install
.. autofunction:: coiled.list_software_environments


Clusters
--------
.. autoclass:: coiled.Cluster
   :members:
   :inherited-members: 
.. autofunction:: coiled.cluster_logs
.. autofunction:: coiled.delete_cluster
.. autofunction:: coiled.list_clusters
.. autofunction:: coiled.list_core_usage
.. autofunction:: coiled.list_gpu_types
.. autofunction:: coiled.list_instance_types
.. autoclass:: coiled.BackendOptions
.. autoclass:: coiled.AWSOptions
.. autoclass:: coiled.GCPOptions
.. autoclass:: coiled.FirewallOptions



Performance Reports
-------------------
.. autofunction:: coiled.list_performance_reports
.. autofunction:: coiled.performance_report


Backend
-------
.. autofunction:: coiled.set_backend_options


Information
-----------
.. autofunction:: coiled.diagnostics
.. autofunction:: coiled.get_billing_activity
.. autofunction:: coiled.get_notifications
.. autofunction:: coiled.list_local_versions
.. autofunction:: coiled.list_user_information


.. _command-line-api:

Command Line API Reference
==========================

.. click:: coiled.cli.login:login
   :prog: coiled login
   :show-nested:

.. _coiled-install-api:

.. click:: coiled.cli.install:install
   :prog: coiled install
   :show-nested:

.. click:: coiled.cli.env:create
   :prog: coiled env create
   :show-nested:

.. click:: coiled.cli.env:delete
   :prog: coiled env delete
   :show-nested:

.. click:: coiled.cli.env:list
   :prog: coiled env list
   :show-nested:

.. click:: coiled.cli.env:inspect
   :prog: coiled env inspect
   :show-nested:
