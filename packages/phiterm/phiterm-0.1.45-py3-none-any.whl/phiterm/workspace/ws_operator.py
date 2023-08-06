from pathlib import Path
from typing import List, Optional, cast
from typing_extensions import Literal

import git
import typer

from phidata.infra.base import InfraConfig
from phidata.infra.docker.config import DockerConfig
from phidata.infra.k8s.config import K8sConfig
from phidata.infra.aws.config import AwsConfig
from phidata.workspace import WorkspaceConfig

from phiterm.backend_api.workspace_api import update_workspace, upsert_workspace
from phiterm.conf.constants import DEFAULT_WS_NAME
from phiterm.conf.phi_conf import PhiConf, PhiWsData
from phiterm.enums.user_enums import VersionControlProviderEnum
from phiterm.utils.cli_console import (
    print_conf_not_available_msg,
    print_heading,
    print_info,
    print_subheading,
    print_warning,
)
from phiterm.utils.common import is_empty, str_to_int
from phiterm.utils.dttm import current_datetime_utc, dttm_to_dttm_str
from phiterm.utils.filesystem import rmdir_recursive
from phiterm.utils.git import GitCloneProgress, get_remote_origin_for_dir
from phiterm.utils.log import logger
from phiterm.workspace.template_to_repo_map import template_to_repo_map
from phiterm.workspace.ws_enums import (
    WorkspaceEnv,
    WorkspaceConfigType,
    WorkspaceStarterTemplate,
    WorkspaceVisibilityEnum,
)
from phiterm.workspace.exceptions import WorkspaceConfigException
from phiterm.workspace.ws_schemas import (
    UpdateWorkspace,
    UpsertWorkspaceFromCli,
    WorkspaceSchema,
)
from phiterm.workspace.ws_utils import (
    get_ws_config_file_path,
    is_valid_ws_config_file_path,
    print_howtofix_pending_actions,
)

# List of reserved workspace names
RESERVED_WS_NAMES = ["root", "bedi", "ashpreet", "ashpreetbedi"]


def create_new_workspace(ws_name: str, template: WorkspaceStarterTemplate) -> bool:
    """Creates a new workspace for the user.
    This function clones a phidata template on the users machine at the path:
        cwd/ws_name
    cwd: current working dir - where the command was ran from.

    Steps:
    1. Validate ws_name and if we can create a folder with that name
    2. Clone the starter template in cwd/ws_name
    3. Delete the .git folder
    4. Provide the user with steps to add a remote origin for this workspace

    NOTE: till the user runs `phi ws setup` the workspace is not registered with phidata
        and can only be used locally
    """

    current_dir: Path = Path(".").resolve()

    # Phidata should be initialized before creating a workspace
    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return False

    # Error if the workspace name provided is a reserved name
    if ws_name in RESERVED_WS_NAMES:
        logger.error(f"The name `{ws_name}` is reserved")
        return False

    # Check if a workspace with the same name exists
    _existing_ws_data: Optional[PhiWsData] = phi_conf.get_ws_data_by_name(ws_name)
    if _existing_ws_data is not None:
        logger.error(f"Found existing record for a workspace: {ws_name}")
        print_info(
            f"\nNote: If you would like to setup the workspace instead, run `phi ws setup` from the workspace directory"
        )
        delete_existing_ws_data = typer.confirm(
            f"Would you like to delete existing workspace data and create a new workspace?",
            default=True,
        )
        if delete_existing_ws_data:
            phi_conf.delete_ws(ws_name)
        else:
            return False

    # Check if we can create the workspace in the current dir
    ws_root_path: Path = current_dir.joinpath(ws_name)
    if ws_root_path.exists():
        logger.error(
            f"Directory {ws_root_path} exists, please delete manually or choose another name for workspace"
        )
        return False

    print_info(f"Creating {str(ws_root_path)}")
    # Clone the starter repo for this cloud in the new directory
    repo_to_clone = template_to_repo_map.get(template)
    logger.debug("Cloning: {}".format(repo_to_clone))
    try:
        _cloned_git_repo: git.Repo = git.Repo.clone_from(
            repo_to_clone, str(ws_root_path), progress=GitCloneProgress()  # type: ignore
        )
    except Exception as e:
        logger.error(e)
        return False

    # Remove existing .git folder
    _dot_git_folder = ws_root_path.joinpath(".git")
    _dot_git_exists = _dot_git_folder.exists()
    if _dot_git_exists:
        # logger.debug(".git folder exists... deleting")
        _dot_git_exists = not rmdir_recursive(_dot_git_folder)
    # logger.debug(f"_dot_git_exists: {_dot_git_exists}")

    # validate that a workspace config file exists
    ws_config_file_path: Path = get_ws_config_file_path(ws_root_path)
    # logger.debug(
    #     "Checking if workspace config file exists: {}".format(ws_config_file_path)
    # )
    if not (ws_config_file_path.exists() and ws_config_file_path.is_file()):
        logger.error(f"Could not find workspace config at: {ws_config_file_path}")
        return False

    phi_conf.add_new_created_ws_to_config(
        ws_name=ws_name,
        ws_root_path=ws_root_path,
        ws_config_file_path=ws_config_file_path,
    )
    print_info(f"Your new workspace is available at {str(ws_root_path)}\n")
    return setup_workspace(ws_root_path=ws_root_path)


def print_git_setup(
    ws_name: str,
    ws_root_path: Path,
    version_control_provider: Optional[
        VersionControlProviderEnum
    ] = VersionControlProviderEnum.GITHUB,
) -> None:
    """Prints commands to setup a remote git repo for a workspace"""

    # Check if a remote origin is available
    _remote_origin_url: Optional[str] = get_remote_origin_for_dir(ws_root_path)
    # logger.debug("_remote_origin_url: {}".format(_remote_origin_url))
    if _remote_origin_url:
        print_info(f"Remote origin already set: {_remote_origin_url}")
        return

    create_new_git_repo_url = "https://github.com/new"
    create_remote_repo_url: str
    # TODO: Add more repo urls
    if version_control_provider == VersionControlProviderEnum.GITHUB:
        create_remote_repo_url = create_new_git_repo_url
    else:
        create_remote_repo_url = create_new_git_repo_url

    print_subheading(f"\nSteps to setup a git repo for workspace: {ws_name}")
    print_info(f"\nCreate a new git repo named {ws_name} at {create_remote_repo_url}")
    print_info(
        f"Then follow the following steps to initialize the directory {ws_name} as a git repo and run git push"
    )
    print_info(
        f"NOTE: These steps will be provided by your version control provider (github, gitlab..), but would look something like:"
    )
    print_info(f"       git init")
    print_info(f"       git add .")
    print_info(f"       git commit -m 'Init Phidata Workspace'")
    print_info(f"       git branch -M main")
    print_info(
        f"       git remote add origin https://github.com/<USERNAME>/{ws_name}.git"
    )
    print_info(f"       git push -u origin main")
    print_info(f"Run `phi ws setup` after running git push to update your workspace\n")

    _open_browser = typer.confirm(
        f"Would you like to open your browser to visit: {create_remote_repo_url}\n-->"
    )
    if _open_browser:
        typer.launch(create_remote_repo_url)


def clone_workspace(ws_to_clone: WorkspaceSchema, phi_conf: PhiConf) -> None:
    """Clones an available phidata workspace on the users machine. To clone a ws, the PhiConf
    already has the ws_data and ws_schema available. We then update the
    ws_root_path and ws_config_file_path in the ws_data. After updating the
    path, we're call setup_workspace() to go through our usual setup flow
    """

    # Check if we can create the workspace in the current dir
    current_dir: Path = Path("../../workspace").resolve()
    logger.debug(f"current_dir: {current_dir}")
    ws_root_path: Path = current_dir.joinpath(ws_to_clone.name)
    if ws_root_path.exists():
        logger.error(
            f"{ws_root_path} already exists, please choose another ws to clone or delete the existing dir and run `phi ws init` again"
        )
        return

    print_info(f"Creating {str(ws_root_path)}")
    # Clone the workspace repo in ws_root_path
    repo_to_clone = ws_to_clone.git_url
    _cloned_git_repo: git.Repo = git.Repo.clone_from(
        repo_to_clone, str(ws_root_path), progress=GitCloneProgress()  # type: ignore
    )
    # Validate ws_root_path exists and is a directory
    if not (ws_root_path.exists() and ws_root_path.is_dir()):
        logger.error(f"Could not clone workspace, please try again")
        return
    # Get ws_config_file_path and validate
    ws_config_file_path: Path = get_ws_config_file_path(ws_root_path)
    if not (ws_config_file_path.exists() and ws_config_file_path.is_file()):
        logger.error(f"Could not find workspace config at: {ws_config_file_path}")
        return
    # Update the ws_data in PhiConf
    phi_conf.update_ws_data_for_cloned_ws(
        ws_name=ws_to_clone.name,
        ws_root_path=ws_root_path,
        ws_config_file_path=ws_config_file_path,
    )
    setup_workspace(ws_root_path)


def create_workspace_using_input():
    """Takes input from the user and calls create_new_workspace()
    This function acts as an intermediary between initialize_workspace() and create_new_workspace()
    """

    # Get workspace name from user
    ws_name_inp_raw = input(f"Workspace name (default: {DEFAULT_WS_NAME}): ")
    if is_empty(ws_name_inp_raw):
        ws_name_inp_raw = DEFAULT_WS_NAME

    # Display available starter templates and ask user to select one
    print_info("Select Starter Template (default: aws)")
    templates = WorkspaceStarterTemplate.values_list()
    for idx, prvdr in enumerate(templates, start=1):
        print_info("  [{}] {}".format(idx, prvdr))

    # Get starter template from the user
    template_inp_raw = input("--> ")
    # Convert input to int value.
    template_inp = str_to_int(template_inp_raw)
    template: WorkspaceStarterTemplate = WorkspaceStarterTemplate.aws

    if template_inp is not None:
        try:
            template = cast(
                WorkspaceStarterTemplate,
                WorkspaceStarterTemplate.from_str(templates[template_inp - 1]),
            )
        except Exception as e:
            logger.error(e)

    logger.debug("Selected: {}".format(template.value))
    print_info(
        f"Creating workspace {ws_name_inp_raw} using the {template.value} template\n"
    )
    create_new_workspace(ws_name_inp_raw, template)


def initialize_workspace() -> None:
    """Initialize a phidata workspace.
    This function is called by `phi ws init` to create/clone a new workspace.
    """
    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    # TODO: uncomment when backend is live
    # available_ws = phi_conf.available_ws
    # if available_ws:
    #     print_info("Would you like to:")
    #     print_info("  [1] Create a new workspace")
    #     print_info("  [2] Clone an existing workspace")
    #     print_info("  [3] Enter any other key to exit")
    #     ws_inp_raw = input("--> ")
    #     ws_inp_int = str_to_int(ws_inp_raw)
    #     if ws_inp_int == 1:
    #         create_workspace_using_input()
    #     elif ws_inp_int == 2:
    #         print_info("\nSelect workspace to clone:")
    #         for idx, avl_ws in enumerate(available_ws, start=1):
    #             print_info("  [{}] {}".format(idx, avl_ws.name))
    #         clone_ws_inp_raw = input("--> ")
    #         clone_ws_inp_int = str_to_int(clone_ws_inp_raw)
    #         if clone_ws_inp_int:
    #             ws_to_clone = available_ws[clone_ws_inp_int - 1]
    #             clone_workspace(ws_to_clone, phi_conf)
    #         return
    #     return
    # else:
    print_heading("Creating a new workspace")
    create_workspace_using_input()


def setup_workspace(ws_root_path: Path) -> bool:
    """Set-up a phidata workspace at directory: `ws_root_path`.
    This is the catchall function for a workspace. Run it in a directory and it
    should figure everything out.

    1. Validate pre-requisites
    1.1 Check ws_root_path is valid
    1.2 Check PhiConf is valid
    1.3 Validate PhiWsData is available
        Get the ws_data using the ws_root_path
        If ws_data is None, read the ws_config_file_path to map it to an available workspace
            This may happen if the user ran `phi init -r`
        If the user cloned this directory directly, there will be no record of this workspace in the PhiConf
        In that case, we manually add the ws to PhiConf and process the ws_config_file_path and setup this workspace.
    1.4 Check if this is the active workspace or if it needs to be set as active
    1.5 Check if remote origin is available

    2. Create or Update WorkspaceSchema
    If a ws_schema exists for this workspace, this workspace has been setup before
    2.1 Create WorkspaceSchema for a NEWLY CREATED WORKSPACE
        If ws_schema is None, this is a NEWLY CREATED WORKSPACE.
        i.e. A new workspace was created using create_new_workspace() <- which is called using `phi ws init`.
        This ws doesnt yet have a ws_schema, make an api call to zeus to create one.
        If the api call returns None, then we could not create the workspace and we exit
    2.2 Update WorkspaceSchema if remote origin has been updated
    2.3 Set as active if needed
    2.4 Refresh PhiWsData

    3. Complete Workspace setup
    3.1 Validate ws_config_file_path
    3.2 Validate PhiWsData
        Reaching here implies a all ws_data is available and updated.
        Validate the ws_data and print any pending setup actions.

    `phi ws setup` is a generic catch-all function. It should handle errors graciously
    and provide "how to fix" messages and "next steps" to get the user running.
    """

    print_heading("Running workspace setup\n")

    ######################################################
    ## 1. Validate Pre-requisites
    ######################################################
    ######################################################
    # 1.1 Check ws_root_path is valid
    ######################################################
    _ws_is_valid: bool = (
        ws_root_path is not None and ws_root_path.exists() and ws_root_path.is_dir()
    )
    if not _ws_is_valid:
        logger.error("Invalid directory: {}".format(ws_root_path))
        return False

    ######################################################
    # 1.2 Check PhiConf is valid
    ######################################################
    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return False

    ######################################################
    # 1.3 Validate PhiWsData is available
    ######################################################
    logger.debug(f"Checking for a workspace at {ws_root_path}")
    ws_data: Optional[PhiWsData] = phi_conf.get_ws_data_by_path(ws_root_path)
    if ws_data is None:
        # This happens if
        # - The user is setting up an existing workspace
        # - the user ran `phi init -r` which erases the self._path_to_ws_data_map
        logger.debug(f"Could not find an existing workspace at path: {ws_root_path}")
        # We'll try to parse this workspace using the workspace config
        # validate that a workspace config file exists
        __ws_config_file_path: Path = get_ws_config_file_path(ws_root_path)

        # In this case, the local workspace directory exists but PhiConf does not have a record
        print_info(f"Adding {ws_root_path} as a workspace")
        phi_conf.add_new_created_ws_to_config(
            ws_name=ws_root_path.stem,
            ws_root_path=ws_root_path,
            ws_config_file_path=__ws_config_file_path,
        )
        ws_data = phi_conf.get_ws_data_by_path(ws_root_path)
        # If the ws_data is still none it means the workspace has bad data in it
        if ws_data is None:
            logger.error(f"Could not create workspace")
            print_info(f"Workspace Dir     : {ws_root_path}")
            print_info(f"Workspace Config   : {__ws_config_file_path}")
            logger.error("Please try again")
            return False
    else:
        logger.debug(f"Found workspace {ws_data.ws_name}")
        phi_conf.refresh_ws_config(ws_data.ws_name)

    ######################################################
    # 1.4 Set workspace as active if needed
    ######################################################
    set_as_active_ws = False

    # If this is the users first workspace i.e. No active_ws is available, then set as active_ws
    if phi_conf.active_ws_name is None:
        set_as_active_ws = True
    # otherwise, ask the user if this should be the active ws
    elif phi_conf.active_ws_name != ws_data.ws_name:
        _set_as_active_ws_inp = typer.confirm(
            f"Would you like to set this as your active workspace",
            default=True,
        )
        if _set_as_active_ws_inp:
            set_as_active_ws = True

    if set_as_active_ws:
        phi_conf.active_ws_name = ws_data.ws_name

    ######################################################
    # 1.5 Check if remote origin is available
    ######################################################
    _remote_origin_url: Optional[str] = get_remote_origin_for_dir(ws_root_path)
    logger.debug("Remote_origin_url: {}".format(_remote_origin_url))

    # TODO: uncomment this block when the backend is up and running
    ######################################################
    ## 2. Create or Update WorkspaceSchema
    ######################################################
    # If a ws_schema exists for this workspace, this workspace has been setup before
    # ws_schema: Optional[WorkspaceSchema] = ws_data.ws_schema

    ######################################################
    # 2.1 Create WorkspaceSchema for a NEWLY CREATED WORKSPACE
    ######################################################
    # if ws_schema is None:
    #     # If ws_schema is None, this is a NEWLY CREATED WORKSPACE.
    #     # We make a call to the backend to create a new ws_schema
    #     logger.debug("ws_schema not found, trying to create one... ")
    #     logger.debug("ws_name: {}".format(ws_data.ws_name))
    #     logger.debug("set_as_active_ws: {}".format(_is_active_ws))
    #
    #     ws_schema = upsert_workspace(
    #         UpsertWorkspaceFromCli(
    #             name=ws_data.ws_name,
    #             visibility=WorkspaceVisibilityEnum.PRIVATE.value,
    #             git_url=_remote_origin_url,
    #             setup_complete=True,
    #             extra_data={"upserted_at": dttm_to_dttm_str(current_datetime_utc())},
    #             is_active_ws_for_user=_is_active_ws,
    #             only_create=True,
    #         )
    #     )
    #     if ws_schema is not None:
    #         phi_conf.update_ws_schema_for_workspace(
    #             ws_schema=ws_schema, set_as_active=_is_active_ws
    #         )

    ######################################################
    # 2.2 Update WorkspaceSchema if available
    ######################################################
    # if ws_schema is not None:
    #     if _remote_origin_url is not None and _remote_origin_url != ws_schema.git_url:
    #         print_info(f"Updating workspace git origin to: {_remote_origin_url}")
    #         ws_schema_updated = update_workspace(
    #             UpdateWorkspace(
    #                 id_workspace=ws_schema.id_workspace,
    #                 git_url=_remote_origin_url,
    #             )
    #         )
    #         if ws_schema_updated is not None:
    #             # Update the ws_schema for this workspace.
    #             phi_conf.update_ws_data(
    #                 ws_name=ws_schema.name,
    #                 ws_schema=ws_schema_updated,
    #             )
    #         else:
    #             logger.error()(
    #                 "Could not update git origin, please run `phi ws setup` again"
    #             )
    #         logger.debug(f"WorkspaceSchema git url updated to: {ws_schema.git_url}")

    ######################################################
    # 2.3 Refresh PhiWsData
    ######################################################
    # Refresh ws_data because phi_conf.update_ws_schema_for_workspace() or phi_conf.update_ws_data()
    # will create a new ws_data object in PhiConf
    # Also, cast it to PhiWsData because ws_data is no longer Optional[PhiWsData]
    ws_data = cast(PhiWsData, phi_conf.get_ws_data_by_name(ws_data.ws_name))

    ######################################################
    ## 3. Complete Workspace setup
    ######################################################

    ######################################################
    # 3.1 Validate ws_config_file_path
    ######################################################
    _ws_config_file_path: Optional[Path] = ws_data.ws_config_file_path
    if not is_valid_ws_config_file_path(_ws_config_file_path):
        logger.error("Could not validate workspace config")
        return False

    ######################################################
    # 3.2 Validate PhiWsData
    ######################################################
    ws_is_valid, pending_actions = phi_conf.validate_workspace(ws_name=ws_data.ws_name)

    if ws_is_valid and ws_data.ws_config is not None:
        scripts_dir = ws_data.ws_config.scripts_dir
        install_deps_file = f"sh {ws_root_path}/{scripts_dir}/install.sh"
        print_subheading(f"Setup complete! Next steps:\n")
        print_info("1. Update your workspace config:")
        print_info(f"\t{str(_ws_config_file_path)}")
        print_info("2. Install your workspace:")
        print_info(f"\t{install_deps_file}")
        print_info("3. Dry-run workspace deploy:")
        print_info("\tphi ws up -dr")
        print_info("4. Deploy your workspace:")
        print_info("\tphi ws up")
        # if pending_actions and len(pending_actions) > 0:
        #     print_info("3. Complete pending actions:")
        #     print_howtofix_pending_actions(pending_actions)
        return True
    else:
        print_info(f"Workspace setup pending.")
        print_howtofix_pending_actions(pending_actions)
        return False

    ######################################################
    ## End Workspace setup
    ######################################################


def filter_and_prep_configs(
    ws_data: PhiWsData,
    target_env: Optional[WorkspaceEnv] = None,
    target_config: Optional[WorkspaceConfigType] = None,
    order: Literal["create", "delete"] = "create",
) -> List[InfraConfig]:

    ws_config: WorkspaceConfig = ws_data.ws_config

    # Step 1. Filter configs
    # 1.1: Filter by config type: docker/k8s/aws
    filtered_configs: List[InfraConfig] = []
    if target_config is None:
        if ws_config.docker is not None:
            filtered_configs.extend(ws_config.docker)
        if order == "delete":
            if ws_config.k8s is not None:
                filtered_configs.extend(ws_config.k8s)
            if ws_config.aws is not None:
                filtered_configs.extend(ws_config.aws)
        else:
            if ws_config.aws is not None:
                filtered_configs.extend(ws_config.aws)
            if ws_config.k8s is not None:
                filtered_configs.extend(ws_config.k8s)
    elif target_config == WorkspaceConfigType.docker:
        if ws_config.docker is not None:
            filtered_configs.extend(ws_config.docker)
        else:
            logger.error("No DockerConfig provided")
    elif target_config == WorkspaceConfigType.k8s:
        if ws_config.k8s is not None:
            filtered_configs.extend(ws_config.k8s)
        else:
            logger.error("No K8sConfig provided")
    elif target_config == WorkspaceConfigType.aws:
        if ws_config.aws is not None:
            filtered_configs.extend(ws_config.aws)
        else:
            logger.error("No AwsConfig provided")

    # 1.2: Filter by env: dev/stg/prd
    configs_after_env_filter: List[InfraConfig] = []
    if target_env is None or target_env == WorkspaceEnv.all:
        configs_after_env_filter = filtered_configs
    else:
        for config in filtered_configs:
            if config.env is None:
                continue
            if config.env.lower() not in WorkspaceEnv.values_list():
                logger.error(f"{config.env} not supported")
                continue
            config_env = WorkspaceEnv.from_str(config.env)

            if config_env == target_env:
                configs_after_env_filter.append(config)
    # logger.debug("Filtered configs: {}".format(configs_after_env_filter))

    # Step 2. Prepare configs
    for config in configs_after_env_filter:
        if not isinstance(config, InfraConfig):
            logger.error(f"{config} is not an instance of InfraConfig")
            continue
        if not config.is_valid():
            logger.error("Config invalid")
            continue
        if not config.enabled:
            logger.debug(
                f"{config.__class__.__name__} for env {config.__class__.env} disabled"
            )
            continue

        ######################################################################
        # NOTE: VERY IMPORTANT TO GET RIGHT
        # Update subconfigs using the WorkspaceConfig
        # 1. Pass down the paths from the WorkspaceConfig
        #       These paths are used everywhere from Infra, Apps, Resources, Workflows
        # 2. Pass down local_env, docker_env, k8s_env for building PhidataApps
        # 3. Pass down common cloud configuration. eg: aws_region, aws_profile
        ######################################################################

        # -*- Path parameters
        # The ws_root_path is the ROOT directory for the workspace
        config.workspace_root_path = ws_data.ws_root_path
        config.workspace_config_file_path = ws_data.ws_config_file_path
        config.scripts_dir = ws_config.scripts_dir
        config.storage_dir = ws_config.storage_dir
        config.meta_dir = ws_config.meta_dir
        config.products_dir = ws_config.products_dir
        config.notebooks_dir = ws_config.notebooks_dir
        config.workspace_config_dir = ws_config.workspace_config_dir

        # -*- Environment parameters
        # only update the param if they are not available.
        # prefer the configs param if provided
        if config.local_env is None and ws_config.local_env is not None:
            config.local_env = ws_config.local_env
        if config.docker_env is None and ws_config.docker_env is not None:
            config.docker_env = ws_config.docker_env
        if config.k8s_env is None and ws_config.k8s_env is not None:
            config.k8s_env = ws_config.k8s_env

        # -*- AWS parameters
        # only update the param if they are available.
        # prefer the configs param if provided
        if config.aws_region is None and ws_config.aws_region is not None:
            config.aws_region = ws_config.aws_region
        if config.aws_profile is None and ws_config.aws_profile is not None:
            config.aws_profile = ws_config.aws_profile
        if config.aws_config_file is None and ws_config.aws_config_file is not None:
            config.aws_config_file = ws_config.aws_config_file
        if (
            config.aws_shared_credentials_file is None
            and ws_config.aws_shared_credentials_file is not None
        ):
            config.aws_shared_credentials_file = ws_config.aws_shared_credentials_file

    # Return filtered and prepared configs
    return configs_after_env_filter


def deploy_workspace(
    ws_data: PhiWsData,
    target_env: Optional[WorkspaceEnv] = None,
    target_config: Optional[WorkspaceConfigType] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
    target_app: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> None:
    """Deploy a Phidata Workspace. This is called from `phi ws up`"""

    if ws_data is None or ws_data.ws_config is None:
        logger.error("WorkspaceConfig invalid")
        return

    configs_to_deploy: List[InfraConfig] = filter_and_prep_configs(
        ws_data=ws_data,
        target_env=target_env,
        target_config=target_config,
        order="create",
    )

    num_configs_to_deploy = len(configs_to_deploy)
    num_configs_deployed = 0
    for config in configs_to_deploy:
        logger.debug(f"Deploying {config.__class__.__name__}")
        if isinstance(config, DockerConfig):
            from phiterm.docker.docker_operator import deploy_docker_config

            deploy_docker_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_deployed += 1
        if isinstance(config, K8sConfig):
            from phiterm.k8s.k8s_operator import deploy_k8s_config

            deploy_k8s_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_deployed += 1
        if isinstance(config, AwsConfig):
            from phiterm.aws.aws_operator import deploy_aws_config

            deploy_aws_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_deployed += 1
        # white space between runs
        print_info("")

    print_info(f"# Configs deployed: {num_configs_deployed}/{num_configs_to_deploy}\n")
    if num_configs_to_deploy == num_configs_deployed:
        if not dry_run:
            print_subheading("Workspace deploy success")
    else:
        logger.error("Workspace deploy failed")


def shutdown_workspace(
    ws_data: PhiWsData,
    target_env: Optional[WorkspaceEnv] = None,
    target_config: Optional[WorkspaceConfigType] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
    target_app: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> None:
    """Shutdown the Phidata Workspace. This is called from `phi ws down`"""

    if ws_data is None or ws_data.ws_config is None:
        logger.error("WorkspaceConfig invalid")
        return

    configs_to_shutdown: List[InfraConfig] = filter_and_prep_configs(
        ws_data=ws_data,
        target_env=target_env,
        target_config=target_config,
        order="delete",
    )

    num_configs_to_shutdown = len(configs_to_shutdown)
    num_configs_shutdown = 0
    for config in configs_to_shutdown:
        logger.debug(f"Shutting down {config.__class__.__name__}")
        if isinstance(config, DockerConfig):
            from phiterm.docker.docker_operator import shutdown_docker_config

            shutdown_docker_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_shutdown += 1
        if isinstance(config, K8sConfig):
            from phiterm.k8s.k8s_operator import shutdown_k8s_config

            shutdown_k8s_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_shutdown += 1
        if isinstance(config, AwsConfig):
            from phiterm.aws.aws_operator import shutdown_aws_config

            shutdown_aws_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_shutdown += 1
        # white space between runs
        print_info("")

    print_info(
        f"\n# Configs shutdown: {num_configs_shutdown}/{num_configs_to_shutdown}"
    )
    if num_configs_to_shutdown == num_configs_shutdown:
        if not dry_run:
            print_subheading("Workspace shutdown success")
    else:
        print_subheading("Workspace shutdown failed")


def patch_workspace(
    ws_data: PhiWsData,
    target_env: Optional[WorkspaceEnv] = None,
    target_config: Optional[WorkspaceConfigType] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
    target_app: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> None:
    """Patch the Phidata Workspace. This is called from `phi ws patch`"""

    if ws_data is None or ws_data.ws_config is None:
        logger.error("WorkspaceConfig invalid")
        return

    configs_to_patch: List[InfraConfig] = filter_and_prep_configs(
        ws_data=ws_data,
        target_env=target_env,
        target_config=target_config,
        order="create",
    )

    num_configs_to_patch = len(configs_to_patch)
    num_configs_patched = 0
    for config in configs_to_patch:
        logger.debug(f"Patching {config.__class__.__name__}")
        if isinstance(config, DockerConfig):
            from phiterm.docker.docker_operator import patch_docker_config

            patch_docker_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_patched += 1
        if isinstance(config, K8sConfig):
            from phiterm.k8s.k8s_operator import patch_k8s_config

            patch_k8s_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_patched += 1
        if isinstance(config, AwsConfig):
            from phiterm.aws.aws_operator import patch_aws_config

            patch_aws_config(
                config=config,
                name_filter=target_name,
                type_filter=target_type,
                app_filter=target_app,
                dry_run=dry_run,
                auto_confirm=auto_confirm,
            )
            num_configs_patched += 1
        # white space between runs
        print_info("")

    print_info(f"\n# Configs patched: {num_configs_patched}/{num_configs_to_patch}")
    if num_configs_to_patch == num_configs_patched:
        if not dry_run:
            print_subheading("Workspace patch success")
    else:
        print_subheading("Workspace patch failed")


def init_workspace_data(ws_schema: WorkspaceSchema, phi_conf: PhiConf):
    """Initializes workspace data like cloud projects"""

    logger.debug("*=* Initializing workspace data for: {}".format(ws_schema.name))
    logger.debug("TO_BE_IMPLEMENTED")
    logger.debug("*=* Workspace data init complete: {}".format(ws_schema.name))


def set_workspace_as_active(ws_name: Optional[str], refresh: bool = True) -> bool:

    ######################################################
    ## 1. Validate Pre-requisites
    ######################################################
    ######################################################
    # 1.1 Check PhiConf is valid
    ######################################################
    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return False

    ######################################################
    # 1.2 Check ws_root_path is valid
    ######################################################
    # By default, we assume this command is run from the workspace directory
    ws_root_path: Optional[Path] = None
    if ws_name is None:
        # If the user does not provide a ws_name, that implies `phi set` is ran from
        # the workspace directory.
        ws_root_path = Path(".").resolve()
    else:
        # If the user provides a workspace name manually, we find the dir for that ws
        ws_root_path = phi_conf.get_ws_root_path_by_name(ws_name)
        if ws_root_path is None:
            logger.error(f"Could not find workspace {ws_name}")
            return False

    ws_dir_is_valid: bool = (
        ws_root_path is not None and ws_root_path.exists() and ws_root_path.is_dir()
    )
    if not ws_dir_is_valid:
        logger.error("Invalid workspace directory: {}".format(ws_root_path))
        return False

    ######################################################
    # 1.3 Validate PhiWsData is available i.e. a workspace is available at this directory
    ######################################################
    logger.debug(f"Checking for a workspace at path: {ws_root_path}")
    active_ws_data: Optional[PhiWsData] = phi_conf.get_ws_data_by_path(ws_root_path)
    if active_ws_data is None:
        # This happens when the workspace is not yet setup
        print_info(f"Could not find a workspace at path: {ws_root_path}")
        print_info(
            f"If this workspace has not been setup, please run `phi ws setup` from the workspace directory"
        )
        return False

    new_active_ws_name: str = active_ws_data.ws_name
    print_heading(f"Setting workspace {new_active_ws_name} as active")
    if refresh:
        try:
            phi_conf.refresh_ws_config(new_active_ws_name)
        except WorkspaceConfigException as e:
            logger.error(
                "Could not refresh workspace config, please fix errors and try again"
            )
            logger.error(e)
            return False

    ######################################################
    # 1.4 Check if this is already the active workspace
    ######################################################
    current_active_ws_name = phi_conf.active_ws_name
    if new_active_ws_name != current_active_ws_name:
        # If a ws_schema exists for this workspace, this workspace has been authenticated
        # with the backend. In this case we need to send an API request to update
        # the active workspace for this user
        ws_schema: Optional[WorkspaceSchema] = active_ws_data.ws_schema
        if ws_schema is not None:
            print_info("Updating active workspace with the backend")
            # If ws_schema is None, this is a local workspace

    ######################################################
    ## 2. Set workspace as active
    ######################################################
    phi_conf.active_ws_name = new_active_ws_name
    print_info("Active workspace updated")
    return True
