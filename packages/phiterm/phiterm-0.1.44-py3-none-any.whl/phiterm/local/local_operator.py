from os import environ
from pathlib import Path
from typing import Optional, Dict, List

from phidata import constants
from phidata.product import DataProduct
from phidata.workflow import Workflow
from phidata.task import Task
from phidata.workspace import WorkspaceConfig
from phidata.types.context import PathContext, RunContext

from phiterm.types.run_status import RunStatus
from phiterm.utils.cli_console import (
    print_info,
    print_heading,
    print_dict,
    print_info,
    print_subheading,
)
from phiterm.utils.log import logger
from phiterm.workspace.phi_ws_data import PhiWsData


def set_local_env(
    ws_config: WorkspaceConfig,
    path_context: PathContext,
) -> None:
    """VERY IMPORTANT TO RUN BEFORE RUNNING ANY LOCAL WORKFLOWS
    This function updates the local environment with Paths and Configuration
    Main uses:
        1. Path env variables used by DataAssets for building file_paths
        2. Cloud config variables used by AwsAssets like aws_region and profile
    """
    # 1. Path env variables used by DataAssets for building file_paths
    if path_context.scripts_dir is not None:
        environ[constants.SCRIPTS_DIR_ENV_VAR] = str(path_context.scripts_dir)
    if path_context.storage_dir is not None:
        environ[constants.STORAGE_DIR_ENV_VAR] = str(path_context.storage_dir)
    if path_context.meta_dir is not None:
        environ[constants.META_DIR_ENV_VAR] = str(path_context.meta_dir)
    if path_context.products_dir is not None:
        environ[constants.PRODUCTS_DIR_ENV_VAR] = str(path_context.products_dir)
    if path_context.notebooks_dir is not None:
        environ[constants.NOTEBOOKS_DIR_ENV_VAR] = str(path_context.notebooks_dir)
    if path_context.workspace_config_dir is not None:
        environ[constants.WORKSPACE_CONFIG_DIR_ENV_VAR] = str(
            path_context.workspace_config_dir
        )
    # 2. Cloud config variables used by AwsAssets like aws_region and profile
    if ws_config.aws_region is not None:
        environ[constants.AWS_REGION_ENV_VAR] = ws_config.aws_region
    if ws_config.aws_profile is not None:
        environ[constants.AWS_PROFILE_ENV_VAR] = ws_config.aws_profile
    if ws_config.aws_config_file is not None:
        environ[constants.AWS_CONFIG_FILE_ENV_VAR] = ws_config.aws_config_file
    if ws_config.aws_shared_credentials_file is not None:
        environ[
            constants.AWS_SHARED_CREDENTIALS_FILE_ENV_VAR
        ] = ws_config.aws_shared_credentials_file
    if ws_config.local_env:
        environ.update(ws_config.local_env)


def run_workflows_local(
    workflow_file: str,
    run_context: RunContext,
    ws_data: PhiWsData,
    workflows: Dict[str, Workflow],
    workflow_name: Optional[str] = None,
    tasks: Optional[Dict[str, Task]] = None,
    task_name: Optional[str] = None,
) -> bool:
    """
    Runs a Workflow/Task in the local environment

    Args:
        workflow_file: Path of the workflow file relative to the products_dir.
            This is used to build the path_context
        run_context: RunContext
        ws_data: PhiWsData
        workflows: Dict[str, Workflow] to run
        workflow_name: Name of workflow to run
        tasks:
        task_name: Name of task to run

    Returns:
        run_status (bool): True is the Workflow ran successfully
    """
    from phidata.utils.cli_console import print_run_status_table

    # Validate
    if ws_data.ws_config is None:
        logger.error("WorkspaceConfig invalid")
        return False
    if ws_data.ws_root_path is None:
        logger.error("Workspace directory invalid")
        return False

    # Step 1: Build the PathContext
    ws_config = ws_data.ws_config
    ws_root_path = ws_data.ws_root_path
    scripts_dir_path = ws_root_path.joinpath(ws_config.scripts_dir).resolve()
    storage_dir_path = ws_root_path.joinpath(ws_config.storage_dir).resolve()
    meta_dir_path = ws_root_path.joinpath(ws_config.meta_dir).resolve()
    products_dir_path = ws_root_path.joinpath(ws_config.products_dir).resolve()
    notebooks_dir_path = ws_root_path.joinpath(ws_config.notebooks_dir).resolve()
    workspace_config_dir_path = ws_root_path.joinpath(
        ws_config.workspace_config_dir
    ).resolve()
    workflow_file_path = Path(products_dir_path).joinpath(workflow_file)
    path_context: PathContext = PathContext(
        scripts_dir=scripts_dir_path,
        storage_dir=storage_dir_path,
        meta_dir=meta_dir_path,
        products_dir=products_dir_path,
        notebooks_dir=notebooks_dir_path,
        workspace_config_dir=workspace_config_dir_path,
        workflow_file=workflow_file_path,
    )
    logger.debug(f"PathContext: {path_context.json(indent=4)}")

    ######################################################################
    # Step 2: Update the local environment with Paths and Configuration
    # NOTE: VERY IMPORTANT TO RUN BEFORE RUNNING ANY LOCAL WORKFLOWS
    ######################################################################
    set_local_env(ws_config=ws_config, path_context=path_context)

    logger.debug("Running:")
    logger.debug(f"\tWorkflow: {workflow_name}")
    logger.debug(f"\tTask: {task_name}")

    # Step 3: If workflow_name or task_name is provided,
    # run single workflow or task
    if workflow_name is not None or task_name is not None:
        # workflow_name != "" means run a workflow
        if workflow_name is not None and workflow_name != "":
            workflow_to_run: Optional[Workflow] = workflows.get(workflow_name, None)
            if workflow_to_run is None:
                logger.error(
                    "Workflow `{}` not found in {}".format(
                        workflow_name, "[{}]".format(", ".join(workflows.keys()))
                    )
                )
                return False

            _name = workflow_to_run.name
            print_subheading(f"\nRunning Workflow: {_name}")
            # Pass down context
            workflow_to_run.run_context = run_context
            workflow_to_run.path_context = path_context
            wf_run_success = workflow_to_run.run_in_local_env(task_id=task_name)
            return wf_run_success

        # workflow_name == "" and task_name != "" means run a task
        elif (
            workflow_name == ""
            and task_name is not None
            and task_name != ""
            and tasks is not None
        ):
            task_to_run: Optional[Task] = tasks.get(task_name, None)
            if task_to_run is None:
                logger.error(
                    "Task `{}` not found in {}".format(
                        task_name, "[{}]".format(", ".join(tasks.keys()))
                    )
                )
                return False

            _name = task_to_run.name
            print_subheading(f"\nRunning Task: {_name}")
            # Pass down context
            task_to_run.run_context = run_context
            task_to_run.path_context = path_context
            task_run_success = task_to_run.run_in_local_env()
            return task_run_success

    # Step 4: If workflow_name is None and task_name is None
    # means this is a file with just workflows and no data products.
    # Run all workflows
    wf_run_status: List[RunStatus] = []
    for wf_name, wf_obj in workflows.items():
        _name = wf_name or wf_obj.name
        print_subheading(f"\nRunning Workflow: {_name}")
        # Pass down context
        wf_obj.run_context = run_context
        wf_obj.path_context = path_context
        wf_run_success = wf_obj.run_in_local_env()
        wf_run_status.append(RunStatus(name=_name, success=wf_run_success))

    print_run_status_table("Workflow Run Status", wf_run_status)
    for run_status in wf_run_status:
        if not run_status.success:
            return False
    return True


def run_data_products_local(
    workflow_file: str,
    data_products: Dict[str, DataProduct],
    run_context: RunContext,
    ws_data: PhiWsData,
) -> bool:
    """
    Runs a DataProduct in the local environment

    Args:
        workflow_file: Path of the workflow file relative to the products_dir.
            This is used to build the path_context
        data_products: Dict[str, DataProduct] to run
        run_context: RunContext
        ws_data: PhiWsData

    Returns:
        run_status (bool): True is the DataProduct ran successfully
    """
    from phidata.utils.cli_console import print_run_status_table

    # Validate
    if ws_data.ws_root_path is None:
        logger.error("Workspace directory invalid")
        return False
    if ws_data.ws_config is None:
        logger.error("WorkspaceConfig invalid")
        return False

    # Step 1: Build the PathContext for the DataProducts.
    ws_config = ws_data.ws_config
    ws_root_path = ws_data.ws_root_path
    scripts_dir_path = ws_root_path.joinpath(ws_config.scripts_dir).resolve()
    storage_dir_path = ws_root_path.joinpath(ws_config.storage_dir).resolve()
    meta_dir_path = ws_root_path.joinpath(ws_config.meta_dir).resolve()
    products_dir_path = ws_root_path.joinpath(ws_config.products_dir).resolve()
    notebooks_dir_path = ws_root_path.joinpath(ws_config.notebooks_dir).resolve()
    workspace_config_dir_path = ws_root_path.joinpath(
        ws_config.workspace_config_dir
    ).resolve()
    workflow_file_path = Path(products_dir_path).joinpath(workflow_file)
    dp_path_context: PathContext = PathContext(
        scripts_dir=scripts_dir_path,
        storage_dir=storage_dir_path,
        meta_dir=meta_dir_path,
        products_dir=products_dir_path,
        notebooks_dir=notebooks_dir_path,
        workspace_config_dir=workspace_config_dir_path,
        workflow_file=workflow_file_path,
    )
    logger.debug(f"PathContext: {dp_path_context.json(indent=4)}")

    ######################################################################
    # Step 2: Update the local environment with Paths and Configuration
    # NOTE: VERY IMPORTANT TO RUN BEFORE RUNNING ANY LOCAL WORKFLOWS
    ######################################################################
    set_local_env(ws_config=ws_config, path_context=dp_path_context)

    # Step 3: Run the DataProducts
    dp_run_status: List[RunStatus] = []
    for dp_name, dp_obj in data_products.items():
        _name = dp_name or dp_obj.name
        print_subheading(f"\nRunning DataProduct: {_name}")
        # Pass down context
        dp_obj.run_context = run_context
        dp_obj.path_context = dp_path_context
        run_success = dp_obj.run_in_local_env()
        dp_run_status.append(RunStatus(name=_name, success=run_success))

    print_run_status_table("DataProduct Run Status", dp_run_status)
    for run_status in dp_run_status:
        if not run_status.success:
            return False
    return True
