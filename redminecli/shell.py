
import redminecli
from redminecli import utils, ProjectListCache
from redminecli import printers
# TMP
from redminecli import strutils


def _get_printer(name, args):
    """
    Get printer *name*.
    Return user_exit one or default one
    """
    printer = None
    user_exit = getattr(args, 'user_exit', None)
    if user_exit is None:
        printer = getattr(printers, name)
    else:
        printer = getattr(user_exit, name)

    return printer
 

def do_project_list(cli, args):
    """
    List all projects
    """

    projects_o = cli.projects

    projects = []
    for p in projects_o:
        projects.append({
            'id': p.id,
            'identifier': p.identifier,
            'name': p.name
        })

    # Sort by project_id
    projects.sort(cmp = lambda x,y: cmp(x['id'], y['id']))

    _get_printer('print_project_list', args)(projects, args)


@utils.arg('project_id',
    metavar = '<project_id>',
    help = 'Project identifier to show detail for (not the numerical one)'
)
def do_project_show(cli, args):
    """
    Get detail for a given project identifier
    """

    project = cli.projects[args.project_id]

    _get_printer('print_project_show', args)(project, args)

@utils.arg('--project-id',
    dest = 'project_id',
    metavar = '<project_id>',
    help = 'Project identifier to retrieve issues for (not the numerical one)'
)
def do_issue_list(cli, args):

    project = _find_project(cli, args.project_id)

    # TODO(remi)
    # Handle None case

    issues = project.issues
    issue = issues.get(4626, parms = {'include': 'journals'})
    return

    for issue in issues(include='journals'):
        return
    return

    print str(issue.journals)

    #issues.update(4626, notes = 'plop')

    #_get_printer('print_issue_list', args)(issues, args)


@utils.arg('issue_id',
    metavar = '<issue_id>',
    help = 'Show details for <issue_id>'
)
@utils.arg('--journal',
    dest = 'get_journal',
    action = 'store_true',
    default = False,
    help = 'Display issue journal'
)
def do_issue_show(cli, args):

    parms = {}

    issue = cli.issues[args.issue_id]

    h = {}
    for attr in ('category', 'created_on',
                 'description', 'done_ratio', 'due_date', 'estimated_hours',
                 'priority', 'project', 'spent_hours', 'start_date',
                 'status', 'subject'):
        h[attr] = getattr(issue, attr, '') or ''

    for attr in ('assigned_to', 'author'):
        user = getattr(issue, attr, None)
        if not user:
            continue
        user.refresh()
        h[attr] = user.mail

    _get_printer('print_issue_show', args)(h, args)

    journals = []
    if args.get_journal is True:
        journals = [_journal_to_dict(j) for j in issue.journals]
        _get_printer('print_issue_show_journals', args)(journals, args)


def _journal_to_dict(journal):
    j = {}

    for attr in ('user', ):
        user = getattr(journal, attr, None)
        if not user:
            continue
        user.refresh()
        j[attr] = user.mail

    for attr in ('notes', 'created_on', 'details', 'id'):
        j[attr] = getattr(journal, attr, '')
        
    return j


def _find_project(cli, project_id):
    """
    Find project by unique identifier
    """
    # TODO(remi)
    # Check everything
    return cli.projects[project_id]
