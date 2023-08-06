====================================
Managing resources created by Coiled
====================================

When using Coiled in your AWS account, you might want to know if Coiled created a
resource. Most of the resources that Coiled creates in your AWS account will be
tagged, you can refer to the following this list of tags when searching for 
Coiled-related resources using the 
`AWS Resource Groups Tag Editor <https://docs.aws.amazon.com/ARG/latest/userguide/find-resources-to-tag.html>`_

.. dropdown:: Coiled Tag
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    - owner: coiled
    - Name: coiled-vm-network-network
    - Name: coiled-vm-network-priv-subnet
    - Name: coiled-vm-network-pub-subnet
    - Name: cloudbridge-inetgateway

If you use the AWS resource groups tag editor, make sure you select 
"All supported resource types" from the Resource types dropdown. This
tool will search for all the resources that share the same tag key. 

You can use ``Name`` as tag and type ``coiled`` in the value input to
get a list of all resources that have Coiled in their tags.

.. figure:: ../images/aws-tag-editor.png
    :width: 100%

Alternatively, you can use ``boto3`` library (AWS SDK for Python)
to search for a list of resources that were created by Coiled.

.. code:: python

  import boto3

  client = boto3.client("resourcegroupstaggingapi")
  response = client.get_resources(
      TagFilters=[
          {"Key": "owner", "Values": ["coiled"]},
          {
              "Key": "Name",
              "Values": [
                  "coiled-vm-network-network",
                  "coiled-vm-network-priv-subnet",
                  "coiled-vm-network-pub-subnet",
                  "cloudbridge-inetgateway",
              ],
          },
      ]
  )
  print(response)

If you get an empty list, you might need to use fewer tags on each request to ``get_resources``.
