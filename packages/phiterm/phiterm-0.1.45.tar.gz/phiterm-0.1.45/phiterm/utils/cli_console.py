from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.style import Style

from phiterm.utils.log import logger

console = Console()

######################################################
## Styles
# Standard Colors: https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
######################################################

heading_style = Style(
    color="green",
    bold=True,
    underline=True,
)
subheading_style = Style(color="chartreuse3", bold=True)
error_style = Style(color="red")
info_style = Style()
warn_style = Style(color="magenta")


######################################################
## Print functions
######################################################


def print_heading(msg: str) -> None:
    console.print(msg, style=heading_style)


def print_subheading(msg: str) -> None:
    console.print(msg, style=subheading_style)


def print_horizontal_line() -> None:
    console.rule()


def print_info(msg: str) -> None:
    console.print(msg, style=info_style)


def print_fix(msg: str) -> None:
    console.print("FIX  : {}".format(msg), style=info_style)


def print_error(msg: str) -> None:
    logger.error("{}".format(msg))


def print_warning(msg: str) -> None:
    logger.warning(f"{msg}")


def print_dict(_dict: dict) -> None:
    from rich.pretty import pprint

    pprint(_dict)


def print_feature_not_supported_msg() -> None:
    console.print(
        "This feature is not yet supported. Please reach out to ashpreet@phidata.com for more info",
        style=info_style,
    )


def print_conf_not_available_msg() -> None:
    logger.error("PhidataConf not available, please run `phi init`")


def print_generic_error_msg() -> None:
    console.print("Something went wrong, please try again", style=error_style)


def log_ws_not_available_msg():
    logger.warning("No active workspace")
    logger.warning("Set a workspace as active using `phi set [ws_name]`")
    logger.warning("Or run `phi ws init` to create a new workspace")


def log_network_error_msg() -> None:
    console.print(
        "NetworkError. Could not reach phidata servers.",
        style=error_style,
    )


def log_server_error_msg() -> None:
    logger.debug("ServerError: could not reach phidata servers.")


def log_auth_error_msg() -> None:
    logger.debug("AuthError: could not authenticate, please run `phi auth` again")


def print_active_workspace_not_available() -> None:
    print_warning("No active workspace")
    print_warning("Run `phi ws init` to create a new workspace")
    print_warning(
        "Run `phi ws setup` from an existing workspace directory to setup the workspace"
    )
    print_warning("Or set an existing workspace as active using `phi set [ws_name]`")


def print_available_workspaces(avl_ws_list) -> None:
    avl_ws_names = [w.name for w in avl_ws_list] if avl_ws_list else []
    print_info("Available Workspaces:\n  - {}".format("\n  - ".join(avl_ws_names)))


def get_validation_error_loc(validation_error: Dict[str, Any]) -> Optional[str]:
    if "loc" not in validation_error:
        return None
    return " -> ".join(str(e) for e in validation_error["loc"])


def print_validation_errors(validation_errors: List[Dict[str, Any]]) -> None:
    """
    Pretty prints pydantic validation errors.
    TODO: pydantic validation is known to be buggy for nested models, test this function
    """
    from rich import box
    from rich.table import Column, Table

    table = Table(
        Column(header="Field", justify="center"),
        Column(header="Error", justify="center"),
        Column(header="Context", justify="center"),
        box=box.MINIMAL,
        show_lines=True,
    )

    for err in validation_errors:
        error_loc = get_validation_error_loc(err)
        _error_ctx_raw = err.get("ctx")
        error_ctx = (
            "\n".join(f"{k}: {v}" for k, v in _error_ctx_raw.items())
            if _error_ctx_raw is not None and isinstance(_error_ctx_raw, dict)
            else ""
        )
        error_msg = err.get("msg")

        if error_loc is not None:
            table.add_row(error_loc, error_msg, error_ctx)

    if table.row_count > 0:
        console.print(table)
