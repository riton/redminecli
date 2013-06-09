# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
# Copyright or © or Copr. Remi Ferrand (2013)
# 
# Remi Ferrand <remi.ferrand_#at#_cc.in2p3.fr>
# 
# This software is a computer program whose purpose is to [describe
# functionalities and technical features of your software].
# 
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#

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

def _set_table_common_opt(pt, args):
    # Table max width
    if not args is None:
        if not args.table_max_width is None:
            if args.table_max_width > 0:
                pt.max_width = int(args.table_max_width)

    return pt

def _get_column_maxlen(args):
    if not args.column_max_len is None:
        return int(args.column_max_len)
    return 0

# Code based on https://github.com/openstack/python-novaclient/blob/master/novaclient/utils.py
def print_list(objs, fields, formatters={}, sortby_index=None, args = None):

    if sortby_index is None:
        sortby = None
    else:
        sortby = fields[sortby_index]

    wrap = _get_column_maxlen(args)

    pt = prettytable.PrettyTable([f for f in fields], caching=False)
    pt.align = 'l' 
    _set_table_common_opt(pt, args)

    data = None
    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                data = formatters[field](o)
                row.append(data)
            else:
                field_name = field.lower().replace(' ', '_')
                data = o.get(field_name, '')
                if wrap > 0:
                    data = textwrap.fill(unicode(data), wrap)
                row.append(data)

        pt.add_row(row)

    s = None
    if sortby is not None:
        s = pt.get_string(sortby=sortby)
    else:
        s = pt.get_string()

    print strutils.safe_encode(s)


# Code based on https://github.com/openstack/python-novaclient/blob/master/novaclient/utils.py
def print_dict(d, dict_property="Property", wrap=0, args = None, sort_f = None):
    pt = prettytable.PrettyTable([dict_property, 'Value'], caching=False)
    pt.align = 'l'
    _set_table_common_opt(pt, args)

    keys = None
    if sort_f is None:
        keys = d.keys()
    else:
        keys = sorted(d.keys(), cmp = sort_f)

    for k in keys:
        v = d[k]
        # convert dict to str to check length
        if isinstance(v, dict):
            v = unicode(v)
        if wrap > 0:
            v = textwrap.fill(unicode(v), wrap)
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


