# from typing import Optional
#
# from google.cloud import container_v1
# from google.protobuf.json_format import MessageToDict
#
# import pak8.enums as pak8_enums
# import pak8.exceptions as pak8_exceptions
# from pak8.gcp.clients.pak8_gke_client import Pak8GKEClient
# from pak8.gcp.conf import Pak8GCPConf
# from pak8.gcp.gcp_pak8 import GCPPak8
# from phiterm.gcp.gcp_schemas import CreateGKECluster, GCPProjectSchema, GKEClusterSchema
# from phiterm.release.release_schemas import ReleaseSchema
# from phiterm.schemas.user_schemas import UserSchema
# from phiterm.utils.common import pprint_status
# from phiterm.utils.dttm import current_datetime_utc
# from phiterm.utils.log import logger
# from phiterm.workspace.ws_schemas import WorkspaceSchema
#
#
# def update_gke_cluster_to_match_gke_cluster_response(
#     gke_cluster: GKEClusterSchema,
#     gke_cluster_response: container_v1.types.Cluster,
# ) -> GKEClusterSchema:
#     logger.debug(
#         f"Updating GKEClusterSchema to match GKEClusterResponse: {gke_cluster.cluster_name}"
#     )
#
#     if gke_cluster_response is None:
#         return gke_cluster
#
#     status_str = container_v1.types.Cluster.Status.Name(gke_cluster_response.status)
#     status: pak8_enums.GKEClusterStatus = pak8_enums.GKEClusterStatus.from_str(
#         status_str
#     )
#     if gke_cluster is not None:
#         gke_cluster.current_cluster_config = MessageToDict((gke_cluster_response))
#         gke_cluster.current_cluster_status = status
#         gke_cluster.is_active = status == pak8_enums.GKEClusterStatus.RUNNING
#         gke_cluster.last_update_ts = current_datetime_utc()
#         gke_cluster.deactivate_ts = (
#             current_datetime_utc()
#             if status == pak8_enums.GKEClusterStatus.STOPPING
#             else None
#         )
#
#     return gke_cluster
#
#
# def create_gke_cluster_using_gke_cluster_response(
#     gke_cluster_response: container_v1.types.Cluster,
#     create_gke_cluster: CreateGKECluster,
# ) -> Optional[GKEClusterSchema]:
#
#     logger.debug(f"Creating GKEClusterSchema using GKEClusterResponse")
#     if gke_cluster_response is None:
#         return None
#
#     _cluster_name = gke_cluster_response.name
#     if _cluster_name is None or (_cluster_name != create_gke_cluster.cluster_name):
#         logger.error(
#             "cluster name from pak8 {} does not match cluster name from gcp {}".format(
#                 create_gke_cluster.cluster_name, _cluster_name
#             )
#         )
#         return None
#
#     status_str = container_v1.types.Cluster.Status.Name(gke_cluster_response.status)
#     status: pak8_enums.GKEClusterStatus = pak8_enums.GKEClusterStatus.from_str(
#         status_str
#     )
#     logger.debug(f"status: {status}")
#     _gke_cluster: GKEClusterSchema = GKEClusterSchema(
#         id_cluster=create_gke_cluster.id_cluster,
#         id_project=create_gke_cluster.id_project,
#         id_workspace=create_gke_cluster.id_workspace,
#         created_by_id_user=create_gke_cluster.created_by_id_user,
#         created_by_email=create_gke_cluster.created_by_email,
#         create_ts=create_gke_cluster.create_ts,
#         gcp_zone=create_gke_cluster.gcp_zone,
#         gcp_project_id=create_gke_cluster.gcp_project_id,
#         cluster_name=create_gke_cluster.cluster_name,
#         current_cluster_status=status,
#         current_cluster_config=MessageToDict(gke_cluster_response),
#         # We don't use the is_valid from CreateGKECluster
#         is_active=(status == pak8_enums.GKEClusterStatus.RUNNING),
#         is_verified=create_gke_cluster.is_verified,
#         is_test=create_gke_cluster.is_test,
#         last_update_ts=None,
#         deactivate_ts=current_datetime_utc()
#         if status == pak8_enums.GKEClusterStatus.STOPPING
#         else None,
#     )
#     logger.debug("New GKEClusterSchema Created")
#
#     return _gke_cluster
#
#
# def get_or_create_gke_cluster_for_pak8(
#     user: UserSchema,
#     release_data: ReleaseSchema,
#     ws_schema: WorkspaceSchema,
#     ws_gcp_project: GCPProjectSchema,
#     ws_gcp_pak8: GCPPak8,
#     ws_gke_cluster: Optional[GKEClusterSchema] = None,
# ) -> Optional[GKEClusterSchema]:
#
#     pprint_status("Creating a GKE cluster if needed, this could take a while...")
#     # The GKEClusterSchema that will be returned
#     gke_cluster: Optional[GKEClusterSchema] = None
#
#     # Determine the current status of this Pak8
#     pak8_status: pak8_enums.Pak8Status = ws_gcp_pak8.get_pak8_status()
#     pak8_gcp_conf: Optional[Pak8GCPConf] = ws_gcp_pak8.pak8_conf.gcp
#
#     # If the Pak8 status > READY_TO_CREATE_K8S_CLUSTER
#     # Use the Pak8GKEClient to get the GKEClusterSchema from GCP, create one if needed
#     logger.debug("Pak8 is {}".format(pak8_status))
#     if pak8_status.can_create_k8s_cluster():
#         # Get the GKE Client
#         pak8_gke_client: Pak8GKEClient = ws_gcp_pak8.pak8_gke_client
#
#         # Get the GKEClusterSchema from GCP, create one if needed
#         # Type for Cluster defined here:
#         # https://google-cloud-python.readthedocs.io/en/0.32.0/container/gapic/v1/types.html#google.cloud.container_v1.types.Cluster
#         gke_cluster_from_gcp: Optional[container_v1.types.Cluster] = None
#         create_gke_cluster_op_from_gcp: Optional[container_v1.types.Operation] = None
#         try:
#             (
#                 gke_cluster_from_gcp,
#                 create_gke_cluster_op_from_gcp,
#             ) = pak8_gke_client.get_or_create_gke_cluster()
#         except (
#             pak8_exceptions.GKEClusterCreateException,
#             # pak8_exceptions.GKEClusterNotFoundException,
#             # pak8_exceptions.Pak8GCPConfInvalidException,
#         ) as e:
#             # If there is an error pass the error back to the client
#             logger.debug("Encountered Error: {}".format(e))
#             logger.exception(e)
#             return None
#
#         # if gke_cluster_from_gcp:
#         # logger.debug("Received GKEClusterSchema from GCP")
#         # logger.debug(
#         #     "Received GKEClusterSchema from GCP:\n{}".format(str(gke_cluster_from_gcp))
#         # )
#
#         # Create GKEClusterSchema model if one doesn't exist
#         existing_ws_gke_cluster = ws_gke_cluster
#         if existing_ws_gke_cluster is None and pak8_gcp_conf is not None:
#             logger.debug("Creating GKEClusterSchema schema")
#             id_cluster = "{}_{}".format(
#                 ws_gcp_project.id_project, pak8_gcp_conf.gke.name
#             )
#             if gke_cluster_from_gcp is not None and pak8_gcp_conf is not None:
#                 logger.debug(
#                     "Using container_v1.types.Cluster response to create GKEClusterSchema"
#                 )
#                 pak8_status = ws_gcp_pak8.get_pak8_status()
#                 logger.debug("Pak8 is {}".format(pak8_status))
#                 gke_cluster = create_gke_cluster_using_gke_cluster_response(
#                     gke_cluster_response=gke_cluster_from_gcp,
#                     create_gke_cluster=CreateGKECluster(
#                         is_verified=False,
#                         is_test=False,
#                         id_cluster=id_cluster,
#                         id_project=ws_gcp_project.id_project,
#                         id_workspace=ws_schema.id_workspace,
#                         created_by_id_user=user.id_user,
#                         created_by_email=user.email,
#                         create_ts=current_datetime_utc(),
#                         gcp_zone=ws_gcp_project.gcp_zone,
#                         gcp_project_id=ws_gcp_project.gcp_project_id,
#                         cluster_name=pak8_gcp_conf.gke.name,
#                     ),
#                 )
#             else:
#                 logger.debug(
#                     "No container_v1.types.Cluster response available, creating GKEClusterSchema"
#                 )
#                 gke_cluster = GKEClusterSchema(
#                     id_cluster=id_cluster,
#                     id_project=ws_gcp_project.id_project,
#                     id_workspace=ws_schema.id_workspace,
#                     created_by_id_user=user.id_user,
#                     created_by_email=user.email,
#                     create_ts=current_datetime_utc(),
#                     gcp_zone=ws_gcp_project.gcp_zone,
#                     gcp_project_id=ws_gcp_project.gcp_project_id,
#                     cluster_name=pak8_gcp_conf.gke.name,
#                     current_cluster_status=pak8_enums.GKEClusterStatus.STATUS_UNSPECIFIED,
#                     current_cluster_config=None,
#                     # We don't use the is_valid from CreateGKECluster
#                     is_active=True,
#                     is_verified=False,
#                     is_test=False,
#                 )
#         # Update the GKEClusterSchema model with any new info
#         else:
#             if existing_ws_gke_cluster is not None and gke_cluster_from_gcp is not None:
#                 gke_cluster = update_gke_cluster_to_match_gke_cluster_response(
#                     existing_ws_gke_cluster, gke_cluster_from_gcp
#                 )
#
#         # if create_gke_cluster_op_from_gcp is not None:
#         #     if release_data is not None:
#         #         release_data.create_gke_cluster__id_operation = (
#         #             create_gke_cluster_op_from_gcp.name
#         #         )
#
#     return gke_cluster
#
#
# def deactivate_gke_cluster(
#     gke_cluster: GKEClusterSchema,
#     gke_cluster_response: Optional[container_v1.types.Cluster],
# ) -> GKEClusterSchema:
#
#     logger.debug(f"Deactivating GKEClusterSchema {gke_cluster.cluster_name}")
#     if gke_cluster_response is None:
#         return gke_cluster
#
#     status_str = container_v1.types.Cluster.Status.Name(gke_cluster_response.status)
#     status: pak8_enums.GKEClusterStatus = pak8_enums.GKEClusterStatus.from_str(
#         status_str
#     )
#     if gke_cluster is not None:
#         gke_cluster.current_cluster_config = MessageToDict((gke_cluster_response))
#         gke_cluster.current_cluster_status = status
#         gke_cluster.is_active = False
#         gke_cluster.last_update_ts = current_datetime_utc()
#         gke_cluster.deactivate_ts = current_datetime_utc()
#
#     return gke_cluster
#
#
# def delete_gke_cluster_for_pak8(
#     release_data: ReleaseSchema,
#     ws_gcp_pak8: GCPPak8,
#     ws_gke_cluster: GKEClusterSchema,
# ) -> GKEClusterSchema:
#
#     pprint_status("Deleting GKEClusterSchema: {}".format(ws_gke_cluster.cluster_name))
#     # The GKEClusterSchema that will be returned
#     deleted_gke_cluster: GKEClusterSchema = ws_gke_cluster
#
#     # Determine the current status of this Pak8
#     pak8_status: pak8_enums.Pak8Status = ws_gcp_pak8.get_pak8_status()
#     pak8_gcp_conf: Optional[Pak8GCPConf] = ws_gcp_pak8.pak8_conf.gcp
#
#     # If the Pak8 status > CREATING_K8S_CLUSTER, i.e. the pak8 cluster has been created
#     # then use the Pak8GKEClient to delete the GKEClusterSchema from GCP
#     logger.debug("Pak8 is {}".format(pak8_status))
#     if pak8_status.can_delete_k8s_cluster():
#         # Get the GKE Client
#         pak8_gke_client: Pak8GKEClient = ws_gcp_pak8.pak8_gke_client
#
#         delete_gke_cluster_op_from_gcp: Optional[
#             container_v1.types.Operation
#         ] = pak8_gke_client.delete_if_exists_cluster()
#
#         # Get the GKEClusterSchema from GCP after deletion
#         # Type for Cluster defined here:
#         # https://google-cloud-python.readthedocs.io/en/0.32.0/container/gapic/v1/types.html#google.cloud.container_v1.types.Cluster
#         deleted_gke_cluster_from_gcp: Optional[container_v1.types.Cluster] = None
#         try:
#             # TODO: This isn't working at the moment
#             deleted_gke_cluster_from_gcp = pak8_gke_client.get_gke_cluster_from_gcp()
#         except Exception as e:
#             # If there is an error pass the error back to the client
#             logger.debug("Encoundered Error: {}".format(e))
#             pass
#
#         # if deleted_gke_cluster_from_gcp:
#         #     # logger.debug("Received GKEClusterSchema from GCP")
#         #     logger.debug(
#         #         "Received GKEClusterSchema from GCP after deletion:\n{}".format(
#         #             str(deleted_gke_cluster_from_gcp)
#         #         )
#         #     )
#
#         deleted_gke_cluster = deactivate_gke_cluster(
#             gke_cluster=deleted_gke_cluster,
#             gke_cluster_response=deleted_gke_cluster_from_gcp,
#         )
#
#         # If we've successfully deleted the GKEClusterSchema, we need to create a models.GCPOperation for the deletion
#         # if delete_gke_cluster_op_from_gcp is not None:
#         #     if release_data is not None:
#         #         release_data.delete_gke_cluster__id_operation = (
#         #             delete_gke_cluster_op_from_gcp.name
#         #         )
#
#     return deleted_gke_cluster
