from pathlib import Path
from typing import Optional, List

from pydantic import ValidationError
from phidata.workspace import WorkspaceConfig

from phiterm.workspace.exceptions import WorkspaceConfigException
from phiterm.utils.cli_console import print_error, print_info, print_validation_errors
from phiterm.utils.log import logger


def add_ws_dir_to_path(ws_root_path: Path) -> None:
    # Add ws_root_path to sys.path so is treated as a package
    try:
        import sys

        logger.debug(f"Adding {ws_root_path} to path")
        sys.path.insert(0, str(ws_root_path))
    except Exception as e:
        logger.warning(
            f"Could not add {ws_root_path} to Path. This will break workspace imports"
        )
        logger.exception(e)


def load_workspace(config_file_path: Path) -> List[WorkspaceConfig]:
    """
    Loads a workspace using a config_file_path and returns List[WorkspaceConfig]
    """

    import importlib.util
    from importlib.machinery import ModuleSpec

    logger.debug(f"--^^-- Loading workspace from: {config_file_path}")
    # Read the WorkspaceConfig objects from config_file_path
    try:
        # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        # Create a ModuleSpec
        ws_config_module_spec: Optional[
            ModuleSpec
        ] = importlib.util.spec_from_file_location("ws_config_module", config_file_path)
        # Using the ModuleSpec create a module
        if ws_config_module_spec:
            ws_config_module = importlib.util.module_from_spec(ws_config_module_spec)
            ws_config_module_spec.loader.exec_module(ws_config_module)  # type: ignore

            # loop over all objects in module and find WorkspaceConfig objects
            ws_configs: List[WorkspaceConfig] = []
            for k, v in ws_config_module.__dict__.items():
                # logger.debug(f"Found {k}: | Type: {v.__class__.__name__}")
                if isinstance(v, WorkspaceConfig):
                    ws_configs.append(v)
            logger.debug("--^^-- Loading complete")
            return ws_configs
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

    raise WorkspaceConfigException(f"No workspace found at {config_file_path}")
