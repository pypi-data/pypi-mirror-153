# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['conficus']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.11,<0.12']

setup_kwargs = {
    'name': 'conficus',
    'version': '0.6.3',
    'description': 'python INI configuration library',
    'long_description': 'Conficus v0.6.1 \n===================\n\nPython INI Configuration\n^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n|version-badge| |coverage-badge|\n\n``conficus`` is a python toml configuration wrapper.\nproviding some extra type coercions (e.g. str -> Path)\neasier access and section inheritance.\n\n``conficus`` python 3.6+.\n\n\nInstallation\n~~~~~~~~~~~~\n\nInstall ``conficus`` with pip.\n\n.. code:: bash\n\n        pip install conficus\n\nQuick Start\n~~~~~~~~~~~\n\nBasic usage\n...........\n\n.. code:: python\n\n    >>> \n    >>> import conficus\n    >>>\n\nConfigurations can be loaded directly from a string variable or read via file path string or Path object:\n\n.. code:: python\n\n    >>> config = conficus.load(\'/Users/mgemmill/config.ini\', toml=True)\n    >>>\n\n``conficus`` will also read a path from an environment variable:\n\n.. code:: python\n\n    >>> config = conficus.load(\'ENV_VAR_CONFIG_PATH\')\n    >>>\n\nEasier Selection\n................\n\nAccessing nested sections is made easier with chained selectors:\n\n.. code:: python\n\n    >>> # regular dictionary access:\n    ... \n    >>> config[\'app\'][\'debug\']\n    True\n    >>>\n    >>> # chained selector access:\n    ... \n    >>> config[\'app.debug\']\n    True\n\n\nInheritance\n...........\n\nInheritance pushes parent values down to any child section:\n\n.. code:: ini\n\n    # config.ini\n\n    [app]\n    debug = true\n\n    [email]\n    _inherit = 0\n    host = "smtp.mailhub.com"\n    port = 2525\n    sender = "emailerdude@mailhub.com"\n\n    [email.alert]\n    to = ["alert-handler@service.com"]\n    subject = "THIS IS AN ALERT"\n    body = "Alerting!"\n\nIt is turned on via the inheritance option:\n\n.. code:: python\n\n   >>> config = conficus.load("config.ini", inheritance=True)\n\nSub-sections will now contain parent values:\n\n.. code:: python\n\n   >>> alert_config = config["email.alert"]\n   >>> alert_config["host"]\n   >>> "smtp.mailhub.com"\n   >>> alert_config["subject"]\n   >>> "THIS IS AN ALERT"\n\nInheritence can be controled per section via the `_inherit` option. `_inherit = 0` will block the section\nfrom inheriting parent values. `_inherit = 1` would only allow inheritance from the sections immediate parent;\n`_inherit = 2` would allow both the immediate parent and grandparent inheritance.\n\n`_inherit` values are stripped from the resulting configuration dictionary.\n\nAdditional Conversion Options\n.............................\n\nIn addition to toml\'s standard type conversions, ``conficus`` has two builtin conversion options and\nalso allows for adding custom conversions.\n\nConversions only work with string values.\n\n**Path Conversions**\n\nThe ``pathlib`` option will convert any toml string value that looks like a path to a python pathlib.Path object:\n\n.. code:: python\n\n    >>> config = conficus.load("path = \'/home/user/.dir\'", pathlib=True)\n    >>> isinstance(config["path"], Path)\n    >>> True\n\n**Decimal Conversions**\n\n\nThe ``decimal`` option will convert any toml string value that matches ``\\d+\\.\\d+`` to a python Decimal object:\n\n.. code:: python\n\n    >>> config = conficus.load("number = \'12.22\'", decimal=True)\n    >>> isinstance(config["number"], Decimal)\n    >>> True\n\n\n.. |version-badge| image:: https://img.shields.io/badge/version-v0.6.1-green.svg\n.. |coverage-badge| image:: https://img.shields.io/badge/coverage-100%25-green.svg\n',
    'author': 'Mark Gemmill',
    'author_email': 'dev@markgemmill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mgemmill-pypi/conficus',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
