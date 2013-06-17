
Redmine CLI
===========

Redmine CLI aims to be a CLI (Command Line Interface) for redmine (http://www.redmine.org)

Interactions with Redmine API are made throw ``pyredminews`` module (currently, only my version is supported until the author merge my changes).

This is a brand new project but it already implements basic interactions such as:

* Issue creation (using an editor or batch mode)
* Get issue details
* List all the issues of a given project
* List trackers
* List projects

Redmine CLI is licensed under CECILL License [1]_ (French version of the GNU License, ).


.. contents:: Contents:
   :local:

Basic configuration
-------------------

Default configuration file is ``~/.redminecli/config`` and its format is the one of python ``ConfigParser``::

    [section]
    key = value

Example::

    [global]
    auth_url = http://demo.redmine.org
    redmine_version = 2.3

    [display]
    table_max_width = 30
    column_max_len = 30

    [credentials]
    api_key = 96cdptgcGuwapJ0dAKUcYrEIIdbByi6W

    [plugins]
    enable_user_exit = no
    plugin_dir = ~/.redminecli/plugins
    user_exit_plugin = user_exit


Plugin configuration
--------------------

Redmine CLI designs is designed to be flexible and adaptable to each user expectation.
To accomplish this, a plugin design has been chosen in order the end user to be available to rewrite (with python code) part of the application.

For now, plugins are only supported for user output.
The default user output is similar to `OpenStack CLI`_ ones, and uses python ``prettytable`` module.

.. _OpenStack CLI: https://github.com/openstack

Example::

    % redminecli.py --auth-url='http://demo.redmine.org' --unauthenticated projects-list
    +-------------------------------------------+-------+------------------------------------------+
    | identifier                                | id    | name                                     |
    +-------------------------------------------+-------+------------------------------------------+
    | testsdf                                   | 10827 | testsdf                                  |
    | mytest01                                  | 10831 | mytest01                                 |
    | test-red-neilson                          | 10832 | test red neilson                         |
    | pronto-forms                              | 10833 | pronto forms                             |
    | test-moufid                               | 10838 | Test Moufid                              |
    [...]


.. [1] http://www.cecill.info/index.en.html
