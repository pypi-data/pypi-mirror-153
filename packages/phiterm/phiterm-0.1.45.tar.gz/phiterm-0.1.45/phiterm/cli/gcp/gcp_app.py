# """Phi GCP Cli
#
# This is the entrypoint for the `phi gcp` commands
# """
#
# from typing import Optional
#
# import typer
#
# from phi import schemas
# from phiterm.gcp import gcp_operator
# from phiterm.conf.phi_conf import PhiConf
# from phiterm.utils.common import conf_not_available_msg, primary_ws_not_available_msg
#
# _phi_gcp_help_text = """
# \b
# Commands to manage the GCP Project for your primary workspaces.
#
# \b
# Main Commands:
# $ phi gcp auth   -> Authenticates the GCP Project used by your primary ws
# $ phi gcp status -> Prints the GCP Project status for the primary ws
# """
# app = typer.Typer(name="gcp", help=_phi_gcp_help_text)
#
#
# @app.command(short_help="Authenticate the GCP Project used by your primary ws")
# def auth():
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
#     gcp_operator.authenticate_gcp_project_for_ws(primary_ws, config)
#
#
# if __name__ == "__main__":
#     app()
