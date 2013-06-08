
import redminecli
from redminecli import utils, ProjectListCache
from redminecli import printers


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

    return str(_find_project(cli, args.project_id))

def _find_project(cli, project_id):
    return cli.projects[project_id]
