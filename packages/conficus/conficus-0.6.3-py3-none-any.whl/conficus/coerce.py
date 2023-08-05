import re
from decimal import Decimal
from pathlib import Path
from .structs import DoubleLinkedDict


def matcher(regex):
    """
    Wrapper around a regex that always returns the
    group dict if there is a match.

    This requires that all regex have named groups.

    """
    rx = re.compile(regex, re.I)

    # pylint: disable=inconsistent-return-statements
    def _matcher(line):
        if not isinstance(line, str):
            return
        m = rx.match(line)
        if m:
            return m.groupdict()

    return _matcher


WINDOWS_PATH_REGEX = r'^(?P<value>[a-z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*)$'
UNIX_PATH_REGEX = r"^(?P<value>(/[^\0/]*)*)$"


def coerce_path(value):
    return Path(value)


coerce_win_path = (matcher(WINDOWS_PATH_REGEX), coerce_path)
coerce_unx_path = (matcher(UNIX_PATH_REGEX), coerce_path)

coerce_str_to_decimal = (matcher(r"^(?P<value>\d+\.\d+)$"), Decimal)


def handle_custom_coercers(custom_coercers):
    if not custom_coercers:
        return
    for name, _coercer in custom_coercers:
        regex_str, converter = _coercer

        if "(?P<value>" not in regex_str:
            raise Exception(
                "Custom matcher regular expressions must contain a named group `<value>`."
            )

        if not callable(converter):
            raise Exception("Custom converter's must be callable.")

        yield name, (matcher(regex_str), converter)


def apply(config, **kwargs):  # pragma pylint: disable=redefined-builtin

    coercers = DoubleLinkedDict()

    if kwargs.get("pathlib", False) is True:
        coercers.append("win_path", coerce_win_path)
        coercers.append("unix_path", coerce_unx_path)

    if kwargs.get("decimal", False) is True:
        coercers.append("decimal", coerce_str_to_decimal)

    # # add any custom coercers
    for name, custom_coercer in handle_custom_coercers(kwargs.get("coercers")):
        if name in coercers:
            coercers.replace(name, custom_coercer)
        else:
            coercers.prepend(name, custom_coercer)

    for section, key, value in config.walk():
        for coercer in coercers:
            m, converter = coercer.content
            if m(value):
                new_value = converter(value)
                section[key] = new_value
                break

    return config
