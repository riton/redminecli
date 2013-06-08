
import redminecli
from redminecli import utils, ProjectListCache

def _get_cache(args):
    return ProjectListCache(cache_file = args.cache_file)

@utils.arg('--create',
    dest = 'operation',
    action = 'store_const',
    const = 'create',
    help = 'Build project list cache'
)
@utils.arg('--flush',
    dest = 'operation',
    action = 'store_const',
    const = 'flush',
    help = 'Flush project list cache'
)
@utils.arg('--dump',
    dest = 'operation',
    action = 'store_const',
    const = 'dump',
    help = 'Dump project list cache'
)
def do_project_cache(cli, args):
    cache = _get_cache(args)
    f_name = '_do_project_cache_%s' % str(args.operation)
    callback = getattr(redminecli.shell, f_name)
    callback(cli, cache, args)

def _do_project_cache_flush(cli, cache, args):
    cache.flush()
    return 0
    

def _do_project_cache_dump(cli, cache, args):
    keys = [int(a) for a in cache.keys()]
    keys.sort()
    for id in keys:
        print "[%s] %s" % (str(id), str(cache.get(str(id))))

def _do_project_cache_create(cli, cache, args):
    projects = cli.projects
    cache.flush()

    #print dir(projects['kerberos'])

    #return 0

    p = []

    for project in projects:
        #cache.set(str(project.id), project.name)
        p.append(project)

    print len(p)
        
    return 0
