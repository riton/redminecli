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

@utils.arg('project_id',
    metavar = '<project_id>',
    help = 'Project identifier to retrieve issues for (not the numerical one)'
)
def do_issue_list(cli, args):

    project = _find_project(cli, args.project_id)

    # TODO(remi)
    # Handle None case

    issues_o = project.issues

    issues = []

    for issue in issues_o:
        h = {}
        for attr in ('id', 'priority', 'category', 'status', 'subject'):
            h[attr] = unicode(getattr(issue, attr, '') or '')
        for attr in ('author', ):
            user = getattr(issue, attr, None)
            if not user:
                h[attr] = ''
            else:
                user.refresh()
                h[attr] = '%s %s' % (user.firstname, user.lastname)
        issues.append(h)

    _get_printer('print_issue_list', args)(issues, args)


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
        h[attr] = unicode(getattr(issue, attr, '') or '')

    for attr in ('assigned_to', 'author'):
        user = getattr(issue, attr, None)
        if user is None:
            h[attr] = ''
        else:
            user.refresh()
            h[attr] = '%s %s' % (user.firstname, user.lastname)

    _get_printer('print_issue_show', args)(h, args)

    journals = []
    if args.get_journal is True:
        journals = [_journal_to_dict(j) for j in issue.journals]
        if len(journals) > 0:
            _get_printer('print_issue_show_journals', args)(journals, args)


def _journal_to_dict(journal):
    j = {}

    for attr in ('user', ):
        user = getattr(journal, attr, None)
        if not user:
            j[attr] = ''
        else:
            user.refresh()
            j[attr] = '%s %s' % (user.firstname, user.lastname)

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
