# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
# Copyright Remi Ferrand (2013)
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

import os
import re
import hashlib
import tempfile
import subprocess
import redminecli
from redminecli import utils, ProjectListCache
from redminecli import printers
# TMP
from redminecli import strutils

##
# Global vars
##

# User cache
__user_cache = {}

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
 

def do_projects_list(cli, args):
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
def do_issues_list(cli, args):

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
                user = _get_user(cli, user.id)
                h[attr] = '%s %s' % (user.firstname, user.lastname)
        issues.append(h)

    _get_printer('print_issue_list', args)(issues, args)


@utils.arg('--subject',
    dest = 'subject',
    help = 'Issue subject'
)
@utils.arg('--description',
    dest = 'description',
    help = 'Issue description'
)
@utils.arg('--tracker',
    dest = 'tracker_id',
    metavar = '<tracker_id>',
    help = 'Use tracker <tracker_id> for this issue'
)
@utils.arg('--priority',
    dest = 'priority_id',
    metavar = '<priority_id>',
    help = 'Use tracker <priority_id> for this issue'
)
@utils.arg('--category',
    dest = 'category_id',
    metavar = '<category_id>',
    help = 'Use category <category_id> for this issue'
)
@utils.arg('--parent',
    dest = 'parent_issue_id',
    metavar = '<parent_id>',
    help = 'Create issue as a child of issue <parent_id>'
)
@utils.arg('--assigned-to',
    dest = 'assigned_to_id',
    metavar = '<user_id>',
    help = 'Assign issue to <user_id>'
)
@utils.arg('-e', '--editor',
    dest = 'use_editor',
    default = False,
    action = 'store_true',
    help = 'Use $EDITOR to setup values'
)
@utils.arg('project_id',
    metavar = '<project_id>',
    help = 'Project ID the new issue belongs to'
)
def do_issue_create(cli, args):

    user_values = {}

    if args.use_editor:
        editor = os.getenv('EDITOR', 'vi')

        fh, f_path = _mkstemp()

        _setup_issue_file(  fh,
                            description = args.description,
                            subject = args.subject,
                            priority_id = args.priority_id,
                            assigned_to_id = args.assigned_to_id,
                            tracker_id = args.tracker_id,
                            category_id = args.category_id,
                            parent_issue_id = args.parent_issue_id
        )

        os.close(fh)

        md5_orig = _md5sum(f_path)

        # Spawn editor
        editor_cmd = [editor, f_path]
        rc = subprocess.call(editor_cmd, stdin = None, stdout = None, stderr = None, shell = False)

        md5_new = _md5sum(f_path)

        if (md5_orig == md5_new):
            answer = raw_input("File wasn't modified, do you want to commit this issue ? (y/n)")
            if (answer == 'n'):
                return

        # Parse issue file
        user_values = _parse_issue_file(f_path)

    else:
        user_values = {
            'description' : args.description,
            'subject' : args.subject,
            'priority_id' : args.priority_id,
            'assigned_to_id' : args.assigned_to_id,
            'tracker_id' : args.tracker_id,
            'category_id' : args.category_id,
            'parent_issue_id' : args.parent_issue_id
        }
   
    # Replace '' with None
    for k in user_values.keys():
        if user_values[k] == '':
            user_values[k] = None

    # Create the issue with user supplied data
    i = cli.projects[args.project_id].issues
    new_issue = i.new(**user_values)

    h = _issue_to_dict(cli, new_issue)
    _get_printer('print_issue_show', args)(h, args)


def _setup_issue_file(fh, **kwargs):
    """
    Setup issue file ready to be edited with $EDITOR
    """

    v = []
    for k in kwargs.keys():
        s = "<%s>\n" % str(k)
        if not kwargs[k] is None:
            s += "%s" % str(kwargs[k])
        s += "</%s>\n" % str(k)

        v.append(s)

    os.write(fh, "\n".join(v))


def _md5sum(file_path):
    """
    Compute the md5sum of a file
    """
    h = hashlib.md5()
    with open(file_path, 'r') as f:
        while True:
            # MD5 has 128 bytes digest blocks
            b = f.read(128)
            if len(b) == 0:
                break
            h.update(b)

    return h.hexdigest()

def _parse_issue_file(file_path):
    """
    Parse content of issue file after user has edited it
    """

    content = ""
    with open(file_path, "r") as f:
        content = "".join(f.readlines())

    a = re.findall("<(?P<key>.+?)>(?P<name>.+?)</(?P=key)>", content, re.DOTALL | re.MULTILINE)

    h = {}
    for key, value in a:
        h[key] = value.strip()

    return h



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

    h = _issue_to_dict(cli, issue)

    _get_printer('print_issue_show', args)(h, args)

    journals = []
    if args.get_journal is True:
        journals = [_journal_to_dict(cli, j) for j in issue.journals]
        if len(journals) > 0:
            _get_printer('print_issue_show_journals', args)(journals, args)

def do_trackers_list(cli, args):
    """
    List trackers
    """
    
    a = []
    for t in cli.trackers:
        a.append({
            'id'    : t.id,
            'name'  : t.name
        })

    a.sort(cmp = lambda x,y: 1 if int(x['id']) > int(y['id']) else -1)

    _get_printer('print_trackers_list', args)(a, args)


def _issue_to_dict(cli, issue):
    """
    Convert an issue object to a python dict ready for *printers*
    """
    h = {}
    for attr in ('id', 'category', 'created_on',
                 'description', 'done_ratio', 'due_date', 'estimated_hours',
                 'priority', 'project', 'spent_hours', 'start_date',
                 'status', 'subject'):
        h[attr] = unicode(getattr(issue, attr, '') or '').replace('\r', '')

    for attr in ('assigned_to', 'author'):
        user = getattr(issue, attr, None)
        if user is None:
            h[attr] = ''
        else:
            user = _get_user(cli, user.id)
            h[attr] = '%s %s' % (user.firstname, user.lastname)
   
    return h


def _journal_to_dict(cli, journal):
    j = {}

    for attr in ('user', ):
        user = getattr(journal, attr, None)
        if not user:
            j[attr] = ''
        else:
            user = _get_user(cli, user.id)
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

def _get_user(cli, user_id):
    global __user_cache

    key = '%s' % (user_id)
    if key in __user_cache:
        return __user_cache[key]

    user = cli.users[user_id]

    __user_cache[key] = user
    return user

def _mkstemp():
    return tempfile.mkstemp(suffix = '', prefix = 'redminecli_', dir = None, text = True)
