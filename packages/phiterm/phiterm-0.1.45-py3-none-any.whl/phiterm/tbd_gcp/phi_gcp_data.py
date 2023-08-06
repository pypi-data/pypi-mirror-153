# import datetime
# from typing import Any, Dict, Optional
#
# from pydantic import BaseModel
#
# from pak8.gcp.conf import Pak8GCPConf
# from phiterm.gcp.gcp_schemas import GCPProjectSchema, GKEClusterSchema
# from phiterm.utils.dttm import current_datetime_utc
#
#
# class PhiGcpData(BaseModel):
#     """The PhiGcpData schema contains all information required for a phidata workspace
#     to interface with the Google Cloud Platform.
#
#     Field Descriptions:
#     gcp_project: GCPProjectSchema schema.
#     gke_cluster: GKEClusterSchema schema.
#     gcloud_default_creds_avl: If the gcloud sdk is available & authenticated on this machine.
#         Then we can use the application-default-credentials: https://googleapis.dev/python/google-auth/latest/user-guide.html#application-default-credentials
#     gcp_svc_account: If this user is the workspace owner, they would probably create the service account
#         for phidata. If they do, then we can store details about that service account in gcp_svc_account
#     """
#
#     gcp_project_id: str
#     gcp_svc_account: Optional[Dict[str, Any]] = None
#     pak8_gcp_conf: Optional[Pak8GCPConf] = None
#     gcloud_default_creds_avl: bool = False
#     last_update_ts: datetime.datetime = current_datetime_utc()
#     gcp_project_schema: Optional[GCPProjectSchema] = None
#     gke_cluster_schema: Optional[GKEClusterSchema] = None
