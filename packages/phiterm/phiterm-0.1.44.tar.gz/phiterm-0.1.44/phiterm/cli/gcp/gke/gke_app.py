# """Phi GKE Cli
#
# This is the entrypoint for the `phi gke` commands
# """
#
# from typing import Optional
#
# import typer
#
# from phi import schemas
# from phiterm.gcp.gke import gke_operator
# from phiterm.conf.phi_conf import PhiConf
# from phiterm.utils.common import (
#     conf_not_available_msg,
#     pprint_info,
#     pprint_heading,
#     pprint_info,
#     pprint_status,
#     primary_ws_not_available_msg,
# )
#
# _phi_gke_help_text = """
# \b
# Commands to manage GKE Clusters for your primary workspaces.
#
# \b
# Main Commands:
# $ phi gke create-cluster   -> Creates the GKE Cluster used by your primary ws
# $ phi gke delete-cluster   -> Deletes the GKE Cluster used by your primary ws
# $ phi gke status           -> Prints the GKE Cluster for your primary ws
# """
# app = typer.Typer(name="gke", help=_phi_gke_help_text)
#
#
# @app.command(short_help="Creates the GKE Cluster used by your primary ws")
# def create_cluster(
#     refresh: bool = typer.Option(
#         False,
#         "-r",
#         "--refresh",
#         help="Skips cache and refreshes the cluster",
#         show_default=True,
#     ),
# ):
#
#     config: Optional[PhiConf] = PhiConf.get_saved_conf()
#     if not config:
#         conf_not_available_msg()
#         raise typer.Exit(1)
#
#     primary_ws: Optional[schemas.WorkspaceSchema] = config.primary_ws
#     if primary_ws is None:
#         primary_ws_not_available_msg()
#         raise typer.Exit(1)
#
#     gke_cluster: Optional[
#         schemas.GKEClusterSchema
#     ] = gke_operator.get_or_create_gke_cluster(primary_ws, config, refresh)
#     if gke_cluster:
#         gcloud_cmd = (
#             f"gcloud container clusters get-credentials {gke_cluster.cluster_name}"
#         )
#         pprint_info(f"To authenticate with gcloud, please run:\n\n\t{gcloud_cmd}\n")
#
#
# @app.command(short_help="Deletes the GKE Cluster for the primary workspace")
# def delete_cluster():
#
#     from phiterm.conf.phi_conf import PhiConf
#
#     config: Optional[PhiConf] = PhiConf.get_saved_conf()
#     if not config:
#         conf_not_available_msg()
#         raise typer.Exit(1)
#
#     primary_ws: Optional[schemas.WorkspaceSchema] = config.primary_ws
#     if primary_ws is None:
#         primary_ws_not_available_msg()
#         raise typer.Exit(1)
#
#     gke_cluster_deleted: bool = gke_operator.delete_gke_cluster_if_exists(
#         primary_ws, config
#     )
#     if gke_cluster_deleted:
#         pprint_info("GKE Cluster deleted")
#
#
# @app.command(short_help="Print the GKE status for the primary workspace")
# def status():
#
#     from phiterm.conf.phi_conf import PhiConf
#
#     config: Optional[PhiConf] = PhiConf.get_saved_conf()
#     if not config:
#         conf_not_available_msg()
#         raise typer.Exit(1)
#
#     primary_ws: Optional[schemas.WorkspaceSchema] = config.primary_ws
#     if primary_ws is None:
#         primary_ws_not_available_msg()
#         raise typer.Exit(1)
#
#     pprint_heading("GKE Cluster Status")
#     pprint_status("WorkspaceSchema: {}".format(primary_ws.name))
#     gke_operator.print_gke_cluster_status(primary_ws, config)
#
#
# if __name__ == "__main__":
#     app()
