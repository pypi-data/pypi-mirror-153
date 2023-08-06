"""Phi Workspace Cli

This is the entrypoint for the `phi ws` commands
"""

from typing import Optional, cast

import typer

from phiterm.utils.cli_console import (
    print_error,
    print_info,
    print_heading,
    print_available_workspaces,
    print_conf_not_available_msg,
    print_active_workspace_not_available,
)
from phiterm.utils.log import logger, set_log_level_to_debug
from phiterm.workspace.ws_enums import (
    WorkspaceEnv,
    WorkspaceStarterTemplate,
    WorkspaceConfigType,
)

ws_app = typer.Typer(
    name="ws",
    short_help="Commands to manage your workspaces",
    help="""\b
Use `phi ws <command>` to create, setup or delete your phidata workspace.
Run `phi ws <command> --help` for more info.
""",
    no_args_is_help=True,
    add_completion=False,
    invoke_without_command=True,
    options_metavar="\b",
    subcommand_metavar="<command>",
)


@ws_app.command(short_help="Create a new phidata workspace in the current directory.")
def init(
    ws_name: str = typer.Option(None, "-ws", help="Name of the new workspace"),
    template: str = typer.Option(
        "aws",
        "-t",
        "--template",
        help="Choose a starter template which comes pre-populated with defaults. Available Options: {}".format(
            ", ".join(WorkspaceStarterTemplate.values_list())
        ),
        show_default=True,
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """\b
    Creates a new workspace in the current directory using the selected starter template
    [default: docker]

    \b
    Examples:
    $ phi ws init                -> Create a new workspace
    $ phi ws init -ws data        -> Create a workspace named data using the default starter template (docker)
    $ phi ws init -ws data -t aws -> Create a workspace named data using the `aws` starter template
    """
    from phiterm.workspace.ws_operator import (
        create_new_workspace,
        initialize_workspace,
    )

    if print_debug_log:
        set_log_level_to_debug()

    if ws_name is None:
        initialize_workspace()
        return

    if (
        template is None
        or template.lower() not in WorkspaceStarterTemplate.values_list()
    ):
        print_error(
            f"{template} is not a supported template, please choose from: {WorkspaceStarterTemplate.values_list()}"
        )
        return
    _template: WorkspaceStarterTemplate = cast(
        WorkspaceStarterTemplate,
        WorkspaceStarterTemplate.from_str(template),
    )

    create_new_workspace(ws_name, _template)


@ws_app.command(short_help="Setup a phidata workspace")
def setup(
    ws_name: str = typer.Option(None, "-ws", help="Name of the workspace to setup"),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """\b
    Setup the current directory as a phidata workspace.
    This command can be run from within the workspace directory
        OR with a -ws flag to setup another workspace.

    \b
    Examples:
    $ `phi ws setup`         -> Setup the current directory as a phidata workspace
    $ `phi ws setup -ws data` -> Setup the workspace named idata
    """
    from pathlib import Path
    from phiterm.workspace.ws_operator import setup_workspace

    if print_debug_log:
        set_log_level_to_debug()

    # By default, we assume this command is run from the workspace directory
    if ws_name is None:
        # If the user does not provide a ws_name, that implies `phi ws setup` is ran from
        # the workspace directory.
        ws_path: Path = Path(".").resolve()
        setup_workspace(ws_path)
    else:
        # If the user provides a workspace name manually, we find the dir for that ws and set it up
        from phiterm.conf.phi_conf import PhiConf

        phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
        if not phi_conf:
            print_conf_not_available_msg()
            return

        _ws_path: Optional[Path] = phi_conf.get_ws_root_path_by_name(ws_name)
        if _ws_path is None:
            print_error(f"Could not find workspace {ws_name}")
            avl_ws = phi_conf.available_ws
            if avl_ws:
                print_available_workspaces(avl_ws)
            return
        setup_workspace(_ws_path)


# @ws_app.command(short_help="Show steps to setup a git repo for the ws")
# def git(
#     ws_name: str = typer.Option(None, "-ws", help="[Optional] Name for the workspace"),
#     print_debug_log: bool = typer.Option(
#         False,
#         "-d",
#         "--debug",
#         help="Print debug logs.",
#     ),
# ):
#     """
#     Print steps to setup a remote git repo for the active workspace.
#
#     \b
#     Examples:
#     $ `phi ws git`
#     $ `phi ws git -ws data`
#     """
#     from pathlib import Path
#     from phiterm.enums.user_enums import VersionControlProviderEnum
#     from phiterm.workspace.ws_operator import print_git_setup
#
#     from phiterm.conf.phi_conf import PhiConf
#
#     phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
#     if not phi_conf:
#         print_conf_not_available_msg()
#         return
#
#     _ws_name: Optional[str] = None
#     ws_root_path: Optional[Path] = None
#     if ws_name:
#         _ws_name = ws_name
#         ws_root_path = phi_conf.get_ws_root_path_by_name(_ws_name)
#     else:
#         # print steps for the active workspace
#         _ws_name = phi_conf.active_ws_name
#         if _ws_name is None:
#             print_info(
#                 "Primary workspace not available, searching current directory for a workspace"
#             )
#             ws_root_path = Path(".").resolve()
#             _ws_name = phi_conf.get_ws_name_by_path(ws_root_path)
#         else:
#             ws_data = phi_conf.get_ws_data_by_name(_ws_name)
#             if ws_data is not None and ws_data.ws_root_path is not None:
#                 ws_root_path = ws_data.ws_root_path
#
#     if _ws_name is None or ws_root_path is None:
#         print_error(f"Could not find workspace at {ws_root_path}")
#         avl_ws = phi_conf.available_ws
#         if avl_ws:
#             print_available_workspaces(avl_ws)
#         return
#
#     version_control_provider = (
#         phi_conf.user.version_control_provider
#         if phi_conf.user and phi_conf.user.version_control_provider
#         else VersionControlProviderEnum.GITHUB
#     )
#     print_git_setup(
#         ws_name=_ws_name,
#         ws_root_path=ws_root_path,
#         version_control_provider=version_control_provider,
#     )


@ws_app.command(
    short_help="Deploy your active workspace",
    options_metavar="\b",
)
def up(
    ws_filter: Optional[str] = typer.Argument(
        None,
        help="Filter the resources to deploy. Format - ENV:APP:NAME:TYPE:CONFIG",
        metavar="[filter]",
    ),
    env_filter: Optional[str] = typer.Option(
        None,
        "-e",
        "--env",
        metavar="",
        help="Filter the environment to deploy. Available Options: {}".format(
            WorkspaceEnv.values_list()
        ),
    ),
    config_filter: Optional[str] = typer.Option(
        None,
        "-c",
        "--config",
        metavar="",
        help="Filter the config to deploy. Available Options: {}".format(
            WorkspaceConfigType.values_list()
        ),
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    app_filter: Optional[str] = typer.Option(
        None, "-a", "--app", metavar="", help="Filter using app name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be deployed and exit.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "-y",
        help="Skip the confirmation before deploying resources.",
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
    Deploys the active workspace.
    Filters can be used to limit deployment by
        - Env (dev, stg, prd)
        - App name
        - Resource name
        - Resource type
        - Config type (docker, aws, k8s)
    \b
    Filters can be provided as a single argument as - ENV:APP:NAME:TYPE:CONFIG
    or using multiple options.
    Examples:
    \b
    $ `phi ws up`           -> Deploy default resources
    $ `phi ws up dev`       -> Deploy all dev resources
    $ `phi ws up prd`       -> Deploy all prd resources
    $ `phi ws up prd:::aws` -> Deploy all prd aws resources
    $ `phi ws up prd::s3`   -> Deploy prd resources with name s3
    """
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.workspace.ws_operator import deploy_workspace

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
    target_config_str: Optional[str] = None
    target_env: Optional[WorkspaceEnv] = None
    target_config: Optional[WorkspaceConfigType] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None
    target_app: Optional[str] = None

    # derive env/name/type/config from ws_filter
    if ws_filter is not None:
        if not isinstance(ws_filter, str):
            raise TypeError(
                f"Invalid workspace filter. Expected: str, Received: {type(ws_filter)}"
            )
        filters = ws_filter.split(":")
        # logger.debug(f"Filters: {filters}")
        num_filters = len(filters)
        if num_filters >= 1:
            target_env_str = filters[0]
        if num_filters >= 2:
            if filters[1] != "":
                target_app = filters[1]
        if num_filters >= 3:
            if filters[2] != "":
                target_name = filters[2]
        if num_filters >= 4:
            if filters[3] != "":
                target_type = filters[3]
        if num_filters >= 5:
            if filters[4] != "":
                target_config_str = filters[4]

    # derive env/app/name/type/config from command options
    if (
        target_env_str is None
        and env_filter is not None
        and isinstance(env_filter, str)
    ):
        target_env_str = env_filter
    if (
        target_config_str is None
        and config_filter is not None
        and isinstance(config_filter, str)
    ):
        target_config_str = config_filter
    if target_name is None and name_filter is not None and isinstance(name_filter, str):
        target_name = name_filter
    if target_type is None and type_filter is not None and isinstance(type_filter, str):
        target_type = type_filter
    if target_app is None and app_filter is not None and isinstance(app_filter, str):
        target_app = app_filter
    # logger.debug(f"app_filter: {type(app_filter)} | {app_filter}")

    # derive env/config/name/type from defaults
    if target_env_str is None:
        target_env_str = (
            active_ws_data.ws_config.default_env if active_ws_data.ws_config else None
        )
    if target_config_str is None:
        target_config_str = (
            active_ws_data.ws_config.default_config
            if active_ws_data.ws_config
            else None
        )

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

    if target_config_str is not None:
        if target_config_str.lower() not in WorkspaceConfigType.values_list():
            print_error(
                f"{target_config_str} is not supported, please choose from: {WorkspaceConfigType.values_list()}"
            )
            return
        target_config = cast(
            WorkspaceConfigType,
            WorkspaceConfigType.from_str(target_config_str),
        )

    logger.debug("Deploying workspace")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_config: {target_config}")
    logger.debug(f"\ttarget_name  : {target_name}")
    logger.debug(f"\ttarget_type  : {target_type}")
    logger.debug(f"\ttarget_app   : {target_app}")
    print_heading("Deploying workspace: {}\n".format(active_ws_data.ws_name))
    deploy_workspace(
        ws_data=active_ws_data,
        target_env=target_env,
        target_config=target_config,
        target_name=target_name,
        target_type=target_type,
        target_app=target_app,
        dry_run=dry_run,
        auto_confirm=auto_confirm,
    )


@ws_app.command(short_help="Shutdown your active workspace - does not delete any data")
def down(
    ws_filter: Optional[str] = typer.Argument(
        None,
        help="Filter the resources to shut down. Format - ENV:APP:NAME:TYPE:CONFIG",
        metavar="[filter]",
    ),
    env_filter: str = typer.Option(
        None,
        "-e",
        "--env",
        metavar="",
        help="Filter the environment to shut down. Available Options: {}".format(
            WorkspaceEnv.values_list()
        ),
    ),
    config_filter: str = typer.Option(
        None,
        "-c",
        "--config",
        metavar="",
        help="Filter the config to shut down. Available Options: {}".format(
            WorkspaceConfigType.values_list()
        ),
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    app_filter: Optional[str] = typer.Option(
        None, "-a", "--app", metavar="", help="Filter using app name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be shut down and exit.",
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
    Shuts down the active workspace but does not delete it.

    \b
    Examples:
    $ `phi ws down`
    """
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.workspace.ws_operator import shutdown_workspace

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
    target_config_str: Optional[str] = None
    target_env: Optional[WorkspaceEnv] = None
    target_config: Optional[WorkspaceConfigType] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None
    target_app: Optional[str] = None

    # derive env/config/name/type from ws_filter
    if ws_filter is not None:
        if not isinstance(ws_filter, str):
            raise TypeError(
                f"Invalid workspace filter. Expected: str, Received: {type(ws_filter)}"
            )
        filters = ws_filter.split(":")
        # logger.debug(f"Filters: {filters}")
        num_filters = len(filters)
        if num_filters >= 1:
            target_env_str = filters[0]
        if num_filters >= 2:
            if filters[1] != "":
                target_app = filters[1]
        if num_filters >= 3:
            if filters[2] != "":
                target_name = filters[2]
        if num_filters >= 4:
            if filters[3] != "":
                target_type = filters[3]
        if num_filters >= 5:
            if filters[4] != "":
                target_config_str = filters[4]

    # derive env/app/name/type/config from command options
    if (
        target_env_str is None
        and env_filter is not None
        and isinstance(env_filter, str)
    ):
        target_env_str = env_filter
    if (
        target_config_str is None
        and config_filter is not None
        and isinstance(config_filter, str)
    ):
        target_config_str = config_filter
    if target_name is None and name_filter is not None and isinstance(name_filter, str):
        target_name = name_filter
    if target_type is None and type_filter is not None and isinstance(type_filter, str):
        target_type = type_filter
    if target_app is None and app_filter is not None and isinstance(app_filter, str):
        target_app = app_filter

    # derive env/config/name/type from defaults
    if target_env_str is None:
        target_env_str = (
            active_ws_data.ws_config.default_env if active_ws_data.ws_config else None
        )
    if target_config_str is None:
        target_config_str = (
            active_ws_data.ws_config.default_config
            if active_ws_data.ws_config
            else None
        )

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

    if target_config_str is not None:
        if target_config_str.lower() not in WorkspaceConfigType.values_list():
            print_error(
                f"{target_config_str} is not supported, please choose from: {WorkspaceConfigType.values_list()}"
            )
            return
        target_config = cast(
            WorkspaceConfigType,
            WorkspaceConfigType.from_str(target_config_str),
        )

    logger.debug("Shutting down workspace")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_config: {target_config}")
    logger.debug(f"\ttarget_name  : {target_name}")
    logger.debug(f"\ttarget_type  : {target_type}")
    logger.debug(f"\ttarget_app   : {target_app}")
    print_heading("Shutdown workspace: {}\n".format(active_ws_data.ws_name))
    shutdown_workspace(
        ws_data=active_ws_data,
        target_env=target_env,
        target_config=target_config,
        target_name=target_name,
        target_type=target_type,
        target_app=target_app,
        dry_run=dry_run,
    )


@ws_app.command(short_help="Update your active workspace")
def patch(
    ws_filter: Optional[str] = typer.Argument(
        None,
        help="Filter the resources to patch. Format - ENV:APP:NAME:TYPE:CONFIG",
        metavar="[filter]",
    ),
    env_filter: str = typer.Option(
        None,
        "-e",
        "--env",
        metavar="",
        help="Filter the environment to patch. Available Options: {}".format(
            WorkspaceEnv.values_list()
        ),
    ),
    config_filter: str = typer.Option(
        None,
        "-c",
        "--config",
        metavar="",
        help="Filter the config to patch. Available Options: {}".format(
            WorkspaceConfigType.values_list()
        ),
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    app_filter: Optional[str] = typer.Option(
        None, "-a", "--app", metavar="", help="Filter using app name"
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Print which resources will be patched and exit.",
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
    Patch the active workspace.
    Filters can be used to limit patching by
        - Env (dev, stg, prd)
        - App name
        - Resource name
        - Resource type
        - Config type (docker, aws, k8s)
    \b
    Filters can be provided as a single argument as - ENV:APP:NAME:TYPE:CONFIG
    or using multiple options.
    Examples:
    \b
    $ `phi ws patch`           -> Patch default resources
    $ `phi ws patch dev`       -> Patch all dev resources
    $ `phi ws patch prd`       -> Patch all prd resources
    $ `phi ws patch prd:::aws` -> Patch all prd aws resources
    $ `phi ws patch prd::s3`   -> Patch prd resources with name s3
    """
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.workspace.ws_operator import patch_workspace

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
    target_config_str: Optional[str] = None
    target_env: Optional[WorkspaceEnv] = None
    target_config: Optional[WorkspaceConfigType] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None
    target_app: Optional[str] = None

    # derive env/name/type/config from ws_filter
    if ws_filter is not None:
        if not isinstance(ws_filter, str):
            raise TypeError(
                f"Invalid workspace filter. Expected: str, Received: {type(ws_filter)}"
            )
        filters = ws_filter.split(":")
        # logger.debug(f"Filters: {filters}")
        num_filters = len(filters)
        if num_filters >= 1:
            target_env_str = filters[0]
        if num_filters >= 2:
            if filters[1] != "":
                target_app = filters[1]
        if num_filters >= 3:
            if filters[2] != "":
                target_name = filters[2]
        if num_filters >= 4:
            if filters[3] != "":
                target_type = filters[3]
        if num_filters >= 5:
            if filters[4] != "":
                target_config_str = filters[4]

    # derive env/app/name/type/config from command options
    if (
        target_env_str is None
        and env_filter is not None
        and isinstance(env_filter, str)
    ):
        target_env_str = env_filter
    if (
        target_config_str is None
        and config_filter is not None
        and isinstance(config_filter, str)
    ):
        target_config_str = config_filter
    if target_name is None and name_filter is not None and isinstance(name_filter, str):
        target_name = name_filter
    if target_type is None and type_filter is not None and isinstance(type_filter, str):
        target_type = type_filter
    if target_app is None and app_filter is not None and isinstance(app_filter, str):
        target_app = app_filter

    # derive env/config/name/type from defaults
    if target_env_str is None:
        target_env_str = active_ws_data.ws_config.default_env
    if target_config_str is None:
        target_config_str = active_ws_data.ws_config.default_config

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

    if target_config_str is not None:
        if target_config_str.lower() not in WorkspaceConfigType.values_list():
            print_error(
                f"{target_config_str} is not supported, please choose from: {WorkspaceConfigType.values_list()}"
            )
            return
        target_config = cast(
            WorkspaceConfigType,
            WorkspaceConfigType.from_str(target_config_str),
        )

    logger.debug("Patching workspace")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_config: {target_config}")
    logger.debug(f"\ttarget_name  : {target_name}")
    logger.debug(f"\ttarget_type  : {target_type}")
    logger.debug(f"\ttarget_app   : {target_app}")
    print_heading("Patching workspace: {}\n".format(active_ws_data.ws_name))
    patch_workspace(
        ws_data=active_ws_data,
        target_env=target_env,
        target_config=target_config,
        target_name=target_name,
        target_type=target_type,
        target_app=target_app,
        dry_run=dry_run,
    )


@ws_app.command(short_help="Restart your active workspace")
def restart(
    ws_filter: Optional[str] = typer.Argument(
        None,
        help="Filter the resources to restart. Format - ENV:APP:NAME:TYPE:CONFIG",
        metavar="[filter]",
    ),
    env_filter: str = typer.Option(
        None,
        "-e",
        "--env",
        metavar="",
        help="Filter the environment to restart. Available Options: {}".format(
            WorkspaceEnv.values_list()
        ),
    ),
    config_filter: str = typer.Option(
        None,
        "-i",
        "--config",
        metavar="",
        help="Filter the config to restart. Available Options: {}".format(
            WorkspaceConfigType.values_list()
        ),
    ),
    name_filter: Optional[str] = typer.Option(
        None, "-n", "--name", metavar="", help="Filter using resource name"
    ),
    type_filter: Optional[str] = typer.Option(
        None,
        "-t",
        "--type",
        metavar="",
        help="Filter using resource type",
    ),
    app_filter: Optional[str] = typer.Option(
        None, "-a", "--app", metavar="", help="Filter using app name"
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
    Restarts the active workspace. i.e. runs `phi ws down` and then `phi ws up`.

    \b
    Examples:
    $ `phi ws restart`
    """
    from time import sleep

    down(
        ws_filter=ws_filter,
        env_filter=env_filter,
        config_filter=config_filter,
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
        dry_run=False,
        print_debug_log=print_debug_log,
    )
    print_info("Sleeping for 2 seconds..")
    sleep(2)
    up(
        ws_filter=ws_filter,
        env_filter=env_filter,
        config_filter=config_filter,
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
        dry_run=False,
        print_debug_log=print_debug_log,
    )
    print_info("Workspace restarted!")


@ws_app.command(short_help="Prints active workspace config")
def config(
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """\b
    Prints the active workspace config

    \b
    Examples:
    $ `phi ws config`         -> Print the active workspace config
    """
    from phiterm.conf.phi_conf import PhiConf, PhiWsData

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

    active_ws_data.print_to_cli()
