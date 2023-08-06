# from typing import Any, Dict, List, Optional, Union, cast
#
# import httpx
#
# from pak8.conf import Pak8Conf
# from phi import exceptions, schemas
# from phiterm.utils.common import (
#     isinstanceany,
#     pprint_info,
#     pprint_error,
#     pprint_info,
#     pprint_network_error,
# )
# from phiterm.utils.log import logger
# from phiterm.zeus_api.client import ZeusApi, get_authenticated_client, validate_response
#
#
# def get_k8s_manifests_for_workspace(
#     id_workspace: int, pak8_conf: Pak8Conf
# ) -> Optional[List[Dict[str, Any]]]:
#
#     logger.debug("Get K8s Resources")
#     authenticated_client = get_authenticated_client()
#     if authenticated_client is None:
#         return None
#     with authenticated_client as api:
#         try:
#             r: httpx.Response = api.post(
#                 "{}/{}".format(ZeusApi.get_k8s_manifests, id_workspace),
#                 data=pak8_conf.json(),
#             )
#             validate_response(r)
#         except httpx.NetworkError as e:
#             pprint_network_error()
#             return None
#
#         # logger.debug("url: {}".format(r.url))
#         # logger.debug("status: {}".format(r.status_code))
#         # logger.debug("json: {}".format(r.json()))
#         resp_data: Union[Dict[Any, Any], List[Any]] = r.json()
#
#         # logger.debug("resp_data type: {}".format(type(resp_data)))
#         if not isinstanceany(resp_data, [dict, list]):
#             raise exceptions.ZeusK8sApiException(
#                 "Could not parse zeus K8s response. Expected `list` or `dict`, Received: {}".format(
#                     type(resp_data)
#                 )
#             )
#
#         if isinstance(resp_data, dict):
#             if (
#                 r.status_code == httpx.codes.BAD_REQUEST
#                 and resp_data.get("status", "FAIL") == "FAIL"
#             ):
#                 pprint_error(resp_data.get("message", resp_data.get("detail", "FAIL")))
#
#         if r.status_code == httpx.codes.OK:
#             return cast(List[Dict[str, Any]], resp_data)
#
#     return None
#
#
# def apply_k8s_manifests_for_workspace(id_workspace: int, pak8_conf: Pak8Conf) -> bool:
#     """Makes an API call to zeus to apply all k8s manifests and
#     returns True if the action was successful
#     """
#
#     logger.debug("Apply K8s Resources")
#     authenticated_client = get_authenticated_client()
#     if authenticated_client is None:
#         return False
#     with authenticated_client as api:
#         try:
#             r: httpx.Response = api.post(
#                 "{}/{}".format(ZeusApi.apply_k8s_manifests, id_workspace),
#                 data=pak8_conf.json(),
#             )
#             validate_response(r)
#         except httpx.NetworkError as e:
#             pprint_network_error()
#             return False
#
#         logger.debug("url: {}".format(r.url))
#         logger.debug("status: {}".format(r.status_code))
#         logger.debug("json: {}".format(r.json()))
#         resp_data: Union[Dict[Any, Any], List[Any]] = r.json()
#
#         # logger.debug("resp_data type: {}".format(type(resp_data)))
#         if not isinstanceany(resp_data, [dict, list]):
#             raise exceptions.ZeusK8sApiException(
#                 "Could not parse zeus K8s response. Expected `list` or `dict`, Received: {}".format(
#                     type(resp_data)
#                 )
#             )
#
#         if isinstance(resp_data, dict):
#             if (
#                 r.status_code == httpx.codes.BAD_REQUEST
#                 and resp_data.get("status", "FAIL") == "FAIL"
#             ):
#                 pprint_error(resp_data.get("message", resp_data.get("detail", "FAIL")))
#             elif r.status_code == httpx.codes.OK:
#                 message_log = resp_data.get("message_log", "Failed")
#                 if resp_data.get("status", "FAIL") == "SUCCESS":
#                     pprint_info(
#                         "Message: {}".format(resp_data.get("message", "Failed"))
#                     )
#                     pprint_info("Log:\n  - {}".format("\n  - ".join(message_log)))
#                     return True
#                 else:
#                     pprint_error(
#                         "Message: {}".format(resp_data.get("message", "Failed"))
#                     )
#                     pprint_info("Log:\n  - {}".format("\n  - ".join(message_log)))
#
#     return False
#
#
# def get_active_resources(
#     id_workspace: int,
#     id_project: str,
#     id_cluster: str,
#     type_filters: Optional[List[str]] = None,
#     name_filters: Optional[List[str]] = None,
# ) -> Optional[List[Any]]:
#     """Makes an API call to zeus to get all active k8s objects
#     TODO: Fix this when needed
#     """
#
#     logger.debug("Get Active K8s Objects")
#     authenticated_client = get_authenticated_client()
#     if authenticated_client is None:
#         return None
#     with authenticated_client as api:
#         try:
#             r: httpx.Response = api.post(
#                 ZeusApi.get_active_resources,
#                 params={
#                     "id_workspace": id_workspace,
#                     "id_project": id_project,
#                     "id_cluster": id_cluster,
#                 },
#                 data=schemas.K8sFilters(
#                     type_filters=type_filters,
#                     name_filters=name_filters,
#                 ).dict(),
#             )
#             validate_response(r)
#         except httpx.NetworkError as e:
#             pprint_network_error()
#             return None
#
#         logger.debug("url: {}".format(r.url))
#         logger.debug("status: {}".format(r.status_code))
#         logger.debug("json: {}".format(r.json()))
#         resp_data: Union[Dict[Any, Any], List[Any]] = r.json()
#
#         logger.debug("resp_data type: {}".format(type(resp_data)))
#         if not isinstanceany(resp_data, [dict, list]):
#             raise exceptions.ZeusK8sApiException(
#                 "Could not parse zeus K8s response. Expected `list` or `dict`, Received: {}".format(
#                     type(resp_data)
#                 )
#             )
#
#         return None
#     #     if isinstance(resp_data, dict):
#     #         if (
#     #             r.status_code == httpx.codes.BAD_REQUEST
#     #             and resp_data.get("status", "FAIL") == "FAIL"
#     #         ):
#     #             pprint_error(resp_data.get("message", resp_data.get("detail", "FAIL")))
#     #         elif r.status_code == httpx.codes.OK:
#     #             message_log = resp_data.get("message_log", "Failed")
#     #             if resp_data.get("status", "FAIL") == "SUCCESS":
#     #                 pprint_info("Message: {}".format(resp_data.get("message", "Failed")))
#     #                 pprint_info("Log:\n  - {}".format("\n  - ".join(message_log)))
#     #                 return True
#     #             else:
#     #                 pprint_error(
#     #                     "Message: {}".format(resp_data.get("message", "Failed"))
#     #                 )
#     #                 pprint_info("Log:\n  - {}".format("\n  - ".join(message_log)))
#
#     # return False
