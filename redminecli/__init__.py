
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
