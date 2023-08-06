import click
import functools
import os
import sys
from typing import Dict, List, Optional
from click_aliases import ClickAliasedGroup

from nexuscli import exception
from nexuscli.cli import constants
from nexuscli.nexus_client import NexusClient
from nexuscli.nexus_config import NexusConfig
from texttable import Texttable


class AliasedGroup(ClickAliasedGroup):
    """
    Implements execution of the first partial match for a command. Fails with a
    message if there are no unique matches.

    See: https://click.palletsprojects.com/en/7.x/advanced/#command-aliases
    """
    def get_command(self, ctx, cmd_name):
        rv = ClickAliasedGroup.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        if len(matches) == 1:
            return ClickAliasedGroup.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


def with_nexus_client(click_command):
    @functools.wraps(click_command)
    @click.pass_context
    def command(ctx: click.Context, **kwargs):
        ctx.obj = get_client()
        return click_command(ctx, **kwargs)

    return command


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


def move_to_key(mydict, new_key, keys_to_move):
    if set(mydict.keys()).intersection(keys_to_move):
        mydict[new_key] = {}
        for k in keys_to_move:
            mydict[new_key][k] = mydict[k]
            del mydict[k]


def mapped_commands(command_map: dict):
    """
    TODO: document command_map format

    :param command_map:
    :return:
    """
    class CommandGroup(click.Group):
        def get_command(self, ctx, cmd_name):
            for real_command, aliases in command_map.items():
                if cmd_name in aliases:
                    return click.Group.get_command(self, ctx, real_command)
            return None

        def list_commands(self, ctx):
            return sorted([a for b in command_map.values() for a in b])

    return CommandGroup


def upcase_values(mydict: dict, keys=[]):
    for key in keys:
        value = mydict.get(key)
        if value is not None:
            mydict[key] = value.upper()


def rename_keys(mydict: dict, rename_map: dict):
    for current_name, new_name in rename_map.items():
        if mydict.get(current_name) is not None:
            mydict[new_name] = mydict[current_name]
            del mydict[current_name]


def _get_client_kwargs() -> Optional[Dict[str, str]]:
    def _without_prefix(name) -> str:
        return name[len(constants.ENV_VAR_PREFIX) + 1:].lower()

    def _with_prefix(names) -> List[str]:
        return [f'{constants.ENV_VAR_PREFIX}_{x}' for x in names]

    # This seemed an easier implementation compared to "exposing" the cli.login options to all the
    # other commands. The part I don't love is that I have to repeat the option names here.
    required_variables = _with_prefix(constants.REQUIRED_NEXUS_OPTIONS)
    defined_env_vars = [x in os.environ for x in required_variables]

    if any(defined_env_vars):
        if not all(defined_env_vars):
            errmsg = 'If any of these environment variables are set, then ALL must be set: ' \
                     f'{required_variables}'
            raise exception.NexusClientInvalidCredentials(errmsg)
        else:
            config_kwargs = {}
            all_env_vars = required_variables + _with_prefix(constants.OPTIONAL_NEXUS_OPTIONS)
            for env_var in all_env_vars:
                if os.environ.get(env_var):
                    config_kwargs[_without_prefix(env_var)] = os.environ[env_var]

            return config_kwargs
    return None


def get_client() -> NexusClient:
    """
    Returns a Nexus Client instance. Prints a warning if the configuration file doesn't exist.
    """
    maybe_config = _get_client_kwargs()
    if maybe_config:
        config = NexusConfig(**_get_client_kwargs())
        return NexusClient(config=config)

    config = NexusConfig()
    try:
        config.load()
    except FileNotFoundError:
        sys.stderr.write(
            'Warning: configuration not found; proceeding with defaults.\n'
            'To remove this warning, please run `nexus3 login`\n')
    return NexusClient(config=config)


def print_as_table(contents: List[Dict], fields: List) -> None:
    """
    Print json API output as a table

    :param contents: table contents
    :param fields: list of key names in contents elements to be added as columns to table
    """
    table = Texttable(max_width=constants.TTY_MAX_WIDTH)
    table.set_deco(Texttable.HEADER)
    table.set_header_align(['l'] * len(fields))
    table.header([x.title() for x in fields])
    table.add_rows([[item[x] for x in fields] for item in contents], header=False)

    print(table.draw())
