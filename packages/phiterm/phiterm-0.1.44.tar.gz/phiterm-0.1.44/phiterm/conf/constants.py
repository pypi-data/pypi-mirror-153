from pathlib import Path

APP_NAME = "phicli"
APP_VERSION = "0.1.0"

DEFAULT_WS_NAME = "data-platform"

PHI_CONF_DIR: Path = Path.home().resolve().joinpath(".phi")
PHI_CONF_PATH: Path = PHI_CONF_DIR.joinpath("conf")
PHI_ACCESSTOKEN_PATH: Path = PHI_CONF_DIR.joinpath("access_token")
PHI_CREDS_PATH: Path = PHI_CONF_DIR.joinpath("creds")
# PHI_KUBE_DIR: Path = PHI_CONF_DIR.joinpath("kube")
# SYSTEM_KUBE_DIR: Path = Path.home().resolve().joinpath(".kube")
# SYSTEM_KUBECONFIG_DIR: Path = SYSTEM_KUBE_DIR.joinpath("config")

# Rest API Constants
PHI_SESSION_COOKIE_KEY: str = "__phi_session"
PHI_SIGNIN_URL_WITHOUT_PARAMS: str = "http://devphi/signin"
BACKEND_API_URL: str = "http://devphi/services/backend/api/v1/"

# Logger Names
PHI_LOGGER_NAME = "phi"
PHIDATA_LOGGER_NAME = "phidata"
