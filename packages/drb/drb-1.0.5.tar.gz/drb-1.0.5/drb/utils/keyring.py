import sys
import click
from drb.utils.keyringconnection import kr_add, kr_check, kr_remove, \
    set_verbose


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always return the full command name
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args


@click.command(cls=AliasedGroup)
def keyring():
    """
    Manages Keyring entries.

    This tool is able to add, delete and check entries from the system keyring.
    The command never manage any transaction with the provided service.

    Service and its credentials are store into the system installed keyring.
    If no keyring is installed on the system, the library automatically
    creates a local encrypted file to store credentials.
    """
    pass


@keyring.command()
@click.option('--service', '-s', 'service', required=True,
              help="The service URL")
@click.option('--username', '-u', 'username', required=True,
              help="Service username")
@click.option('--password', '-p', 'password', required=True,
              help="Service password")
@click.option('--verbose', '-v', required=False, is_flag=True, default=False,
              help="Make the command more verbose.")
def add(service, username, password, verbose=None):
    """
    Create or replace credentials of a service. When the service is already
    present, credentials are overwritten.
    """
    if verbose is not None:
        set_verbose(verbose)
    try:
        kr_add(service, username, password)
        sys.exit(0)
    except Exception:
        sys.exit(1)


@keyring.command()
@click.option('--service', '-s', 'service', required=True,
              help="The service URL")
@click.option('--verbose', '-v', required=False, is_flag=True, default=False,
              help="Make the command more verbose.")
def delete(service, verbose=None):
    """
    Deletes the service and its credentials from the keyring.
    """
    if verbose is not None:
        set_verbose(verbose)
    try:
        kr_remove(service)
        sys.exit(0)
    except Exception:
        sys.exit(1)


@keyring.command()
@click.option('--service', '-s', 'service', required=True,
              help="The service URL")
@click.option('--username', '-u', 'username', help="Service username")
@click.option('--verbose', '-v', required=False, is_flag=True, default=False,
              help="Make the command more verbose.")
def check(service, username, verbose=None):
    """
    Checks the service exists in keyring.
    When username is provided, it also
    matches it.
    """
    if verbose is not None:
        set_verbose(verbose)
    sys.exit(kr_check(service, username))


if __name__ == '__main__':
    keyring()
