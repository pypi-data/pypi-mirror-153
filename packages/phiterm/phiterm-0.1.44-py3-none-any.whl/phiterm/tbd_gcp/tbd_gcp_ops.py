# from typing import Optional
#
# from pak8.conf import Pak8Conf
# from phi import schemas
# from phiterm.cli.gcp.gke import gke_operator
# from phiterm.conf.phi_conf import PhiConf
# from phiterm.utils.common import pprint_info, pprint_error, pprint_heading
#
#
# def deploy_workspace_to_gcp(
#     ws_schema: schemas.WorkspaceSchema, config: PhiConf, refresh_pak8_conf: bool = False
# ) -> None:
#
#     pprint_heading(f"Deploying {ws_schema.name} to gcp")
#
#     # Step 1: Get the Pak8Conf for this workspace
#     ws_name: str = ws_schema.name
#     ws_pak8_conf: Optional[Pak8Conf] = config.get_ws_pak8_conf_by_name(
#         ws_name, refresh=refresh_pak8_conf
#     )
#     if ws_pak8_conf is None:
#         pprint_error(f"Unable to get config for {ws_name}")
#         return None
#
#     # Step 2: Check pending actions
#     # ws_pending_actions: Optional[
#     #     Set[enums.WorkspaceSetupActions]
#     # ] = config.get_ws_pending_actions_by_name(ws_name)
#     # if enums.WorkspaceSetupActions.GCP_SVC_ACCOUNT_IS_AVL in ws_pending_actions:
#     #     pprint_error(
#     #         "A GCP Service Account is not available for this workspace, run `phi gcp auth`"
#     #     )
#     #     return None
#
#     # Step 3: Get the GCPProjectSchema for this workspace
#     gcp_project: Optional[
#         schemas.GCPProjectSchema
#     ] = config.get_gcp_project_schema_by_ws_name(ws_name)
#     if gcp_project is None:
#         pprint_error("No GCP Project for this workspace, please run `phi gcp auth`")
#         return None
#
#     # Step 4: Get or create the GKEClusterSchema for this workspace
#     gke_cluster: Optional[
#         schemas.GKEClusterSchema
#     ] = gke_operator.get_or_create_gke_cluster(ws_schema, config, refresh_pak8_conf)
#     if gke_cluster:
#         gcloud_cmd = (
#             f"gcloud container clusters get-credentials {gke_cluster.cluster_name}"
#         )
#         pprint_info(f"To authenticate with gcloud, please run:\n\n\t{gcloud_cmd}\n")
#
#     # id_ws = ws_schema.id_workspace
#     # id_prj = gcp_project.id_project
#     # gke_cluster: Optional[schemas.GKEClusterSchema] = None
#     # if id_ws and id_prj:
#     #     pprint_status("Creating a GKE cluster if needed, this could take a while...")
#     #
#     #     # gke_cluster_release: Optional[
#     #     #     schemas.GKEClusterRelease
#     #     # ] = zeus_api.get_or_create_gke_cluster_for_gcp_project(
#     #     #     id_workspace=id_ws, id_project=id_prj, pak8_conf=ws_pak8_conf
#     #     # )
#     #     # if gke_cluster_release is not None:
#     #     #     # Note, since we're not providing the gcp_project_id arg, this would fail if
#     #     #     # ws_gcp_data is not setup.
#     #     #     gke_cluster = gke_cluster_release.gke_cluster
#     #     #     gke_create_cluster_release = gke_cluster_release.release
#     #     #     if gke_cluster is not None:
#     #     #         config.update_ws_gcp_data(ws_name=ws_name, gke_cluster=gke_cluster)
#     #     #     if gke_create_cluster_release is not None:
#     #     #         config.add_release_for_ws(
#     #     #             ws_name=ws_name, release=gke_create_cluster_release
#     #     #         )
#
#     # Step 5: Deploy all Pak8 Services
#
#     # Step 6: Validate
