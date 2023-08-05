Conficus v0.6.1 
===================

Python INI Configuration
^^^^^^^^^^^^^^^^^^^^^^^^


|version-badge| |coverage-badge|

``conficus`` is a python toml configuration wrapper.
providing some extra type coercions (e.g. str -> Path)
easier access and section inheritance.

``conficus`` python 3.6+.


Installation
~~~~~~~~~~~~

Install ``conficus`` with pip.

.. code:: bash

        pip install conficus

Quick Start
~~~~~~~~~~~

Basic usage
...........

.. code:: python

    >>> 
    >>> import conficus
    >>>

Configurations can be loaded directly from a string variable or read via file path string or Path object:

.. code:: python

    >>> config = conficus.load('/Users/mgemmill/config.ini', toml=True)
    >>>

``conficus`` will also read a path from an environment variable:

.. code:: python

    >>> config = conficus.load('ENV_VAR_CONFIG_PATH')
    >>>

Easier Selection
................

Accessing nested sections is made easier with chained selectors:

.. code:: python

    >>> # regular dictionary access:
    ... 
    >>> config['app']['debug']
    True
    >>>
    >>> # chained selector access:
    ... 
    >>> config['app.debug']
    True


Inheritance
...........

Inheritance pushes parent values down to any child section:

.. code:: ini

    # config.ini

    [app]
    debug = true

    [email]
    _inherit = 0
    host = "smtp.mailhub.com"
    port = 2525
    sender = "emailerdude@mailhub.com"

    [email.alert]
    to = ["alert-handler@service.com"]
    subject = "THIS IS AN ALERT"
    body = "Alerting!"

It is turned on via the inheritance option:

.. code:: python

   >>> config = conficus.load("config.ini", inheritance=True)

Sub-sections will now contain parent values:

.. code:: python

   >>> alert_config = config["email.alert"]
   >>> alert_config["host"]
   >>> "smtp.mailhub.com"
   >>> alert_config["subject"]
   >>> "THIS IS AN ALERT"

Inheritence can be controled per section via the `_inherit` option. `_inherit = 0` will block the section
from inheriting parent values. `_inherit = 1` would only allow inheritance from the sections immediate parent;
`_inherit = 2` would allow both the immediate parent and grandparent inheritance.

`_inherit` values are stripped from the resulting configuration dictionary.

Additional Conversion Options
.............................

In addition to toml's standard type conversions, ``conficus`` has two builtin conversion options and
also allows for adding custom conversions.

Conversions only work with string values.

**Path Conversions**

The ``pathlib`` option will convert any toml string value that looks like a path to a python pathlib.Path object:

.. code:: python

    >>> config = conficus.load("path = '/home/user/.dir'", pathlib=True)
    >>> isinstance(config["path"], Path)
    >>> True

**Decimal Conversions**


The ``decimal`` option will convert any toml string value that matches ``\d+\.\d+`` to a python Decimal object:

.. code:: python

    >>> config = conficus.load("number = '12.22'", decimal=True)
    >>> isinstance(config["number"], Decimal)
    >>> True


.. |version-badge| image:: https://img.shields.io/badge/version-v0.6.1-green.svg
.. |coverage-badge| image:: https://img.shields.io/badge/coverage-100%25-green.svg
