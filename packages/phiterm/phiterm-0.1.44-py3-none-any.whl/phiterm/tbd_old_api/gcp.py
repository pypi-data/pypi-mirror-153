# from typing import Any, Dict, List, Optional, Union
#
# import httpx
#
# from pak8.conf import Pak8Conf
# from phi import exceptions, schemas
# from phiterm.utils.common import pprint_error, pprint_network_error
# from phiterm.utils.log import logger
# from phiterm.zeus_api.client import ZeusApi, get_authenticated_client, validate_response
#
#
# def convert_gcp_project_response_to_schema(
#     resp: httpx.Response,
# ) -> Optional[schemas.GCPProjectSchema]:
#
#     gcp_project_dict = resp.json()
#     if gcp_project_dict is None:
#         return None
#     if not isinstance(gcp_project_dict, dict):
#         raise exceptions.ZeusGcpApiException(
#             "Could not parse GCPProjectSchema response"
#         )
#
#     # If the request failed, display the message from BackendResponse
#     if (
#         resp.status_code == httpx.codes.BAD_REQUEST
#         and gcp_project_dict.get("status", "FAIL") == "FAIL"
#     ):
#         pprint_error(
#             gcp_project_dict.get("message", gcp_project_dict.get("detail", "FAIL"))
#         )
#
#     # If everything is good, convert gcp_project_dict to GCPProjectSchema and return
#     if resp.status_code == httpx.codes.OK:
#         return schemas.GCPProjectSchema.from_dict(gcp_project_dict)
#
#     return None
#
#
# def get_primary_gcp_project(
#     id_workspace: int,
# ) -> Optional[schemas.GCPProjectSchema]:
#
#     logger.debug("Getting active GCPProjectSchema")
#     authenticated_client = get_authenticated_client()
#     if authenticated_client is None:
#         return None
#     with authenticated_client as api:
#         try:
#             r: httpx.Response = api.get(
#                 "{}/{}".format(ZeusApi.read_primary_gcp_project, id_workspace)
#             )
#             validate_response(r)
#         except httpx.NetworkError as e:
#             pprint_network_error()
#             return None
#
#         # logger.debug("url: {}".format(r.url))
#         # logger.debug("status: {}".format(r.status_code))
#         # logger.debug("json: {}".format(r.json()))
#         return convert_gcp_project_response_to_schema(r)
#
#
# def upsert_gcp_project(
#     gcp_project_upsert: schemas.UpsertGCPProjectFromCli,
# ) -> Optional[schemas.GCPProjectSchema]:
#
#     logger.debug(
#         "Upserting GCPProjectSchema. Post: {}".format(ZeusApi.upsert_gcp_project)
#     )
#     authenticated_client = get_authenticated_client()
#     if authenticated_client is None:
#         return None
#     with authenticated_client as api:
#         try:
#             r: httpx.Response = api.post(
#                 ZeusApi.upsert_gcp_project,
#                 data=gcp_project_upsert.dict(),
#             )
#             validate_response(r)
#         except httpx.NetworkError as e:
#             pprint_network_error()
#             return None
#
#         # logger.debug("url: {}".format(r.url))
#         # logger.debug("status: {}".format(r.status_code))
#         # logger.debug("json: {}".format(r.json()))
#
#         if r.status_code == httpx.codes.OK:
#             logger.debug("GCPProjectSchema Upserted")
#             return convert_gcp_project_response_to_schema(r)
#
#     return None
#
#
# def update_gcp_project(
#     gcp_project_update: schemas.UpdateGCPProject,
# ) -> Optional[schemas.GCPProjectSchema]:
#
#     logger.debug(
#         "Updating GCPProjectSchema. Post: {}".format(ZeusApi.update_gcp_project)
#     )
#     authenticated_client = get_authenticated_client()
#     if authenticated_client is None:
#         return None
#     with authenticated_client as api:
#         try:
#             r: httpx.Response = api.post(
#                 ZeusApi.update_gcp_project, data=gcp_project_update.dict()
#             )
#             validate_response(r)
#         except httpx.NetworkError as e:
#             pprint_network_error()
#             return None
#
#         # logger.debug("url: {}".format(r.url))
#         # logger.debug("status: {}".format(r.status_code))
#         # logger.debug("json: {}".format(r.json()))
#         return convert_gcp_project_response_to_schema(r)
#
#
# def get_gke_cluster_for_gcp_project(
#     id_workspace: int,
#     id_project: str,
# ) -> Optional[schemas.GKEClusterSchema]:
#
#     logger.debug(
#         "Getting GKEClusterSchema for workspace {} and project {}".format(
#             id_workspace, id_project
#         )
#     )
#     authenticated_client = get_authenticated_client()
#     if authenticated_client is None:
#         return None
#     with authenticated_client as api:
#         try:
#             r: httpx.Response = api.get(
#                 ZeusApi.get_gke_cluster,
#                 params={"id_project": id_project, "id_workspace": id_workspace},
#             )
#             validate_response(r)
#         except httpx.NetworkError as e:
#             pprint_network_error()
#             return None
#
#         # logger.debug("url: {}".format(r.url))
#         # logger.debug("status: {}".format(r.status_code))
#         # logger.debug("json: {}".format(r.json()))
#
#         gke_cluster_dict: Union[Dict[Any, Any], List[Any]] = r.json()
#
#         if gke_cluster_dict is None:
#             return None
#         if not isinstance(gke_cluster_dict, dict):
#             raise exceptions.ZeusGcpApiException(
#                 "Could not parse GKEClusterSchema response"
#             )
#
#         # If the request failed, display the message from BackendResponse
#         if (
#             r.status_code == httpx.codes.BAD_REQUEST
#             and gke_cluster_dict.get("status", "FAIL") == "FAIL"
#         ):
#             logger.debug(
#                 "Error while getting GKEClusterSchema: {}".format(
#                     gke_cluster_dict.get(
#                         "message", gke_cluster_dict.get("detail", "FAIL")
#                     )
#                 )
#             )
#
#         # If everything is good, convert gke_cluster_response to GKEClusterSchema and return
#         if r.status_code == httpx.codes.OK:
#             return schemas.GKEClusterSchema.from_dict(gke_cluster_dict)
#
#     return None
#
#
# def get_or_create_gke_cluster_for_gcp_project(
#     id_workspace: int, id_project: str, pak8_conf: Pak8Conf
# ) -> Optional[schemas.GKEClusterRelease]:
#
#     logger.debug(
#         "Creating GKEClusterSchema for workspace {} and project {}".format(
#             id_workspace, id_project
#         )
#     )
#     authenticated_client = get_authenticated_client()
#     if authenticated_client is None:
#         return None
#     with authenticated_client as api:
#         try:
#             # Set the timeout to None because the response for this request could take a while
#             r: httpx.Response = api.post(
#                 ZeusApi.get_or_create_gke_cluster,
#                 params={"id_project": id_project, "id_workspace": id_workspace},
#                 data=pak8_conf.json(),
#                 timeout=None,
#             )
#             validate_response(r)
#         except httpx.NetworkError as e:
#             pprint_error(
#                 "NetworkError, please confirm you are connected to the internet"
#             )
#             return None
#
#         logger.debug("url: {}".format(r.url))
#         logger.debug("status: {}".format(r.status_code))
#         logger.debug("json: {}".format(r.json()))
#
#         gke_cluster_release_dict: Union[Dict[Any, Any], List[Any]] = r.json()
#
#         if gke_cluster_release_dict is None:
#             return None
#         if not isinstance(gke_cluster_release_dict, dict):
#             raise exceptions.ZeusGcpApiException(
#                 "Could not parse GKEClusterRelease response"
#             )
#
#         # If the request failed, display the message from BackendResponse
#         if (
#             r.status_code == httpx.codes.BAD_REQUEST
#             and gke_cluster_release_dict.get("status", "FAIL") == "FAIL"
#         ):
#             pprint_error(
#                 gke_cluster_release_dict.get(
#                     "message", gke_cluster_release_dict.get("detail", "FAIL")
#                 )
#             )
#
#         # If everything is good, convert gke_cluster_response to GKEClusterSchema and return
#         if r.status_code == httpx.codes.OK:
#             return schemas.GKEClusterRelease.from_dict(gke_cluster_release_dict)
#
#     return None
#
#
# def delete_gke_cluster_if_exists(
#     id_workspace: int, id_project: str
# ) -> Optional[schemas.GKEClusterRelease]:
#
#     logger.debug(
#         "Deleting GKEClusterSchema for workspace {} and project {}".format(
#             id_workspace, id_project
#         )
#     )
#     authenticated_client = get_authenticated_client()
#     if authenticated_client is None:
#         return None
#     with authenticated_client as api:
#         try:
#             # Set the timeout to None because the response for this request could take a while
#             r: httpx.Response = api.get(
#                 ZeusApi.delete_gke_cluster_if_exists,
#                 params={"id_project": id_project, "id_workspace": id_workspace},
#                 timeout=None,
#             )
#             validate_response(r)
#         except httpx.NetworkError as e:
#             pprint_network_error()
#             return None
#
#         logger.debug("url: {}".format(r.url))
#         logger.debug("status: {}".format(r.status_code))
#         logger.debug("json: {}".format(r.json()))
#
#         gke_cluster_release_dict: Union[Dict[Any, Any], List[Any]] = r.json()
#
#         if gke_cluster_release_dict is None:
#             return None
#         if not isinstance(gke_cluster_release_dict, dict):
#             raise exceptions.ZeusGcpApiException(
#                 "Could not parse GKEClusterRelease response"
#             )
#
#         # If the request failed, display the message from BackendResponse
#         if (
#             r.status_code == httpx.codes.BAD_REQUEST
#             and gke_cluster_release_dict.get("status", "FAIL") == "FAIL"
#         ):
#             pprint_error(
#                 gke_cluster_release_dict.get(
#                     "message", gke_cluster_release_dict.get("detail", "FAIL")
#                 )
#             )
#
#         # If everything is good, convert gke_cluster_response to GKEClusterRelease and return
#         if r.status_code == httpx.codes.OK:
#             return schemas.GKEClusterRelease.from_dict(gke_cluster_release_dict)
#
#     return None
