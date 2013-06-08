
from redminecli import utils

def print_project_list(objs, args):

    fields = ('identifier', 'id', 'name')

    utils.print_list(objs, fields, args = args)
    
def print_project_show(obj, args):
    
    o = {}
    #for f in ('id', 'description', 'identifier', 'name', 'created_on', 'updated_on'):
    for f in ('id', 'description', 'identifier', 'name'):
        o[f] = getattr(obj, f, '')

    utils.print_dict(o, args = args)
