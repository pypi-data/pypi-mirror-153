# from typing import Any, Dict, List, Optional
#
# import pydantic
#
# import pak8.enums as pak8_enums
# from pak8.conf import Pak8Conf
# from pak8.gcp.gcp_pak8 import GCPPak8
# from pak8.k8s.clients.pak8_k8s_client import Pak8K8sClient
# from phiterm.utils.common import is_empty
# from phiterm.utils.log import logger
#
#
# def get_k8s_resources_as_dicts(
#     pak8_conf: Pak8Conf,
#     type_filters: Optional[List[str]] = None,
#     name_filters: Optional[List[str]] = None,
# ) -> Optional[List[Dict[str, Any]]]:
#     """For a given Pak8Conf, gets the k8s manifests as Dictionaries and returns them
#     as a List of Dicts.
#
#     Args:
#     pak8_conf: Conf being deployed
#
#     Returns:
#     Optional[List[Dict[str, Any]]]: List of K8s resources which can be applied to a k8s cluster after converting to yaml
#     """
#
#     logger.debug("Creating Pak8: {}".format(pak8_conf.name))
#
#     # Step 1: Create a GCPPak8 from the pak8_conf and validate
#     ws_pak8: Optional[GCPPak8] = None
#     try:
#         if pak8_conf.cloud_provider == pak8_enums.Pak8CloudProvider.GCP:
#             ws_pak8 = GCPPak8(pak8_conf)
#             logger.debug("GCPPak8 Created")
#             if ws_pak8 is None or not isinstance(ws_pak8, GCPPak8):
#                 logger.error("Invalid GCPPak8: {}".format(ws_pak8))
#                 return None
#         else:
#             logger.error(
#                 "Cloud Provider {} not yet supported".format(pak8_conf.cloud_provider)
#             )
#             return None
#     except pydantic.ValidationError as e:
#         logger.debug("e: {}".format(e))
#         error_msg = "Config Validation Errors. Details:\n{}".format(e)
#         logger.error(error_msg)
#         return None
#
#     ws_k8s_resource = ws_pak8.get_k8s_resources_as_dicts(
#         type_filters=type_filters, name_filters=name_filters
#     )
#
#     return ws_k8s_resource
#
#
# def get_k8s_resource_groups_as_dicts(
#     pak8_conf: Pak8Conf,
#     type_filters: Optional[List[str]] = None,
#     name_filters: Optional[List[str]] = None,
# ) -> Optional[Dict[str, List[Dict[str, Any]]]]:
#     """For a given Pak8Conf, gets the k8s manifests as Dictionaries and returns them
#     as a List of Dicts.
#
#     Args:
#     pak8_conf: Conf being deployed
#
#     Returns:
#     Optional[List[Dict[str, Any]]]: List of K8s resources which can be applied to a k8s cluster after converting to yaml
#     """
#
#     logger.debug("Creating Pak8: {}".format(pak8_conf.name))
#
#     # Step 1: Create a GCPPak8 from the pak8_conf and validate
#     ws_pak8: Optional[GCPPak8] = None
#     try:
#         if pak8_conf.cloud_provider == pak8_enums.Pak8CloudProvider.GCP:
#             ws_pak8 = GCPPak8(pak8_conf)
#             logger.debug("GCPPak8 Created")
#             if ws_pak8 is None or not isinstance(ws_pak8, GCPPak8):
#                 logger.error("Invalid GCPPak8: {}".format(ws_pak8))
#                 return None
#         else:
#             logger.error(
#                 "Cloud Provider {} not yet supported".format(pak8_conf.cloud_provider)
#             )
#             return None
#     except pydantic.ValidationError as e:
#         logger.debug("e: {}".format(e))
#         error_msg = "Config Validation Errors. Details:\n{}".format(e)
#         logger.error(error_msg)
#         return None
#
#     ws_k8s_resource_groups: Optional[
#         Dict[str, List[Dict[str, Any]]]
#     ] = ws_pak8.get_k8s_resource_groups_as_dicts(
#         type_filters=type_filters, name_filters=name_filters
#     )
#
#     return ws_k8s_resource_groups
#
#
# def apply_k8s_resources_for_k8s_client(
#     pak8_conf: Pak8Conf,
#     pak8_k8s_client: Pak8K8sClient,
#     service_filters: Optional[List[str]] = None,
#     type_filters: Optional[List[str]] = None,
#     name_filters: Optional[List[str]] = None,
# ) -> bool:
#     """For a given Pak8Conf and Pak8K8sClient, applies the k8s manifests
#
#     Args:
#     pak8_conf: Conf being deployed
#     pak8_k8s_client:
#
#     Returns:
#     bool: True is the resources were applied successfully
#     """
#
#     if is_empty(service_filters):
#         pak8_k8s_client.create_resources(
#             type_filters=type_filters,
#             name_filters=name_filters,
#         )
#         return True
#
#     ######################################################
#     ## Applying Pak8 Services
#     ######################################################
#
#     # if pak8_conf.services is None:
#     #     return False
#     #
#     # # Create a list of services to apply
#     # _pak8_svc_dict = {s.name: s for s in pak8_conf.services}
#     # _pak8_services_to_apply: List[pak8.Pak8AppConf] = []
#     # for _svc_nm in service_filters:
#     #     if _svc_nm not in _pak8_svc_dict:
#     #         pprint_error(f"Service {_svc_nm} not found")
#     #         continue
#     #     _pak8_services_to_apply.append(_pak8_svc_dict[_svc_nm])
#     # if len(_pak8_services_to_apply) == 0:
#     #     pprint_status(f"No Pak8Services found")
#     #     return False
#     #
#     # pprint_status(f"Applying {len(_pak8_services_to_apply)} Pak8Services")
#     # pprint_status(f"Applying Namespace Resource")
#     # k8s_namespace_created = pak8_k8s_client.create_namespace_resource()
#     # pprint_status(f"Applying RBAC Resources")
#     # k8s_rbac_created = pak8_k8s_client.create_rbac_resources()
#     #
#     # k8s_namespace: str = pak8_k8s_client.get_k8s_namespace_to_use()
#     # k8s_sa: str = pak8_k8s_client.get_k8s_service_account_to_use()
#     # services_to_apply: List[pak8.Pak8ServiceBase] = []
#     # for _pak8_svc in _pak8_services_to_apply:
#     #     services_to_apply.append(
#     #        services.build_pak8_service_from_conf(
#     #             pak8_svc_conf=_pak8_svc,
#     #             namespace=k8s_namespace,
#     #             service_account=k8s_sa,
#     #             pak8_name=pak8_conf.name,
#     #             pak8_version=pak8_conf.version,
#     #             pak8_cloud_provider=pak8_conf.cloud_provider,
#     #         )
#     #     )
#     #
#     # k8s_api: Optional[pak8.K8sApi] = pak8_k8s_client.k8s_api
#     # for svc in services_to_apply:
#     #     svc.create_resources(
#     #         k8s_api=k8s_api,
#     #         namespace=k8s_namespace,
#     #         type_filters=type_filters,
#     #         name_filters=name_filters,
#     #     )
#     return True
#
#
# def get_active_k8s_resources_for_k8s_client(
#     pak8_conf: Pak8Conf,
#     pak8_k8s_client: Pak8K8sClient,
#     service_filters: Optional[List[str]] = None,
#     type_filters: Optional[List[str]] = None,
#     name_filters: Optional[List[str]] = None,
# ) -> Optional[Dict[str, List]]:
#     """For a given Pak8Conf and Pak8K8sClient, applies the k8s manifests
#
#     Args:
#     pak8_conf: Conf being deployed
#     pak8_k8s_client:
#
#     Returns:
#     bool: True is the resources were applied successfully
#     """
#
#     if is_empty(service_filters):
#         logger.debug("Getting Active K8s Resources")
#         return pak8_k8s_client.get_active_resources(
#             type_filters=type_filters,
#             name_filters=name_filters,
#         )
#
#     ######################################################
#     ## Get active resources for Pak8 Services
#     ######################################################
#
#     return None
#     # if pak8_conf.services is None:
#     #     return False
#     #
#     # # Create a list of services to apply
#     # _pak8_svc_dict = {s.name: s for s in pak8_conf.services}
#     # _pak8_services_to_scan: List[pak8.Pak8AppConf] = []
#     # for _svc_nm in service_filters:
#     #     if _svc_nm not in _pak8_svc_dict:
#     #         pprint_error(f"Service {_svc_nm} not found")
#     #         continue
#     #     _pak8_services_to_scan.append(_pak8_svc_dict[_svc_nm])
#     # if len(_pak8_services_to_scan) > 0:
#     #     pprint_status(
#     #         f"Getting Active K8s Resources for {len(_pak8_services_to_scan)} Pak8Services"
#     #     )
#     #
#     # k8s_namespace: str = pak8_k8s_client.get_k8s_namespace_to_use()
#     # k8s_sa: str = pak8_k8s_client.get_k8s_service_account_to_use()
#     # services_to_scan: List[pak8.Pak8ServiceBase] = []
#     # for _pak8_svc in _pak8_services_to_scan:
#     #     services_to_scan.append(
#     #        services.build_pak8_service_from_conf(
#     #             pak8_svc_conf=_pak8_svc,
#     #             namespace=k8s_namespace,
#     #             service_account=k8s_sa,
#     #             pak8_name=pak8_conf.name,
#     #             pak8_version=pak8_conf.version,
#     #             pak8_cloud_provider=pak8_conf.cloud_provider,
#     #         )
#     #     )
#     #
#     # k8s_api: Optional[pak8.K8sApi] = pak8_k8s_client.k8s_api
#     # active_k8s_resources: Dict[str, List] = defaultdict(list)
#     # for svc in services_to_scan:
#     #     _resources_for_svc = svc.get_active_resources(
#     #         k8s_api=k8s_api,
#     #         namespace=k8s_namespace,
#     #         type_filters=type_filters,
#     #         name_filters=name_filters,
#     #     )
#     #     for resource_type, active_objects in _resources_for_svc.items():
#     #         active_k8s_resources[resource_type].extend(active_objects)
#     # return active_k8s_resources
