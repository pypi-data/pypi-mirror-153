django-huey-email-backend
=========================

A simple Django email backend which uses Huey.

Usage
-----

Add the app to your settings:

.. code-block:: python

    # settings.py

    INSTALLED_APPS = [
        ...
        "huey.contrib.djhuey",
        "hueymail",
        ...
    ]


and use it as your email backend:

.. code-block:: python

    # settings.py

    EMAIL_BACKEND = 'hueymail.backends.EmailBackend'


Last, choose which email backend Huey should dispatch to via the ``HUEY_EMAIL_BACKEND``
setting:

.. code-block:: python

    # settings.py

    HUEY_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


How it works
------------

What happens when you send an email?
Basically this:

- Django creates a new instance of ``hueymail.backends.EmailBackend``, and calls its
  ``send_messages()`` method with the email messages it wants to send.

- The ``send_messages()`` method of the ``hueymail.backends.EmailBackend`` instance
  dispatches a Huey task called ``dispatch_messages()``, which is responsible for
  sending those messages.

- The ``dispatch_messages()`` task creates an instance of ``HUEY_EMAIL_BACKEND`` and
  calls its ``send_messages()`` method with the original email messages.


License
-------

Copyright (c) 2022 Christopher McDonald

Distributed under the terms of the
`MIT <https://github.com/chris-mcdo/django-overcomingbias-pages/blob/main/LICENSE>`_
license.
