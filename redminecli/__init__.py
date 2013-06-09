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
__author__ = "Remi Ferrand <remi.ferrand__at__cc.in2p3.fr>"
__version__ =' 1.0'
__all__ = []

import os
import shelve

class ProjectListCache(object):

    def __init__(this, cache_file):
        
        this._shelve = None

        if cache_file is None:
            cache_file = "~/.redminecli/projects.cache"

        this.cache_file = os.path.expanduser(cache_file)

        this._mkdir()
        this._open()

    def _mkdir(this):
        d = os.path.dirname(this.cache_file)
        if not os.path.exists(d):
            os.mkdir(d, 0750)

    def _open(this):
        this._shelve = shelve.open(this.cache_file, flag = 'c')

    def flush(this):
        if os.path.exists(this.cache_file):
            this.close()
            os.unlink(this.cache_file)
            this._open()


    def set(this, key, value):
        this._shelve[key] = value

    def get(this, key):
        return this._shelve[key]

    def has_key(this, key):
        return this._shelve.has_key(key)

    def keys(this):
        return this._shelve.keys()
        
    def close(this):
        this._shelve.close()
