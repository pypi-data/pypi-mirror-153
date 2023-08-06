Usage
=====

Once you have a running noclouddotnet; you need to configure your consumer
Linux physical/virtual machines to come under your cloud-init regime.

To do this permanently; you should edit ``/etc/default/grub`` and the
``GRUB_CMDLINE_LINUX`` should include
``ds=nocloud-net;s=<nocloudnet ip>:<nocloudnet port>``

You will then need to run the following:

.. code-block::
   :caption: regenerate grub

   grub2-mkconfig


You may also do one-off cloud-inits by editing the boot loader line via the
grub menu on machine startup.

To close the loop; making your system secure; you would bake the grub
configuration into your machine image and password protect your grub/boot
configuration:

.. code-block::
   :caption: secure grub

   grub2-setpassword
   vi /boot/grub2/user.cfg
   grub2-mkconfig


Instance Data
*************

It is perhaps beyond the scope of this document to discuss how you deploy a
custom ``/etc/cloud/cloud.cfg`` and any scripts into ``/var/lib/cloud`` that
is a task for the tool(s) you use to create machine images; and/or
orchestrate/configure your machines.

Your metaserver does, however, support serving `instance metadata
<https://cloudinit.readthedocs.io/en/latest/topics/instancedata.html>`_.
Instance (and vendor) data may be prepared/bundled into files as per
`cloud-init formats
<https://cloudinit.readthedocs.io/en/latest/topics/format.html>`_ using
cloud-init tools (or otherwise) and may be deployed by placing them in the
configured paths for ``VENDOR_DATA``, ``USER_DATA``


Phone home
**********

Cloud-init has a `phone home <https://cloudinit.readthedocs.io/en/latest/topics/modules.html#phone-home>`_ module which you can configure to point to your nocloud.net server to capture the data publishable by this mechanism.

