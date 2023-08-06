Configure Your Cloud Provider
=============================

.. toctree::
   :maxdepth: 1
   :hidden:

   aws_configure
   gcp_configure

Coiled manages launching Dask clusters and creating software environments for
you. You can run Coiled on AWS or GCP in your own cloud provider account.
This allows you to make use of security/data access controls, compliance standards,
and promotional credits that you already have in place.

Coiled is only responsible for provisioning resources for
clusters you create. Once a Dask cluster is created, all computations,
data transfer, and client-to-scheduler communication occurs entirely
within your cloud provider account.

.. figure:: images/backend-external-aws-vm.png
   :width: 100%


.. panels::
   :card: border-0
   :container: container-lg pb-3
   :column: col-md-6 col-md-6 p-2
   :body: text-center border-0
   :header: text-center border-0 h4 bg-white
   :footer: border-0 bg-white

   Use Coiled with AWS
   ^^^^^^^^^^^^^^^^^^^

   .. figure:: images/logo-aws.png
      :width: 35%
      :alt: Use Coiled with Amazon Web Services (AWS)

   +++

   .. link-button:: aws_configure
      :type: ref
      :text: Configure your AWS account
      :classes: btn-full btn-block stretched-link

   ---


   Use Coiled with GCP
   ^^^^^^^^^^^^^^^^^^^

   .. figure:: images/logo-gcp.png
      :width: 100%
      :alt: Use Coiled with Google Cloud Platform (GCP)

   +++

   .. link-button:: gcp_configure
      :type: ref
      :text: Configure your GCP account
      :classes: btn-full btn-block stretched-link
