from typing import Any, Dict, List, Optional, Union

import httpx

from phiterm.backend_api.api_client import BackendApi, get_authenticated_client
from phiterm.backend_api.api_exceptions import CliAuthException
from phiterm.backend_api.api_utils import headers, response_is_invalid
from phiterm.enums.response_enums import BackendResponseStatus
from phiterm.schemas.auth_schemas import EmailPasswordSignInSchema
from phiterm.schemas.user_schemas import UserSchema
from phiterm.utils.cli_console import log_network_error_msg, print_error
from phiterm.utils.log import logger


def is_user_authenticated() -> bool:
    logger.debug("++**++ Authenticating user")
    authenticated_client = get_authenticated_client()
    if authenticated_client is None:
        logger.debug("Session not available")
        return False

    logger.debug("Cookie Jar: {}".format(authenticated_client.cookies.jar))
    with authenticated_client as api:
        try:
            r: httpx.Response = api.get(BackendApi.authenticate)
            if response_is_invalid(r):
                return False
        except httpx.NetworkError as e:
            log_network_error_msg()
            return False

        logger.debug("url: {}".format(r.url))
        logger.debug("status: {}".format(r.status_code))
        logger.debug("headers: {}".format(r.headers))
        logger.debug("cookies: {}".format(r.cookies))

        _data: Union[Dict[Any, Any], List[Any]] = r.json()
        logger.debug("_data: {}".format(_data))

        if _data is None or not isinstance(_data, dict):
            print_error("Could not parse response")
            return False

        if _data.get("status", "FAIL") == BackendResponseStatus.SUCCESS.value:
            return True
        return False


def authenticate_and_get_user_schema(
    tmp_access_token: str,
) -> Optional[UserSchema]:
    from phiterm.conf.constants import BACKEND_API_URL, PHI_SESSION_COOKIE_KEY
    from phiterm.conf.phi_cli_creds import save_session_cookie

    with httpx.Client(base_url=BACKEND_API_URL, headers=headers, timeout=None) as api:
        logger.debug(f"authenticate_and_get_user_schema: {tmp_access_token}")
        try:
            r: httpx.Response = api.post(
                BackendApi.cli_auth, json={"access_token": tmp_access_token}
            )
            if response_is_invalid(r):
                return None
        except httpx.NetworkError as e:
            log_network_error_msg()
            return None

        logger.debug("status: {}".format(r.status_code))
        logger.debug("headers: {}".format(r.headers))
        logger.debug("cookies: {}".format(r.cookies))
        logger.debug("url: {}".format(r.url))
        logger.debug("json: {}".format(r.json()))

        phidata_session_cookie = r.cookies.get(PHI_SESSION_COOKIE_KEY)
        if phidata_session_cookie is None:
            print_error("Could not authenticate")
            return None

        user_data = r.json()
        if not isinstance(user_data, dict):
            raise CliAuthException("Could not parse response after authentication")

        current_user: UserSchema = UserSchema.from_dict(user_data)
        if current_user is not None:
            save_session_cookie(phidata_session_cookie)
            return current_user
        return None


def sign_in_user(
    sign_in_data: EmailPasswordSignInSchema,
) -> Optional[UserSchema]:
    logger.debug("--o-o-- Sign in user")
    from phiterm.conf.constants import BACKEND_API_URL, PHI_SESSION_COOKIE_KEY
    from phiterm.conf.phi_cli_creds import save_session_cookie

    with httpx.Client(base_url=BACKEND_API_URL, headers=headers, timeout=None) as api:
        try:
            r: httpx.Response = api.post(BackendApi.sign_in, json=sign_in_data.dict())
            if response_is_invalid(r):
                return None
        except httpx.NetworkError as e:
            log_network_error_msg()
            return None

        # logger.debug("status: {}".format(r.status_code))
        # logger.debug("headers: {}".format(r.headers))
        # logger.debug("cookies: {}".format(r.cookies))
        # logger.debug("url: {}".format(r.url))
        # logger.debug("json: {}".format(r.json()))

        phidata_session_cookie = r.cookies.get(PHI_SESSION_COOKIE_KEY)
        if phidata_session_cookie is None:
            print_error("Could not authenticate")
            return None

        user_data = r.json()
        if not isinstance(user_data, dict):
            raise CliAuthException("Could not parse response after authentication")

        current_user: UserSchema = UserSchema.from_dict(user_data)
        if current_user is not None:
            save_session_cookie(phidata_session_cookie)
            return current_user
        return None


def auth_ping() -> bool:
    """Returns true if phidata servers are reachable"""

    logger.debug("--o-o-- Pinging backend")
    from phiterm.conf.constants import BACKEND_API_URL

    with httpx.Client(base_url=BACKEND_API_URL, headers=headers, timeout=None) as api:
        try:
            r: httpx.Response = api.get(BackendApi.ping)
            if response_is_invalid(r):
                return False
        except httpx.NetworkError as e:
            logger.exception(e)
            log_network_error_msg()
            return False

        # logger.debug("status: {}".format(r.status_code))
        # logger.debug("headers: {}".format(r.headers))
        # logger.debug("cookies: {}".format(r.cookies))
        # logger.debug("url: {}".format(r.url))
        # logger.debug("json: {}".format(r.json()))
        if r.status_code == httpx.codes.OK:
            return True

    return False
