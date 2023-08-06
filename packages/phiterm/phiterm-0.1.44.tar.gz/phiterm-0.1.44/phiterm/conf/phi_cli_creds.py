from typing import Optional

from phiterm.conf.constants import PHI_CREDS_PATH
from phiterm.utils.common import pickle_object_to_file, unpickle_object_from_file
from phiterm.utils.log import logger


class PhiCliCreds:
    def __init__(self, session_cookie: str):
        self._session_cookie = session_cookie

    @property
    def session_cookie(self) -> str:
        return self._session_cookie


def save_session_cookie(session_cookie: str):
    # logger.debug(f"Storing {session_cookie} to {str(PHI_CREDS_PATH)}")
    creds = PhiCliCreds(session_cookie)
    pickle_object_to_file(creds, PHI_CREDS_PATH)


def read_session_cookie() -> Optional[str]:
    # logger.debug(f"Reading session_cookie from {str(PHI_CREDS_PATH)}")
    creds: PhiCliCreds = unpickle_object_from_file(PHI_CREDS_PATH)
    return creds.session_cookie
