from typing import Dict, Optional

import typer
from httpx import Client, Response, codes

from phiterm.conf.constants import (
    APP_NAME,
    APP_VERSION,
    BACKEND_API_URL,
    PHI_SESSION_COOKIE_KEY,
)
from phiterm.conf.phi_cli_creds import read_session_cookie
from phiterm.utils.cli_console import print_error


class ZeusApi:
    # Auth paths
    authenticate: str = "auth/authenticate"
    cli_auth: str = "auth/cli-auth"
    # WorkspaceSchema paths
    upsert_workspace: str = "workspaces/upsertfromcli"
    update_workspace: str = "workspaces/update"
    read_primary_workspace: str = "workspaces/read/primary"
    read_available_workspaces: str = "workspaces/read/available"
    deploy_workspace: str = "workspaces/deploy"
    shutdown_workspace: str = "workspaces/shutdown"
    sync_pak8_conf: str = "workspaces/syncpak8conf"
    # GCP paths
    upsert_gcp_project: str = "gcp/upsertfromcli"
    update_gcp_project: str = "gcp/update/gcpproject"
    read_primary_gcp_project: str = "gcp/read/primarygcpproject"
    get_gke_cluster: str = "gcp/gke/getcluster"
    get_or_create_gke_cluster: str = "gcp/gke/getorcreatecluster"
    delete_gke_cluster_if_exists: str = "gcp/gke/deleteclusterifexists"
    # Kubectl paths
    get_k8s_manifests: str = "kubectl/get/manifests"
    get_active_resources: str = "kubectl/get/active"
    apply_k8s_manifests: str = "kubectl/apply/manifests"


paths: Dict[str, str] = {
    # Auth paths
    "authenticate": "auth/authenticate",
    "cli_auth": "auth/cli-auth",
    # WorkspaceSchema paths
    "upsert_workspace": "workspaces/upsertfromcli",
    "update_workspace": "workspaces/update",
    "read_primary_workspace": "workspaces/read/primary",
    "read_available_workspaces": "workspaces/read/available",
    "deploy_workspace": "workspaces/deploy",
    "shutdown_workspace": "workspaces/shutdown",
    "sync_pak8_conf": "workspaces/syncpak8conf",
    # GCP paths
    "upsert_gcp_project": "gcp/upsertfromcli",
    "update_gcp_project": "gcp/update/gcpproject",
    "read_active_gcp_project": "gcp/read/activegcpproject",
    "get_gke_cluster": "gcp/gke/getcluster",
    "get_or_create_gke_cluster": "gcp/gke/getorcreatecluster",
    "delete_gke_cluster_if_exists": "gcp/gke/deleteclusterifexists",
    # Kubectl paths
    "get_k8s_manifests": "kubectl/get/manifests",
    "get_active_resources": "kubectl/get/active",
    "apply_k8s_manifests": "kubectl/apply/manifests",
}

headers = {"user-agent": f"{APP_NAME}/{APP_VERSION}"}


def validate_response(r: Response) -> None:
    """Exits the application if the response is invalid
    Use it like:
        r: Response = api.get(paths["authenticate"])
        validate_response(r)
    """
    # Check status code:
    if r.status_code == codes.UNAUTHORIZED:
        print_error(
            "There seems to be an authentication issue, please run `phi init` again"
        )
        raise typer.Exit()


def get_authenticated_client() -> Optional[Client]:
    # Returns an instance of httpx.Client which with preconfigured auth and base url.
    try:
        session_cookie: Optional[str] = read_session_cookie()
    except Exception:
        # print_error("Could not authenticating user. Please run `phi auth` to fix")
        return None

    if session_cookie is None:
        return None
    return Client(
        base_url=BACKEND_API_URL,
        headers=headers,
        cookies={PHI_SESSION_COOKIE_KEY: session_cookie},
        timeout=60,
    )
