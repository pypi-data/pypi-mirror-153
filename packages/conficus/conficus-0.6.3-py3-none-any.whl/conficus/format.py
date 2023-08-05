def _format_value(key, value):
    name = key.split(".")[-1]
    if any([pw in name for pw in ("password", "passwd", "pwd", "secret", "salt")]):
        return "**********"
    return str(value)


def _format_sequence(sequence):
    start, end = "[]" if isinstance(sequence, list) else "()"
    _list = [str(v) for v in sequence]

    _short_list = ", ".join(_list)

    if len(_short_list) + 2 < 80:
        return start + _short_list + end

    _long_list = ["    " + str(v) for v in _list]

    return start + "\n" + "\n".join(_long_list) + end


def formatter(cdict, output=None):
    if not output:
        output = []

    for _, key, value in cdict.walk(full_key=True):
        if not isinstance(value, (dict, list, tuple)):
            _value = _format_value(key, value)
            _output = "[config] {}: {}".format(key, _value)
            output.append(_output)
        elif isinstance(value, (list, tuple)):
            _output = "[config] {}: {}".format(key, _format_sequence(value))
            output.append(_output)
    return "\n".join(output)
