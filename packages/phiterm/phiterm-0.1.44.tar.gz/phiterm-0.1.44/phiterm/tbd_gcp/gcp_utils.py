# from typing import Optional
#
# from phi import schemas
# from phiterm.conf.phi_conf import PhiGcpData, PhiWsData
# from phiterm.utils.common import pprint_info, pprint_info
# from phiterm.utils.log import logger
#
#
# def secho_gcp_status(ws_data: PhiWsData) -> None:
#     ws_gcp_data: Optional[PhiGcpData] = ws_data.ws_gcp_data
#     if ws_gcp_data is None:
#         pprint_info("")
#         pprint_info(
#             "No GCP Project set up, run `phi gcp auth` to setup your GCP Project"
#         )
#         return None
#
#     # pprint_heading("GCP")
#
#     gcp_project: Optional[schemas.GCPProjectSchema] = ws_gcp_data.gcp_project
#     # if gcp_project:
#     #     gcp_project.secho_status()
#
#     gke_cluster: Optional[schemas.GKEClusterSchema] = ws_gcp_data.gke_cluster
#     # if gke_cluster:
#     #     gke_cluster.secho_status()
#
#     gcloud_default_creds_avl = ws_gcp_data.gcloud_default_creds_avl
#     # gcp_svc_account: Optional[Dict[str, Any]] = ws_gcp_data.gcp_svc_account
#     # gcp_svc_account_key: Optional[Dict[str, Any]] = ws_gcp_data.gcp_svc_account_key
#     logger.debug(
#         "Gcloud Default Credentials Available: {}".format(gcloud_default_creds_avl)
#     )
#     # logger.debug("gcp_svc_account: {}".format(gcp_svc_account))
#     # logger.debug("gcp_svc_account_key: {}".format(gcp_svc_account_key))
