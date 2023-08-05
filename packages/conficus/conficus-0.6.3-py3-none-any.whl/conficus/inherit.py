from copy import deepcopy
from .structs import ConfigDict


def apply(config):  # noqa C901
    """
    ficus.inherit pushes the configuration values of
    parent section down to its child sections.

    This can be used as a way of simplifying config usage. For example:

    [email]
    server=smtp.location.com
    user=SMTPUSR
    password=CKrit
    from=smtp@location.com

    [email.notifications]
    _inherit=1
    to=[peter@boondoggle.ca, liz@boondoggle.ca]
    subject=The Subject of Notification
    body=notification_template.txt

    [email.errors]
    _inherit=1
    to=[errors@boondoggle.ca]
    subject=[Alert] Error
    body=error_template.txt

    """
    INHERIT_KEY = "_inherit"

    def _inherit(inheritable_options, current_section):
        # first inherit any options
        # that do not exist

        # collect all of the current options on the section
        # this does not include any inherited values
        section_options = {}
        for key, val in current_section.items():
            if not isinstance(val, ConfigDict) and key != "_inherit":
                section_options[key] = val

        # make a new copy of inheritenc levels
        _inheritable_options = deepcopy(inheritable_options)

        # determine the level instance of the current section's inheritence
        apply_inheritence = current_section.get(INHERIT_KEY, 99)
        if not isinstance(apply_inheritence, int):
            raise Exception("'_inherit' option must be an integer.")

        if INHERIT_KEY in current_section:
            current_section.pop(INHERIT_KEY)
        apply_inheritence = apply_inheritence * -1

        # get the last x inheritable sections
        if apply_inheritence == 0:
            _inheritables = []
        else:
            _inheritables = _inheritable_options[apply_inheritence:]

        # apply each level of inheritance to the current section
        for options in _inheritables:
            for key, val in options.items():
                if key not in current_section:
                    current_section[key] = val

        # add the current sections options to the inheritence levels
        _inheritable_options.append(section_options)

        # finally, push down the sections options
        # to all its sub-sections
        for key, child_section in current_section.items():
            if isinstance(child_section, ConfigDict):
                _inherit(_inheritable_options, child_section)

    _inherit([], config)

    return config
