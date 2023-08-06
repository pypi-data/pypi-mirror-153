Sym Python SDK
================

`Sym <https://symops.com/>`_ is the security workflow platform made for engineers, by engineers.

We solve the intent-to-execution gap between policies and workflows by providing fast-moving engineering teams with the just-right primitives to roll out best-practice controls.

This is the Python SDK for Sym.
For guides and other help, check out our `main docs site <https://docs.symops.com/>`_.

The SDK docs are broken into several core modules, which are described below.
Click on one to see the classes and functions available in your `Handlers <https://docs.symops.com/docs/handlers>`_.

The Sym SDK is used to customize workflow templates that are exposed by our `Terraform provider <https://docs.symops.com/docs/terraform-provider>`_. Here's an example using the ``sym:approve`` Template!

.. code-block:: python

   from sym.sdk.annotations import reducer
   from sym.sdk.integrations import pagerduty, okta, slack

   @reducer
   def get_approvers(evt):
      # The import here uses credentials defined in an Integration in Terraform
      if pagerduty.is_on_call(evt.user, schedule="id_of_eng_on_call"):
         # This is a self-approval in a DM
         return slack.user(evt.user)

      if evt.payload.fields["urgency"] == "Emergency":
         # This is a self-approval in a channel
         return slack.channel("#break-glass", allow_self=True)

      on_call_mgrs = okta.group("OnCallManagers").members()
      # This would cause each on-call manager to be DMed
      return slack.group([slack.user(x) for x in on_call_mgrs])

If you're interested in using Sym, please `reach out <https://symops.com/sales>`_!
