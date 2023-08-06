import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

from phiterm.utils.dttm import dttm_str_to_dttm
from phiterm.workspace.ws_enums import WorkspaceVisibilityEnum

######################################################
# WorkspaceSchema Schemas
# These should match ~/philab/services/zeus/zeus/schemas/workspaces.py
######################################################


# The WorkspaceSchema defines the properties which are returned by the backend api
# Need to be careful that this doesn't contain any sensitive info
class WorkspaceSchema(BaseModel):
    name: str
    visibility: WorkspaceVisibilityEnum
    git_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    is_test: bool
    setup_complete: bool
    id_workspace: int
    created_by_id_user: int
    created_by_email: str
    create_ts: datetime.datetime
    last_update_ts: Optional[datetime.datetime] = None
    extra_data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, workspace_dict: Dict[str, Any]):
        return cls(
            name=workspace_dict.get("name", None),
            id_workspace=workspace_dict.get("id_workspace", None),
            visibility=WorkspaceVisibilityEnum.from_str(
                workspace_dict.get("visibility", None)
            ),
            git_url=workspace_dict.get("git_url", None),
            is_active=workspace_dict.get("is_valid", False),
            is_verified=workspace_dict.get("is_verified", False),
            is_test=workspace_dict.get("is_test", False),
            setup_complete=workspace_dict.get("setup_complete", False),
            created_by_id_user=workspace_dict.get("created_by_id_user", None),
            created_by_email=workspace_dict.get("created_by_email", None),
            create_ts=dttm_str_to_dttm(workspace_dict.get("create_ts", None)),
            last_update_ts=dttm_str_to_dttm(workspace_dict.get("last_update_ts", None)),
            extra_data=workspace_dict.get("extra_data", None),
        )


class UpsertWorkspaceFromCli(BaseModel):
    name: str
    visibility: Optional[str] = None
    git_url: Optional[str] = None
    setup_complete: Optional[bool] = None
    extra_data: Optional[Dict[str, Any]] = None
    is_active_ws_for_user: Optional[bool] = None
    # The UpsertWorkspaceFromCli model can be used to create or update a workspace
    # But sometimes we want to use it for ONLY creation or ONLY update
    # These 2 flags help us limit the functionality
    # If true, we can ONLY CREATE a workspace, not UPDATE it
    only_create: bool = False
    # If true, we can ONLY UPDATE a workspace, not CREATE it
    only_update: bool = False


class UpdateWorkspace(BaseModel):
    id_workspace: int
    name: Optional[str]
    visibility: Optional[WorkspaceVisibilityEnum]
    git_url: Optional[str]
    is_active: Optional[bool]
    is_verified: Optional[bool]
    is_test: Optional[bool]
    setup_complete: Optional[bool]
    is_primary_ws_for_user: Optional[bool]
    extra_data: Optional[Dict[str, Any]] = None
