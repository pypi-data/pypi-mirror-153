from pathlib import Path
from typing import Optional, Dict, List

from phidata.asset import DataAsset
from phidata.task import Task
from phidata.dq import DQCheck
from phidata.product import DataProduct
from phidata.workflow import Workflow
from phidata.workspace import WorkspaceConfig
from phidata.types.context import RunContext
from pydantic import ValidationError

from phiterm.utils.cli_console import (
    print_subheading,
    print_heading,
    print_info,
    print_warning,
)
from phiterm.utils.log import logger
from phiterm.workflow.wf_enums import WorkflowEnv
from phiterm.workflow.wf_utils import (
    parse_workflow_file,
    parse_workflow_description,
)
from phiterm.workspace.phi_ws_data import PhiWsData


def run_workflow(
    wf_description: str,
    ws_data: PhiWsData,
    target_env: WorkflowEnv,
    target_dt: str,
    dry_run: bool,
    detach: bool,
    target_app: Optional[str] = None,
    run_env_vars: Optional[Dict[str, str]] = None,
    run_params: Optional[Dict[str, str]] = None,
) -> None:
    """Runs the Phidata Workflow in the target environment.
    The run_workflow() function is called from `phi wf run`

    Step 1: Get the ws_root_path and products_dir
    Step 2: Get the workflow_file and workflow_name
    Step 3: Get the absolute workflow_file_path
    Step 4: Get DataProducts/Workflows/Tasks in the workflow_file_path
    Step 5: Run DataProducts/Workflows/Tasks in target runtime
    """

    if ws_data is None or ws_data.ws_config is None:
        logger.error("WorkspaceConfig invalid")
        return
    ws_config: WorkspaceConfig = ws_data.ws_config

    # Step 1: Get the ws_root_path and products_dir
    if ws_data.ws_root_path is None:
        logger.error("Workspace directory invalid")
        return
    ws_root_path: Path = ws_data.ws_root_path

    if ws_config.products_dir is None:
        logger.error("Products directory invalid")
        return
    products_dir: str = ws_config.products_dir

    # Step 2: Get the workflow_file and workflow_name
    # The workflow_file is the path of the file relative to the products_dir.
    print_subheading(f"Parsing: {wf_description}")
    workflow_file, workflow_name, task_name = parse_workflow_description(
        wf_description=wf_description,
        ws_root_path=ws_root_path,
        products_dir=products_dir,
    )
    # Validate workflow_file
    if workflow_file is None:
        logger.error("Workflow file not found")
        return

    print_info("\tFile: {}".format(workflow_file))
    if workflow_name:
        print_info("\tWorkflow: {}".format(workflow_name))
    if task_name:
        print_info("\tTask: {}".format(task_name))

    # Step 3: Get the absolute workflow_file_path
    workflow_file_path: Path
    try:
        workflow_file_path = (
            ws_root_path.joinpath(products_dir)
            .joinpath(workflow_file)
            .resolve(strict=True)
        )
    except FileNotFoundError as e:
        logger.error("Workflow file not found: {}".format(workflow_file))
        return

    # Step 4: Get DataProducts/Workflows/Tasks in the workflow_file_path
    dp_dict: Dict[str, DataProduct]
    wf_dict: Dict[str, Workflow]
    task_dict: Dict[str, Task]
    da_dict: Dict[str, DataAsset]
    dq_dict: Dict[str, DQCheck]
    try:
        dp_dict, wf_dict, task_dict, da_dict, dq_dict = parse_workflow_file(
            workflow_file_path
        )
    except ValidationError as e:
        from phidata.utils.cli_console import print_validation_errors

        print_validation_errors(e.errors())
        print_info("Please fix and try again")
        return
    logger.debug(f"dp_dict: {dp_dict}")
    logger.debug(f"wf_dict: {wf_dict}")
    logger.debug(f"task_dict: {task_dict}")
    logger.debug(f"da_dict: {da_dict}")
    logger.debug(f"dq_dict: {dq_dict}")

    # Final run status
    run_status: bool = False
    # Build the RunContext
    run_context = RunContext(
        run_date=target_dt,
        dry_run=dry_run,
        detach=detach,
        run_env=target_env.value,
        run_env_vars=run_env_vars,
        run_params=run_params,
    )

    # Step 5: Run DataProducts/Workflows/Tasks in target runtime

    # Run Workflow locally
    if target_env == WorkflowEnv.local:
        from phiterm.local.local_operator import run_workflows_local
        from phiterm.local.local_operator import run_data_products_local

        # ** CASE 1: If a workflow_name or a task_name is provided
        if (workflow_name is not None and len(wf_dict) > 0) or (
            task_name is not None and len(task_dict) > 0
        ):
            run_status = run_workflows_local(
                workflow_file=workflow_file,
                run_context=run_context,
                ws_data=ws_data,
                workflows=wf_dict,
                workflow_name=workflow_name,
                tasks=task_dict,
                task_name=task_name,
            )
        # ** CASE 2: If a workflow_name or a task name is not provided
        #   and workflow_file contains DataProducts.
        #   Run the DataProducts
        elif dp_dict is not None and len(dp_dict) > 0:
            run_status = run_data_products_local(
                workflow_file=workflow_file,
                data_products=dp_dict,
                run_context=run_context,
                ws_data=ws_data,
            )
        # ** CASE 3: If a workflow_name is not provided
        #   and workflow_file does NOT contain DataProducts
        #   but workflow_file contains Workflows
        #   Run all Workflows
        elif wf_dict is not None and len(wf_dict) > 0:
            run_status = run_workflows_local(
                workflow_file=workflow_file,
                run_context=run_context,
                ws_data=ws_data,
                workflows=wf_dict,
            )

    # Run Workflow in docker
    elif target_env == WorkflowEnv.dev:
        from phidata.infra.docker.config import DockerConfig
        from phiterm.docker.docker_operator import (
            run_workflows_docker,
            run_data_products_docker,
        )

        # Find the DockerConfig to use
        docker_configs: Optional[List[DockerConfig]] = ws_config.docker
        docker_config_to_use: Optional[DockerConfig] = None
        if docker_configs is not None and isinstance(docker_configs, list):
            if len(docker_configs) == 1:
                docker_config_to_use = docker_configs[0]
            else:
                for dc in docker_configs:
                    if dc.env == target_env:
                        docker_config_to_use = dc
                        break
        if docker_config_to_use is None:
            logger.error(f"No DockerConfig found for env: {target_env.value}")
            return

        ######################################################################
        # NOTE: VERY IMPORTANT TO GET RIGHT
        # Update sub-configs data using WorkspaceConfig
        # 1. Pass down the paths from the WorkspaceConfig
        #       These paths are used everywhere from Infra to Apps
        # 2. Pass down docker_env which is used to set the env variables
        #       when running the docker command
        ######################################################################

        # The ws_root_path is the ROOT directory for the workspace
        docker_config_to_use.workspace_root_path = ws_data.ws_root_path
        docker_config_to_use.workspace_config_file_path = ws_data.ws_config_file_path
        docker_config_to_use.scripts_dir = ws_config.scripts_dir
        docker_config_to_use.storage_dir = ws_config.storage_dir
        docker_config_to_use.meta_dir = ws_config.meta_dir
        docker_config_to_use.products_dir = ws_config.products_dir
        docker_config_to_use.notebooks_dir = ws_config.notebooks_dir
        docker_config_to_use.workspace_config_dir = ws_config.workspace_config_dir
        docker_config_to_use.docker_env = ws_config.docker_env

        # ** CASE 1: If a workflow_name or a task_name is provided
        if (workflow_name is not None and len(wf_dict) > 0) or (
            task_name is not None and len(task_dict) > 0
        ):
            # Because we are running this workflow/task as an airflow task,
            # we need to identify the DAG it belongs to.
            # Workflow DAGs are usually provided by their DataProducts
            # but can also have their own DAGs.
            dag_id_to_use = None

            # If a workflow is provided, lets find out if this workflow
            # is a part of a DataProduct. If it is, update the dag_id_to_use
            if workflow_name != "" and len(dp_dict) > 0:
                logger.debug(f"Finding DAG for workflow: {workflow_name}")
                if workflow_name not in wf_dict:
                    logger.error(
                        "Could not find '{}' in {}".format(
                            workflow_name, "[{}]".format(", ".join(wf_dict.keys()))
                        )
                    )
                    return

                # find the workflow to run
                workflow_to_run = wf_dict[workflow_name]
                logger.debug(f"Found workflow: {workflow_to_run}")

                # Check if the workflow is part of a DP
                # if it is, get the dag_id_to_use
                for dp_name, dp_obj in dp_dict.items():
                    dp_workflows = dp_obj.workflows
                    logger.debug(f"dp_workflows: {dp_workflows}")
                    if dp_workflows is not None and workflow_to_run in dp_workflows:
                        logger.debug(f"Using data product: {dp_name}")
                        dag_id_to_use = dp_obj.dag_id
                        logger.info(f"DAG.id: {dag_id_to_use}")

            # TODO: update this when testing `phi wf run dp::task`
            # # If a workflow is not provided, but a task is
            # # find the workflow for the task and use the dag_id from the workflow
            # elif task_name != "" and len(wf_dict) > 0:
            #     workflow = None
            #     if len(wf_dict) == 1:
            #         workflow = wf_dict.get(list(wf_dict.keys())[0])
            #     else:
            #         for wf_name, wf_obj in wf_dict.items():
            #             wf_tasks = {t.task_id: t for t in wf_obj.tasks}
            #             logger.debug(f"wf_tasks: {wf_tasks}")
            #             if wf_tasks is not None and task_name in wf_tasks:
            #                 workflow = wf_obj
            #
            #     if workflow is not None:
            #         logger.debug(f"Using workflow: {workflow.name}")
            #         dag_id_to_use = workflow.dag_id
            #         logger.debug(f"Using DAG: {dag_id_to_use}")

            run_status = run_workflows_docker(
                workflow_file=workflow_file,
                run_context=run_context,
                docker_config=docker_config_to_use,
                target_app=target_app,
                workflows=wf_dict,
                workflow_name=workflow_name,
                task_name=task_name,
                dag_id=dag_id_to_use,
            )
        # ** CASE 2: If a workflow_name or a task name is not provided
        #   and workflow_file contains DataProducts.
        #   Run the DataProducts
        elif dp_dict is not None and len(dp_dict) > 0:
            run_status = run_data_products_docker(
                workflow_file=workflow_file,
                data_products=dp_dict,
                run_context=run_context,
                docker_config=docker_config_to_use,
                target_app=target_app,
            )
        # ** CASE 3: If a workflow_name is not provided
        #   and workflow_file does NOT contain DataProducts
        #   but workflow_file contains Workflows
        #   Run the Workflows
        elif wf_dict is not None and len(wf_dict) > 0:
            run_status = run_workflows_docker(
                workflow_file=workflow_file,
                run_context=run_context,
                docker_config=docker_config_to_use,
                target_app=target_app,
                workflows=wf_dict,
            )
    # Run Workflow in staging k8s
    elif target_env == WorkflowEnv.stg:
        logger.error(f"WorkflowEnv: {target_env} not yet supported")
    # Run Workflow in prod k8s
    elif target_env == WorkflowEnv.prd:
        print_warning(
            f"Running workflows in {target_env.value} is in alpha, please verify results"
        )
        from phidata.infra.k8s.config import K8sConfig
        from phiterm.k8s.k8s_operator import (
            run_workflows_k8s,
            run_data_products_k8s,
        )

        k8s_configs: Optional[List[K8sConfig]] = ws_config.k8s
        k8s_config_to_use: Optional[K8sConfig] = None
        if k8s_configs is not None and isinstance(k8s_configs, list):
            if len(k8s_configs) == 1:
                k8s_config_to_use = k8s_configs[0]
            else:
                for dc in k8s_configs:
                    if dc.env == target_env:
                        k8s_config_to_use = dc
                        break
        if k8s_config_to_use is None:
            logger.error(f"No K8sConfig found for env: {target_env.value}")
            return

        ######################################################################
        # NOTE: VERY IMPORTANT TO GET RIGHT
        # Update sub-configs data using WorkspaceConfig
        # 1. Pass down the paths from the WorkspaceConfig
        #       These paths are used everywhere from Infra to Apps
        # 2. Pass down k8s_env which is used to set the env variables
        #       when running the k8s command
        ######################################################################

        # The ws_root_path is the ROOT directory for the workspace
        k8s_config_to_use.workspace_root_path = ws_data.ws_root_path
        k8s_config_to_use.workspace_config_file_path = ws_data.ws_config_file_path
        k8s_config_to_use.scripts_dir = ws_config.scripts_dir
        k8s_config_to_use.storage_dir = ws_config.storage_dir
        k8s_config_to_use.meta_dir = ws_config.meta_dir
        k8s_config_to_use.products_dir = ws_config.products_dir
        k8s_config_to_use.notebooks_dir = ws_config.notebooks_dir
        k8s_config_to_use.workspace_config_dir = ws_config.workspace_config_dir
        k8s_config_to_use.k8s_env = ws_config.k8s_env

        # ** CASE 1: If a workflow_name is provided
        #   Run only the Workflow
        if workflow_name is not None and len(wf_dict) > 0:
            # Because this is a single workflow, we need to identify the DAG
            # it belongs to. Workflow DAGs are usually provided by their DataProducts.
            # But Workflows can independently have their own DAGs as well.
            # To run a single workflow, lets find out if this workflow
            #   is a part of a DataProduct
            #   or an independent workflow
            wf_dag_id = None
            logger.debug(f"Finding DAG for {workflow_name}")
            if len(dp_dict) > 0:
                if workflow_name not in wf_dict:
                    logger.error(
                        "Could not find '{}' in {}".format(
                            workflow_name, "[{}]".format(", ".join(wf_dict.keys()))
                        )
                    )
                else:
                    _workflow = wf_dict[workflow_name]
                    # logger.debug(f"Found workflow: {_workflow}")
                    for dp_name, dp_obj in dp_dict.items():
                        dp_workflows = dp_obj.workflows
                        # logger.debug(f"dp_workflows: {dp_workflows}")
                        if dp_workflows is not None and _workflow in dp_workflows:
                            # logger.debug(f"Found data product: {dp_name}")
                            wf_dag_id = dp_obj.dag_id
                            print_info(f"Workflow DAG: {wf_dag_id}")

            run_status = run_workflows_k8s(
                workflow_file=workflow_file,
                workflows=wf_dict,
                run_context=run_context,
                k8s_config=k8s_config_to_use,
                target_app=target_app,
                workflow_name=workflow_name,
                use_dag_id=wf_dag_id,
            )
        # ** CASE 2: If a workflow_name is not provided
        #   but workflow_file contains DataProducts.
        #   Run the DataProducts
        elif dp_dict is not None and len(dp_dict) > 0:
            run_status = run_data_products_k8s(
                workflow_file=workflow_file,
                data_products=dp_dict,
                run_context=run_context,
                k8s_config=k8s_config_to_use,
                target_app=target_app,
            )
        # ** CASE 3: If a workflow_name is not provided
        #   and workflow_file does NOT contain DataProducts
        #   but workflow_file contains Workflows
        #   Run the Workflows
        elif wf_dict is not None and len(wf_dict) > 0:
            run_status = run_workflows_k8s(
                workflow_file=workflow_file,
                workflows=wf_dict,
                run_context=run_context,
                k8s_config=k8s_config_to_use,
                target_app=target_app,
            )
    else:
        logger.error(f"WorkflowEnv: {target_env} not supported")

    # Report the run_status
    print_info("")
    if run_status:
        logger.info("Success")
    else:
        logger.error("Fail")


def print_workflow_details(wf: Workflow) -> None:
    # Print workflow objects which are not imported in the file
    # print workflow tasks
    print_subheading(f"\nWorkflow: {wf.name}")
    family_tree: Dict[str, Dict[str, List[str]]] = wf.family_tree_dict
    if wf.tasks is not None:
        print_subheading(f"  Tasks: {len(wf.tasks)}")
        for task in wf.tasks:
            print_info("   * {}".format(task.name))
            if task.task_id in family_tree:
                task_tree = family_tree[task.task_id]
                for relation_type, relatives in task_tree.items():
                    logger.debug("{}: {}".format(relation_type, relatives))

    # print workflow pre-checks
    if wf.pre_checks is not None:
        print_subheading(f"  Pre-Checks: {len(wf.pre_checks)}")
        for pre_checks in wf.pre_checks:
            print_info("   * {}".format(pre_checks.name))
    # print workflow post-checks
    if wf.post_checks is not None:
        print_subheading(f"  Post-Checks: {len(wf.post_checks)}")
        for post_check in wf.post_checks:
            print_info("   * {}".format(post_check.name))
    # print workflow inputs
    if wf.inputs is not None:
        print_subheading(f"  Inputs: {len(wf.inputs)}")
        for _input in wf.inputs:
            print_info("   * {}".format(_input.name))
    # print workflow outputs
    if wf.outputs is not None:
        print_subheading(f"  Outputs: {len(wf.outputs)}")
        for output in wf.outputs:
            print_info("   * {} : {}".format(output.name, output.__class__.__name__))
    # if wf.tree is not None:
    #     print_subheading(f"  Tree:")
    #     print_info(json.dumps(wf.tree, indent=2))


def list_workflows(
    wf_description: str,
    ws_data: PhiWsData,
) -> None:

    if ws_data is None or ws_data.ws_config is None:
        logger.error("WorkspaceConfig invalid")
        return
    ws_config: WorkspaceConfig = ws_data.ws_config

    # Step 1: Get the ws_root_path and products_dir
    if ws_data.ws_root_path is None:
        logger.error("Workspace directory invalid")
        return
    ws_root_path: Path = ws_data.ws_root_path

    if ws_config.products_dir is None:
        logger.error("Products directory invalid")
        return
    products_dir: str = ws_config.products_dir

    # Step 2: Get the workflow_file and workflow_name
    # The workflow_file is the path of the file relative to the products_dir.
    print_subheading(f"Parsing: {wf_description}")
    workflow_file, workflow_name, task_name = parse_workflow_description(
        wf_description=wf_description,
        ws_root_path=ws_root_path,
        products_dir=products_dir,
    )
    # Validate workflow_file
    if workflow_file is None:
        logger.error("Workflow file not found")
        return

    print_info("File: {}".format(workflow_file))
    if workflow_name:
        print_info("Workflow: {}".format(workflow_name))
    if task_name:
        print_info("Task: {}".format(task_name))

    # Step 3: Get the absolute workflow_file_path
    workflow_file_path: Path
    try:
        workflow_file_path = (
            ws_root_path.joinpath(products_dir)
            .joinpath(workflow_file)
            .resolve(strict=True)
        )
    except FileNotFoundError as e:
        logger.error("Workflow file not found: {}".format(workflow_file))
        return

    # Step 4: Get DataProducts/Workflows in the workflow_file_path
    dp_dict: Dict[str, DataProduct]
    wf_dict: Dict[str, Workflow]
    task_dict: Dict[str, Task]
    da_dict: Dict[str, DataAsset]
    dq_dict: Dict[str, DQCheck]
    try:
        dp_dict, wf_dict, task_dict, da_dict, dq_dict = parse_workflow_file(
            workflow_file_path
        )
    except ValidationError as e:
        from phidata.utils.cli_console import print_validation_errors

        print_validation_errors(e.errors())
        print_info("Please fix and try again")
        return

    # Step 5: Print :)

    if dp_dict is not None and len(dp_dict) > 0:
        print_heading(f"\nDataProducts: {len(dp_dict)}")
        for key, dp in dp_dict.items():
            print_info(" * {}".format(dp.name))

    if wf_dict is not None and len(wf_dict) > 0:
        print_heading(f"\nWorkflows: {len(wf_dict)}")
        if workflow_name is None:
            for key, wf in wf_dict.items():
                print_workflow_details(wf)
        else:
            wf = wf_dict.get(workflow_name, None)
            if wf is None:
                logger.error(
                    "Could not find '{}' in {}".format(
                        workflow_name, "[{}]".format(", ".join(wf_dict.keys()))
                    )
                )
            else:
                print_workflow_details(wf)

    if task_dict is not None and len(task_dict) > 0:
        print_heading(f"\nTasks: {len(task_dict)}")
        for key, task in task_dict.items():
            print_info(" * {}".format(task.name))

    if dq_dict is not None and len(dq_dict) > 0:
        print_heading(f"\nDQ Checks: {len(dq_dict)}")
        for key, dq in dq_dict.items():
            print_info(" * {}".format(dq.name))

    if da_dict is not None and len(da_dict) > 0:
        print_heading(f"\nDataAssets: {len(da_dict)}")
        for key, da in da_dict.items():
            print_info("{}: {}".format(da.__class__.__name__, da.name))
