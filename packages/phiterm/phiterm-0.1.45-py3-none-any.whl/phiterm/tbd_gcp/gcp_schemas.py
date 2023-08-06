# import datetime
# from typing import Any, Dict, Optional
#
# from pydantic import BaseModel
#
# import pak8.gcp.enums as pak8_gcp_enums
# from phiterm.gcp.gcp_enums import GCPProjectStatus
# from phiterm.utils.dttm import dttm_str_to_dttm
#
# ######################################################
# # GCP Schemas
# # These should match ~/philab/services/zeus/zeus/schemas/gcp_schemas.py
# ######################################################
#
#
# class GCPProjectSchema(BaseModel):
#     name: str
#     is_active: bool
#     is_verified: bool = False
#     is_test: bool = False
#     gcp_project_id: str
#     id_project: str
#     id_workspace: int
#     created_by_id_user: int
#     created_by_email: str
#     create_ts: datetime.datetime
#     gcp_zone: Optional[str] = None
#     gcp_service_account_key_available: bool = False
#     vpc_network: Optional[str]
#     last_update_ts: Optional[datetime.datetime] = None
#     project_status: Optional[GCPProjectStatus]
#
#     @classmethod
#     def from_dict(cls, gcp_project_dict: Dict[str, Any]):
#         return cls(
#             name=gcp_project_dict.get("name", None),
#             is_active=gcp_project_dict.get("is_valid", None),
#             is_verified=gcp_project_dict.get("is_verified", None),
#             is_test=gcp_project_dict.get("is_test", None),
#             gcp_project_id=gcp_project_dict.get("gcp_project_id", None),
#             id_project=gcp_project_dict.get("id_project", None),
#             id_workspace=gcp_project_dict.get("id_workspace", None),
#             created_by_id_user=gcp_project_dict.get("created_by_id_user", None),
#             created_by_email=gcp_project_dict.get("created_by_email", None),
#             create_ts=dttm_str_to_dttm(gcp_project_dict.get("create_ts", None)),
#             gcp_zone=gcp_project_dict.get("gcp_zone", None),
#             gcp_service_account_key_available=gcp_project_dict.get(
#                 "gcp_service_account_key_available", False
#             ),
#             vpc_network=gcp_project_dict.get("vpc_network", None),
#             last_update_ts=dttm_str_to_dttm(
#                 gcp_project_dict.get("last_update_ts", None)
#             ),
#             project_status=GCPProjectStatus.from_str(
#                 gcp_project_dict.get("project_status", None)
#             ),
#         )
#
#     # def secho_status(self):
#     #     pprint_info("")
#     #     pprint_subheading("GCP Project: {}".format(self.gcp_project_id))
#     #     pprint_status("Active: {}".format(self.is_valid))
#     #     pprint_status(
#     #         "Status: {}".format(
#     #             self.project_status.value if self.project_status else "unavailable"
#     #         )
#     #     )
#     #     pprint_status("name: {}".format(gcp_project.name))
#     #     pprint_status("id_project: {}".format(gcp_project.id_project))
#     #     pprint_status("id_workspace: {}".format(gcp_project.id_workspace))
#     #     pprint_status("gcp_service_account_key_available: {}".format(gcp_project.gcp_service_account_key_available))
#
#
# class UpsertGCPProjectFromCli(BaseModel):
#     # Required
#     name: str
#     id_project: str
#     id_workspace: int
#     gcp_project_id: str
#     gcp_service_account_key: Dict[str, Any]
#     # Optional
#     gcp_service_account: Optional[Dict[str, Any]] = None
#     gcp_zone: Optional[str] = None
#     vpc_network: Optional[str] = None
#     is_active: bool = True
#     is_verified: bool = False
#     is_test: bool = False
#     set_as_primary_project_for_ws: bool = False
#
#
# class UpdateGCPProject(BaseModel):
#     id_project: str
#     id_workspace: int
#     name: Optional[str]
#     is_active: Optional[bool]
#     is_verified: Optional[bool]
#     is_test: Optional[bool]
#     gcp_zone: Optional[str]
#     gcp_project_id: Optional[str]
#     gcp_service_account_key: Optional[Dict[str, Any]]
#     vpc_network: Optional[str]
#     set_as_primary_project_for_ws: Optional[bool]
#
#
# class GKEClusterSchema(BaseModel):
#     is_active: bool
#     is_verified: bool = False
#     is_test: bool = False
#     id_cluster: str
#     id_project: str
#     id_workspace: int
#     created_by_id_user: int
#     created_by_email: str
#     create_ts: datetime.datetime
#     gcp_zone: Optional[str]
#     gcp_project_id: str
#     cluster_name: str
#     current_cluster_status: pak8_gcp_enums.GKEClusterStatus
#     current_cluster_config: Optional[Dict[str, Any]] = None
#     last_update_ts: Optional[datetime.datetime] = None
#     deactivate_ts: Optional[datetime.datetime] = None
#
#     class Config:
#         arbitrary_types_allowed = True
#
#     @classmethod
#     def from_dict(cls, gke_cluster_dict: Dict[str, Any]):
#         return cls(
#             is_active=gke_cluster_dict.get("is_valid", None),
#             is_verified=gke_cluster_dict.get("is_verified", None),
#             is_test=gke_cluster_dict.get("is_test", None),
#             id_cluster=gke_cluster_dict.get("id_cluster", None),
#             id_project=gke_cluster_dict.get("id_project", None),
#             id_workspace=gke_cluster_dict.get("id_workspace", None),
#             created_by_id_user=gke_cluster_dict.get("created_by_id_user", None),
#             created_by_email=gke_cluster_dict.get("created_by_email", None),
#             create_ts=dttm_str_to_dttm(gke_cluster_dict.get("create_ts", None)),
#             gcp_zone=gke_cluster_dict.get("gcp_zone", None),
#             gcp_project_id=gke_cluster_dict.get("gcp_project_id", None),
#             cluster_name=gke_cluster_dict.get("cluster_name", None),
#             current_cluster_status=pak8_gcp_enums.GKEClusterStatus.from_str(
#                 gke_cluster_dict.get("current_cluster_status", None)
#             ),
#             current_cluster_config=gke_cluster_dict.get("current_cluster_config", None),
#             last_update_ts=dttm_str_to_dttm(
#                 gke_cluster_dict.get("last_update_ts", None)
#             ),
#             deactivate_ts=dttm_str_to_dttm(gke_cluster_dict.get("deactivate_ts", None)),
#         )
#
#     # def secho_status(self):
#     #     pprint_info("")
#     #     pprint_subheading("GKE Cluster: {}".format(self.cluster_name))
#     #     pprint_status("Active: {}".format(self.is_valid))
#     #     pprint_status("Status: {}".format(self.current_cluster_status.value))
#     #     pprint_status("Cluster config: {})".format(gke_cluster.current_cluster_config))
#
#
# class CreateGKECluster(BaseModel):
#     is_verified: bool = False
#     is_test: bool = False
#     id_cluster: str
#     id_project: str
#     id_workspace: int
#     created_by_id_user: int
#     created_by_email: str
#     create_ts: datetime.datetime
#     gcp_zone: Optional[str]
#     gcp_project_id: str
#     cluster_name: str
#
#     class Config:
#         arbitrary_types_allowed = True
