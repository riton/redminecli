
from redminecli import utils

def print_project_list(objs, sortby_index = None):

    fields = ('identifier', 'id', 'name')

    utils.print_list(objs, fields, sortby_index = sortby_index)
    
def print_project_show(obj):
    
    o = {}
    #for f in ('id', 'description', 'identifier', 'name', 'created_on', 'updated_on'):
    for f in ('id', 'description', 'identifier', 'name'):
        o[f] = getattr(obj, f, '')

    utils.print_dict(o)
