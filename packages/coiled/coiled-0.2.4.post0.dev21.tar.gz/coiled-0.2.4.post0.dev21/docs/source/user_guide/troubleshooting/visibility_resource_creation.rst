.. _visibility_resource_creation:

===============================
Visibility on resource creation
===============================

It can be hard to debug some resource creation processes. VPC creation is one
of those processes that might fail due to various reasons, having some visibility
to this process can help when trying to understand why something might have
failed.

Coiled implemented the :meth:`coiled.get_notifications` method to help you
see the steps that run so far and any success/failure notifications.

If you encounter any problems when setting a VPC in your account, you can
contact support@coiled.io and supply the output of ``coiled.get_notifications()``.
To make it easy to share these notifications with our team, you can use the
``json=`` keyword argument.

.. code:: python

    import coiled

    coiled.get_notifications(json=True)
