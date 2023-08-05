#!python
# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#

"""A small caosdb client with a focus on administration of the server."""

from __future__ import print_function, unicode_literals

import getpass
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

import caosdb as db
from caosdb import administration as admin
from caosdb.exceptions import HTTPClientError

__all__ = []
__version__ = 0.3
__date__ = '2016-09-19'
__updated__ = '2018-12-11'


def do_update_role(args):
    admin._update_role(name=args.role_name, description=args.role_description)


def do_create_role(args):
    admin._insert_role(name=args.role_name, description=args.role_description)


def do_retrieve_role(args):
    print(admin._retrieve_role(name=args.role_name))


def do_delete_role(args):
    admin._delete_role(name=args.role_name)


def do_retrieve(args):
    c = None

    if args.query:
        if len(args.entities) > 1:
            raise Exception("Only one query at a time can be retrieved.")
        c = db.execute_query(args.entities[0], flags=eval(args.flags))
    else:
        c = db.Container()

        for i in args.entities:
            try:
                eid = int(i)
                c.append(db.Entity(id=eid))
            except ValueError:
                c.append(db.Entity(name=i))
        c.retrieve(flags=eval(args.flags))
    print(c)


def do_update(args):
    fdict = eval(args.flags)
    xml = open(args.xml_path, "r")
    ret = db.get_connection().update(
        entity_uri_segment=["Entity"], reconnect=True, body=xml)
    db.Container._response_to_entities(ret)


def do_delete(args):
    c = db.Container()

    for i in args.entities:
        c.append(db.Entity(id=i))

    c.delete()


def do_insert(args):
    fdict = eval(args.flags)
    xml = open(args.xml_path, "r")
    ret = db.get_connection().insert(
        entity_uri_segment=["Entity"],
        reconnect=True,
        query_dict=fdict,
        body=xml)
    print(db.Container._response_to_entities(ret))


def _promt_for_pw():
    password = getpass.getpass(prompt="Please type password: ")
    password2 = getpass.getpass(prompt="Please type password again: ")

    if password != password2:
        raise Exception("Password strings didn't match")

    return password


def do_create_user(args):
    password = args.user_password

    if args.ask_password is True:
        password = _promt_for_pw()
    try:
        admin._insert_user(name=args.user_name,
                           email=args.user_email, password=password)

        if args.activate_user:
            do_activate_user(args)
    except HTTPClientError as e:
        print(e.msg)


def do_activate_user(args):
    try:
        admin._update_user(name=args.user_name, status="ACTIVE")
    except HTTPClientError as e:
        print(e.msg)


def do_deactivate_user(args):
    try:
        admin._update_user(name=args.user_name, status="INACTIVE")
    except HTTPClientError as e:
        print(e.msg)


def do_set_user_password(args):
    if args.user_password is None:
        password = _promt_for_pw()
    else:
        password = args.user_password
    try:
        admin._update_user(name=args.user_name, password=password)
    except HTTPClientError as e:
        print(e.msg)


def do_add_user_roles(args):
    roles = admin._get_roles(username=args.user_name, realm=None)

    for r in args.user_roles:
        roles.add(r)
    admin._set_roles(username=args.user_name, roles=roles)


def do_remove_user_roles(args):
    roles = admin._get_roles(username=args.user_name, realm=None)

    for r in args.user_roles:
        if r in roles:
            roles.remove(r)
    admin._set_roles(username=args.user_name, roles=roles)


def do_set_user_entity(args):
    admin._update_user(name=args.user_name, entity=args.user_entity)


def do_reset_user_entity(args):
    admin._update_user(name=args.user_name, entity="")


def do_set_user_email(args):
    admin._update_user(name=args.user_name, email=args.user_email)


def do_retrieve_user(args):
    print(admin._retrieve_user(name=args.user_name))


def do_delete_user(args):
    admin._delete_user(name=args.user_name)


def do_retrieve_user_roles(args):
    print(admin._get_roles(username=args.user_name))


def do_retrieve_role_permissions(args):
    print(admin._get_permissions(role=args.role_name))


def do_grant_role_permissions(args):
    perms = admin._get_permissions(args.role_name)

    for p in args.role_permissions:
        g = admin.PermissionRule(
            action="Grant", permission=p, priority=args.permissions_priority)
        d = admin.PermissionRule(
            action="Deny", permission=p, priority=args.permissions_priority)

        if g in perms:
            perms.remove(g)

        if d in perms:
            perms.remove(d)
        perms.add(g)
    admin._set_permissions(role=args.role_name, permission_rules=perms)


def do_revoke_role_permissions(args):
    perms = admin._get_permissions(args.role_name)

    for p in args.role_permissions:
        g = admin.PermissionRule(
            action="Grant", permission=p, priority=args.permissions_priority)
        d = admin.PermissionRule(
            action="Deny", permission=p, priority=args.permissions_priority)

        if g in perms:
            perms.remove(g)

        if d in perms:
            perms.remove(d)
    admin._set_permissions(role=args.role_name, permission_rules=perms)


def do_deny_role_permissions(args):
    perms = admin._get_permissions(args.role_name)

    for p in args.role_permissions:
        g = admin.PermissionRule(
            action="Grant", permission=p, priority=args.permissions_priority)
        d = admin.PermissionRule(
            action="Deny", permission=p, priority=args.permissions_priority)

        if g in perms:
            perms.remove(g)

        if d in perms:
            perms.remove(d)
        perms.add(d)
    admin._set_permissions(role=args.role_name, permission_rules=perms)


def do_retrieve_entity_acl(args):
    entities = db.execute_query(q=args.query, flags={"ACL": None})

    for entity in entities:
        print(entity.id)
        print(entity.acl)


def do_action_entity_permissions(args):
    entities = db.execute_query(q=args.query, flags={"ACL": None})

    for entity in entities:
        for p in args.permissions:
            getattr(entity, args.action)(role=args.role, priority=args.priority,
                                         permission=p)
    entities.update(flags={"ACL": None})

    for entity in entities:
        print(entity.id)
        print(entity.acl)


def main(argv=None):
    """Command line options."""

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (
        program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__
    program_license = '''%s

USAGE
''' % (program_shortdesc)

    # Setup argument parser
    parser = ArgumentParser(description=program_license,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-V', '--version', action='version',
                        version=program_version_message)
    parser.add_argument("--auth-token", metavar="AUTH_TOKEN",
                        dest="auth_token",
                        help=("A CaosDB authentication token (default: None). "
                              "If the authentication token is passed, the "
                              "`password_method` of the connection is set to "
                              "`auth_token` and the respective configuration "
                              "from the pycaosdb.ini is effectively being "
                              "overridden.\nTODO: Also allow passing the token "
                              "via environmenty variables."))
    subparsers = parser.add_subparsers(
        title="commands",
        metavar="COMMAND",
        description="You can invoke the following commands. Print the detailed help for each command with #> caosdb_admin COMMAND -h")

    # users (CRUD)
    subparser = subparsers.add_parser(
        "create_user",
        help="Create a new user in caosdb's internal user database. You need "
        " to activate the user before use.")
    subparser.set_defaults(call=do_create_user)
    mg = subparser.add_mutually_exclusive_group()
    mg.add_argument("-a", "--ask-password",
                    help="Prompt for a password.", action="store_true")
    mg.add_argument(
        "--password",
        dest="user_password",
        default=None,
        help="Alternative way to provide the new user's password. Please "
        "consider to use the more secure, interactive way (-a option).")
    subparser.add_argument("-c", "--activate-user",
                           help="Activate the user after creation.",
                           action="store_true")
    subparser.add_argument(
        metavar='USERNAME',
        dest="user_name",
        help="A user name which is unique in the internal user database.")
    subparser.add_argument(
        metavar="EMAIL",
        nargs='?',
        dest="user_email",
        help="The email address of the new user.")

    subparser = subparsers.add_parser(
        "activate_user", help="(Re-)activate an inactive (but existing) user.")
    subparser.set_defaults(call=do_activate_user)
    subparser.add_argument(metavar='USERNAME', dest="user_name",
                           help="The name of the user who is to be activated.")

    subparser = subparsers.add_parser(
        "deactivate_user", help="Deactivate an active user.")
    subparser.set_defaults(call=do_deactivate_user)
    subparser.add_argument(
        metavar='USERNAME',
        dest="user_name",
        help="The name of the user who is to be deactivated.")

    subparser = subparsers.add_parser(
        "set_user_password",
        help="Set a new password for a user. "
        "By default, you will be prompted for the password.")
    subparser.set_defaults(call=do_set_user_password)
    subparser.add_argument(
        metavar='USERNAME',
        dest="user_name",
        help="The name of the user who's password is to be set.")
    subparser.add_argument(
        metavar='PASSWORD',
        nargs="?",
        dest="user_password",
        default=None,
        help="Alternative way to provide the user's new password. "
        "The more secure (and default way) is to provide it interactively.")

    subparser = subparsers.add_parser(
        "set_user_entity",
        help="Associate a user with an existing entity (which should represent a person, a program, an organization or something similar).")
    subparser.set_defaults(call=do_set_user_entity)
    subparser.add_argument(
        metavar='USERNAME',
        dest="user_name",
        help="The name of the user who's associated entity you want to set.")
    subparser.add_argument(metavar='ENTITY', dest="user_entity",
                           help="An ID of an existing entity.")

    subparser = subparsers.add_parser(
        "reset_user_entity",
        help="Terminate the association of a user with an entity.")
    subparser.set_defaults(call=do_reset_user_entity)
    subparser.add_argument(
        metavar='USERNAME',
        dest="user_name",
        help="The name of the user who's associated entity you want to reset.")

    subparser = subparsers.add_parser(
        "set_user_email", help="Set a new email for a user.")
    subparser.set_defaults(call=do_set_user_email)
    subparser.add_argument(
        metavar='USERNAME',
        dest="user_name",
        help="The name of the user who's email is to be set.")
    subparser.add_argument(
        metavar='EMAIL',
        dest="user_email",
        help="The name of the user who's email is to be set.")

    subparser = subparsers.add_parser(
        "retrieve_user", help="Retrieve a user (email, entity)")
    subparser.set_defaults(call=do_retrieve_user)
    subparser.add_argument(
        metavar='USERNAME', dest="user_name", help="The name of the user.")

    subparser = subparsers.add_parser(
        "delete_user",
        help="Delete a user from caosdb's internal user database.")
    subparser.set_defaults(call=do_delete_user)
    subparser.add_argument(metavar='USERNAME', dest="user_name",
                           help="The name of the user who is to be deleted.")

    # user roles
    subparser = subparsers.add_parser(
        "add_user_roles", help="Extend the roles of a user.")
    subparser.set_defaults(call=do_add_user_roles)
    subparser.add_argument(
        metavar='USERNAME',
        dest="user_name",
        help="The name of the user who's roles are to be extended.")
    subparser.add_argument(
        metavar='ROLES',
        dest="user_roles",
        nargs='+',
        help="A space separated list of (existing) roles.")

    subparser = subparsers.add_parser(
        "remove_user_roles", help="Remove some of the roles of a user.")
    subparser.set_defaults(call=do_remove_user_roles)
    subparser.add_argument(
        metavar='USERNAME',
        dest="user_name",
        help="The name of the user from whom you want to take some roles away.")
    subparser.add_argument(
        metavar='ROLES',
        dest="user_roles",
        nargs='+',
        help="A space separated list of (existing) roles.")

    subparser = subparsers.add_parser(
        "retrieve_user_roles", help="Retrieve a user's roles.")
    subparser.set_defaults(call=do_retrieve_user_roles)
    subparser.add_argument(
        metavar='USERNAME', dest="user_name", help="The name of the user.")

    # role permissions
    subparser = subparsers.add_parser(
        "retrieve_role_permissions",
        help="Retrieve the set of permission rules of a role.")
    subparser.set_defaults(call=do_retrieve_role_permissions)
    subparser.add_argument(
        metavar='ROLE',
        dest="role_name",
        help="The name of the role which permissions are to be retrieved.")

    subparser = subparsers.add_parser(
        "grant_role_permissions", help="Grant permissions to a role.")
    subparser.set_defaults(call=do_grant_role_permissions)
    subparser.add_argument(
        '--priority',
        dest="permissions_priority",
        action="store_true",
        default=False,
        help="This flag enables priority permission rules.")
    subparser.add_argument(
        metavar='ROLE',
        dest="role_name",
        help="The name of the role to which the permissions are to be granted.")
    subparser.add_argument(
        metavar='PERMISSIONS',
        dest="role_permissions",
        nargs='+',
        help="A space separated list of permissions.")

    subparser = subparsers.add_parser(
        "revoke_role_permissions",
        help="Remove previously granted or denied permissions from a role.")
    subparser.set_defaults(call=do_revoke_role_permissions)
    subparser.add_argument(
        '--priority',
        dest="permissions_priority",
        action="store_true",
        default=False,
        help="This flag is needed to revoke priority permissions.")
    subparser.add_argument(
        metavar='ROLE',
        dest="role_name",
        help="The name of the role from which you want to revoke permissions.")
    subparser.add_argument(
        metavar='PERMISSIONS',
        dest="role_permissions",
        nargs='+',
        help="A space separated list of permissions.")

    subparser = subparsers.add_parser(
        "deny_role_permissions", help="Deny a role permissions.")
    subparser.set_defaults(call=do_deny_role_permissions)
    subparser.add_argument(
        '--priority',
        dest="permissions_priority",
        action="store_true",
        default=False,
        help="This flag enables priority permission rules.")
    subparser.add_argument(
        metavar='ROLE',
        dest="role_name",
        help="The name of the role which you want to deny permissions.")
    subparser.add_argument(
        metavar='PERMISSIONS',
        dest="role_permissions",
        nargs='+',
        help="A space separated list of permissions.")

    # entities (CRUD)
    subparser = subparsers.add_parser("insert", help="Insert entities.")
    subparser.set_defaults(call=do_insert)
    subparser.add_argument(
        '-f',
        '--flags',
        dest="flags",
        help="A python dictionary (dict) with flag keys and their values.",
        metavar="FLAGS",
        default="{}")
    subparser.add_argument(metavar='PATH', dest="xml_path",
                           help="Path to an xml file.")

    subparser = subparsers.add_parser("retrieve", help="Retrieve entities.")
    subparser.set_defaults(call=do_retrieve)
    subparser.add_argument(
        '-f',
        '--flags',
        dest="flags",
        help="A python dictionary (dict) with flag keys and their values.",
        metavar="FLAGS",
        default="{}")
    subparser.add_argument('-q', '--query', dest='query', action="store_true",
                           help="If the ENTITIES argument is a query.")
    subparser.add_argument(metavar='ENTITIES', dest="entities", nargs='+',
                           help="A space separated list of ids or names of"
                           "entities or ai single query.")

    subparser = subparsers.add_parser("update", help="Update entities.")
    subparser.set_defaults(call=do_update)
    subparser.add_argument(
        '-f',
        '--flags',
        dest="flags",
        help="A python dictionary (dict) with flag keys and their values.",
        metavar="FLAGS",
        default="{}")
    subparser.add_argument(metavar='PATH', dest="xml_path",
                           help="Path to an xml file.")

    subparser = subparsers.add_parser("delete", help="Delete entities.")
    subparser.set_defaults(call=do_delete)
    subparser.add_argument(
        '-f',
        '--flags',
        dest="flags",
        help="A python dictionary (dict) with flag keys and their values.",
        metavar="FLAGS",
        default="{}")
    subparser.add_argument(
        metavar='ENTITIES',
        dest="entities",
        nargs='+',
        help="A space separated list of ids or names of entities.")

    # roles (CRUD)
    create_role_parser = subparsers.add_parser(
        "create_role", help="Create a new role.")
    create_role_parser.set_defaults(call=do_create_role)
    create_role_parser.add_argument(
        dest="role_name", metavar="ROLENAME", help="The name of the new role.")
    create_role_parser.add_argument(
        dest="role_description",
        metavar="DESCRIPTION",
        help="A description of the role's purpose, it's intended use case, characteristics of the users who have this role, etc.")

    retrieve_role_parser = subparsers.add_parser(
        "retrieve_role", help="Retrieve the description of an existing role.")
    retrieve_role_parser.set_defaults(call=do_retrieve_role)
    retrieve_role_parser.add_argument(
        dest="role_name",
        metavar="ROLENAME",
        help="The name of the existing role.")

    update_role_parser = subparsers.add_parser(
        "update_role", help="Change the description of an existing role.")
    update_role_parser.set_defaults(call=do_update_role)
    update_role_parser.add_argument(
        dest="role_name",
        metavar="ROLENAME",
        help="The name of the existing role.")
    update_role_parser.add_argument(
        dest="role_description",
        metavar="DESCRIPTION",
        help="A new description of the role's purpose, it's intended use case, characteristics of the users who have this role, etc.")

    delete_role_parser = subparsers.add_parser(
        "delete_role", help="Delete a role.")
    delete_role_parser.set_defaults(call=do_delete_role)
    delete_role_parser.add_argument(
        dest="role_name",
        metavar="ROLENAME",
        help="The name of the existing role.")

    # entity acl
    retrieve_entity_acl_parser = subparsers.add_parser(
        "retrieve_entity_acl", help="Retrieve an entity ACL.")
    retrieve_entity_acl_parser.set_defaults(call=do_retrieve_entity_acl)
    retrieve_entity_acl_parser.add_argument(dest="query", metavar="QUERY",
                                            help="A FIND query.")

    for action in ["grant", "deny", "revoke_denial", "revoke_grant"]:
        action_entity_permissions_parser = subparsers.add_parser(
            "{}_entity_permissions".format(action),
            help="{} entity permissions to a role.".format(action))
        action_entity_permissions_parser.set_defaults(
            call=do_action_entity_permissions, action=action)
        action_entity_permissions_parser.add_argument(dest="query", metavar="QUERY",
                                                      help="A FIND query.")
        action_entity_permissions_parser.add_argument(dest="role", metavar="ROLE",
                                                      help="The name of an exising role.")
        action_entity_permissions_parser.add_argument(
            dest="permissions",
            metavar="PERMISSION",
            help="A list of permissions",
            nargs='+')
        action_entity_permissions_parser.add_argument(
            '--priority',
            dest="priority",
            action="store_true",
            default=False,
            help="This flag enables priority permission rules.")

    # Process arguments
    args = parser.parse_args()
    auth_token = args.auth_token
    if auth_token is not None:
        db.configure_connection(password_method="auth_token",
                                auth_token=auth_token)
    else:
        db.configure_connection()

    return args.call(args)


if __name__ == "__main__":
    sys.exit(main())
