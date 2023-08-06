"""Phi Databox Cli

This is the entrypoint for the `phi dx` commands
"""

from typing import Optional, cast

import typer

from phiterm.utils.cli_console import (
    print_info,
    print_conf_not_available_msg,
    print_active_workspace_not_available,
    print_available_workspaces,
)
from phiterm.utils.log import logger, set_log_level_to_debug
from phiterm.workspace.ws_enums import WorkspaceEnv

dx_app = typer.Typer(
    name="dx",
    short_help="Run commands in databox",
    no_args_is_help=True,
    add_completion=False,
    invoke_without_command=True,
    options_metavar="\b",
    subcommand_metavar="<command>",
)


@dx_app.command(
    short_help="Run commands in databox",
    options_metavar="\b",
    no_args_is_help=True,
)
def run(
    command: str = typer.Argument(..., help="Command to run.", metavar="[cmd]"),
    env_filter: Optional[str] = typer.Option(
        None,
        "-e",
        "--env",
        metavar="",
        help="The environment to use. Available Options: {}".format(
            WorkspaceEnv.values_list()
        ),
    ),
    app_name: Optional[str] = typer.Option(
        None,
        "-a",
        metavar="",
        help="The App to run the command in. Default: databox",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.databox.databox_operator import run_command

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    active_ws_data: Optional[PhiWsData] = phi_conf.get_active_ws_data(refresh=True)
    if active_ws_data is None:
        print_active_workspace_not_available()
        avl_ws = phi_conf.available_ws
        if avl_ws:
            print_available_workspaces(avl_ws)
        return

    target_env: Optional[WorkspaceEnv] = None
    target_app: Optional[str] = app_name

    default_env = (
        active_ws_data.ws_config.default_env if active_ws_data.ws_config else None
    )
    target_env_str = env_filter or default_env or "dev"
    try:
        target_env = cast(WorkspaceEnv, WorkspaceEnv.from_str(target_env_str))
    except Exception as e:
        logger.error(e)
        logger.error(
            f"{target_env_str} is not supported, please choose from: {WorkspaceEnv.values_list()}"
        )
        return

    logger.debug("Running command")
    logger.debug(f"\tcommand      : {command}")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_app   : {target_app}")
    run_command(
        command=command,
        ws_data=active_ws_data,
        target_env=target_env,
        target_app=target_app,
    )
