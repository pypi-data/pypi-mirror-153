"""The Phi Cli

This is the entrypoint for the `phi` cli application.
"""

import typer

from phiterm.cli.ws.ws_app import ws_app
from phiterm.cli.k8s.k8s_app import k8s_app
from phiterm.cli.wf.wf_app import wf_app
from phiterm.cli.dx.dx_app import dx_app
from phiterm.utils.log import set_log_level_to_debug

cli_app = typer.Typer(
    help="""\b
phi is a tool for building high-quality data products.
\b
Usage:
- Run `phi init` to initialize phidata
- Run `phi ws init` to create a new workspace
- Run `phi ws setup` from an existing directory to setup the workspace
- Run `phi ws up` to deploy the workspace
""",
    no_args_is_help=True,
    add_completion=False,
    invoke_without_command=True,
    options_metavar="\b",
    subcommand_metavar="<command>",
)
cli_app.add_typer(ws_app)
cli_app.add_typer(k8s_app)
cli_app.add_typer(wf_app)
cli_app.add_typer(dx_app)


@cli_app.command(short_help="Initialize phidata, use -r to reset")
def init(
    reset: bool = typer.Option(
        False, "--reset", "-r", help="Reset phidata", show_default=True
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """
    \b
    Initialize phidata, use -r to reset

    \b
    Examples:
    * `phi init`    -> Initializing phidata
    * `phi init -r` -> Reset and initializing phidata
    """
    from phiterm.cli.cli_operator import initialize_phidata

    if print_debug_log:
        set_log_level_to_debug()

    init_success: bool = initialize_phidata(reset)


@cli_app.command(short_help="Authenticate with phidata.com", hidden=True)
def auth(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """
    \b
    Authenticate your account with phidata.

    \b
    Examples:
    * `phi auth`
    """
    from phiterm.cli.cli_operator import authenticate_phidata

    if print_debug_log:
        set_log_level_to_debug()

    auth_success: bool = authenticate_phidata()


@cli_app.command(short_help="Set current directory as active workspace")
def set(
    ws_name: str = typer.Option(None, "-ws", help="Active workspace name"),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """
    \b
    Setup the current directory as the active workspace.
    This command can be run from within the workspace directory
        OR with a -ws flag to set another workspace as primary.

    Set a workspace as active

    \b
    Examples:
    $ `phi ws set`          -> Set the current directory as the active phidata workspace
    $ `phi ws set -w idata` -> Set the workspace named idata as the active phidata workspace
    """
    from phiterm.workspace.ws_operator import set_workspace_as_active

    if print_debug_log:
        set_log_level_to_debug()

    operation_success: bool = set_workspace_as_active(ws_name)


@cli_app.command(short_help="Authenticate from the cli", hidden=True)
def cliauth(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """
    \b
    Authenticate from cli

    \b
    Examples:
    * `phi cliauth`
    """
    from phiterm.cli.cli_operator import sign_in_using_cli

    if print_debug_log:
        set_log_level_to_debug()

    auth_success: bool = sign_in_using_cli()


@cli_app.command(short_help="Reset phidata installation", hidden=True)
def reset(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """
    \b
    Reset the existing phidata installation
    After resetting please run `phi init` to initialize again.
    """
    from phiterm.cli.cli_operator import delete_phidata_conf

    if print_debug_log:
        set_log_level_to_debug()

    delete_phidata_conf()


@cli_app.command(short_help="Ping phidata servers", hidden=True)
def ping(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """Ping the phidata servers and check if you are authenticated"""
    from phiterm.backend_api.auth_api import auth_ping
    from phiterm.utils.cli_console import print_info

    if print_debug_log:
        set_log_level_to_debug()

    ping_success = auth_ping()
    if ping_success:
        print_info("Ping successful")
    else:
        print_info("Could not reach phidata servers")


@cli_app.command(short_help="Print phidata config", hidden=True)
def config(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """Print your current phidata config"""
    from typing import Optional

    from phiterm.conf.phi_conf import PhiConf
    from phiterm.utils.cli_console import print_info

    if print_debug_log:
        set_log_level_to_debug()

    conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if conf is not None:
        conf.print_to_cli()
    else:
        print_info("Phidata has not been setup, run `phi init` to get started")


######################################################
## Notes
# * Documentation for invoke_without_command=True
#   https://typer.tiangolo.com/tutorial/commands/context/#executable-callback
# * To prevent re-wrapping during cli output, use \b before the paragraph.
#   More info: https://click.palletsprojects.com/en/5.x/documentation/#preventing-rewrapping
######################################################
