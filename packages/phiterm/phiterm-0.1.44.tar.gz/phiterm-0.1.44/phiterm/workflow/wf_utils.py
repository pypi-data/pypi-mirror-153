from collections import OrderedDict
from pathlib import Path
from typing import Optional, Dict, Tuple

from phidata.asset import DataAsset
from phidata.task import Task
from phidata.dq import DQCheck
from phidata.product import DataProduct
from phidata.workflow import Workflow

from phiterm.workflow.exceptions import WorkflowNotFoundException
from phiterm.utils.cli_console import print_error, print_info, print_validation_errors
from phiterm.utils.log import logger


def parse_workflow_description(
    wf_description: str, ws_root_path: Path, products_dir: str
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    This function parses a workflow description string in the format:
    Dir/File:Workflow:Task and return (workflow_file, workflow_name, task_name)

    The workflow_file is the path of the file starting after the products_dir.
    The workflow_file string can then be joined to the `products_dir` in the current env
    to get the absolute workflow file path
    Examples:

    `dau` -> (dau/dau.py, None)
    `dau:save` -> (dau/dau.py, save)
    `dau:save:test` -> (dau/dau.py, save, test)
    `dau/dau2:save:test` -> (dau/dau2.py, save, test)

    Args:
        wf_description:
        ws_root_path:
        products_dir:

    Returns:
        workflow_file: string path to the file containing the workflow,
                        relative to the products dir
        workflow_name: name of the workflow (if provided)
        task_name: name of the task (if provided)
    """

    # Split the wf_description by ":"
    wf_desc_slices = wf_description.strip().split(":")
    wf_path_slice: str = wf_desc_slices[0]
    wf_py_file: str = wf_path_slice + ".py"

    workflow_file: Optional[str] = None
    workflow_name: Optional[str] = (
        wf_desc_slices[1] if len(wf_desc_slices) > 1 else None
    )
    task_name: Optional[str] = wf_desc_slices[2] if len(wf_desc_slices) > 2 else None

    # Check if products dir is valid
    products_dir_path: Path = ws_root_path.joinpath(products_dir)
    if not (products_dir_path.exists() and products_dir_path.is_dir()):
        logger.error("Invalid products dir: {}".format(products_dir_path))
        return None, None, None

    # Check if the wf_path_slice is a file or a directory
    wf_py_file_path: Path = products_dir_path.joinpath(wf_py_file)
    wf_path_slice_path: Path = products_dir_path.joinpath(wf_path_slice)

    if wf_py_file_path.exists() and wf_py_file_path.is_file():
        # the path slice is a file
        workflow_file = wf_py_file
    elif wf_path_slice_path.exists() and wf_path_slice_path.is_dir():
        # the path slice is a dir and we should get the matching file.py
        wf_file_in_dir_path = wf_path_slice_path.joinpath(wf_py_file)
        if wf_file_in_dir_path.exists() and wf_file_in_dir_path.is_file():
            workflow_file = "{}/{}".format(wf_path_slice, wf_py_file)

    if workflow_file is None:
        logger.error("Workflow file not found")
        return None, None, None

    return workflow_file, workflow_name, task_name


def get_data_products_and_workflows_from_file(
    file_path: Path,
) -> Tuple[Dict[str, DataProduct], Dict[str, Workflow]]:
    """
    Reads the DataProducts & Workflows from filepath
    Args:
        file_path:

    Returns:

    """

    import importlib.util
    from importlib.machinery import ModuleSpec
    from pydantic import ValidationError

    logger.debug(f"Reading {file_path}")

    # Read DataProduct and Workflow objects from file_path
    try:
        # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        # Create a ModuleSpec
        dp_module_spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location(
            "dp_module", file_path
        )
        # Using the ModuleSpec create a module
        if dp_module_spec:
            dp_module = importlib.util.module_from_spec(dp_module_spec)
            dp_module_spec.loader.exec_module(dp_module)  # type: ignore

            # loop over all objects in module and find DataProduct and Workflow objects
            dp_dict: Dict[str, DataProduct] = OrderedDict()
            wf_dict: Dict[str, Workflow] = OrderedDict()
            for k, v in dp_module.__dict__.items():
                if isinstance(v, DataProduct):
                    logger.debug(f"Found {k} | Type: {v.__class__.__name__}")
                    dp_dict[k] = v
                if isinstance(v, Workflow):
                    logger.debug(f"Found {k} | Type: {v.__class__.__name__}")
                    wf_dict[k] = v
            logger.debug("--^^-- Loading complete")
            return dp_dict, wf_dict
    except NameError as name_err:
        print_error("Variable not defined")
        raise
    except ValidationError as validation_err:
        print_error(str(validation_err))
        # print_validation_errors(validation_err.errors())
        print_info("Please fix and try again")
        exit(0)
    except (ModuleNotFoundError, Exception) as e:
        # logger.exception(e)
        raise
    raise WorkflowNotFoundException(f"No workflow found at {file_path}")


def parse_workflow_file(
    wf_file_path: Path,
) -> Tuple[
    Dict[str, DataProduct],
    Dict[str, Workflow],
    Dict[str, Task],
    Dict[str, DataAsset],
    Dict[str, DQCheck],
]:
    """
    Reads a workflow_file and returns the
        - DataProducts
        - Workflows
        - Tasks
        - DataAssets
        - DQChecks
    Args:
        wf_file_path:

    Returns:

    """

    import importlib.util
    from importlib.machinery import ModuleSpec
    from pydantic import ValidationError

    logger.debug(f"Reading {wf_file_path}")

    # Read wf_file_path
    try:
        # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        # Create a ModuleSpec
        wf_module_spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location(
            "wf_module", wf_file_path
        )
        # Using the ModuleSpec create a module
        if wf_module_spec:
            dp_module = importlib.util.module_from_spec(wf_module_spec)
            wf_module_spec.loader.exec_module(dp_module)  # type: ignore

            # loop over all objects in module and find DataProduct and Workflow objects
            dp_dict: Dict[str, DataProduct] = OrderedDict()
            wf_dict: Dict[str, Workflow] = OrderedDict()
            task_dict: Dict[str, Task] = OrderedDict()
            da_dict: Dict[str, DataAsset] = OrderedDict()
            dq_dict: Dict[str, DQCheck] = OrderedDict()
            for k, v in dp_module.__dict__.items():
                if isinstance(v, DataProduct):
                    logger.debug(f"Adding {v.__class__.__name__}: {v.name}")
                    dp_dict[v.name] = v
                if isinstance(v, Workflow):
                    logger.debug(f"Adding {v.__class__.__name__}: {v.name}")
                    wf_dict[v.name] = v
                if isinstance(v, Task):
                    logger.debug(f"Adding {v.__class__.__name__}: {v.name}")
                    task_dict[v.name] = v
                if isinstance(v, DataAsset):
                    logger.debug(f"Adding {v.__class__.__name__}: {v.name}")
                    da_dict[v.name] = v
                if isinstance(v, DQCheck):
                    logger.debug(f"Adding {v.__class__.__name__}: {v.name}")
                    dq_dict[v.name] = v

            logger.debug("--^^-- Loading complete")
            return dp_dict, wf_dict, task_dict, da_dict, dq_dict
    except NameError as name_err:
        print_error("Variable not defined")
        raise
    except ValidationError as validation_err:
        print_error(str(validation_err))
        # print_validation_errors(validation_err.errors())
        print_info("Please fix and try again")
        exit(0)
    except (ModuleNotFoundError, Exception) as e:
        # logger.exception(e)
        raise
    raise WorkflowNotFoundException(f"No workflow found at {wf_file_path}")
