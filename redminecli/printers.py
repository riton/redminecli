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
