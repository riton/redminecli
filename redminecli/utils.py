
from redminecli import strutils
import textwrap
import prettytable

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

# Code base on https://github.com/openstack/python-novaclient/blob/master/novaclient/utils.py
def print_list(objs, fields, formatters={}, sortby_index=None):

    if sortby_index is None:
        sortby = None
    else:
        sortby = fields[sortby_index]
    pt = prettytable.PrettyTable([f for f in fields], caching=False)
    pt.align = 'l' 

    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                field_name = field.lower().replace(' ', '_')
                data = o.get(field_name, '')
                row.append(data)

        pt.add_row(row)

    s = None
    if sortby is not None:
        s = pt.get_string(sortby=sortby)
    else:
        s = pt.get_string()

    print strutils.safe_encode(s)

# Code base on https://github.com/openstack/python-novaclient/blob/master/novaclient/utils.py
def print_dict(d, dict_property="Property", wrap=0):
    pt = prettytable.PrettyTable([dict_property, 'Value'], caching=False)
    pt.align = 'l'
    for k, v in d.iteritems():
        # convert dict to str to check length
        if isinstance(v, dict):
            v = str(v)
        if wrap > 0:
            v = textwrap.fill(str(v), wrap)
        # if value has a newline, add in multiple rows
        # e.g. fault with stacktrace
        if v and isinstance(v, basestring) and r'\n' in v:
            lines = v.strip().split(r'\n')
            col1 = k
            for line in lines:
                pt.add_row([col1, line])
                col1 = ''
        else:
            pt.add_row([k, v])
    print strutils.safe_encode(pt.get_string())


