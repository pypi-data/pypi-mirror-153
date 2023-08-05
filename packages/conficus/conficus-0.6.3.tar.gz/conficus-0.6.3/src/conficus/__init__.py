# -*- coding: utf-8 -*-
from os import environ
from os import path
from pathlib import Path
import tomlkit
from . import coerce
from . import inherit
from .readonly import ReadOnlyDict
from .structs import ConfigDict

__version__ = "0.6.3"


def read_config(config_input):
    """
    read_config assumes `config_input` is one of the following in this
    order:

        1. a file path string.
        2. an environment variable name.
        3. a raw config string.

    """
    if isinstance(config_input, Path):
        config_input = config_input.read_text()

    if path.exists(config_input):
        config_input = Path(config_input).read_text()

    elif config_input in environ and path.exists(environ[config_input]):
        config_input = Path(environ[config_input]).read_text()

    return config_input.split("\n")


def load(config_path, **kwargs):
    """
    keyword arguments:

        inheritance=False
        readonly=True
        use_pathlib=False
        use_decimal=False
        coercers=None

    """

    use_pathlib = kwargs.get("use_pathlib", False) or kwargs.get("pathlib", False)
    use_decimal = kwargs.get("use_decimal", False) or kwargs.get("decimal", False)
    coercers = kwargs.get("coercers")

    config = ConfigDict(tomlkit.parse("\n".join(read_config(config_path))))

    config = coerce.apply(
        config, pathlib=use_pathlib, decimal=use_decimal, coercers=coercers
    )

    if kwargs.get("inheritance", False) is True:
        config = inherit.apply(config)

    if kwargs.get("readonly", True) is True:
        config = ReadOnlyDict(config)

    return config
