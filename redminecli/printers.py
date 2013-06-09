
import textwrap
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

def print_issue_list(objs, args):
    fields = objs[0].keys()
    utils.print_list(objs, fields, args = args)

def print_issue_show(objs, args):
    utils.print_dict(objs, args = args)

def print_issue_show_journals(objs, args):
    
    fields = objs[0].keys()

    #utils.print_list(objs, fields, args = args)
    for journal in objs:
        #utils.print_dict(journal, args = args)
        print_issue_show_journal(journal, args)

        print ""

def print_issue_show_journal(obj, args):
    max_len = 70
    if not args.column_max_len is None:
        max_len = int(args.column_max_len)

    utils.print_dict(obj, wrap = max_len, args = args, sort_f = _sort_notes_least)

def _sort_notes_least(x, y):
    if x == 'notes':
        return 1
    return -1
