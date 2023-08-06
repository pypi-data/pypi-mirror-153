from typing import List, Optional

import httpx

from phiterm.backend_api.api_client import BackendApi, get_authenticated_client
from phiterm.backend_api.api_utils import response_is_invalid
from phiterm.utils.cli_console import log_network_error_msg
from phiterm.utils.log import logger
from phiterm.workspace.ws_schemas import (
    UpdateWorkspace,
    UpsertWorkspaceFromCli,
    WorkspaceSchema,
)


def convert_ws_response_to_schema(
    resp: httpx.Response,
) -> Optional[WorkspaceSchema]:

    ws_dict = resp.json()
    if ws_dict is None or not isinstance(ws_dict, dict):
        logger.debug("Could not parse ws data: {}".format(ws_dict))
        return None

    if resp.status_code == httpx.codes.OK:
        return WorkspaceSchema.from_dict(ws_dict)

    return None


def get_primary_workspace() -> Optional[WorkspaceSchema]:

    logger.debug("--o-o-- Get primary workspace")
    authenticated_client = get_authenticated_client()
    if authenticated_client is None:
        return None

    with authenticated_client as api:
        try:
            r: httpx.Response = api.get(BackendApi.workspace_read_primary)
            if response_is_invalid(r):
                return None
        except httpx.NetworkError:
            log_network_error_msg()
            return None

        # logger.debug("url: {}".format(r.url))
        # logger.debug("status: {}".format(r.status_code))
        # logger.debug("json: {}".format(r.json()))
        return convert_ws_response_to_schema(r)


def get_available_workspaces() -> Optional[List[WorkspaceSchema]]:

    logger.debug("--o-o-- Get available workspaces")
    authenticated_client = get_authenticated_client()
    if authenticated_client is None:
        return None

    with authenticated_client as api:
        try:
            r: httpx.Response = api.get(BackendApi.workspaces_read_available)
            if response_is_invalid(r):
                return None
        except httpx.NetworkError:
            log_network_error_msg()
            return None

        # logger.debug("url: {}".format(r.url))
        # logger.debug("status: {}".format(r.status_code))
        # logger.debug("json: {}".format(r.json()))

        ws_list_dict = r.json()
        # logger.debug("ws_list_dict type: {}".format(type(ws_list_dict)))
        if ws_list_dict is None or not isinstance(ws_list_dict, list):
            logger.debug("no workspaces available")
            return []
        # convert ws_list_dict to List[WorkspaceSchema] and return
        if r.status_code == httpx.codes.OK:
            ws_list: List[WorkspaceSchema] = []
            for ws_dict in ws_list_dict:
                if not isinstance(ws_dict, dict):
                    logger.debug("Could not parse {}".format(ws_dict))
                    continue
                ws_list.append(WorkspaceSchema.from_dict(ws_dict))

            return ws_list

    return None


def upsert_workspace(
    ws_upsert: UpsertWorkspaceFromCli,
) -> Optional[WorkspaceSchema]:

    logger.debug("--o-o-- Upsert workspace")
    authenticated_client = get_authenticated_client()
    if authenticated_client is None:
        logger.debug("User not authenticated")
        return None
    with authenticated_client as api:
        try:
            # logger.debug("data: {}".format(ws_upsert.dict()))
            r: httpx.Response = api.post(
                BackendApi.workspace_upsert_from_cli, json=ws_upsert.dict()
            )
            if response_is_invalid(r):
                return None
        except httpx.NetworkError:
            log_network_error_msg()
            return None

        # logger.debug("url: {}".format(r.url))
        # logger.debug("status: {}".format(r.status_code))
        # logger.debug("json: {}".format(r.json()))
        return convert_ws_response_to_schema(r)


def update_workspace(
    ws_update: UpdateWorkspace,
) -> Optional[WorkspaceSchema]:

    logger.debug("--o-o-- Update workspace")
    authenticated_client = get_authenticated_client()
    if authenticated_client is None:
        return None
    with authenticated_client as api:
        try:
            r: httpx.Response = api.post(
                BackendApi.workspace_update, json=ws_update.dict()
            )
            if response_is_invalid(r):
                return None
        except httpx.NetworkError:
            log_network_error_msg()
            return None

        logger.debug("url: {}".format(r.url))
        logger.debug("status: {}".format(r.status_code))
        logger.debug("json: {}".format(r.json()))
        return convert_ws_response_to_schema(r)
