from typing import List, Optional, cast, Dict, Any
from pathlib import Path

from docker.models.containers import Container
from phidata.infra.docker.api_client import DockerApiClient
from phidata.infra.docker.config import DockerConfig
from phidata.infra.docker.exceptions import DockerConfigException
from phidata.infra.docker.manager import DockerManager
from phidata.infra.docker.utils.container import execute_command
from phidata.product import DataProduct
from phidata.task import Task
from phidata.workflow import Workflow
from phidata.types.context import PathContext, RunContext

from phiterm.types.run_status import RunStatus
from phiterm.utils.cli_console import (
    print_error,
    print_heading,
    print_info,
    print_warning,
    print_subheading,
)
from phiterm.utils.log import logger


def deploy_docker_config(
    config: DockerConfig,
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    app_filter: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> bool:

    # Step 1: Get the DockerManager
    docker_manager: DockerManager = config.get_docker_manager()
    if docker_manager is None:
        raise DockerConfigException("DockerManager unavailable")
    print_heading(f"--**-- Docker env: {config.env}\n")

    # Step 2: If dry_run, print the resources and return True
    if dry_run:
        docker_manager.create_resources_dry_run(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        return True

    # Step 3: Create resources
    try:
        success: bool = docker_manager.create_resources(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        if not success:
            return False
    except Exception as e:
        logger.error(e)
        return False

    # Step 4: Validate resources are created
    resource_creation_valid: bool = docker_manager.validate_resources_are_created(
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
    )
    if not resource_creation_valid:
        logger.error("DockerResource creation could not be validated")
        return False

    print_info("Docker config deployed")
    return True


def shutdown_docker_config(
    config: DockerConfig,
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    app_filter: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> bool:

    # Step 1: Get the DockerManager
    docker_manager: DockerManager = config.get_docker_manager()
    if docker_manager is None:
        raise DockerConfigException("DockerManager unavailable")
    print_heading(f"--**-- Docker env: {config.env}\n")

    # Step 2: If dry_run, print the resources and return True
    if dry_run:
        docker_manager.delete_resources_dry_run(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        return True

    # Step 3: Delete resources
    try:
        success: bool = docker_manager.delete_resources(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        if not success:
            return False
    except Exception as e:
        logger.error(e)
        return False

    # Step 4: Validate resources are delete
    resources_deletion_valid: bool = docker_manager.validate_resources_are_deleted(
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
    )
    if not resources_deletion_valid:
        logger.error("DockerResource deletion could not be validated")
        return False

    print_info("Docker config shut down")
    return True


def patch_docker_config(
    config: DockerConfig,
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    app_filter: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> bool:

    # Step 1: Get the DockerManager
    docker_manager: DockerManager = config.get_docker_manager()
    if docker_manager is None:
        raise DockerConfigException("DockerManager unavailable")
    print_heading(f"--**-- Docker env: {config.env}\n")

    # Step 2: If dry_run, print the resources and return True
    if dry_run:
        docker_manager.patch_resources_dry_run(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        return True

    # Step 3: Patch resources
    try:
        success: bool = docker_manager.patch_resources(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        if not success:
            return False
    except Exception:
        raise

    # Step 4: Validate resources are patched
    resources_patch_valid: bool = docker_manager.validate_resources_are_deleted(
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
    )
    if not resources_patch_valid:
        logger.error("DockerResource patch could not be validated")
        return False

    print_info("Docker config patched")
    return True


def run_workflows_docker(
    workflow_file: str,
    run_context: RunContext,
    docker_config: DockerConfig,
    workflows: Dict[str, Workflow],
    workflow_name: Optional[str] = None,
    tasks: Optional[Dict[str, Task]] = None,
    task_name: Optional[str] = None,
    target_app: Optional[str] = None,
    dag_id: Optional[str] = None,
) -> bool:
    from phidata.utils.cli_console import print_run_status_table

    from phidata.app.databox import DataboxArgs, default_databox_name
    from phidata.infra.docker.resource.types import (
        DockerResourceType,
        DockerContainer,
    )

    logger.debug("Running Workflow in DockerContainer")
    # Step 1: Get the DockerManager
    docker_manager: DockerManager = docker_config.get_docker_manager()
    if docker_manager is None:
        raise DockerConfigException("DockerManager unavailable")

    # Step 2: Check if a Databox is available for running the Workflow
    # If available get the DataboxArgs
    databox_app_name = target_app or docker_config.databox_name or default_databox_name
    logger.debug(f"Using App: {databox_app_name}")
    databox_app = docker_config.get_app_by_name(databox_app_name)
    if databox_app is None:
        print_error("Databox not available")
        return False
    databox_app_args: Optional[Any] = databox_app.args
    # logger.debug(f"DataboxArgs: {databox_app_args}")
    if databox_app_args is None or not isinstance(databox_app_args, DataboxArgs):
        print_error("DataboxArgs invalid")
        return False
    databox_app_args = cast(DataboxArgs, databox_app_args)

    # Step 3: Build the PathContext for the workflows.
    # NOTE: The PathContext uses directories relative to the
    # workspace_parent_container_path
    workspace_name = docker_config.workspace_root_path.stem
    workspace_root_container_path = Path(
        databox_app_args.workspace_parent_container_path
    ).joinpath(workspace_name)
    scripts_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.scripts_dir
    )
    storage_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.storage_dir
    )
    meta_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.meta_dir
    )
    products_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.products_dir
    )
    notebooks_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.notebooks_dir
    )
    workspace_config_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.workspace_config_dir
    )
    workflow_file_path = Path(products_dir_container_path).joinpath(workflow_file)
    wf_path_context: PathContext = PathContext(
        scripts_dir=scripts_dir_container_path,
        storage_dir=storage_dir_container_path,
        meta_dir=meta_dir_container_path,
        products_dir=products_dir_container_path,
        notebooks_dir=notebooks_dir_container_path,
        workspace_config_dir=workspace_config_dir_container_path,
        workflow_file=workflow_file_path,
    )
    logger.debug(f"PathContext: {wf_path_context.json(indent=4)}")

    # Step 4: Get the container to run the Workflow
    databox_containers: Optional[
        List[DockerResourceType]
    ] = docker_manager.get_resources(
        name_filter=databox_app_name, type_filter="Container"
    )
    # logger.debug(f"databox_containers: {databox_containers}")
    if databox_containers is None or len(databox_containers) == 0:
        logger.error(f"Container:{databox_app_name} not found")
        return False
    if len(databox_containers) > 1:
        print_warning(
            "Running commands in multiple containers is not yet supported. "
            + "Running in the first container. "
        )
    databox_container: DockerContainer = databox_containers[0]
    # logger.debug("databox_container: ")
    # logger.debug("Name: {}".format(databox_container.name))
    # logger.debug("Class: {}".format(databox_container.__class__))
    # logger.debug("Resource: {}".format(databox_container))
    docker_client: DockerApiClient = docker_manager.docker_worker.docker_client
    active_container: Optional[Container] = databox_container.read(docker_client)
    # logger.debug("active_container: {}".format(active_container.attrs))
    # logger.debug("Class: {}".format(active_container.__class__))
    # logger.debug("Type: {}".format(type(active_container)))
    if active_container is None or not isinstance(active_container, Container):
        print_error("Container not available, please check your workspace is deployed.")
        return False

    logger.debug("Running:")
    logger.debug(f"\tWorkflow: {workflow_name}")
    logger.debug(f"\tTask: {task_name}")

    # Step 5: If workflow_name or task_name is provided,
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
            workflow_to_run.path_context = wf_path_context
            # Use DataProduct dag_id if provided
            if dag_id is not None:
                workflow_to_run.dag_id = dag_id
            wf_run_success = workflow_to_run.run_in_docker_container(
                active_container=active_container,
                docker_env=docker_config.docker_env,
                task_id=task_name,
            )
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
            task_to_run.path_context = wf_path_context
            # Use DataProduct dag_id if provided
            if dag_id is not None:
                task_to_run.dag_id = dag_id
            task_run_success = task_to_run.run_in_docker_container(
                active_container=active_container,
                docker_env=docker_config.docker_env,
            )
            return task_run_success

    # Step 6: If workflow_name is None and task_name is None
    # means this is a file with just workflows and no data products
    # Run all workflows
    wf_run_status: List[RunStatus] = []
    for wf_name, wf_obj in workflows.items():
        _name = wf_name or wf_obj.name
        print_subheading(f"\nRunning Workflow: {_name}")
        # Pass down context
        wf_obj.run_context = run_context
        wf_obj.path_context = wf_path_context
        wf_run_success = wf_obj.run_in_docker_container(
            active_container=active_container, docker_env=docker_config.docker_env
        )
        wf_run_status.append(RunStatus(name=_name, success=wf_run_success))

    print_run_status_table("Workflow Run Status", wf_run_status)
    for run_status in wf_run_status:
        if not run_status.success:
            return False
    return True


def run_data_products_docker(
    workflow_file: str,
    data_products: Dict[str, DataProduct],
    run_context: RunContext,
    docker_config: DockerConfig,
    target_app: Optional[str] = None,
) -> bool:
    from phidata.app.databox import Databox, DataboxArgs, default_databox_name
    from phidata.infra.docker.resource.types import (
        DockerResourceType,
        DockerContainer,
    )

    logger.debug("Running DataProducts in DockerContainer")
    # Step 1: Get the DockerManager
    docker_manager: DockerManager = docker_config.get_docker_manager()
    if docker_manager is None:
        raise DockerConfigException("DockerManager unavailable")

    # Step 2: Check if a DataboxApp is available for running the DataProduct
    # If available get the DataboxAppArgs
    databox_app_name = target_app or docker_config.databox_name or default_databox_name
    logger.debug(f"Using App: {databox_app_name}")
    databox_app = docker_config.get_app_by_name(databox_app_name)
    if databox_app is None or not isinstance(databox_app, Databox):
        print_error("Databox not available")
        return False
    databox_app_args: Optional[Any] = databox_app.args
    # logger.debug(f"DataboxAppArgs: {databox_app_args}")
    if databox_app_args is None or not isinstance(databox_app_args, DataboxArgs):
        print_error("DataboxArgs invalid")
        return False
    databox_app_args = cast(DataboxArgs, databox_app_args)

    # Step 3: Build the PathContext for the DataProducts.
    # NOTE: The PathContext uses directories relative to the workspace_parent_container_path
    workspace_name = docker_config.workspace_root_path.stem
    workspace_root_container_path = Path(
        databox_app_args.workspace_parent_container_path
    ).joinpath(workspace_name)
    scripts_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.scripts_dir
    )
    storage_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.storage_dir
    )
    meta_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.meta_dir
    )
    products_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.products_dir
    )
    notebooks_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.notebooks_dir
    )
    workspace_config_dir_container_path = workspace_root_container_path.joinpath(
        docker_config.workspace_config_dir
    )
    workflow_file_path = Path(products_dir_container_path).joinpath(workflow_file)
    dp_path_context: PathContext = PathContext(
        scripts_dir=scripts_dir_container_path,
        storage_dir=storage_dir_container_path,
        meta_dir=meta_dir_container_path,
        products_dir=products_dir_container_path,
        notebooks_dir=notebooks_dir_container_path,
        workspace_config_dir=workspace_config_dir_container_path,
        workflow_file=workflow_file_path,
    )
    logger.debug(f"PathContext: {dp_path_context.json(indent=4)}")

    # Step 4: Get the container to run the DataProduct
    databox_container_name = databox_app.get_container_name()
    databox_containers: Optional[
        List[DockerResourceType]
    ] = docker_manager.get_resources(
        name_filter=databox_container_name, type_filter="Container"
    )
    if databox_containers is None or len(databox_containers) == 0:
        logger.error(f"DockerContainer:{databox_container_name} not found")
        return False
    if len(databox_containers) > 1:
        print_info(
            "Running commands in multiple containers is not yet supported. "
            + "Running in the first container. "
        )
    databox_container: DockerContainer = databox_containers[0]
    # logger.debug("databox_container: ")
    # logger.debug("Name: {}".format(databox_container.name))
    # logger.debug("Class: {}".format(databox_container.__class__))
    # logger.debug("Resource: {}".format(databox_container))
    docker_client: DockerApiClient = docker_manager.docker_worker.docker_client
    active_container: Optional[Container] = databox_container.read(docker_client)
    # logger.debug("active_container: {}".format(active_container.attrs))
    # logger.debug("Class: {}".format(active_container.__class__))
    # logger.debug("Type: {}".format(type(active_container)))
    if active_container is None or not isinstance(active_container, Container):
        print_error("Container not available, please check your workspace is deployed.")
        return False

    # Step 5: Run the DataProducts
    dp_run_status: List[RunStatus] = []
    for dp_name, dp_obj in data_products.items():
        _name = dp_name or dp_obj.name
        print_subheading(f"\nRunning {_name}")
        # Pass down context
        dp_obj.run_context = run_context
        dp_obj.path_context = dp_path_context
        run_success = dp_obj.run_in_docker_container(
            active_container=active_container, docker_env=docker_config.docker_env
        )
        dp_run_status.append(RunStatus(name=_name, success=run_success))

    print_subheading("DataProduct run status:")
    print_info(
        "\n".join(
            [
                "{}: {}".format(wf.name, "Success" if wf.success else "Fail")
                for wf in dp_run_status
            ]
        )
    )
    print_info("")
    for _run in dp_run_status:
        if not _run.success:
            return False
    return True


def run_command_docker(
    command: str,
    docker_config: DockerConfig,
    target_app: Optional[str] = None,
) -> bool:
    from phidata.app.databox import DataboxArgs, default_databox_name
    from phidata.infra.docker.resource.types import (
        DockerResourceType,
        DockerContainer,
    )

    logger.debug("Running command in DockerContainer")
    # Step 1: Get the DockerManager
    docker_manager: DockerManager = docker_config.get_docker_manager()
    if docker_manager is None:
        raise DockerConfigException("DockerManager unavailable")

    # Step 2: Check if a Databox is available for running the DataProduct
    # If available get the DataboxArgs
    databox_app_name = target_app or docker_config.databox_name or default_databox_name
    logger.debug(f"Using App: {databox_app_name}")
    databox_app = docker_config.get_app_by_name(databox_app_name)
    if databox_app is None:
        print_error("Databox not available")
        return False
    databox_app_args: Optional[Any] = databox_app.args
    # logger.debug(f"DataboxArgs: {databox_app_args}")
    if databox_app_args is None or not isinstance(databox_app_args, DataboxArgs):
        print_error("DataboxArgs invalid")
        return False
    databox_app_args = cast(DataboxArgs, databox_app_args)

    # Step 3: Get the container to run the command
    databox_containers: Optional[
        List[DockerResourceType]
    ] = docker_manager.get_resources(
        name_filter=databox_app_name, type_filter="Container"
    )
    # logger.debug(f"databox_containers: {databox_containers}")
    if databox_containers is None or len(databox_containers) == 0:
        logger.error(f"Container: {databox_app_name} not found")
        return False
    if len(databox_containers) > 1:
        print_info(
            "Running commands in multiple containers is not yet supported. "
            + "Running in the first container. "
        )
    databox_container: DockerContainer = databox_containers[0]
    # logger.debug("databox_container: ")
    # logger.debug("Name: {}".format(databox_container.name))
    # logger.debug("Class: {}".format(databox_container.__class__))
    # logger.debug("Resource: {}".format(databox_container))
    docker_client: DockerApiClient = docker_manager.docker_worker.docker_client
    active_container: Optional[Container] = databox_container.read(docker_client)
    # logger.debug("active_container: {}".format(active_container.attrs))
    # logger.debug("Class: {}".format(active_container.__class__))
    # logger.debug("Type: {}".format(type(active_container)))
    if active_container is None or not isinstance(active_container, Container):
        print_error("Container not available, please check your workspace is deployed.")
        return False

    # Step 4: Run the command
    print_subheading(f"Running command: `{command}`")
    run_status = execute_command(
        cmd=command,
        container=active_container,
        docker_env=docker_config.docker_env,
    )
    logger.debug(f"Run status: {run_status}")
    return run_status
