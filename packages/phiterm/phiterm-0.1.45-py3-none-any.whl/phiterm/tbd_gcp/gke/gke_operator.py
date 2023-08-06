# import time
# from typing import Optional, cast
#
# import pydantic
#
# import pak8.exceptions as pak8_exceptions
# from pak8.conf import Pak8Conf
# from pak8.gcp.gcp_pak8 import GCPPak8
# from pak8.k8s.resources.kubeconfig import Kubeconfig
# from phi import enums, schemas, zeus_api
# from phiterm.gcp.gke.gke_utils import (
#     delete_gke_cluster_for_pak8,
#     get_or_create_gke_cluster_for_pak8,
# )
# from phiterm.conf.phi_conf import PhiConf, PhiGcpData, PhiK8sData, WsReleases
# from phiterm.utils.common import (
#     pprint_info,
#     pprint_error,
#     pprint_info,
#     pprint_status,
#     pprint_subheading,
# )
# from phiterm.utils.dttm import current_datetime_utc
# from phiterm.utils.log import logger
# from phiterm.zeus_api.gcp import get_gke_cluster_for_gcp_project
#
#
# def secho_gke_cluster_status(
#     gke_cluster: Optional[schemas.GKEClusterSchema] = None,
# ) -> None:
#     if gke_cluster is None:
#         pprint_error(
#             "No GKEClusterSchema available, you can create one using `phi ws up` or `phi gke create-cluster`"
#         )
#         return
#     else:
#         pprint_subheading("GKEClusterSchema:")
#         logger.debug("GKEClusterSchema: {}".format(gke_cluster.json(indent=2)))
#
#
# def print_gke_cluster_status(
#     ws_schema: schemas.WorkspaceSchema, config: PhiConf
# ) -> None:
#     """Print the GKEClusterSchema status for a workspace if available
#     This function will first validate and sync the Pak8 with zeus
#     """
#
#     # Step 1: Get the Pak8 Conf for this workspace
#     # The refresh=True will reprocess the ws config
#     pak8_conf: Optional[Pak8Conf] = config.get_ws_pak8_conf_by_name(
#         ws_schema.name, refresh=True
#     )
#     if pak8_conf is None:
#         pprint_error(f"Unable to parse config for {ws_schema.name}")
#         return
#
#     # Step 2: Sync the Pak8Conf with Zeus
#     pprint_info("Syncing WorkspaceSchema Config")
#     synced_ws: Optional[schemas.WorkspaceSchema] = zeus_api.sync_ws_pak8_config(
#         id_workspace=ws_schema.id_workspace, pak8_conf=pak8_conf
#     )
#     if synced_ws is not None:
#         pprint_info("WorkspaceSchema Sync'd")
#
#     # Step 3: Get the GCPProjectSchema for this workspace
#     gcp_project: Optional[
#         schemas.GCPProjectSchema
#     ] = config.get_gcp_project_schema_by_ws_name(ws_schema.name)
#     if gcp_project is None:
#         pprint_error(
#             "No GCP Project available, please run `phi ws setup` to setup a GCP Project for this workspace"
#         )
#         return
#
#     # Step 4: Get the GKEClusterSchema from zeus
#     pprint_info("Getting GKE Cluster status")
#     pprint_info("TO BE IMPLEMENTED: GET THE GKECLUSTER STATUS FROM GCP")
#     id_ws = gcp_project.id_workspace
#     id_prj = gcp_project.id_project
#     gke_cluster: Optional[schemas.GKEClusterSchema] = None
#     if id_ws and id_prj:
#         gke_cluster = get_gke_cluster_for_gcp_project(
#             id_workspace=id_ws,
#             id_project=id_prj,
#         )
#         if gke_cluster is not None:
#             config.update_ws_gcp_data(ws_name=ws_schema.name, gke_cluster=gke_cluster)
#             secho_gke_cluster_status(gke_cluster)
#
#
# def get_or_create_gke_cluster(
#     ws_schema: schemas.WorkspaceSchema, config: PhiConf, skip_cache: bool = False
# ) -> Optional[schemas.GKEClusterSchema]:
#     """Checks if a GKEClusterSchema for a workspace is available, if yes, returns that cluster
#     If no cluster is available, creates a GKEClusterSchema for the workspace
#     """
#
#     ws_name: str = ws_schema.name
#     logger.debug(f"Getting GKEClusterSchema for ws: {ws_name}")
#
#     # Step 1: Get the Pak8Conf for the workspace
#     # Refresh the Pak8Conf to read new changes
#     pprint_status("Reading the latest config")
#     ws_pak8_conf: Optional[Pak8Conf] = config.get_ws_pak8_conf_by_name(
#         ws_name, refresh=True
#     )
#     if ws_pak8_conf is None:
#         pprint_error("WorkspaceSchema Config invalid")
#         pprint_status("Please fix your workspace config and try again")
#         return None
#     if ws_pak8_conf.gcp is None:
#         pprint_error("This workspace does not have a GCP project configured")
#         return None
#     if ws_pak8_conf.gcp.gke_cluster_config is None:
#         pprint_error(
#             "Invalid GKE Config, please fix the gcp.gke section of your config"
#         )
#         return None
#
#     # Step 2: Get the PhiGcpData, GCPProjectSchema and check if a GKEClusterSchema is already available.
#     # If not, then we create a new GKE_CLUSTER
#     ws_gcp_data: Optional[PhiGcpData] = config.get_ws_gcp_data_by_name(ws_name)
#     if ws_gcp_data is None or ws_gcp_data.gcp_project is None:
#         pprint_error(
#             "No GCP Project available, please run `phi gcp auth` to setup a GCP Project for this workspace"
#         )
#         return None
#     # Get the GCPProjectSchema for this workspace
#     # logger.debug("Getting GCPProjectSchema for this workspace")
#     gcp_project_id: str = ws_gcp_data.gcp_project_id
#     ws_gcp_project: schemas.GCPProjectSchema = ws_gcp_data.gcp_project
#     # Check if a GKEClusterSchema is already available, if not create a new GKE_CLUSTER
#     logger.debug("Checking if a GKEClusterSchema is already available")
#     ws_gke_cluster: Optional[schemas.GKEClusterSchema] = ws_gcp_data.gke_cluster
#     # logger.debug("GKE Cluster: {}".format(ws_gke_cluster.json()))
#     if ws_gke_cluster is not None and ws_gke_cluster.is_valid and not skip_cache:
#         pprint_info(
#             f"GKEClusterSchema: {ws_gke_cluster.cluster_name} is already available and active"
#         )
#         return ws_gke_cluster
#
#     ## CREATING A NEW GKE_CLUSTER
#     pprint_info(
#         f"Creating GKEClusterSchema: {ws_pak8_conf.gcp.gke_cluster_config.name}"
#     )
#
#     # Step 3: Get the GCPPak8 for this workspace
#     ws_gcp_pak8: Optional[GCPPak8] = None
#     try:
#         ws_gcp_pak8 = GCPPak8(ws_pak8_conf)
#         # logger.debug("GCPPak8 Created")
#     except pydantic.ValidationError as e:
#         error_msg = "Config Validation Error. Details:\n{}".format(e)
#         logger.error(error_msg)
#         return None
#     # If a GCPPak8 cannot be created then return None
#     if ws_gcp_pak8 is None or not isinstance(ws_gcp_pak8, GCPPak8):
#         logger.error("Invalid GCPPak8: {}".format(ws_gcp_pak8))
#         return None
#     # We need the user details to create the cluster
#     user: schemas.UserSchema = config.user
#
#     # Step 4: Check if there is an existing CREATE_GKE_CLUSTER releases available
#     # If not, create a new CREATE_GKE_CLUSTER release
#     # TODO: Ensure there is max 1 active release
#     ws_releases: WsReleases = cast(WsReleases, config.get_ws_releases_by_name(ws_name))
#     create_gke_cluster_release: Optional[schemas.ReleaseSchema] = None
#     if ws_releases is not None:
#         existing_create_gke_cluster_releases = ws_releases.get_releases_by_type(
#             enums.ReleaseType.CREATE_GKE_CLUSTER
#         )
#         if existing_create_gke_cluster_releases:
#             logger.debug(
#                 "Found {} active {} releases".format(
#                     len(existing_create_gke_cluster_releases),
#                     enums.ReleaseType.CREATE_GKE_CLUSTER.value,
#                 )
#             )
#             for rls in existing_create_gke_cluster_releases:
#                 # logger.debug(f"id_release: {rls.id_release}")
#                 if (
#                     rls.release_data
#                     and rls.release_data.ws_gcp_project__gcp_project_id
#                     == gcp_project_id
#                 ):
#                     logger.debug(f"Using active release: {rls.id_release}")
#                     create_gke_cluster_release = rls
#                     break
#
#     # Create a CREATE_GKE_CLUSTER release if needed
#     _ws_release_data: Optional[schemas.ReleaseData] = None
#     if create_gke_cluster_release is None:
#         logger.debug("Creating new CREATE_GKE_CLUSTER ReleaseSchema")
#         _ws_release_data = schemas.ReleaseData(
#             ws__id_workspace=ws_schema.id_workspace,
#             ws_gcp_project__id_project=ws_gcp_project.id_project,
#             # This is the same as ws_gcp_project.gcp_project_id
#             ws_gcp_project__gcp_project_id=gcp_project_id,
#             ws_gke_cluster__id_cluster=None,
#             ws_gke_cluster__cluster_name=None,
#         )
#         create_gke_cluster_release = schemas.ReleaseSchema(
#             id_release="{}_{}_{}_{}".format(
#                 enums.ReleaseType.CREATE_GKE_CLUSTER.value,
#                 gcp_project_id,
#                 ws_schema.id_workspace,
#                 int(time.time()) % 1000,  # Get the last 3 digits
#             ),
#             id_workspace=ws_schema.id_workspace,
#             id_user=user.id_user,
#             is_valid=True,
#             is_at_desired_state=False,
#             release_type=enums.ReleaseType.CREATE_GKE_CLUSTER.value,
#             release_data=_ws_release_data,
#             start_ts=current_datetime_utc(),
#             end_ts=None,
#             at_desired_state_ts=None,
#             last_update_ts=None,
#         )
#         # Final check that we have a working ReleaseSchema
#         if create_gke_cluster_release is None:
#             error_msg = f"Could not create a release for project: {gcp_project_id}, please try again"
#             logger.error(error_msg)
#             return None
#         # Add release to config
#         ws_releases.add_release(create_gke_cluster_release)
#     else:
#         _ws_release_data = create_gke_cluster_release.release_data
#     # Casting _ws_release_data to schemas.ReleaseData for the typechecker
#     # Documentation: https://docs.python.org/3/library/typing.html#typing.cast
#     _ws_release_data = cast(schemas.ReleaseData, _ws_release_data)
#
#     # Now that a CREATE_GKE_CLUSTER is available, mark all existing DELETE_GKE_CLUSTER
#     # releases as complete.
#     ws_releases.set_active_releases_as_complete(enums.ReleaseType.DELETE_GKE_CLUSTER)
#
#     # Step 5: Create a GKEClusterSchema if needed
#     try:
#         ws_gke_cluster = get_or_create_gke_cluster_for_pak8(
#             user=user,
#             release_data=_ws_release_data,
#             ws_schema=ws_schema,
#             ws_gcp_project=ws_gcp_project,
#             ws_gcp_pak8=ws_gcp_pak8,
#             ws_gke_cluster=ws_gke_cluster,
#         )
#     except pak8_exceptions.GCPAuthException as e:
#         pprint_error("Received exception: {}".format(e))
#         pprint_info(
#             "Please run `phi gcp auth` and recreate the service account key again"
#         )
#     # Final check that we have a working GKEClusterSchema
#     if ws_gke_cluster is None:
#         return None
#     # Add the GKE_CLUSTER to the config and save the progress
#     config.update_ws_gcp_data(ws_name=ws_name, gke_cluster=ws_gke_cluster)
#     config.save_config()
#
#     # Step 6: Update the release data to reflect the current state
#     _ws_release_data.ws_gke_cluster__id_cluster = ws_gke_cluster.id_cluster
#     _ws_release_data.ws_gke_cluster__cluster_name = ws_gke_cluster.cluster_name
#     create_gke_cluster_release.release_data = _ws_release_data
#
#     # Step 7: Mark the release at desired state if the gke cluster is active on both phidata & gcp
#     # Mark the release as at desired state if the GKEClusterSchema is active and
#     # pak8 status implies that the GKEClusterSchema is available
#     pak8_status = ws_gcp_pak8.get_pak8_status()
#     logger.debug("Pak8 is {}".format(pak8_status))
#     if ws_gke_cluster.is_valid and pak8_status.k8s_cluster_is_available():
#         # Save the kubeconfig for this cluster
#         kconf_resource: Optional[Kubeconfig] = ws_gcp_pak8.get_kubeconfig()
#         if kconf_resource:
#             ws_k8s_data: Optional[PhiK8sData] = config.update_ws_k8s_data(
#                 ws_name=ws_name, kubeconfig_resource=kconf_resource
#             )
#             if ws_k8s_data:
#                 pprint_status(f"Kubeconfig saved to: {ws_k8s_data.kubeconfig_path}")
#         create_gke_cluster_release.set_at_desired_state()
#
#     config.save_config()
#     return ws_gke_cluster
#
#
# def delete_gke_cluster_if_exists(
#     ws_schema: schemas.WorkspaceSchema, config: PhiConf
# ) -> bool:
#     """Deletes the GKEClusterSchema for a workspace if available. Returns true if successfully
#     deleted.
#     """
#
#     ws_name: str = ws_schema.name
#     logger.debug(f"Deleting GKEClusterSchema for ws: {ws_name}")
#
#     # Step 1: Get the Pak8Conf for the workspace
#     # Refresh the Pak8Conf to read new changes
#     pprint_status("Reading the latest workspace configuration")
#     ws_pak8_conf: Optional[Pak8Conf] = config.get_ws_pak8_conf_by_name(
#         ws_name, refresh=True
#     )
#     if ws_pak8_conf is None:
#         pprint_error("WorkspaceSchema Config invalid")
#         pprint_status("Please fix your workspace config and try again")
#         return False
#     if ws_pak8_conf.gcp is None:
#         pprint_error("This workspace does not have a GCP project configured")
#         return False
#     if ws_pak8_conf.gcp.gke_cluster_config is None:
#         pprint_error(
#             "Invalid GKE Config, please fix the gcp.gke section of your config"
#         )
#         return False
#
#     # Step 2: Get the PhiGcpData, GCPProjectSchema and check if a GKEClusterSchema is available.
#     ws_gcp_data: Optional[PhiGcpData] = config.get_ws_gcp_data_by_name(ws_name)
#     if ws_gcp_data is None or ws_gcp_data.gcp_project is None:
#         pprint_error(
#             "No GCP Project available, please run `phi gcp auth` to setup a GCP Project for this workspace"
#         )
#         return False
#     # Get the GCPProjectSchema for this workspace
#     logger.debug("Getting GCPProjectSchema for this workspace")
#     gcp_project_id: str = ws_gcp_data.gcp_project_id
#     ws_gcp_project: schemas.GCPProjectSchema = ws_gcp_data.gcp_project
#     # Check if a GKEClusterSchema is already available
#     logger.debug("Checking if a GKEClusterSchema is already available")
#     ws_gke_cluster: Optional[schemas.GKEClusterSchema] = ws_gcp_data.gke_cluster
#     if ws_gke_cluster is None:
#         pprint_info("No GKEClusterSchema available to delete")
#         return True
#
#     ## DELETE THE GKE_CLUSTER
#     pprint_info(
#         f"Deleting GKEClusterSchema: {ws_pak8_conf.gcp.gke_cluster_config.name}"
#     )
#
#     # Step 3: Get the GCPPak8 for this workspace
#     ws_gcp_pak8: Optional[GCPPak8] = None
#     try:
#         ws_gcp_pak8 = GCPPak8(ws_pak8_conf)
#         logger.debug("GCPPak8 Created")
#     except pydantic.ValidationError as e:
#         error_msg = "Config Validation Error. Details:\n{}".format(e)
#         logger.error(error_msg)
#         return False
#     # If a GCP Pak8 cannot be created then return False
#     if ws_gcp_pak8 is None or not isinstance(ws_gcp_pak8, GCPPak8):
#         logger.error("Invalid GCPPak8: {}".format(ws_gcp_pak8))
#         return False
#     # We need the user details to delete the cluster
#     user: schemas.UserSchema = config.user
#
#     # Step 4: Check if there is an existing DELETE_GKE_CLUSTER releases available
#     # TODO: Ensure there is max 1 active release
#     ws_releases: WsReleases = cast(WsReleases, config.get_ws_releases_by_name(ws_name))
#     delete_gke_cluster_release: Optional[schemas.ReleaseSchema] = None
#     if ws_releases is not None:
#         existing_delete_gke_cluster_releases = ws_releases.get_releases_by_type(
#             enums.ReleaseType.DELETE_GKE_CLUSTER
#         )
#         if existing_delete_gke_cluster_releases:
#             logger.debug(
#                 "Found {} active {} releases".format(
#                     len(existing_delete_gke_cluster_releases),
#                     enums.ReleaseType.DELETE_GKE_CLUSTER.value,
#                 )
#             )
#             for rls in existing_delete_gke_cluster_releases:
#                 # logger.debug(f"id_release: {rls.id_release}")
#                 if (
#                     rls.release_data
#                     and rls.release_data.ws_gcp_project__gcp_project_id
#                     == gcp_project_id
#                 ):
#                     logger.debug(f"Using active release: {rls.id_release}")
#                     delete_gke_cluster_release = rls
#                     break
#
#     # Create a DELETE_GKE_CLUSTER release if needed
#     _ws_release_data: Optional[schemas.ReleaseData] = None
#     if delete_gke_cluster_release is None:
#         logger.debug("Creating new DELETE_GKE_CLUSTER ReleaseSchema")
#         _ws_release_data = schemas.ReleaseData(
#             ws__id_workspace=ws_schema.id_workspace,
#             ws_gcp_project__id_project=ws_gcp_project.id_project,
#             # This is the same as ws_gcp_project.gcp_project_id
#             ws_gcp_project__gcp_project_id=gcp_project_id,
#             ws_gke_cluster__id_cluster=None,
#             ws_gke_cluster__cluster_name=None,
#         )
#         delete_gke_cluster_release = schemas.ReleaseSchema(
#             id_release="{}_{}_{}_{}".format(
#                 enums.ReleaseType.DELETE_GKE_CLUSTER.value,
#                 gcp_project_id,
#                 ws_schema.id_workspace,
#                 int(time.time()) % 1000,  # Get the last 3 digits
#             ),
#             id_workspace=ws_schema.id_workspace,
#             id_user=user.id_user,
#             is_valid=True,
#             is_at_desired_state=False,
#             release_type=enums.ReleaseType.DELETE_GKE_CLUSTER.value,
#             release_data=_ws_release_data,
#             start_ts=current_datetime_utc(),
#             end_ts=None,
#             at_desired_state_ts=None,
#             last_update_ts=None,
#         )
#         # Final check that we have a working ReleaseSchema
#         if delete_gke_cluster_release is None:
#             error_msg = f"Could not create a release for project: {gcp_project_id}, please try again"
#             logger.error(error_msg)
#             return False
#         # Add release to config
#         ws_releases.add_release(delete_gke_cluster_release)
#     else:
#         _ws_release_data = delete_gke_cluster_release.release_data
#     # Casting _ws_release_data to schemas.ReleaseData for the typechecker
#     # Documentation: https://docs.python.org/3/library/typing.html#typing.cast
#     _ws_release_data = cast(schemas.ReleaseData, _ws_release_data)
#
#     # Step 5: Delete the GKEClusterSchema if needed
#     ws_gke_cluster = delete_gke_cluster_for_pak8(
#         release_data=_ws_release_data,
#         ws_gcp_pak8=ws_gcp_pak8,
#         ws_gke_cluster=ws_gke_cluster,
#     )
#     # Add the GKE_CLUSTER to the config and save the progress
#     config.update_ws_gcp_data(ws_name=ws_name, gke_cluster=ws_gke_cluster)
#     config.save_config()
#
#     # Step 6: Update the release data
#     delete_gke_cluster_release.release_data = _ws_release_data
#
#     # Step 7: Mark the release at desired state if the gke cluster is deleted on both phidata & gcp
#     # Mark the release as at desired state if the GKEClusterSchema is deleted and
#     # pak8 status implies that the GKEClusterSchema is deleted
#     pak8_status = ws_gcp_pak8.get_pak8_status()
#     logger.debug("Pak8 is {}".format(pak8_status))
#     if not ws_gke_cluster.is_valid and pak8_status.k8s_cluster_is_deleted():
#         delete_gke_cluster_release.set_at_desired_state()
#
#     # Step 8: Mark existing CREATE_GKE_CLUSTER releases as complete
#     # Getting here implies that a GKEClusterSchema is deleted so we should mark any existing
#     # CREATE_GKE_CLUSTER releases as complete
#     ws_releases.set_active_releases_as_complete(enums.ReleaseType.CREATE_GKE_CLUSTER)
#     config.save_config()
#     return True
