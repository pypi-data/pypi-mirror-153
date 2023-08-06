"""Phidata Kubectl Cli

This is the entrypoint for the `phi k` commands.
"""

from typing import Optional, cast

import typer

from phiterm.utils.cli_console import (
    print_error,
    print_info,
    print_available_workspaces,
    print_conf_not_available_msg,
    print_active_workspace_not_available,
)
from phiterm.workspace.ws_enums import WorkspaceEnv
from phiterm.utils.log import logger, set_log_level_to_debug

k8s_app = typer.Typer(
    name="k",
    help="Commands to manage your k8s resources",
    no_args_is_help=True,
    invoke_without_command=True,
)


@k8s_app.command(short_help="Save your K8s Resources")
def save(
    ws_filter: Optional[str] = typer.Argument(
        None,
        help="Filter which K8s configs to save. Format - ENV:NAME:TYPE",
        metavar="[filter]",
    ),
    env_filter: str = typer.Option(
        None,
        "-e",
        "--env",
        metavar="",
        help="The environment to use. Available Options: {}".format(
            WorkspaceEnv.values_list()
        ),
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using app name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """
    Saves your k8s resources so you know exactly what is being deployed

    \b
    Examples:
    * `phi k save`      -> Save resources for the active workspace
    """

    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.k8s.k8s_operator import save_k8s_resources

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

    target_env_str: Optional[str] = None
    target_env: Optional[WorkspaceEnv] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None

    if ws_filter is not None:
        if not isinstance(ws_filter, str):
            raise TypeError(
                f"Invalid workspace filter. Expected: str, Received: {type(ws_filter)}"
            )
        filters = ws_filter.split(":")
        # logger.debug(f"filters: {filters}")
        num_filters = len(filters)
        if num_filters >= 1:
            target_env_str = filters[0]
        if num_filters >= 2:
            target_name = filters[2]
        if num_filters >= 3:
            target_type = filters[3]

    if target_env_str is None:
        target_env_str = env_filter
    if target_name is None:
        target_name = name_filter
    if target_type is None:
        target_type = type_filter

    if target_env_str is not None:
        if target_env_str.lower() not in WorkspaceEnv.values_list():
            print_error(
                f"{target_env_str} is not supported, please choose from: {WorkspaceEnv.values_list()}"
            )
            return
        target_env = cast(
            WorkspaceEnv,
            WorkspaceEnv.from_str(target_env_str),
        )

    logger.debug("Processing workspace")
    logger.debug(f"\ttarget_env: {target_env}")
    logger.debug(f"\ttarget_name: {target_name}")
    logger.debug(f"\ttarget_type: {target_type}")
    save_k8s_resources(
        ws_data=active_ws_data,
        target_env=target_env,
        target_name=target_name,
        target_type=target_type,
    )


# @app.command(short_help="Print your K8s Resources")
# def print(
#     refresh: bool = typer.Option(
#         False,
#         "-r",
#         "--refresh",
#         help="Refresh the workspace config, use this if you've just changed your phi-config.yaml",
#         show_default=True,
#     ),
#     type_filters: List[str] = typer.Option(
#         None, "-k", "--kind", help="Filter the K8s resources by kind"
#     ),
#     name_filters: List[str] = typer.Option(
#         None, "-n", "--name", help="Filter the K8s resources by name"
#     ),
# ):
#     """
#     Print your k8s resources so you know exactly what is being deploying
#
#     \b
#     Examples:
#     * `phi k print`      -> Print resources for the primary workspace
#     * `phi k print data` -> Print resources for the workspace named data
#     """
#
#     from phi import schemas
#     from phiterm.k8s import k8s_operator
#     from phiterm.conf.phi_conf import PhiConf
#
#     config: Optional[PhiConf] = PhiConf.get_saved_conf()
#     if not config:
#         conf_not_available_msg()
#         raise typer.Exit(1)
#
#     primary_ws: Optional[schemas.WorkspaceSchema] = config.primary_ws
#     if primary_ws is None:
#         primary_ws_not_available_msg()
#         raise typer.Exit(1)
#
#     k8s_operator.print_k8s_resources_as_yaml(
#         primary_ws, config, refresh, type_filters, name_filters
#     )
#
#
# @app.command(short_help="Apply your K8s Resources")
# def apply(
#     refresh: bool = typer.Option(
#         False,
#         "-r",
#         "--refresh",
#         help="Refresh the workspace config, use this if you've just changed your phi-config.yaml",
#         show_default=True,
#     ),
#     service_filters: List[str] = typer.Option(
#         None, "-s", "--svc", help="Filter the Services"
#     ),
#     type_filters: List[str] = typer.Option(
#         None, "-k", "--kind", help="Filter the K8s resources by kind"
#     ),
#     name_filters: List[str] = typer.Option(
#         None, "-n", "--name", help="Filter the K8s resources by name"
#     ),
# ):
#     """
#     Apply your k8s resources. You can filter the resources by services, kind or name
#
#     \b
#     Examples:
#     * `phi k apply`      -> Apply resources for the primary workspace
#     """
#
#     from phi import schemas
#     from phiterm.k8s import k8s_operator
#     from phiterm.conf.phi_conf import PhiConf
#
#     config: Optional[PhiConf] = PhiConf.get_saved_conf()
#     if not config:
#         conf_not_available_msg()
#         raise typer.Exit(1)
#
#     primary_ws: Optional[schemas.WorkspaceSchema] = config.primary_ws
#     if primary_ws is None:
#         primary_ws_not_available_msg()
#         raise typer.Exit(1)
#
#     k8s_operator.apply_k8s_resources(
#         primary_ws, config, refresh, service_filters, type_filters, name_filters
#     )
#
#
# @app.command(short_help="Get active K8s Objects")
# def get(
#     service_filters: List[str] = typer.Option(
#         None, "-s", "--svc", help="Filter the Services"
#     ),
#     type_filters: List[str] = typer.Option(
#         None, "-k", "--kind", help="Filter the K8s resources by kind"
#     ),
#     name_filters: List[str] = typer.Option(
#         None, "-n", "--name", help="Filter the K8s resources by name"
#     ),
# ):
#     """
#     Get active k8s resources.
#
#     \b
#     Examples:
#     * `phi k apply`      -> Get active resources for the primary workspace
#     """
#
#     from phi import schemas
#     from phiterm.k8s import k8s_operator
#     from phiterm.conf.phi_conf import PhiConf
#
#     config: Optional[PhiConf] = PhiConf.get_saved_conf()
#     if not config:
#         conf_not_available_msg()
#         raise typer.Exit(1)
#
#     primary_ws: Optional[schemas.WorkspaceSchema] = config.primary_ws
#     if primary_ws is None:
#         primary_ws_not_available_msg()
#         raise typer.Exit(1)
#
#     k8s_operator.print_active_k8s_resources(
#         primary_ws, config, service_filters, type_filters, name_filters
#     )
#
#
# if __name__ == "__main__":
#     app()
