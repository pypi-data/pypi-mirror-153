:notoc:

===
FAQ
===

Usage
-----

.. dropdown:: Can I use Coiled to do machine learning, data science, etc.?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes! Coiled builds on the popular PyData ecosystem of tools, and Dask in
    particular. Refer to the following resources to learn more about what you
    can do with Dask and Python:

    - `Dask <https://dask.org>`_
    - `Dask Examples <https://examples.dask.org>`_
    - :doc:`Dask Examples on Coiled <examples>`

    You may also want to check out our `YouTube channel
    <https://youtube.com/c/Coiled>`_ for interviews with community members that
    are using Python at scale.


.. dropdown:: Does Coiled support Jupyter notebooks?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, you can use Coiled from anywhere that you can run Python, including a
    Jupyter Notebook on your laptop, a cloud-hosted Jupyter Notebook, or a
    multi-user JupyterHub instance.

    And if you're using JupyterLab, you can learn more about
    :doc:`some extensions <jupyter>` that we recommend trying to make JupyterLab
    even better when working with Coiled and Dask.


.. dropdown:: Can I use Coiled from Sagemaker, VS Code, PyCharm, etc.?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, in addition to using Coiled from Jupyter Notebooks, you can use Coiled
    from anywhere that you can run Python. Coiled is agnostic to any specific
    user environment, editor, or IDE.

    Coiled was built for the purpose of making it easy to work with remote Dask
    clusters from anywhere, and most of our users work with Jupyter Notebooks or
    their favorite Python IDE to work with Coiled and Dask.


.. dropdown:: Does Coiled support GPUs?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, however, access to GPU resources is not currently available when using
    the free tier in Coiled Cloud.

    For more information on using GPUs with Coiled Pay As You Go and Coiled
    Enterprise, refer to `coiled.io/pricing <https://coiled.io/pricing>`_ or
    reach out to us at sales@coiled.io.


.. dropdown:: Can I use a container registry other than DockerHub or ECR?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, you can use any Docker registry that supports the Docker Registry API
    V2. Get in touch with our support team at support@coiled.io if you encounter
    any issues.


Data
----

.. dropdown:: How do I access my data from Coiled?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When you run computations on Dask clusters managed by Coiled, you can access
    many different file formats using the typical approaches used by Dask,
    Python, and related libraries.

    -   `Tabular data <https://docs.dask.org/en/latest/dataframe-create.html>`_
    -   `Array data <https://docs.dask.org/en/latest/array-creation.html>`_
    -   `Text data <https://docs.dask.org/en/latest/bag-creation.html>`_

    Coiled can provision Dask clusters on different cloud providers. Therefore,
    large datasets should be stored on the cloud using services such as Amazon
    S3 to avoid large data transfer costs. Be sure to also consider which region
    you are running Coiled in compared to which region the data resides in.


.. dropdown:: Do I need to migrate my data to Coiled?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    No, Coiled does not store any of your data. Rather, your data can remain in
    its current location. Coiled manages computation and helps you load data
    from your existing data sources, process it, and write results to those same
    (or other) data sources.


.. dropdown:: Does Coiled collect logs from my cluster?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    If you have configured Coiled to run within your own cloud provider account
    on AWS or GCP, then Coiled doesn't collect or store cluster or server logs.
    In these cases, Coiled uses a token to access the logs in your account to
    display them from within the cluster dashboard.


.. dropdown:: Why does Coiled need permissions for my container registry?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled stores built software environments as Docker images in the container
    registry in your cloud provider account based on your pip/conda dependencies
    and uses these images when you create a cluster. Even if you don't plan to
    install any dependencies, Coiled still needs the permissions to access your
    container registries when creating container-only software environments.


Libraries
---------

.. dropdown:: How do I install libraries on my Coiled clusters?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled helps you manage software environments both on your local machine and
    on cloud providers. You can specify custom environments using pip or conda
    environment files with the :func:`coiled.create_software_environment` function
    and Coiled will manage building Docker images that can then be used as
    software environments in Dask clusters on the cloud.

    Refer to the documentation on :doc:`software_environment` for more
    information.


.. _why-local-software:


.. dropdown:: Why do I need a local software environment?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When performing distributed computations with Dask, you’ll create a
    :class:`distributed.Client` object which connects your local Python process
    (e.g., your laptop) to your remote Dask cluster (e.g., running on the
    cloud). The Dask ``Client`` is the user-facing entry point for submitting
    tasks to a Dask cluster. When using a ``Client`` to submit tasks to your
    cluster, Dask will package up and send data, functions, and other Python
    objects needed for your computations *from* your local Python process where
    your ``Client`` is running *to* your remote Dask cluster in order for them
    to be executed.

    This means that if you want to run a function on your Dask cluster, for
    example NumPy’s :func:`numpy.mean` function, then you must have NumPy
    installed in your local Python process so Dask can send the ``numpy.mean``
    function from your local Dask ``Client`` to the workers in your Dask
    cluster. For this reason, it’s recommended to have the same
    libraries/versions installed on both your local machine and on the remote
    workers in your cluster.

    Refer to the documentation on :doc:`software_environment` for more details
    on how to easily synchronize your local and remote software environments
    using Coiled.


.. _faq-version-mismatch:

.. dropdown:: Why do I get Version Mismatch warnings?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When running cloud computations from your local machine, we need to ensure
    some level of consistency between your local and remote environments. For
    example, your Python versions should match, and if you want to use a library
    like PyTorch or Pandas remotely, then you should probably also install it
    locally. When Coiled detects a mismatch, it will inform you with a warning.

    Matching versions can be challenging if handled manually. Fortunately,
    Coiled provides functionality to help build and maintain software
    environments that match across local and remote environments. Refer to the
    documentation on :doc:`software_environment_local` for more information.


Deployment
----------

.. dropdown:: Which cloud providers does Coiled support?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled currently supports running within our managed AWS environment or
    within your own AWS or GCP account. Refer to the documentation on
    :doc:`backends` for more information on backend configuration, supported
    regions, and GPUs.


.. dropdown:: Can Coiled provision resources in my own cloud account?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes! By default, Coiled creates Dask clusters in our managed AWS
    environment. However, for security or compliance reasons, you may prefer to
    have Coiled provision compute resources within your own AWS or GCP account.
    Refer to the documentation on :doc:`backends` for more information.


.. dropdown:: Can I run Coiled on-premises?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    If you want to use Coiled in your own private cloud account, Coiled can be
    configured to run within your own AWS or GCP account. Refer to the question
    "Can Coiled provision resources in my own cloud account?" above.

    If you want to run Coiled on your own machines in your own data center, we
    would love to hear from you. Please contact sales@coiled.io to start a
    conversation with us.


Availability
------------

.. dropdown:: How much does Coiled cost?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When using the free tier in Coiled Cloud, you will not be charged for any of
    the compute resources you use, however there is a limit of 100 concurrently
    running cores per user and a monthly quota/limit based on usage.

    For more information on pricing, Coiled Pro, and Coiled Enterprise, refer to
    `coiled.io/pricing <https://coiled.io/pricing>`_.


.. dropdown:: How do I invite colleagues, students, etc.?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    We're glad that you're enjoying Coiled and want to invite colleagues or
    students. Coiled is currently open access, so your colleagues can join on
    their own without any additional steps.

    If you want to work within a team account with a group of users from your
    organization, then you can send an e-mail to sales@coiled.io with a team
    name and we'll set you up as an administrator for your new team. Refer to
    the documentation on :doc:`teams` for more information.


Security
--------

.. dropdown:: Can I use Coiled to read private data on AWS?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes. If you create a Coiled cluster from an environment that has AWS
    credentials defined, then Coiled will generate a secure token from those
    credentials and forward it to your Dask workers. The Dask workers will have
    the same rights and permissions that you have by default.

    For additional control, Coiled can be deployed within your own AWS or GCP
    account where you can specify and manage IAM roles directly. Refer to the
    documentation on :doc:`security` for more information.


.. dropdown:: Are my computations and data secure?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled provides end-to-end network security by the use of both cloud
    networking policies and with SSL/TLS encryption. Coiled does not persist or
    store any of your data, data only resides in memory as long as you are
    performing computations.

    For additional control, Coiled can be deployed within your own AWS account
    where you can specify and manage data access controls directly. Refer to the
    documentation on :doc:`security` for more information.


Pricing
--------

.. dropdown:: How much does Coiled cost?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled pricing is usage-based and depends on the size of your Dask clusters,
    how much CPU/RAM/GPU the workers have, and how long your clusters are
    running. Refer to the `pricing details <https://coiled.io/pricing/>`_ page
    for more information.


.. dropdown:: What is a Coiled Credit?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    A Coiled Credit is a credit that can be used to pay for Coiled
    clusters/usage in your individual Coiled account or your shared Coiled team
    account. The list price for 1 Coiled credit is $0.06. You can also purchase
    Coiled Credits at volume/discounted rates. Refer to the
    `pricing details <https://coiled.io/pricing/>`_ page for more information.


.. dropdown:: What is the pricing if I run Coiled in my own cloud account?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    If you run Coiled in your own cloud account, then the pricing is 1 Coiled
    Credit ($0.06) per CPU-hour, and 5 Coiled Credits ($0.30) per GPU-hour,
    which accounts for the Coiled rate only. You'll also pay your cloud provider
    for instance and networking costs. Special instance types such as
    high-memory or special GPU instances might have higher rates. Refer to the
    `pricing details <https://coiled.io/pricing/>`_ page for more information.


.. dropdown:: What is the pricing if I use Coiled's managed cloud account?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    If you use Coiled's managed cloud account, then the pricing is 2 Coiled
    Credits ($0.12) per CPU-hour, and 10 Coiled Credits ($0.60) per GPU-hour,
    which accounts for the Coiled rate plus the cloud costs. You will not pay
    any cloud provider for additional instance and networking costs since you
    are using Coiled's managed cloud provider account. Special instance types
    such as high-memory or special GPU instances might have higher rates. Refer
    to the `pricing details <https://coiled.io/pricing/>`_ page for more
    information.


.. dropdown:: Do you offer discounts for long-term commitments on usage?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes! We offer Coiled Enterprise packages that include Coiled Credits at
    discounted rates, enterprise support, and office hours. Refer to the
    `pricing details <https://coiled.io/pricing/>`_ page for more information.


.. dropdown:: Can you show me some example pricing for Coiled clusters?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    **Example: Small cluster with Coiled in your own cloud provider account**

    If you are using a Coiled cluster with 10 workers (instance type
    ``t3.medium on AWS``), these instances have 2 vCPU and 4 GB RAM each.
    Accounting for the scheduler instance and 10 worker instances, the Coiled
    cost would be ``1 Coiled Credit x 11 instances x 2 CPU``, which is equal to
    ``$0.06 x 11 x 2``, for a total of **$1.32 per hour** while this cluster is
    running. In this case, you'll also pay your cloud provider for instance and
    networking costs.

    .. raw:: html

       <hr>

    **Example: Large cluster in Coiled's managed cloud provider account**

    If you are using a Coiled cluster with 200 workers (instance type
    ``t3.2xlarge on AWS``), these instances have 8 vCPU and 32 GB RAM each.
    Accounting for the scheduler instance and 200 worker instances, the Coiled
    cost would be ``$0.12 x 1 instance x 2 CPU`` for the scheduler CPU and
    ``$0.12 x 200 x 8`` for the worker CPU, for a total of **$192.24 per hour**
    while this cluster is running. In this case, you will not pay any cloud
    provider for additional instance and networking costs since you are using
    Coiled's managed cloud provider account.


    .. raw:: html

       <hr>

    **Example: GPU cluster with Coiled in your own cloud provider account**

    If you are using a Coiled cluster with 5 workers (instance type
    ``gd4n.xlarge on AWS``), these instances have 4 vCPU, 16 GB RAM, and 1 GPU
    each. Accounting for the scheduler instance and 5 worker instances, the
    Coiled cost would be ``$0.06 x 1 x 2`` for the scheduler CPU,
    ``$0.06 x 5 x 4`` for the worker CPU, and ``$0.30 x 5 x 1`` for the worker
    GPU, for a total of **$2.82 per hour** while this cluster is running. In
    this case, you'll also pay your cloud provider for instance and networking
    costs.


Connect with us
---------------

.. dropdown:: How can I submit a bug report, feature request, or other question?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    First, thank you! Your feedback is highly valuable and will help influence
    the future of Coiled.

    For **bug reports, feature requests, or other usability feedback**, we'd love to hear from
    you! Please `submit an issue <https://github.com/coiled/feedback/issues/new>`_.

    For **other questions**, please join our
    `Coiled Community Slack <https://join.slack.com/t/coiled-users/shared_invite/zt-hx1fnr7k-In~Q8ui3XkQfvQon0yN5WQ>`_
    where you can ask questions and interact with our engineers as well as the
    Coiled community.


.. dropdown:: How can I keep up with the latest news about Coiled?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    To stay up to date with Coiled, you can
    `subscribe to our newsletter <https://coiled.io>`_ and follow us on
    `Twitter <https://twitter.com/coiledhq>`_,
    `YouTube <https://youtube.com/c/Coiled>`_, and
    `LinkedIn <https://www.linkedin.com/company/coiled-computing/>`_.
