#!/usr/bin/python

import os
import sys
import argparse
import ConfigParser

sys.path.insert(0, "/home/rferrand/Sources/python/redmine/pyredminews")
import redmine

from redminecli import utils, ProjectListCache
import redminecli.projects
import redminecli.shell

api_key = "d85c410e6795b3cd08dacb7c875889e29d338d2c"

ENDPOINT = "https://forge.in2p3.fr"

options = None

# def _setup_client():
# 
#     client = redmine.Redmine(ENDPOINT, key = api_key)
#     return client

class RedmineCliShell(object):

    def __init__(this):
        this.subcommands = {}
        this.config = None

    def get_base_parser(this):
        parser = argparse.ArgumentParser(
            prog='redminecli',
            #description=__doc__.strip(),
            epilog='See "redminecli help COMMAND" '
                   'for help on a specific command.',
            add_help=False
        )

        parser.add_argument('-h', '--help',
            action='store_true',
            help=argparse.SUPPRESS
        )

        parser.add_argument('-c', '--config',
            dest='config_file',
            metavar='<config_file>',
            default = '~/.redminecli/config',
            help='Use <config_file> instead of ~/.redminecli/config'
        )

        parser.add_argument('--auth-url',
            dest='auth_url',
            metavar='<auth_url>',
            help='Use <auth_url> to interact with redmine API'
        )

        parser.add_argument('--cache-file',
            dest='cache_file',
            metavar='<file>',
            help='Use <file> to cache projects IDs'
        )

        return parser

    def get_subcommand_parser(this):
        parser = this.get_base_parser()
        subparsers = parser.add_subparsers(metavar = '<subcommand>')

        this._find_actions(subparsers, redminecli.shell)
        this._find_actions(subparsers, this)
        return parser

    def _find_actions(this, subparsers, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            # I prefer to be hypen-separated instead of underscores.
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            action_help = desc.strip().split('\n')[0]
            arguments = getattr(callback, 'arguments', [])

            subparser = subparsers.add_parser(command,
                help=action_help,
                description=desc,
                add_help=False
            )
            subparser.add_argument('-h', '--help',
                action='help',
                help=argparse.SUPPRESS,
            )
            this.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    def main(this, argv):
        
        parser = this.get_base_parser()
        (options, args) = parser.parse_known_args(argv)

        config = this.parse_config(options)

        subcommand_parser = this.get_subcommand_parser()
        this.parser = subcommand_parser

        if options.help or not argv:
            subcommand_parser.print_help()
            return 0

        api_key = os.getenv('REDCLI_API_KEY', None)
        if api_key is None:
            try:
                api_key = config.get('credentials', 'api_key')

            except ConfigParser.NoOptionError as e:
                print >>sys.stderr, "You need to specify your API key either via " \
                        "$REDCLI_API_KEY or in your configuration file"
                return 1

        auth_url = options.auth_url
        if auth_url is None:
            try:
                auth_url = config.get('global', 'auth_url')

            except ConfigParser.NoOptionError as e:
                print >>sys.stderr, "You need to specify your authentication url either via " \
                        "--auth-url or in your configuration file"
                return 2

        args = subcommand_parser.parse_args(argv)

        # Merge args from command line and config file
        this.merge_config_args(args)

        if args.func == this.do_help:
            this.do_help(args)
            return 0

        cli = redmine.Redmine(auth_url, key = api_key, debug = True, version = 2.1)

        return args.func(cli, args)


    def parse_config(this, args):
        config = ConfigParser.ConfigParser()
        config.read(os.path.expanduser(args.config_file))
        this.config = config

        return config

    def merge_config_args(this, args):
        config = this.config

        for attr in ('global/cache_file', ):
            section, opt_name = attr.split('/')

            if not getattr(args, opt_name, None) is None:
                continue

            v = None
            try:
                v = config.get(section, opt_name)

            except ConfigParser.NoOptionError:
                pass

            setattr(args, opt_name, v)

        

    @utils.arg('command', metavar='<subcommand>', nargs='?',
               help = 'Display help for <subcommand>')
    def do_help(this, args):
        """
        Display help about this program or one of its subcommands.
        """
        if args.command:
            if args.command in this.subcommands:
                this.subcommands[args.command].print_help()
            else:
                print >>sys.stderr, "'%s' is not a valid subcommand" % args.command
        else:
            this.parser.print_help()
        

def main():

    rc = RedmineCliShell().main(sys.argv[1:])

    sys.exit(rc)


    







#     cli = redminecli
# 
#     projects = client.projects
#     
#     tsm = projects['tsm']
# 
#     print dir(tsm)
# 
#     print str(tsm.issues)
# 
#     for issue in tsm.issues:
#         try:
#             print str(issue)
#         except UnicodeEncodeError:
#             pass

if __name__ == '__main__':
    main()
