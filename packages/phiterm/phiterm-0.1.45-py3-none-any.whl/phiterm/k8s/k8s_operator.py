from pathlib import Path
from typing import List, Optional, cast, Dict, Tuple, Any

from phidata.infra.base import InfraConfig
from phidata.infra.k8s.api_client import K8sApiClient
from phidata.infra.k8s.config import K8sConfig
from phidata.infra.k8s.exceptions import K8sConfigException
from phidata.infra.k8s.manager import K8sManager
from phidata.infra.k8s.resource.types import K8sResourceType
from phidata.infra.k8s.resource.group import K8sResourceGroup
from phidata.infra.k8s.resource.utils import filter_and_flatten_k8s_resource_groups
from phidata.product import DataProduct
from phidata.workflow import Workflow
from phidata.types.context import PathContext, RunContext

from phiterm.workspace.phi_ws_data import PhiWsData
from phiterm.workspace.ws_enums import WorkspaceEnv
from phiterm.types.run_status import RunStatus
from phiterm.utils.filesystem import delete_files_in_dir
from phiterm.utils.cli_console import (
    print_error,
    print_heading,
    print_subheading,
    print_info,
    print_warning,
)
from phiterm.utils.log import logger


def deploy_k8s_config(
    config: K8sConfig,
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    app_filter: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> bool:

    # Step 1: Get the K8sManager
    k8s_manager: K8sManager = config.get_k8s_manager()
    if k8s_manager is None:
        raise K8sConfigException("K8sManager unavailable")
    print_heading(f"--**-- K8s env: {config.env}\n")

    # Step 2: If dry_run, print the resources and return True
    if dry_run:
        k8s_manager.create_resources_dry_run(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        return True

    # Step 3: Create resources
    try:
        success: bool = k8s_manager.create_resources(
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
    resource_creation_valid: bool = k8s_manager.validate_resources_are_created(
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
    )
    if not resource_creation_valid:
        logger.error("K8sResource creation could not be validated")
        return False

    print_info("K8s config deployed")
    return True


def shutdown_k8s_config(
    config: K8sConfig,
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    app_filter: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> bool:

    # Step 1: Get the K8sManager
    k8s_manager: K8sManager = config.get_k8s_manager()
    if k8s_manager is None:
        raise K8sConfigException("K8sManager unavailable")
    print_heading(f"--**-- K8s env: {config.env}\n")

    # Step 2: If dry_run, print the resources and return True
    if dry_run:
        k8s_manager.delete_resources_dry_run(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        return True

    # Step 3: Delete resources
    try:
        success: bool = k8s_manager.delete_resources(
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

    # Step 4: Validate resources are deleted
    resources_deletion_valid: bool = k8s_manager.validate_resources_are_deleted(
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
    )
    if not resources_deletion_valid:
        logger.error("K8sResource deletion could not be validated")
        return False

    print_info("K8s config shut down")
    return True


def patch_k8s_config(
    config: K8sConfig,
    name_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    app_filter: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
) -> bool:

    # Step 1: Get the K8sManager
    k8s_manager: K8sManager = config.get_k8s_manager()
    if k8s_manager is None:
        raise K8sConfigException("K8sManager unavailable")
    print_heading(f"--**-- K8s env: {config.env}\n")

    # Step 2: If dry_run, print the resources and return True
    if dry_run:
        k8s_manager.patch_resources_dry_run(
            name_filter=name_filter,
            type_filter=type_filter,
            app_filter=app_filter,
            auto_confirm=auto_confirm,
        )
        return True

    # Step 3: Patch resources
    try:
        success: bool = k8s_manager.patch_resources(
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

    # Step 4: Validate resources are patched
    resources_patch_valid: bool = k8s_manager.validate_resources_are_patched(
        name_filter=name_filter,
        type_filter=type_filter,
        app_filter=app_filter,
    )
    if not resources_patch_valid:
        logger.error("K8sResource patch could not be validated")
        return False

    print_info("K8s config patched")
    return True


def save_k8s_resources(
    ws_data: PhiWsData,
    target_env: Optional[WorkspaceEnv] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
) -> None:
    """Saves the K8s resources"""

    if ws_data is None or ws_data.ws_config is None:
        print_error("WorkspaceConfig invalid")
        return
    ws_config = ws_data.ws_config

    # Step 1: Get the K8sConfigs to build
    configs_to_build: List[InfraConfig] = []
    if target_env is None:
        if ws_data.ws_config.k8s is not None:
            configs_to_build.extend(ws_data.ws_config.k8s)
    else:
        for config in ws_data.ws_config.k8s:
            if config.env is None:
                continue
            if config.env.lower() not in WorkspaceEnv.values_list():
                print_error(f"{config.env} not supported")
                continue
            config_env = WorkspaceEnv.from_str(config.env)
            if config_env == target_env:
                configs_to_build.append(config)

    num_configs_to_build = len(configs_to_build)
    num_configs_built = 0
    for config in configs_to_build:
        env = config.env
        print_heading(
            "\nBuilding K8s manifests{}\n".format(
                f" for env: {env}" if env is not None else ""
            )
        )
        if not isinstance(config, InfraConfig):
            print_error(f"{config} is not an instance of InfraConfig")
            continue
        if not isinstance(config, K8sConfig):
            print_error(f"{config} is not an instance of K8sConfig")
            continue
        if not config.is_valid():
            print_error("K8sConfig invalid")
            continue
        if not config.enabled:
            logger.debug(
                f"{config.__class__.__name__} for env {config.__class__.env} disabled"
            )
            num_configs_built += 1
            continue

        ######################################################################
        # NOTE: VERY IMPORTANT TO GET RIGHT
        # Update sub-configs data using WorkspaceConfig
        # 1. Pass down the paths from the WorkspaceConfig
        #       These paths are used everywhere from Infra to Apps
        # 2. Pass down local_env, k8s_env, k8s_env for building PhidataApps
        # 3. Pass down common cloud configuration. eg: aws_region, aws_profile
        ######################################################################

        # The ws_root_path is the ROOT directory for the workspace
        config.workspace_root_path = ws_data.ws_root_path
        config.workspace_config_file_path = ws_data.ws_config_file_path
        config.scripts_dir = ws_config.scripts_dir
        config.storage_dir = ws_config.storage_dir
        config.meta_dir = ws_config.meta_dir
        config.products_dir = ws_config.products_dir
        config.notebooks_dir = ws_config.notebooks_dir
        config.workspace_config_dir = ws_config.workspace_config_dir

        # Step 2: Get the K8sManager
        k8s_manager: K8sManager = config.get_k8s_manager()
        if k8s_manager is None:
            raise K8sConfigException("K8sManager unavailable")

        # Step 3: Prep the directory to write to
        workspace_config_file_path: Optional[Path] = ws_data.ws_config_file_path
        if workspace_config_file_path is None:
            print_error("workspace_config_file_path invalid")
            continue
        workspace_config_dir: Path = workspace_config_file_path.parent.resolve()
        if workspace_config_dir is None:
            print_error("workspace_config_dir invalid")
            continue

        resources_dir: Path = workspace_config_dir.joinpath(config.resources_dir)
        if config.env is not None:
            resources_dir = resources_dir.joinpath(config.env)
        if config.args.name is not None:
            resources_dir = resources_dir.joinpath(config.args.name)

        # Step 4: Get the K8sResources
        k8s_resources: Optional[
            Dict[str, K8sResourceGroup]
        ] = k8s_manager.get_resources()
        if k8s_resources is None or len(k8s_resources) == 0:
            print_error("No K8sResources to save")
            return

        # delete directory to save resources if needed
        if resources_dir.exists():
            print_info(f"Deleting {str(resources_dir)}")
            if resources_dir.is_file():
                resources_dir.unlink()
            elif resources_dir.is_dir():
                delete_files_in_dir(resources_dir)
        print_info(f"Saving to {str(resources_dir)}")
        resources_dir.mkdir(exist_ok=True, parents=True)

        for rg_name, resource_group in k8s_resources.items():
            print_info(f"Processing {rg_name}")
            rg_dir: Path = resources_dir.joinpath(rg_name)
            rg_dir.mkdir(exist_ok=True)
            resource_list: Optional[
                List[K8sResourceType]
            ] = filter_and_flatten_k8s_resource_groups(
                k8s_resource_groups={rg_name: resource_group},
                name_filter=target_name,
                type_filter=target_type,
            )
            if resource_list is None:
                continue
            for resource in resource_list:
                if resource is not None:
                    resource_name = resource.get_resource_name()
                    resource_file: Path = rg_dir.joinpath(f"{resource_name}.yaml")
                    try:
                        manifest_yaml = resource.get_k8s_manifest_yaml(
                            default_flow_style=False
                        )  # use default_style='"' for debugging
                        if manifest_yaml is not None:
                            logger.debug(f"Writing {str(resource_file)}")
                            resource_file.write_text(manifest_yaml)
                    except Exception as e:
                        logger.error(f"Could not parse {resource_name}")
                        continue
        num_configs_built += 1

    print_info(f"\n# Configs built: {num_configs_built}/{num_configs_to_build}")


def run_workflows_k8s(
    workflow_file: str,
    workflows: Dict[str, Workflow],
    run_context: RunContext,
    k8s_config: K8sConfig,
    target_app: Optional[str] = None,
    workflow_name: Optional[str] = None,
    use_dag_id: Optional[str] = None,
) -> bool:
    from phidata.app.databox import Databox, DataboxArgs, default_databox_name
    from phidata.infra.k8s.enums.api_version import ApiVersion
    from phidata.infra.k8s.enums.kind import Kind
    from phidata.infra.k8s.resource.types import K8sResourceType
    from phidata.infra.k8s.resource.apps.v1.deployment import Deployment
    from phidata.infra.k8s.resource.core.v1.pod import Pod
    from phidata.infra.k8s.resource.meta.v1.object_meta import ObjectMeta

    logger.debug("Running Workflow in K8sContainer")
    # Step 1: Get the K8sManager
    k8s_manager: K8sManager = k8s_config.get_k8s_manager()
    if k8s_manager is None:
        raise K8sConfigException("K8sManager unavailable")

    # Step 2: Check if a Databox is available for running the Workflow
    # If available get the DataboxArgs
    databox_app_name = target_app or k8s_config.databox_name or default_databox_name
    logger.debug(f"Using App: {databox_app_name}")
    databox_app = k8s_config.get_app_by_name(databox_app_name)
    if databox_app is None or not isinstance(databox_app, Databox):
        print_error("Databox not available")
        return False
    databox_app_args: DataboxArgs = databox_app.args
    # logger.debug(f"DataboxArgs: {databox_app_args}")
    if databox_app_args is None or not isinstance(databox_app_args, DataboxArgs):
        print_error("DataboxArgs invalid")
        return False
    databox_app_args = cast(DataboxArgs, databox_app_args)

    # Step 3: Build the PathContext for the workflows.
    # NOTE: The PathContext uses directories relative to the
    # workspace_parent_container_path
    workspace_name = k8s_config.workspace_root_path.stem
    workspace_root_container_path = Path(
        databox_app_args.workspace_parent_container_path
    ).joinpath(workspace_name)
    scripts_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.scripts_dir
    )
    storage_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.storage_dir
    )
    meta_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.meta_dir
    )
    products_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.products_dir
    )
    notebooks_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.notebooks_dir
    )
    workspace_config_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.workspace_config_dir
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

    # Step 4: Gather Pod and K8sApiClient to use
    # Step 4.1: Get the deployment to run the Workflow
    databox_deployments: Optional[List[K8sResourceType]] = k8s_manager.read_resources(
        name_filter=databox_app_name, type_filter="Deployment"
    )
    # logger.debug(f"databox_deployments: {databox_deployments}")
    if databox_deployments is None or len(databox_deployments) == 0:
        logger.error(f"Deployment: {databox_app_name} not found")
        return False
    if len(databox_deployments) > 1:
        logger.info(
            f"Found {len(databox_deployments)} deployments for {databox_app_name}, using the first one."
        )
    databox_deploy: Deployment = databox_deployments[0]
    # Step 4.2: Get the deployment name which generates the pod name
    databox_deploy_name = databox_deploy.get_resource_name()
    if databox_deploy_name is None:
        logger.error(f"Deployment name not available")
        return False
    logger.debug("databox_deploy_name: {}".format(databox_deploy_name))
    # Step 4.3: Get the pod using the databox_deploy_name
    databox_pod = Pod(
        name=databox_deploy_name,
        api_version=ApiVersion.CORE_V1,
        kind=Kind.POD,
        metadata=ObjectMeta(
            name=databox_deploy_name,
            namespace=k8s_config.namespace,
        ),
    )
    # Step 4.4: Get the container name
    databox_container_name = databox_app.get_container_name()
    # Step 4.5: Get the K8sApiClient
    k8s_api_client: K8sApiClient = k8s_manager.k8s_worker.k8s_api_client

    # Step 5: Run single Workflow if workflow_name is provided
    if workflow_name is not None:
        if workflow_name not in workflows:
            print_error(
                "Could not find '{}' in {}".format(
                    workflow_name, "[{}]".format(", ".join(workflows.keys()))
                )
            )
            return False

        wf_run_success: bool = False
        workflow_to_run = workflows[workflow_name]
        _name = workflow_name or workflow_to_run.name
        print_subheading(f"\nRunning {_name}")
        # Pass down context
        workflow_to_run.run_context = run_context
        workflow_to_run.path_context = wf_path_context
        # Use DataProduct dag_id if provided
        if use_dag_id is not None:
            workflow_to_run.dag_id = use_dag_id
        wf_run_success = workflow_to_run.run_in_k8s_container(
            pod=databox_pod,
            k8s_api_client=k8s_api_client,
            container_name=databox_container_name,
            k8s_env=k8s_config.k8s_env,
        )

        print_subheading("\nWorkflow run status:")
        print_info("{}: {}".format(_name, "Success" if wf_run_success else "Fail"))
        print_info("")
        return wf_run_success
    # Step 6: Run all Workflows if workflow_name is None
    else:
        wf_run_status: List[RunStatus] = []
        for wf_name, wf_obj in workflows.items():
            _name = wf_name or wf_obj.name
            print_subheading(f"\nRunning {_name}")
            # Pass down context
            wf_obj.run_context = run_context
            wf_obj.path_context = wf_path_context
            run_success = wf_obj.run_in_k8s_container(
                pod=databox_pod,
                k8s_api_client=k8s_api_client,
                container_name=databox_container_name,
                k8s_env=k8s_config.k8s_env,
            )
            wf_run_status.append(RunStatus(name=_name, success=run_success))

        print_subheading("\nWorkflow run status:")
        print_info(
            "\n".join(
                [
                    "{}: {}".format(wf.name, "Success" if wf.success else "Fail")
                    for wf in wf_run_status
                ]
            )
        )
        print_info("")
        for _run in wf_run_status:
            if not _run.success:
                return False
        return True


def run_data_products_k8s(
    workflow_file: str,
    data_products: Dict[str, DataProduct],
    run_context: RunContext,
    k8s_config: K8sConfig,
    target_app: Optional[str] = None,
) -> bool:
    from phidata.app.databox import Databox, DataboxArgs, default_databox_name
    from phidata.infra.k8s.enums.api_version import ApiVersion
    from phidata.infra.k8s.enums.kind import Kind
    from phidata.infra.k8s.resource.types import K8sResourceType
    from phidata.infra.k8s.resource.apps.v1.deployment import Deployment
    from phidata.infra.k8s.resource.core.v1.pod import Pod
    from phidata.infra.k8s.resource.meta.v1.object_meta import ObjectMeta

    logger.debug("Running DataProducts in K8sContainer")
    # Step 1: Get the K8sManager
    k8s_manager: K8sManager = k8s_config.get_k8s_manager()
    if k8s_manager is None:
        raise K8sConfigException("K8sManager unavailable")

    # Step 2: Check if a Databox is available for running the Workflow
    # If available get the DataboxArgs
    databox_app_name = target_app or k8s_config.databox_name or default_databox_name
    logger.debug(f"Using App: {databox_app_name}")
    databox_app = k8s_config.get_app_by_name(databox_app_name)
    if databox_app is None or not isinstance(databox_app, Databox):
        print_error("Databox not available")
        return False
    databox_app_args: DataboxArgs = databox_app.args
    # logger.debug(f"DataboxArgs: {databox_app_args}")
    if databox_app_args is None or not isinstance(databox_app_args, DataboxArgs):
        print_error("DataboxArgs invalid")
        return False
    databox_app_args = cast(DataboxArgs, databox_app_args)

    # Step 3: Build the PathContext for the DataProducts.
    # NOTE: The PathContext uses directories relative to the
    # workspace_parent_container_path
    workspace_name = k8s_config.workspace_root_path.stem
    workspace_root_container_path = Path(
        databox_app_args.workspace_parent_container_path
    ).joinpath(workspace_name)
    scripts_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.scripts_dir
    )
    storage_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.storage_dir
    )
    meta_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.meta_dir
    )
    products_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.products_dir
    )
    notebooks_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.notebooks_dir
    )
    workspace_config_dir_container_path = workspace_root_container_path.joinpath(
        k8s_config.workspace_config_dir
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

    # Step 4: Gather Pod and K8sApiClient to use
    # Step 4.1: Get the deployment to run the Workflow
    databox_deployments: Optional[List[K8sResourceType]] = k8s_manager.read_resources(
        name_filter=databox_app_name, type_filter="Deployment"
    )
    # logger.debug(f"databox_deployments: {databox_deployments}")
    if databox_deployments is None or len(databox_deployments) == 0:
        logger.error(f"Deployment: {databox_app_name} not found")
        return False
    if len(databox_deployments) > 1:
        logger.info(
            f"Found {len(databox_deployments)} deployments for {databox_app_name}, using the first one."
        )
    databox_deploy: Deployment = databox_deployments[0]
    # Step 4.2: Get the deployment name which generates the pod name
    databox_deploy_name = databox_deploy.get_resource_name()
    if databox_deploy_name is None:
        logger.error(f"Deployment name not available")
        return False
    logger.debug("databox_deploy_name: {}".format(databox_deploy_name))
    # Step 4.3: Get the pod using the databox_deploy_name
    databox_pod = Pod(
        name=databox_deploy_name,
        api_version=ApiVersion.CORE_V1,
        kind=Kind.POD,
        metadata=ObjectMeta(
            name=databox_deploy_name,
            namespace=k8s_config.namespace,
        ),
    )
    # Step 4.4: Get the container name
    databox_container_name = databox_app.get_container_name()
    # Step 4.5: Get the K8sApiClient
    k8s_api_client: K8sApiClient = k8s_manager.k8s_worker.k8s_api_client

    # Step 5: Run the DataProducts
    dp_run_status: List[RunStatus] = []
    for dp_name, dp_obj in data_products.items():
        _name = dp_name or dp_obj.name
        print_subheading(f"\nRunning {_name}")
        # Pass down context
        dp_obj.run_context = run_context
        dp_obj.path_context = dp_path_context
        run_success = dp_obj.run_in_k8s_container(
            pod=databox_pod,
            k8s_api_client=k8s_api_client,
            container_name=databox_container_name,
            k8s_env=k8s_config.k8s_env,
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


def run_command_k8s(
    command: List[str],
    k8s_config: K8sConfig,
    target_app: Optional[str] = None,
) -> bool:
    from phidata.app.databox import Databox, DataboxArgs, default_databox_name
    from phidata.infra.k8s.enums.api_version import ApiVersion
    from phidata.infra.k8s.enums.kind import Kind
    from phidata.infra.k8s.resource.types import K8sResourceType
    from phidata.infra.k8s.resource.apps.v1.deployment import Deployment
    from phidata.infra.k8s.resource.core.v1.pod import Pod
    from phidata.infra.k8s.resource.meta.v1.object_meta import ObjectMeta
    from phidata.infra.k8s.utils.pod import execute_command

    logger.debug("Running command in K8sContainer")
    # Step 1: Get the K8sManager
    k8s_manager: K8sManager = k8s_config.get_k8s_manager()
    if k8s_manager is None:
        raise K8sConfigException("K8sManager unavailable")

    # Step 2: Check if a Databox is available for running the Workflow
    # If available get the DataboxArgs
    databox_app_name = target_app or k8s_config.databox_name or default_databox_name
    logger.debug(f"Using App: {databox_app_name}")
    databox_app = k8s_config.get_app_by_name(databox_app_name)
    if databox_app is None or not isinstance(databox_app, Databox):
        print_error("Databox not available")
        return False
    databox_app_args: DataboxArgs = databox_app.args
    # logger.debug(f"DataboxArgs: {databox_app_args}")
    if databox_app_args is None or not isinstance(databox_app_args, DataboxArgs):
        print_error("DataboxArgs invalid")
        return False
    databox_app_args = cast(DataboxArgs, databox_app_args)

    # Step 3: Gather Pod and K8sApiClient to use
    # Step 3.1: Get the deployment to run the Workflow
    databox_deployments: Optional[List[K8sResourceType]] = k8s_manager.read_resources(
        name_filter=databox_app_name, type_filter="Deployment"
    )
    # logger.debug(f"databox_deployments: {databox_deployments}")
    if databox_deployments is None or len(databox_deployments) == 0:
        logger.error(f"Deployment: {databox_app_name} not found")
        return False
    if len(databox_deployments) > 1:
        logger.info(
            f"Found {len(databox_deployments)} deployments for {databox_app_name}, using the first one."
        )
    databox_deploy: Deployment = databox_deployments[0]
    # Step 3.2: Get the deployment name which generates the pod name
    databox_deploy_name = databox_deploy.get_resource_name()
    if databox_deploy_name is None:
        logger.error(f"Deployment name not available")
        return False
    logger.debug("databox_deploy_name: {}".format(databox_deploy_name))
    # Step 3.3: Get the pod using the databox_deploy_name
    databox_pod = Pod(
        name=databox_deploy_name,
        api_version=ApiVersion.CORE_V1,
        kind=Kind.POD,
        metadata=ObjectMeta(
            name=databox_deploy_name,
            namespace=k8s_config.namespace,
        ),
    )
    # Step 3.4: Get the container name
    databox_container_name = databox_app.get_container_name()
    # Step 3.5: Get the K8sApiClient
    k8s_api_client: K8sApiClient = k8s_manager.k8s_worker.k8s_api_client

    # Step 4: Run the command
    print_subheading(f"Running command: `{command}`")
    run_status = execute_command(
        cmd=command,
        pod=databox_pod,
        k8s_api_client=k8s_api_client,
        container_name=databox_container_name,
        k8s_env=k8s_config.k8s_env,
    )
    logger.debug(f"Run status: {run_status}")
    return run_status
