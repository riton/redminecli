
# Code based on https://github.com/openstack/python-novaclient/blob/master/novaclient/utils.py
def arg(*args, **kwargs):
    """Decorator for CLI args."""
    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func
    return _decorator


# Code based on https://github.com/openstack/python-novaclient/blob/master/novaclient/utils.py
def add_arg(f, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""

    if not hasattr(f, 'arguments'):
        f.arguments = []

    # NOTE(sirp): avoid dups that can occur when the module is shared across
    # tests.
    if (args, kwargs) not in f.arguments:
        # Because of the sematics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        f.arguments.insert(0, (args, kwargs))


# Code based on https://github.com/openstack/python-novaclient/blob/master/novaclient/utils.py
def bool_from_str(val):
    """Convert a string representation of a bool into a bool value"""

    if not val:
        return False
    try:
        return bool(int(val))
    except ValueError:
        if val.lower() in ['true', 'yes', 'y']:
            return True
        if val.lower() in ['false', 'no', 'n']:
            return False
        raise
