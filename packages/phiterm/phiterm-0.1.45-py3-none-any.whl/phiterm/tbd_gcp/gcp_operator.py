# import json
# from pathlib import Path
# from typing import Any, Dict, Optional
#
# import typer
#
# from pak8.conf import Pak8Conf
# from phi import schemas
# from phiterm.conf.phi_conf import PhiConf, PhiGcpData, PhiWsData
# from phiterm.utils.common import (
#     pprint_info,
#     pprint_error,
#     pprint_heading,
#     pprint_info,
#     pprint_status,
#     pprint_subheading,
#     str_to_int,
# )
# from phiterm.utils.filesystem import delete_from_fs
# from phiterm.utils.log import logger
# from phiterm.zeus_api.gcp import (
#     get_gke_cluster_for_gcp_project,
#     get_primary_gcp_project,
#     upsert_gcp_project,
# )
#
#
# def get_default_sa_key_path_(ws_root_path: Path) -> Path:
#     return ws_root_path.joinpath("phi").joinpath("keys").joinpath("phidata-sa-pk.json")
#
#
# def _upsert_primary_gcp_project_for_ws(
#     ws_name: str, config: PhiConf
# ) -> Optional[schemas.GCPProjectSchema]:
#     """For a given ws, reads the current GCP data and makes a call to zeus to create or update
#     the schemas.GCPProjectSchema for this workspace. We also set this project as primary project for this workspace.
#
#     Note: We use ws_name to get existing ws_gcp_data because prior to calling this function
#     the authenticate_gcp_project_for_ws() function would update the ws_gcp_data with the
#     service_account and key.
#     """
#     ws_schema: Optional[schemas.WorkspaceSchema] = config.get_ws_schema_by_name(ws_name)
#     ws_gcp_data: Optional[PhiGcpData] = config.get_ws_gcp_data_by_name(ws_name)
#     ws_pak8_conf: Optional[Pak8Conf] = config.get_ws_pak8_conf_by_name(ws_name)
#     if ws_gcp_data is None or ws_schema is None:
#         pprint_error(
#             "Could not authenticate GCP Project, please run `phi gcp auth` again"
#         )
#         return None
#
#     gcp_project: Optional[schemas.GCPProjectSchema] = ws_gcp_data.gcp_project
#     gcp_project_id = ws_gcp_data.gcp_project_id
#     logger.debug(f"Upserting GCPProjectSchema for {ws_name}: {gcp_project_id}")
#     gcp_project_schema_from_api: Optional[
#         schemas.GCPProjectSchema
#     ] = upsert_gcp_project(
#         schemas.UpsertGCPProjectFromCli(
#             name=gcp_project_id,
#             id_project=f"{ws_schema.id_workspace}_{gcp_project_id}",
#             id_workspace=ws_schema.id_workspace,
#             gcp_project_id=gcp_project_id,
#             gcp_service_account_key=ws_gcp_data.gcp_svc_account_key,
#             gcp_service_account=ws_gcp_data.gcp_svc_account,
#             gcp_zone=ws_pak8_conf.gcp.zone
#             if ws_pak8_conf and ws_pak8_conf.gcp
#             else None,
#             vpc_network=ws_pak8_conf.gcp.vpc_network
#             if ws_pak8_conf and ws_pak8_conf.gcp
#             else None,
#             set_as_primary_project_for_ws=True,
#         )
#     )
#     if gcp_project_schema_from_api:
#         config.update_ws_gcp_data(
#             ws_name=ws_schema.name, gcp_project=gcp_project_schema_from_api
#         )
#         gcp_project = ws_gcp_data.gcp_project
#         return gcp_project
#     # This codeblock would be used for bypassing zeus in creating a gcp project
#     # else:
#     #     gcp_project_schema: schemas.GCPProjectSchema = schemas.GCPProjectSchema(
#     #         name=gcp_project_id,
#     #         is_valid=True,
#     #         is_verified=False,
#     #         is_test=False,
#     #         gcp_project_id=gcp_project_id,
#     #         id_project=f"{ws_schema.id_workspace}_{gcp_project_id}",
#     #         id_workspace=ws_schema.id_workspace,
#     #         created_by_id_user=user.id_user,
#     #         created_by_email=user.email,
#     #         create_ts=current_datetime_utc(),
#     #         gcp_zone=ws_pak8_conf.gcp.zone if ws_pak8_conf and ws_pak8_conf.gcp else None,
#     #         gcp_service_account_key_available=True if ws_gcp_data.gcp_svc_account_key is not None else False,
#     #         vpc_network=ws_pak8_conf.gcp.vpc_network if ws_pak8_conf and ws_pak8_conf.gcp else None,
#     #         last_update_ts=None,
#     #         project_status=enums.GCPProjectStatus.NEW,
#     #     )
#
#     return gcp_project
#
#
# def create_service_account_key_application_default_creds(
#     ws_name: str,
#     config: PhiConf,
#     phi_sa_name: str,
#     phi_sa_displayname: str,
#     sa_key_path: Path,
# ) -> Optional[Dict[str, Any]]:
#     """Creates a GCP Service Account and returns the Service Account JSON Key using the
#     Google API Client Library: https://github.com/googleapis/google-zeus_api-python-client
#
#     Google has 2 types of client libraries: https://cloud.google.com/apis/docs/client-libraries-explained
#     1. Cloud Client Libraries (preferred)
#     2. Api Client Libraries (in maintenance mode now)
#     Ideally, we would use the IAM Cloud Client Library: https://github.com/googleapis/python-iam
#     But that doesn't have the ability to create service accounts yet, issue: https://github.com/googleapis/python-iam/issues/10
#     So we use Api Client Library with IAM V1 Service: http://googleapis.github.io/google-zeus_api-python-client/docs/dyn/iam_v1.html
#
#     Reference:
#     * https://cloud.google.com/iam/docs/creating-managing-service-accounts#iam-service-accounts-create-python
#     * https://cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts.keys
#     """
#
#     ######################################################
#     # To perform any kind of GCP actions, we need a "Credentials" object of type: google.auth.credentials.Credentials
#     # First we check if the Application Default Credentials are available
#     # https://googleapis.dev/python/google-auth/latest/user-guide.html#application-default-credentials
#     #
#     # For now ADCs are working and hopefully they will continue to work.
#     # If these stop working, we may have to revert to creating credentials
#     # using OAuth 2.0 for Installed Applications with the `google-auth-oauthlib` library
#     # https://github.com/googleapis/google-zeus_api-python-client/blob/master/docs/oauth-installed.md
#     ######################################################
#     import google.auth  # type: ignore
#     import google.oauth2  # type: ignore
#     import googleapiclient.discovery  # type: ignore
#
#     # The Service Account Key which will be used by phidata to manage GCP resources for the user
#     sa_key: Optional[Dict[str, Any]] = None
#
#     ######################################################
#     # Check if GCP Application Default Credentials are avialable
#     ######################################################
#     gcp_default_creds: Optional[google.oauth2.credentials.Credentials] = None
#     gcp_default_project: Optional[str] = None
#     try:
#         # google.auth.default() function docstring lists return type: Tuple[~google.auth.credentials.Credentials, Optional[str]]
#         # But upon inspecting the object, the credentials object returned is google.oauth2.credentials.Credentials
#         # which is a subclass of google.auth.credentials.Credentials
#         gcp_default_creds, gcp_default_project = google.auth.default(
#             scopes=["https://www.googleapis.com/auth/cloud-platform"]
#         )
#         # logger.debug("project: {}".format(gcp_default_project))
#         # logger.debug("credentials: {}".format(gcp_default_creds))
#         # logger.debug("refresh_token: {}".format(gcp_default_creds.refresh_token))
#         # logger.debug("client_id: {}".format(gcp_default_creds.client_id))
#         # logger.debug("valid: {}".format(gcp_default_creds.valid))
#     except google.auth.exceptions.DefaultCredentialsError as e:
#         logger.exception(e)
#
#     if gcp_default_creds is None:
#         pprint_error(
#             "gcloud default credentials unavailable, please authenticate the gcloud sdk and try again."
#         )
#         pprint_info("")
#         pprint_info("\tgcloud auth application-default login")
#         pprint_info("")
#         pprint_info(
#             "If you do not have the gcloud sdk installed, please follow the gcloud docs: https://cloud.google.com/sdk/docs"
#         )
#         return sa_key
#     if gcp_default_project is None:
#         pprint_error("No GCP Project available, please set one using:")
#         pprint_info("")
#         pprint_info("\tgcloud config set project <YOUR_GCP_PROJECT_HERE>")
#         pprint_info("")
#         return sa_key
#
#     # since this could be the first time we're creating a PhiGcpData for this ws
#     # set the gcp_project_id
#     # We have also confirmed that ADCs are available, so we set the flag to True as well
#     config.update_ws_gcp_data(
#         ws_name=ws_name,
#         gcp_project_id=gcp_default_project,
#         gcloud_default_creds_avl=True,
#     )
#     pprint_info("")
#     pprint_status(
#         f"Using gcloud default credentials for project: {gcp_default_project} to create a service account {phi_sa_displayname}"
#     )
#
#     ######################################################
#     # Build iAM Service to use to create the sa and key
#     ######################################################
#     iam_v1_service: Optional[googleapiclient.discovery.Resource] = None
#     try:
#         iam_v1_service = googleapiclient.discovery.build(
#             "iam", "v1", credentials=gcp_default_creds
#         )
#     except Exception as e:
#         logger.debug("could not create iam_v1_service")
#         logger.exception(e)
#     if iam_v1_service is None:
#         pprint_error("Could not connect to the Google IAM Service, please try again")
#         return sa_key
#
#     # Get all Service Accounts to first check if phidata already has a service account
#     _phi_svc_account: Optional[Dict[str, Any]] = None
#     # Follow: https://cloud.google.com/iam/docs/creating-managing-service-accounts#iam-service-accounts-create-python
#     _list_svc_accounts_resp: Optional[Dict[str, Any]] = (
#         iam_v1_service.projects()
#         .serviceAccounts()
#         .list(name=f"projects/{gcp_default_project}")
#         .execute()
#     )
#     if (
#         isinstance(_list_svc_accounts_resp, dict)
#         and "accounts" in _list_svc_accounts_resp
#     ):
#         # logger.debug("_list_svc_accounvts_resp: {}".format(_list_svc_accounts_resp))
#         # logger.debug("_list_svc_accounts_resp type: {}".format(type(_list_svc_accounts_resp)))
#         for _svc_accnt in _list_svc_accounts_resp["accounts"]:
#             if isinstance(_svc_accnt, dict):
#                 if _svc_accnt.get("displayName", None) == phi_sa_displayname:
#                     _phi_svc_account = _svc_accnt
#                     # break
#                 # logger.debug(f"svc accnt type: {type(_svc_accnt)}")
#                 # logger.debug(f"Found Service Account: {_svc_accnt}")
#
#     if _phi_svc_account is not None:
#         pprint_status("Found existing Service Account for phidata")
#         # logger.debug(f"_phi_svc_account type: {type(_phi_svc_account)}")
#         # logger.debug(f"{_phi_svc_account}")
#     else:
#         pprint_status("Creating a new Service Account for phidata")
#         _new_svc_account = (
#             iam_v1_service.projects()
#             .serviceAccounts()
#             .create(
#                 name=f"projects/{gcp_default_project}",
#                 body={
#                     "accountId": phi_sa_name,
#                     "serviceAccount": {"displayName": phi_sa_displayname},
#                 },
#             )
#             .execute()
#         )
#         # logger.debug("Created service account: {}".format(_new_svc_account))
#         # TODO: validate _new_svc_account before using
#         _phi_svc_account = _new_svc_account
#
#     if _phi_svc_account is None:
#         pprint_error(
#             "Could not create a service account for phidata, please run `phi gcp auth` again"
#         )
#         return sa_key
#
#     # Now that a service account is available, update the PhiGcpData for this ws
#     config.update_ws_gcp_data(
#         ws_name=ws_name,
#         gcp_svc_account=_phi_svc_account,
#     )
#
#     ######################################################
#     # Create the Service Account Key if needed
#     ######################################################
#     pprint_status("Creating a Service Account Key for phidata")
#     # Get the service account email
#     _phi_sa_email = _phi_svc_account["email"]
#     # https://cloud.google.com/iam/docs/creating-managing-service-account-keys
#     try:
#         _sa_key_resp = (
#             iam_v1_service.projects()
#             .serviceAccounts()
#             .keys()
#             .create(
#                 name=f"projects/{gcp_default_project}/serviceAccounts/{_phi_sa_email}"
#                 # TODO: Possibly add body={'privateKeyType':'TYPE_GOOGLE_CREDENTIALS_FILE'} here
#             )
#             .execute()
#         )
#     except googleapiclient.errors.HttpError as e:
#         _reason = e._get_reason()
#         pprint_error("Error while creating service account key")
#         pprint_error(_reason)
#         return sa_key
#
#     # logger.debug("_sa_key_resp: {}".format(_sa_key_resp))
#     # logger.debug("_sa_key_resp type: {}".format(type(_sa_key_resp)))
#
#     # Validate the key we just created before using it
#     _sa_key_private_key_type: Optional[str] = _sa_key_resp.get("privateKeyType", None)
#     if (
#         _sa_key_private_key_type is not None
#         and _sa_key_private_key_type != "TYPE_GOOGLE_CREDENTIALS_FILE"
#     ):
#         pprint_error("Error while creating service account key")
#         pprint_error(
#             f"Unexpected `privateKeyType` in Service Account Key, found {_sa_key_private_key_type} expected 'TYPE_GOOGLE_CREDENTIALS_FILE'"
#         )
#         return sa_key
#
#     sa_key = _sa_key_resp
#     if sa_key is None:
#         pprint_error(
#             "Could not create a service account key for phidata, please run `phi gcp auth` again"
#         )
#         return sa_key
#
#     # Set the service account key in the PhiGcpData
#     # Then save it in a file on the users machine
#     config.update_ws_gcp_data(
#         ws_name=ws_name,
#         gcp_svc_account_key=sa_key,
#     )
#     pprint_info(
#         f"Saving Service Account Key to file {str(sa_key_path)}\nPlease ensure that you don't check the key to version control"
#     )
#     if sa_key_path.exists():
#         pprint_info("")
#         pprint_status(f"Deleting existing file at {str(sa_key_path)}")
#         delete_from_fs(sa_key_path)
#
#     try:
#         sa_key_path.parent.mkdir(parents=True, exist_ok=True)
#         sa_key_path.write_text(json.dumps(sa_key))
#     except Exception as e:
#         logger.exception(e)
#         pprint_error(
#             f"Could not write service account key to file: {str(sa_key_path)}\nplease run `phi gcp auth` again"
#         )
#         return None
#
#     try:
#         _list_sa_keys_resp = (
#             iam_v1_service.projects()
#             .serviceAccounts()
#             .keys()
#             .list(
#                 name=f"projects/{gcp_default_project}/serviceAccounts/{_phi_sa_email}"
#             )
#             .execute()
#         )
#         # logger.debug("_list_sa_keys_resp: {}".format(_list_sa_keys_resp))
#         # logger.debug("_list_sa_keys_resp type: {}".format(type(_list_sa_keys_resp)))
#         _available_keys = _list_sa_keys_resp.get("keys", [])
#         _num_avl_keys = len(_available_keys)
#         if _num_avl_keys > 0:
#             pprint_status(f"This service account has {_num_avl_keys} active keys")
#     except Exception as e:
#         pass
#
#     return sa_key
#
#
# def create_service_account_key_manually(
#     ws_name: str,
#     config: PhiConf,
#     phi_sa_name: str,
#     phi_sa_displayname: str,
#     sa_key_path: Path,
#     ws_config_file_path: Path,
# ) -> Optional[Dict[str, Any]]:
#
#     # The Service Account Key which will be used by phidata to manage GCP resources for the user
#     sa_key: Optional[Dict[str, Any]] = None
#
#     pprint_subheading("Steps to create a service account and key:")
#     # PREREQUISITES
#     pprint_info(
#         "Open another terminal and create a service account using the following steps:"
#     )
#     pprint_subheading("\nI. Setup GCloud SDK (skip if you already have gcloud setup)")
#     pprint_info("  1. Install gcloud: https://cloud.google.com/sdk/docs")
#     pprint_info("  2. Initialize gcloud using `gcloud init`")
#     pprint_info("  3. Please select the GCP project for phidata to use")
#
#     pprint_subheading("\nII. Create Service Account for phidata and grant permissions")
#     pprint_info(
#         f"  1. Create a service account using:\n\ngcloud iam service-accounts create {phi_sa_name} --display-name='{phi_sa_displayname}'\n"
#     )
#     pprint_info(
#         f"  2. Get the service account email using:\n\ngcloud iam service-accounts list --filter='NAME:{phi_sa_displayname}' --format='value(EMAIL)'\n"
#     )
#     pprint_info(
#         f"  3. Grant the Service Account permissions to manage resources on your behalf\n"
#     )
#     pprint_info(f"gcloud projects add-iam-policy-binding [PROJECT_ID] \ ")
#     pprint_info(f"--member='serviceAccount:[SERVICE_ACCOUNT_EMAIL]' \ ")
#     pprint_info(f"--role='roles/editor'\n")
#     pprint_info(f"  4. Finally, create a key so phi can use the service account\n")
#     pprint_info(f"gcloud iam service-accounts keys create \ ")
#     pprint_info(f"{str(sa_key_path)} \ ")
#     pprint_info(f"--iam-account='[SERVICE_ACCOUNT_EMAIL]'")
#
#     pprint_subheading(
#         "\nIII. Update workspace configuration with GCP Project information"
#     )
#     pprint_info(f"\nConfig file to be updated: {str(ws_config_file_path)}\n")
#
#     prereq_complete = input("Press Enter when done: ")
#     pprint_info("")
#     if not sa_key_path.exists() or not sa_key_path.is_file():
#         pprint_error(f"Could not find key at {str(sa_key_path)}, please try again")
#         return sa_key
#
#     sa_key = json.load(sa_key_path.open())
#     print(f"Key type: {type(sa_key)}")
#     print(f"Key: {sa_key}")
#
#     if sa_key is None:
#         pprint_error(
#             f"Could not read key at {str(sa_key_path)}, please verify key exists and try again"
#         )
#         return None
#
#     sa_key_type: Optional[str] = sa_key.get("type", None)
#     sa_key_project_id: Optional[str] = sa_key.get("project_id", None)
#     sa_key_client_email: Optional[str] = sa_key.get("client_email", None)
#     print(f"sa_key_type: {sa_key_type}")
#     print(f"sa_key_project_id: {sa_key_project_id}")
#
#     if sa_key_type != "service_account":
#         pprint_error(
#             f"Unexpected `type` in Service Account Key, found {sa_key_type} expected 'service_account'"
#         )
#         return None
#
#     # set the ws_gcp_data before returning the key
#     # since this could be the first time we're creating PhiGcpData for this ws
#     # we provide the project_id as well
#     config.update_ws_gcp_data(
#         ws_name=ws_name, gcp_project_id=sa_key_project_id, gcp_svc_account_key=sa_key
#     )
#     return sa_key
#
#
# def authenticate_gcp_project_for_ws(
#     ws_schema: schemas.WorkspaceSchema, config: PhiConf
# ) -> Optional[schemas.GCPProjectSchema]:
#     """Handles Authenticating a GCP project for the WorkspaceSchema.
#     Results in using the existing GCPProjectSchema for the ws OR creating a new schemas.GCPProjectSchema
#     Requires:
#     * schemas.WorkspaceSchema is valid
#     * PhiConf is valid
#     * Pak8Conf is valid
#
#     Steps:
#     1. Validate the ws_data, ws_root_path and ws_config_file_path
#     2. Validate that the Pak8Conf has `gcp` key set.
#     3. Check if an existing GCPProjectSchema exists for this workspace,
#         if yes, check if a GKEClusterSchema is available as well. Return the existing GCPProjectSchema
#     4. Create a new GCPProjectSchema for this workspace using a service account key
#     5. Check if an existing key is available on the users machine,
#         if yes, ask the user if they'd like to use that key instead
#     6. If no key is available, or if the user would like to create a new key
#         Ask the user how they would like to create the service account and key
#         Option 1: phi creates the service account and key for the user
#         Option 2: user manually creates the key
#     7. Using the service account and key, upload the data to zeus and get a GCPProjectSchema in return.
#         Return this GCPProjectSchema
#
#     Returns
#     schemas.GCPProjectSchema: The GCPProjectSchema received from zeus
#     """
#
#     if ws_schema is None or config is None:
#         return None
#     ws_name: str = ws_schema.name
#     id_workspace: int = ws_schema.id_workspace
#     logger.debug(f"Authenticating GCPProjectSchema for {ws_name}")
#
#     ######################################################
#     # Validate WorkspaceSchema Data
#     ######################################################
#     # Step 1: Validate the ws_data, ws_root_path and ws_config_file_path
#     ws_data: Optional[PhiWsData] = config.get_ws_data_by_name(ws_name)
#     if ws_data is None:
#         pprint_error(
#             f"WorkspaceSchema {ws_name} not registered with `phi` on this machine, please run `phi ws setup -w {ws_name}`"
#         )
#         return None
#
#     # Validate that this workspace has a ws_root_path and ws_config_file_path set
#     # Because without the ws_root_path and ws_config_file_path there's not point in reading the config
#     ws_root_path: Optional[Path] = ws_data.ws_root_path
#     ws_config_file_path: Optional[Path] = ws_data.ws_config_file_path
#     if ws_root_path is None or ws_config_file_path is None:
#         pprint_error(
#             f"WorkspaceSchema {ws_name} has incomplete data, please run `phi ws setup -w {ws_name}` to fix"
#         )
#         return None
#
#     # Step 2: Validate that the Pak8Conf has `gcp` key set.
#     ws_pak8_conf: Optional[Pak8Conf] = config.get_ws_pak8_conf_by_name(
#         ws_name=ws_name, refresh=True
#     )
#     if ws_pak8_conf is None:
#         pprint_error("WorkspaceSchema Config invalid")
#         pprint_status("Please fix your workspace config and try again")
#         return None
#     if ws_pak8_conf.gcp is None:
#         pprint_error("This workspace does not have a GCP project configured")
#         pprint_status("Please set the `gcp` section of your ws config")
#         return None
#
#     # Step 3: Check if an existing GCPProjectSchema exists for this workspace,
#     # if yes, check if a GKEClusterSchema is available as well.
#     # Add these objects to the PhidatConfig
#     gcp_project_from_api: Optional[schemas.GCPProjectSchema] = get_primary_gcp_project(
#         id_workspace
#     )
#     if gcp_project_from_api:
#         pprint_status("Found an existing GCPProjectSchema for this workspace")
#         # since this could be the first time we're creating a PhiGcpData for this ws
#         # we set the gcp_project_id and gcp_project for this workspace
#         config.update_ws_gcp_data(
#             ws_name=ws_name,
#             gcp_project_id=gcp_project_from_api.gcp_project_id,
#             gcp_project=gcp_project_from_api,
#         )
#         gke_cluster: Optional[
#             schemas.GKEClusterSchema
#         ] = get_gke_cluster_for_gcp_project(
#             id_workspace=id_workspace,
#             id_project=gcp_project_from_api.id_project,
#         )
#         if gke_cluster is not None:
#             pprint_status("Found an existing GKEClusterSchema for this workspace")
#             config.update_ws_gcp_data(ws_name=ws_name, gke_cluster=gke_cluster)
#
#     # Step 4: Create a new GCPProjectSchema for this workspace using a service account key
#     _sa_key_path: Path = (
#         ws_pak8_conf.gcp.credentials.service_account_key_path
#         if ws_pak8_conf.gcp.credentials
#         and ws_pak8_conf.gcp.credentials.service_account_key_path
#         else get_default_sa_key_path_(ws_root_path)
#     )
#
#     # Step 5: Check if an existing key is available on the users machine,
#     # if yes, ask the user if they'd like to use that key instead
#     _sa_key_json: Optional[Dict[str, Any]] = (
#         ws_pak8_conf.gcp.credentials.service_account_key_json
#         if ws_pak8_conf.gcp.credentials
#         and ws_pak8_conf.gcp.credentials.service_account_key_json
#         else None
#     )
#     if _sa_key_json is not None:
#         # If it does, ask the user if they'd like to use it
#         pprint_status(f"phi found a key at {_sa_key_path}")
#         use_existing_key: bool = typer.confirm(
#             "Would you like to use the existing key?"
#         )
#         if use_existing_key:
#             config.update_ws_gcp_data(
#                 ws_name=ws_name,
#                 gcp_project_id=ws_pak8_conf.gcp.project_id,
#                 gcp_svc_account_key=_sa_key_json,
#             )
#             return _upsert_primary_gcp_project_for_ws(ws_name, config)
#
#     ######################################################
#     # Create a GCP Service Account and Key for phidata
#     ######################################################
#     # Step 6: If no key is available, or if the user would like to create a new key
#     # Ask the user how they would like to create the service account and key
#     # Option 1: phi creates the service account and key for the user
#     # Option 2: user manually creates the key
#     phi_sa_name = "phidata-{}-sa".format(ws_name)
#     phi_sa_displayname = "phidata-sa"
#
#     pprint_heading("Using Phidata with Google Cloud")
#     pprint_info(
#         "To work with GCP, phi needs a Service Account to manage your resources."
#     )
#     pprint_info(
#         "Please select how you would like to create the service account and key:"
#     )
#     pprint_info(
#         "  [1] Authorize phi to use your local gcloud to create a service account and key for you (Recommended)"
#     )
#     pprint_info("  [2] Manually create the service account and key")
#     _create_sa_inp_raw: str = input("--> ")
#     _create_sa_inp: Optional[int] = str_to_int(_create_sa_inp_raw)
#     pprint_info("")
#     if _create_sa_inp is None:
#         pprint_info("\nExiting...\n")
#         return None
#
#     sa_key: Optional[Dict[str, Any]] = None
#     # NOTE: Both of these methods are expected to create the PhiGcpData for this workspace
#     # The following _upsert_gcp_project_for_ws() function only updates the gcp_project
#     if _create_sa_inp == 1:
#         sa_key = create_service_account_key_application_default_creds(
#             ws_name,
#             config,
#             phi_sa_name,
#             phi_sa_displayname,
#             _sa_key_path,
#         )
#     elif _create_sa_inp == 2:
#         sa_key = create_service_account_key_manually(
#             ws_name,
#             config,
#             phi_sa_name,
#             phi_sa_displayname,
#             _sa_key_path,
#             ws_config_file_path,
#         )
#     else:
#         pprint_error("Sorry, could not parse input. Please run `phi gcp auth` again.")
#
#     if sa_key is None:
#         pprint_error(
#             "Service Account creation failed, please run `phi gcp auth` again."
#         )
#
#     # Step 7: Using the service account and key, upload the data to zeus and get a GCPProjectSchema in return.
#     # Return this GCPProjectSchema
#     return _upsert_primary_gcp_project_for_ws(ws_name, config)
