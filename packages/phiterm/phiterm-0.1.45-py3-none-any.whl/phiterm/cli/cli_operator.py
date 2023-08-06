from typing import List, Optional

from typer import launch as typer_launch

from phiterm.backend_api.api_exceptions import CliAuthException
from phiterm.backend_api.auth_api import (
    authenticate_and_get_user_schema,
    is_user_authenticated,
    sign_in_user,
)
from phiterm.backend_api.workspace_api import (
    get_available_workspaces,
    get_primary_workspace,
)
from phiterm.conf.constants import PHI_CONF_DIR, PHI_SIGNIN_URL_WITHOUT_PARAMS
from phiterm.conf.phi_conf import PhiConf
from phiterm.schemas.auth_schemas import EmailPasswordSignInSchema
from phiterm.schemas.user_schemas import UserSchema
from phiterm.utils.cli_auth_server import (
    get_port_for_auth_server,
    get_tmp_access_token_from_web_flow,
)
from phiterm.utils.cli_console import (
    print_info,
    print_error,
    print_heading,
    print_info,
    print_info,
    print_subheading,
)
from phiterm.utils.common import is_empty
from phiterm.utils.filesystem import delete_from_fs
from phiterm.utils.log import logger
from phiterm.workspace.ws_operator import init_workspace_data
from phiterm.workspace.ws_schemas import WorkspaceSchema


def delete_phidata_conf() -> None:
    logger.debug("Removing existing Phidata configuration")
    delete_from_fs(PHI_CONF_DIR)


def initialize_phidata(reset: bool = False) -> bool:
    """This function is called by `phi init` and initializes phidata on the users machine.
    Steps:
    1. Check if PHI_CONF_DIR exists, if not, create it. If reset == True, recreate PHI_CONF_DIR.
    2. Check if PhiConf exists, if it does, try and authenticate the user
        If the user is authenticated, phi is configured and authenticated. Return True.
    3. If PhiConf does not exist, create a new PhiConf. Return True.
    """

    print_heading("Welcome to phidata!\n")
    if reset:
        delete_phidata_conf()

    logger.debug("Initializing phidata")

    # Check if ~/.phi exists, if its not a dir - delete it and create the dir
    if PHI_CONF_DIR.exists():
        # logger.debug(f"{PHI_CONF_DIR} exists")
        if not PHI_CONF_DIR.is_dir():
            try:
                delete_from_fs(PHI_CONF_DIR)
            except Exception as e:
                logger.exception(e)
                print_info(
                    f"Something went wrong, please delete {PHI_CONF_DIR} and run `phi init` again"
                )
                return False
            PHI_CONF_DIR.mkdir(parents=True)
    else:
        # logger.debug(f"creating {PHI_CONF_DIR}")
        PHI_CONF_DIR.mkdir(parents=True)
        logger.debug(f"created {PHI_CONF_DIR}")

    # Confirm PHI_CONF_DIR exists otherwise we should return
    if PHI_CONF_DIR.exists():
        logger.debug(f"Your phidata config is stored at: {PHI_CONF_DIR}")
    else:
        print_info(f"Something went wrong, please run `phi init` again")
        return False

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if phi_conf is None:
        # Create a new PhiConf
        phi_conf = PhiConf()

    # Authenticate user
    is_authenticated = is_user_authenticated()
    if is_authenticated:
        logger.debug(f"Phidata is configured and authenticated")
        return True

    if phi_conf is not None:
        print_info("Phidata is initialized. Next steps:\n")
        print_info(" - Run `phi ws init` to create a new workspace")
        print_info(
            " - Run `phi ws setup` from an existing directory to setup the workspace"
        )
        print_info(" - Run `phi ws up -dr` to dry-run workspace deploy")
        print_info(" - Run `phi ws up` to deploy the workspace")
    return True


def authenticate_phidata() -> bool:
    """Authenticate the user with the phidata backend.
    Steps:
    1. Authenticate the user by opening the phidata sign-in url
        and the web-app will post back a temporary CLI auth token
        to our mini http server running on auth_server_port.
    2. Using the tmp_access_token, authenticate the CLI with backend and
        save the phidata_session_cookie to PHI_CREDS_PATH.
        This step is handled by authenticate_and_get_user_schema()
    5. Once the user is authenticated, create a PhiConf for ths user.
    6. Get the primary and available workspaces for this user.
    7. If the user has workspaces available, initialize additional workspace requirements
    """

    print_heading("Authenticating with phidata")

    auth_server_port = get_port_for_auth_server()
    redirect_uri = "http%3A%2F%2Flocalhost%3A{}%2F".format(auth_server_port)
    auth_url = "{}?source=cli&action=INIT_CLI_AUTH&redirect_uri={}".format(
        PHI_SIGNIN_URL_WITHOUT_PARAMS, redirect_uri
    )
    print_info("\nYour browser will be opened to visit:\n{}".format(auth_url))
    typer_launch(auth_url)
    print_info("\nWaiting for a response from browser...\n")

    tmp_access_token = get_tmp_access_token_from_web_flow(auth_server_port)
    if tmp_access_token is None:
        print_error(f"Could not authenticate, please run `phi auth` again")
        return False

    try:
        user: Optional[UserSchema] = authenticate_and_get_user_schema(tmp_access_token)
    except CliAuthException as e:
        logger.exception(e)
        print_error(f"Could not authenticate, please run `phi auth` again")
        return False

    if user is None:
        print_error(f"Could not retrieve user data, please run `phi auth` again")
        return False

    print_info("Welcome {}, you are now authenticated\n".format(user.username))

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if phi_conf is None:
        phi_conf = PhiConf()

    phi_conf.user = user
    # Get Primary/Available Workspaces for the user
    active_ws_name: Optional[str] = phi_conf.active_ws_name
    available_workspaces: Optional[List[WorkspaceSchema]] = phi_conf.available_ws

    # If the active_ws_name is None, call backend to get the primary_ws
    if active_ws_name is None:
        logger.debug("Getting primary workspace from api")
        primary_ws = get_primary_workspace()
        if primary_ws is not None:
            logger.debug(
                "Received primary workspace:\n{}".format(primary_ws.json(indent=2))
            )
            phi_conf.active_ws_name = primary_ws.name
        else:
            logger.debug("No primary workspace available")

    # If available_workspaces is empty and a primary_ws is available
    # call backend to get the available workspaces
    if is_empty(available_workspaces) and active_ws_name is not None:
        logger.debug("Getting available workspaces from api")
        available_workspaces = get_available_workspaces()
        if available_workspaces:
            logger.debug(
                "Received {} available workspace(s)".format(len(available_workspaces))
            )
            phi_conf.available_ws = available_workspaces
            for _ws in available_workspaces:
                init_workspace_data(_ws, phi_conf)

    return True


def sign_in_using_cli() -> bool:
    from getpass import getpass

    print_heading("Sign in")
    email_raw = input("email: ")
    pass_raw = getpass()

    if email_raw is None or pass_raw is None:
        print_error("incorrect email or password")

    try:
        user: Optional[UserSchema] = sign_in_user(
            EmailPasswordSignInSchema(email=email_raw, password=pass_raw)
        )
    except CliAuthException as e:
        logger.exception(e)
        return False

    if user is None:
        print_error("Could not get user data, sign in again")
        return False

    print_info("Welcome {}, you are now authenticated\n".format(user.username))

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if phi_conf is None:
        phi_conf = PhiConf()

    phi_conf.user = user
    # Get Primary/Available Workspaces for the user
    active_ws_name: Optional[str] = phi_conf.active_ws_name
    available_workspaces: Optional[List[WorkspaceSchema]] = phi_conf.available_ws

    # If the active_ws_name is None, call backend to get the primary_ws
    if active_ws_name is None:
        logger.debug("Getting primary workspace from api")
        primary_ws = get_primary_workspace()
        if primary_ws is not None:
            logger.debug(
                "Received primary workspace:\n{}".format(primary_ws.json(indent=2))
            )
            phi_conf.active_ws_name = primary_ws.name
        else:
            logger.debug("No primary workspace available")

    # If available_workspaces is empty and a primary_ws is available
    # call backend to get the available workspaces
    if is_empty(available_workspaces) and active_ws_name is not None:
        logger.debug("Getting available workspaces from api")
        available_workspaces = get_available_workspaces()
        if available_workspaces:
            logger.debug(
                "Received {} available workspace(s)".format(len(available_workspaces))
            )
            phi_conf.available_ws = available_workspaces
            for _ws in available_workspaces:
                init_workspace_data(_ws, phi_conf)

    return True
