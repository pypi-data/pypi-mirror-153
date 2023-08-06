# from pathlib import Path
# from typing import Any, Dict, List, Optional
#
# import pydantic
# import yaml
#
# import pak8.enums as pak8_enums
# from pak8.conf import Pak8Conf
# from pak8.gcp.gcp_pak8 import GCPPak8
# from pak8.k8s.pak8_k8s_client import Pak8K8sClient
# from pak8.k8s.resources.kubeconfig import Kubeconfig
# from phi import schemas
# from phiterm.conf.phi_conf import PhiConf, PhiK8sData
# from phiterm.k8s.k8s_ops import (
#     apply_k8s_resources_for_k8s_client,
#     get_active_k8s_resources_for_k8s_client,
#     get_k8s_resource_groups_as_dicts,
#     get_k8s_resources_as_dicts,
# )
# from phiterm.utils.common import pprint_error, pprint_info, pprint_status, pprint_subheading
# from phiterm.utils.filesystem import delete_files_in_dir
# from phiterm.utils.log import logger
#
#
# def save_k8s_resources_as_yaml(
#     ws_schema: schemas.WorkspaceSchema,
#     config: PhiConf,
#     refresh: bool = False,
#     type_filters: Optional[List[str]] = None,
#     name_filters: Optional[List[str]] = None,
# ) -> bool:
#     """Saves the K8s resources for a workspace in the `phi` dir for that workspace.
#     There are 2 ways of generating the K8s resources:
#     1. API call to zeus, zeus sends back the manifests as dicts, we save them as yaml
#     2. Use Pak8 directly, this leads to a faster development process
#
#     Currently we're using 2, but switching to 1 is easy if needed.
#     """
#
#     ws_name: str = ws_schema.name
#     logger.debug(f"Generating K8s resources for ws: {ws_name}")
#
#     # Step 1: Get the Pak8Conf for the workspace
#     pak8_conf: Optional[Pak8Conf] = config.get_ws_pak8_conf_by_name(ws_name, refresh)
#     if pak8_conf is None:
#         pprint_error(f"Unable to parse config for {ws_name}")
#         return False
#
#     # Step 2: Get the K8s resource groups
#     k8s_resource_groups: Optional[
#         Dict[str, List[Dict[str, Any]]]
#     ] = get_k8s_resource_groups_as_dicts(
#         pak8_conf=pak8_conf, type_filters=type_filters, name_filters=name_filters
#     )
#     # This snippet receives the manifests from zues, currently commented out
#     # pak8_k8s_resources: Optional[Dict[str, List[Dict[str, Any]]]] = zeus_api.get_k8s_resource_groups_as_dicts(
#     #     id_workspace=ws_schema.id_workspace, pak8_conf=pak8_conf
#     # )
#
#     _resource_list: List[str] = []
#     _resources_str: str = ""
#     _resources_dir: Optional[Path] = config.get_k8s_resources_dir_path_by_ws_name(
#         ws_name
#     )
#     if k8s_resource_groups is None:
#         pprint_error("No K8s Resources available")
#         return False
#     elif _resources_dir is None:
#         pprint_error("Could not find path to store K8s resources")
#         return False
#
#     # delete directory to save resources if needed
#     if _resources_dir.exists():
#         if _resources_dir.is_file():
#             _resources_dir.unlink()
#         elif _resources_dir.is_dir():
#             delete_files_in_dir(_resources_dir)
#     _resources_dir.mkdir(exist_ok=True)
#
#     for rg_name, _rsrc_list in k8s_resource_groups.items():
#         # logger.debug("Processing K8sResourceGroup: {}\n{}".format(rg_name, _rsrc_list))
#         _rg_dir: Path = _resources_dir.joinpath(rg_name)
#         _rg_dir.mkdir(exist_ok=True)
#         for _rsrc_dict in _rsrc_list:
#             if _rsrc_dict:
#                 _fn_str = _rsrc_dict.get("metadata", {"name": "no_metadata_avl"}).get(
#                     "name", "no_name_avl"
#                 )
#                 _rsrc_file: Path = _rg_dir.joinpath(f"{_fn_str}.yaml")
#                 logger.debug(f"Creating {str(_rsrc_file)}")
#                 with open(_rsrc_file, "w") as _rsrc_f:
#                     yaml.dump(_rsrc_dict, _rsrc_f)
#
#     pprint_info(f"K8s resources saved under: {str(_resources_dir)}")
#     return True
#
#
# def print_k8s_resources_as_yaml(
#     ws_schema: schemas.WorkspaceSchema,
#     config: PhiConf,
#     refresh: bool = False,
#     type_filters: Optional[List[str]] = None,
#     name_filters: Optional[List[str]] = None,
# ) -> bool:
#     """Print the K8s resources for a workspace.
#     Similar to save but prints the resources instead
#     """
#
#     ws_name: str = ws_schema.name
#     logger.debug(f"Generating K8s resources for ws: {ws_name}")
#
#     # Step 1: Get the Pak8Conf for the workspace
#     pak8_conf: Optional[Pak8Conf] = config.get_ws_pak8_conf_by_name(ws_name, refresh)
#     if pak8_conf is None:
#         pprint_error(f"Unable to parse config for {ws_name}")
#         return False
#
#     # Step 2: Get the K8s resources
#     pak8_k8s_resources: Optional[List[Dict[str, Any]]] = get_k8s_resources_as_dicts(
#         pak8_conf=pak8_conf, type_filters=type_filters, name_filters=name_filters
#     )
#     if pak8_k8s_resources is None:
#         pprint_error("No K8s resources available")
#         return False
#
#     print(yaml.dump_all(pak8_k8s_resources))
#     # pprint_info(pak8_k8s_resources)
#     # for _rsrc_dict in pak8_k8s_resources:
#     #     if _rsrc_dict:
#     #         pprint_info(yaml.dump(_rsrc_dict))
#     return True
#
#
# def apply_k8s_resources(
#     ws_schema: schemas.WorkspaceSchema,
#     config: PhiConf,
#     refresh: bool = False,
#     service_filters: Optional[List[str]] = None,
#     type_filters: Optional[List[str]] = None,
#     name_filters: Optional[List[str]] = None,
# ) -> bool:
#     """Apply the K8s resources for a workspace"""
#
#     ws_name: str = ws_schema.name
#     logger.debug(f"Applying K8s resources for ws: {ws_schema.name}")
#
#     # Step 1: Get the Pak8Conf for the workspace
#     pak8_conf: Optional[Pak8Conf] = config.get_ws_pak8_conf_by_name(
#         ws_name=ws_name, refresh=refresh, add_kubeconfig=True
#     )
#     if pak8_conf is None:
#         pprint_error(f"Unable to parse config for {ws_schema.name}")
#         return False
#
#     # Step 2: Create a GCPPak8 from the pak8_conf and validate
#     # TODO: Use Pak8Type
#     ws_pak8: Optional[GCPPak8] = None
#     try:
#         if pak8_conf.cloud_provider == pak8_enums.Pak8CloudProvider.GCP:
#             ws_pak8 = GCPPak8(pak8_conf)
#             logger.debug("GCPPak8 Created")
#             if ws_pak8 is None or not isinstance(ws_pak8, GCPPak8):
#                 logger.error("Invalid GCPPak8: {}".format(ws_pak8))
#                 return False
#         else:
#             logger.error(
#                 "Cloud Provider {} not yet supported".format(pak8_conf.cloud_provider)
#             )
#             return False
#     except pydantic.ValidationError as e:
#         logger.debug("e: {}".format(e))
#         error_msg = "Config Validation Errors. Details:\n{}".format(e)
#         logger.error(error_msg)
#         return False
#
#     # Step 3: Get the current status of this Pak8
#     pak8_status: pak8_enums.Pak8Status = ws_pak8.get_pak8_status()
#     logger.debug("Pak8 is {}".format(pak8_status))
#
#     if pak8_status == pak8_enums.Pak8Status.CREATING_K8S_CLUSTER:
#         pprint_info("The cluster is being created, please try again in a few minutes")
#         return False
#     if not pak8_status.k8s_cluster_is_available():
#         pprint_info("No K8s Cluster available.")
#         return False
#
#     pak8_k8s_client: Optional[Pak8K8sClient] = ws_pak8.get_pak8_k8s_client()
#     if pak8_k8s_client is None:
#         pprint_error("K8s client unavailable.")
#         return False
#
#     # Step 4: After the GKEClusterSchema & K8sApiClient is available, we should have a PhiK8sData and kubeconfig
#     # If the PhiK8sData is not available, save the kubeconfig for future use
#     ws_k8s_data: Optional[PhiK8sData] = config.get_ws_k8s_data_by_name(ws_name)
#     if ws_k8s_data is None:
#         kconf_resource: Optional[Kubeconfig] = ws_pak8.get_kubeconfig()
#         if kconf_resource:
#             ws_k8s_data = config.update_ws_k8s_data(
#                 ws_name=ws_name, kubeconfig_resource=kconf_resource
#             )
#             if ws_k8s_data:
#                 pprint_status(f"Kubeconfig saved to: {ws_k8s_data.kubeconfig_path}")
#
#     # Step 5: Apply the K8s resources
#     return apply_k8s_resources_for_k8s_client(
#         pak8_conf=pak8_conf,
#         pak8_k8s_client=pak8_k8s_client,
#         service_filters=service_filters,
#         type_filters=type_filters,
#         name_filters=name_filters,
#     )
#
#
# def get_active_k8s_resources(
#     ws_schema: schemas.WorkspaceSchema,
#     config: PhiConf,
#     service_filters: Optional[List[str]] = None,
#     type_filters: Optional[List[str]] = None,
#     name_filters: Optional[List[str]] = None,
# ) -> Optional[Dict[str, List[Any]]]:
#     """Get active K8s resources for a workspace"""
#
#     ws_name: str = ws_schema.name
#     logger.debug(f"Getting active K8s resources for ws: {ws_schema.name}")
#
#     # Step 1: Get the Pak8Conf for the workspace
#     pak8_conf: Optional[Pak8Conf] = config.get_ws_pak8_conf_by_name(
#         ws_name=ws_name, refresh=False, add_kubeconfig=True
#     )
#     if pak8_conf is None:
#         pprint_error(f"Unable to parse config for {ws_schema.name}")
#         return None
#
#     # Step 2: Create a GCPPak8 from the pak8_conf and validate
#     # TODO: Use pak8.Pak8Type
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
#     # Step 3: Validate the current status of this Pak8
#     pak8_status: pak8_enums.Pak8Status = ws_pak8.get_pak8_status()
#     logger.debug("Pak8 is {}".format(pak8_status))
#
#     if pak8_status not in (
#         pak8_enums.Pak8Status.READY_TO_DEPLOY_K8S_RESOURCES,
#         pak8_enums.Pak8Status.K8S_RESOURCES_ACTIVE,
#     ):
#         logger.debug(f"returning because pak8_status: {pak8_status}")
#         return None
#
#     pak8_k8s_client: Optional[Pak8K8sClient] = ws_pak8.get_pak8_k8s_client()
#     if pak8_k8s_client is None:
#         pprint_error("K8s client unavailable.")
#         return None
#
#     # Step 4: After the GKEClusterSchema & K8sApiClient is available, we should have a PhiK8sData and kubeconfig
#     # If the PhiK8sData is not available, save the kubeconfig for future use
#     ws_k8s_data: Optional[PhiK8sData] = config.get_ws_k8s_data_by_name(ws_name)
#     if ws_k8s_data is None:
#         kconf_resource: Optional[Kubeconfig] = ws_pak8.get_kubeconfig()
#         if kconf_resource:
#             ws_k8s_data = config.update_ws_k8s_data(
#                 ws_name=ws_name, kubeconfig_resource=kconf_resource
#             )
#             if ws_k8s_data:
#                 pprint_status(f"Kubeconfig saved to: {ws_k8s_data.kubeconfig_path}")
#
#     # Step 5: Get the active K8s resources from the K8s Client
#     return get_active_k8s_resources_for_k8s_client(
#         pak8_conf=pak8_conf,
#         pak8_k8s_client=pak8_k8s_client,
#         service_filters=service_filters,
#         type_filters=type_filters,
#         name_filters=name_filters,
#     )
#
#
# def print_active_k8s_resources(
#     ws_schema: schemas.WorkspaceSchema,
#     config: PhiConf,
#     service_filters: Optional[List[str]] = None,
#     type_filters: Optional[List[str]] = None,
#     name_filters: Optional[List[str]] = None,
# ) -> None:
#     """Print active K8s objects for a workspace"""
#
#     active_k8s_resources: Optional[Dict[str, List[Any]]] = get_active_k8s_resources(
#         ws_schema=ws_schema,
#         config=config,
#         service_filters=service_filters,
#         type_filters=type_filters,
#         name_filters=name_filters,
#     )
#     if active_k8s_resources:
#         pprint_subheading("Active Resources: FIX ME")
#         # pprint_info(active_k8s_resources)
#     else:
#         pprint_subheading("No Active Resources")
