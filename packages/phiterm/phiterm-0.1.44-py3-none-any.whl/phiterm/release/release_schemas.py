import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

from phiterm.utils.cli_console import print_info, print_subheading
from phiterm.utils.dttm import current_datetime_utc
from phiterm.utils.log import logger

######################################################
# ReleaseSchema Schemas
# These should match ~/philab/services/zeus/zeus/schemas/release_schemas.py
######################################################


class ReleaseSchema(BaseModel):
    id_release: str
    is_active: Optional[bool] = None
    is_at_desired_state: Optional[bool] = None
    release_type: Optional[str] = None
    release_data: Dict[str, Any] = {}
    start_ts: datetime.datetime = current_datetime_utc()
    end_ts: Optional[datetime.datetime] = None
    at_desired_state_ts: Optional[datetime.datetime] = None

    @classmethod
    def from_dict(cls, release_dict: Dict[str, Any]):
        return cls(
            id_release=release_dict.get("id_release", None),
            is_active=release_dict.get("is_valid", None),
            is_at_desired_state=release_dict.get("is_at_desired_state", None),
            release_type=release_dict.get("release_type", None),
            release_data=release_dict.get("release_data", {}),
            start_ts=release_dict.get("start_ts", current_datetime_utc()),
            end_ts=release_dict.get("end_ts", None),
            at_desired_state_ts=release_dict.get("at_desired_state_ts", None),
        )

    def set_at_desired_state(self):
        if self.is_at_desired_state:
            logger.debug(f"Release {self.id_release} already at desired state")
        else:
            logger.debug(f"Setting release {self.id_release} at desired state")
            self.is_at_desired_state = True
            self.at_desired_state_ts = current_datetime_utc()

    def print_info(self):
        print_subheading("Release: {}".format(self.id_release))
        print_info("Active: {}".format(self.is_active))
        print_info("At desired state: {}".format(self.is_at_desired_state))
        print_info("Release Type: {}".format(self.release_type))


#
#
# class ReleaseData(BaseModel):
#     # id_workspace of the WorkspaceSchema
#     ws__id_workspace: Optional[int]
#     # id_project of the GCPProjectSchema
#     ws_gcp_project__id_project: Optional[str]
#     # gcp project id
#     ws_gcp_project__gcp_project_id: Optional[str]
#     # id_cluster of the GKEClusterSchema
#     ws_gke_cluster__id_cluster: Optional[str]
#     # GKEClusterSchema name
#     ws_gke_cluster__cluster_name: Optional[str]
#
#     # other deployment datapoints
#     create_gke_cluster__id_operation: Optional[str]
#     delete_gke_cluster__id_operation: Optional[str]
#
#     class Config:
#         use_enum_values = True
#
#     @classmethod
#     def from_dict(cls, release_data_dict: Dict[str, Any]):
#         return cls(
#             ws__id_workspace=release_data_dict.get("ws__id_workspace", None),
#             ws_gcp_project__id_project=release_data_dict.get(
#                 "ws_gcp_project__id_project", None
#             ),
#             ws_gcp_project__gcp_project_id=release_data_dict.get(
#                 "ws_gcp_project__gcp_project_id", None
#             ),
#             ws_gke_cluster__id_cluster=release_data_dict.get(
#                 "ws_gke_cluster__id_cluster", None
#             ),
#             ws_gke_cluster__cluster_name=release_data_dict.get(
#                 "ws_gke_cluster__cluster_name", None
#             ),
#             create_gke_cluster__id_operation=release_data_dict.get(
#                 "create_gke_cluster__id_operation", None
#             ),
#             delete_gke_cluster__id_operation=release_data_dict.get(
#                 "delete_gke_cluster__id_operation", None
#             ),
#         )


# class GKEClusterRelease(BaseModel):
#     gke_cluster: GKEClusterSchema
#     release: ReleaseSchema
#
#     @classmethod
#     def from_dict(cls, gke_cluster_release_dict: Dict[str, Any]):
#         return cls(
#             gke_cluster=GKEClusterSchema.from_dict(
#                 gke_cluster_release_dict.get("gke_cluster", {})
#             ),
#             release=ReleaseSchema.from_dict(
#                 gke_cluster_release_dict.get("release", {})
#             ),
#         )
