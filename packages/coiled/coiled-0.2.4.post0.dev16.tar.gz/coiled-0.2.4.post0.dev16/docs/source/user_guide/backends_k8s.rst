Kubernetes Backend
==================

.. note::

    Kubernetes support is currently experimental with new features under active
    development.

.. note::
    Software environments are not yet fully supported and we recommend building
    your own Docker images for the moment.

You can have Coiled launch computations on a Kubernetes cluster that you
control. This is a good way to run Coiled on other cloud providers or on-prem
infrastructure. In this situation you provide Coiled a
`Kubernetes configuration <https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/>`_,
or ``kubeconfig``, file that grants access to a particular namespace in a
Kubernetes cluster (the following two sections discuss how to generate this
``kubeconfig`` file). The ``kubeconfig`` file and namespace can then be added to
the "Cloud Backend Options" section of the Account page of your Coiled account.
Once this is done, any clusters you create with Coiled will be launched in your
Kubernetes cluster.

.. tip::

    Once a Coiled cluster is up and running, any issues normally captured by
    Dask's logging system will be available as usual. However, Coiled does not
    collect logs related to Kubernetes resources failing to launch on your k8s
    cluster (e.g. a pod which launches a Dask worker doesn't run successfully).
    The most common example of this is if a Kubernetes cluster does not have
    sufficient resources to start the pods you request.


Local authentication
""""""""""""""""""""

Cloud providers (e.g. Google Kubernetes Engine) offer
a way, through their command line interfaces (e.g. ``gcloud``, ``az``), to
generate a local ``kubeconfig`` file which is used to authenticate your machine.

Below you'll find information on how to authenticate your local machine for GKE

.. tabbed:: GKE
   :selected:

    To generate a Kubernetes configuration file with the ``gcloud`` CLI for GKE:

    .. code-block:: bash

        gcloud container clusters get-credentials <cluster-name>

    For more information, see the
    `GKE documentation <https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl>`_.

    .. note::

        ``gcloud`` will generate a ``kubeconfig`` file with short-lived,
        temporary credentials. In order to give Coiled sustained access to your
        cluster, you must also follow the step in the
        :ref:`next section <create-kubeconfig>` which generates a ``kubeconfig``
        file with long-lived credentials.

.. _create-kubeconfig:

Configure restricted access (optional)
""""""""""""""""""""""""""""""""""""""

The configuration file cloud providers generate often grant admin access to your
full Kubernetes cluster. This level of access is not required to run Coiled on
your cluster so we recommend restricting the permissions given to Coiled.

To accommodate this, Coiled provides a ``coiled create-kubeconfig`` command line
interface to generate a separate ``kubeconfig`` file with restricted access to
your cluster. Running:

.. code-block:: bash

    $ coiled create-kubeconfig

locally will create a new ``kubeconfig`` file in the current working directory
which grants minimal access to a single ``coiled`` namespace within the cluster.

Note that using ``coiled create-kubeconfig`` requires you to have ``kubectl``
`installed <https://kubernetes.io/docs/tasks/tools/install-kubectl/>`_ locally,
and to have `sufficient permissions
<https://kubernetes.io/docs/reference/access-authn-authz/rbac/#rolebinding-and-clusterrolebinding>`__ (e.g. in Google Cloud this requires the ``roles/container.admin`` or ``roles/container.clusterAdmin``
IAM roles)
