from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from phiterm.conf.constants import PHI_CONF_PATH
from phiterm.schemas.user_schemas import UserSchema
from phiterm.utils.cli_console import (
    print_available_workspaces,
    print_info,
    print_error,
    print_heading,
    print_horizontal_line,
    print_info,
    print_subheading,
)
from phiterm.utils.common import pickle_object_to_file, unpickle_object_from_file
from phiterm.utils.dttm import current_datetime_utc
from phiterm.utils.filesystem import delete_from_fs
from phiterm.utils.log import logger
from phiterm.workspace.phi_ws_data import PhiWsData
from phiterm.workspace.ws_enums import WorkspaceSetupActions
from phiterm.workspace.ws_schemas import WorkspaceSchema


class PhiConf:
    """The PhiConf class manages user data for the phi cli"""

    def __init__(self):
        # Current user, populated after authenticating with the backend
        # To add a user, use the user setter
        self._user: Optional[UserSchema] = None

        # Active ws - used as the default for all phi commands
        # To add an active workspace, use the active_ws_name setter
        self._active_ws_name: Optional[str] = None

        # ** The self._ws_data_map holds the mapping from ws_name to ws_data.
        self._ws_data_map: Dict[str, PhiWsData] = OrderedDict()
        # When phi is initialized using `phi init`, this is an empty dict
        # When the user is authenticated, we get a list of all the workspaces this user has access to.
        # These workspaces are then added to PhiConf using the `active_ws_name` and `available_ws` setters.
        # Note: These workspaces arent yet cloned on the users machines and only a record of their availability is kept.
        # When the workspace is setup on the users machine, we update the remaining workspace data.

        # Quick access from ws_path -> ws data.
        self._path_to_ws_data_map: Dict[Path, PhiWsData] = OrderedDict()

        # Save the config to disk once initialized
        self.save_config()

    ######################################################
    ## User functions
    ######################################################

    @property
    def user(self) -> Optional[UserSchema]:
        return self._user

    @user.setter
    def user(self, user: Optional[UserSchema]) -> None:
        """Sets the user"""
        if user is not None:
            self._user = user
            self.save_config()

    ######################################################
    ## Workspace functions
    ######################################################

    @property
    def active_ws_name(self) -> Optional[str]:
        return self._active_ws_name

    @active_ws_name.setter
    def active_ws_name(self, ws_name: Optional[str]) -> None:
        if ws_name is not None:
            self._active_ws_name = ws_name
            self._add_or_update_ws_data(ws_name=ws_name)
            self.save_config()

    @property
    def available_ws(self) -> List[WorkspaceSchema]:
        return [
            w.ws_schema for w in self._ws_data_map.values() if w.ws_schema is not None
        ]

    @available_ws.setter
    def available_ws(self, avl_ws: Optional[List[WorkspaceSchema]]) -> None:
        if avl_ws:
            for ws_schema in avl_ws:
                self._add_or_update_ws_data(ws_name=ws_schema.name, ws_schema=ws_schema)
            self.save_config()

    def _add_or_update_ws_data(
        self,
        ws_name: str,
        ws_schema: Optional[WorkspaceSchema] = None,
        ws_root_path: Optional[Path] = None,
        ws_config_file_path: Optional[Path] = None,
    ) -> None:
        """The main function to create, update or refresh PhiWsData in PhiConf.

        Notes:
        * ws_name is the only required argument.
        * This function does not call self.save_config(). call it from the parent.

        This function is called from 5 places:
        1. During `phi auth` when active/available workspaces are requested from the backend.
        2. During `phi ws init` when a new workspace is created on the users machine.
        3. When the user already has a local workspace dir on their machine
            and need to manually add the ws to the PhiConf
            (possible after running `phi init -r` which deletes the config)
        4. Whenever ws config, creds or data needs to be refreshed. This function is called with just the `ws_name` arg
        5. When active or available workspaces are updated, this function is called from the
            @active_ws_name.setter and @available_ws.setter with the ws_name and ws_schema
        """

        ######################################################
        # Validate ws_name
        ######################################################

        # ws_name should not be None
        if ws_name is None or not isinstance(ws_name, str):
            return

        ######################################################
        # Create ws_data if it does not exist
        ######################################################

        if ws_name not in self._ws_data_map:
            logger.debug(f"Creating workspace: {ws_name}")
            self._ws_data_map[ws_name] = PhiWsData(
                ws_name=ws_name,
                ws_schema=ws_schema,
                ws_root_path=ws_root_path,
                ws_config_file_path=ws_config_file_path,
            )
            if ws_root_path is not None:
                self._path_to_ws_data_map[ws_root_path] = self._ws_data_map[ws_name]
                logger.debug(f"Workspace dir: {ws_root_path}")
            logger.debug(f"Workspace created: `{ws_name}`")

        ######################################################
        # Update ws_data
        ######################################################

        # By this point there should be a PhiWsData object for this ws_name
        existing_ws_data: PhiWsData = self._ws_data_map.get(
            ws_name, PhiWsData(ws_name=ws_name)
        )
        # Make a deep copy of the existing workspace data
        # This allows us to update the fields we want, and keep any existing fields as is
        _ws_data: PhiWsData = existing_ws_data.copy(deep=True)

        # Update values where available
        if ws_schema is not None and ws_schema != existing_ws_data.ws_schema:
            logger.debug("Updating ws_schema")
            _ws_data.ws_schema = ws_schema
        if ws_root_path is not None and ws_root_path != existing_ws_data.ws_root_path:
            logger.debug("Updating ws_root_path")
            _ws_data.ws_root_path = ws_root_path
        if (
            ws_config_file_path is not None
            and ws_config_file_path != existing_ws_data.ws_config_file_path
        ):
            logger.debug("Updating ws_config_file_path")
            _ws_data.ws_config_file_path = ws_config_file_path

        # Load the WorkspaceConfig
        _ws_data.last_update_ts = current_datetime_utc()

        # Point the ws_data in _ws_data_map and _path_to_ws_data_map
        # to new _ws_data
        logger.debug(f"Updating mapping for: {ws_name}")

        # 1. Pop the existing object from the self._ws_data_map
        if ws_name in self._ws_data_map:
            popped_ws_data_from_map: Optional[PhiWsData] = self._ws_data_map.pop(
                ws_name
            )
            # logger.debug(f"Removed {ws_name} from _ws_data_map")
        self._ws_data_map[ws_name] = _ws_data

        # 2. Pop the existing object from the self._path_to_ws_data_map
        if _ws_data.ws_root_path is not None:
            if (
                existing_ws_data.ws_root_path is not None
                and existing_ws_data.ws_root_path in self._path_to_ws_data_map
            ):
                popped_ws_data_from_path_map: Optional[
                    PhiWsData
                ] = self._path_to_ws_data_map.pop(existing_ws_data.ws_root_path)
                logger.debug(
                    f"Pop {existing_ws_data.ws_root_path} from _path_to_ws_data_map"
                )
            self._path_to_ws_data_map[_ws_data.ws_root_path] = self._ws_data_map[
                ws_name
            ]

        ######################################################
        # END
        ######################################################

    def add_new_created_ws_to_config(
        self,
        ws_name: str,
        ws_root_path: Path,
        ws_config_file_path: Path,
    ) -> None:
        """Adds a newly created workspace to the PhiConf"""
        self._add_or_update_ws_data(
            ws_name=ws_name,
            ws_root_path=ws_root_path,
            ws_config_file_path=ws_config_file_path,
        )
        self.save_config()

    def update_ws_schema_for_workspace(
        self,
        ws_schema: WorkspaceSchema,
        set_as_active: bool = False,
    ) -> None:
        """Updates the schema for a workspace and sets as active if needed"""
        self._add_or_update_ws_data(
            ws_name=ws_schema.name,
            ws_schema=ws_schema,
        )
        if set_as_active:
            self.active_ws_name = ws_schema.name
        self.save_config()

    def update_ws_data(
        self,
        ws_name: str,
        ws_schema: Optional[WorkspaceSchema] = None,
        ws_root_path: Optional[Path] = None,
        ws_config_file_path: Optional[Path] = None,
    ) -> None:
        """Update workspace data and return True if successful"""

        logger.debug(f"Updating ws_data for {ws_name}")
        self._add_or_update_ws_data(
            ws_name=ws_name,
            ws_schema=ws_schema,
            ws_root_path=ws_root_path,
            ws_config_file_path=ws_config_file_path,
        )
        self.save_config()

    def update_ws_data_for_cloned_ws(
        self,
        ws_name: str,
        ws_root_path: Path,
        ws_config_file_path: Path,
    ) -> bool:
        """For a workspace to be cloned, it would already have ws_data and ws_schema available.
        After the directory from the git_url is cloned, we can fill in the gaps to update
        the ws_data for the workspace. Call this function through ws_operator.clone_workspace()
        """
        ws_data: Optional[PhiWsData] = self._ws_data_map.get(ws_name, None)
        if ws_data is None:
            return False

        self._add_or_update_ws_data(
            ws_name=ws_name,
            ws_root_path=ws_root_path,
            ws_config_file_path=ws_config_file_path,
        )
        self.save_config()
        return True

    def add_ws_data_using_config_file(
        self, ws_root_path: Path, ws_config_file_path: Optional[Path]
    ) -> Optional[PhiWsData]:
        """Maps a ws at `ws_root_path` to an available workspace. using the config file at `ws_config_file_path`.
        Also updates the ws_config_file_path in the ws_data if provided.

        This is used in 2 cases:
        1. If the user ran `phi init -r`, the PhiConf gets erased and so does self._path_to_ws_data_map
            So there is no link from the ws_root_path to the workspace.
        2. The user manually cloned the workspace directory. In that case we don't have a record of this
            ws_root_path matching any available workspace.

        This function basically reads the workspace config and tries to map it to an available workspace.
        Returns the PhiWsData if successful
        """

        logger.debug(f"Looking for the workspace at {ws_root_path}")
        _best_guess_ws_name = ws_root_path.stem
        logger.debug(f"_best_guess_ws_name: {_best_guess_ws_name}")
        _ws_schema: Optional[WorkspaceSchema] = None
        for avl_ws in self.available_ws:
            if avl_ws.name == _best_guess_ws_name:
                _ws_schema = avl_ws
            break
        if _ws_schema is None:
            print_error(
                f"Workspace name: {_best_guess_ws_name} does not match any available workspaces"
            )
            print_available_workspaces(self.available_ws)
            return None

        logger.debug(f"Found matching workspace {_ws_schema.name}")
        logger.debug(
            f"Mapping {_ws_schema.name} to dir: {ws_root_path} and config: {ws_config_file_path}"
        )
        self._add_or_update_ws_data(
            ws_name=_ws_schema.name,
            ws_schema=_ws_schema,
            ws_root_path=ws_root_path,
            ws_config_file_path=ws_config_file_path,
        )
        self.save_config()
        return self._ws_data_map.get(_ws_schema.name, None)

    def validate_workspace(
        self, ws_name: str
    ) -> Tuple[bool, Optional[Set[WorkspaceSetupActions]]]:
        """Validates a workspace and returns a tuple of [validation_status, pending_setup_actions]
        Returns:
            (False, None): If PhiWsData is not valid
            (True, None): If Validation is successful and everything is properly setup
            (True, set(WorkspaceSetupActions)): If Validation is successful but user has pending setup actions
            (False, set(WorkspaceSetupActions)): If Validation is unsuccessful and user has pending setup actions
        """

        # Validate the ws has a valid entry
        if ws_name is None or ws_name not in self._ws_data_map:
            return False, None
        logger.debug(f"Validating workspace: {ws_name}")

        ws_data: PhiWsData = self._ws_data_map[ws_name]

        # If ws_config is missing add a pending action
        if ws_data.ws_config is None:
            ws_data.pending_actions.add(WorkspaceSetupActions.WS_CONFIG_IS_AVL)
        else:
            ws_data.pending_actions.discard(WorkspaceSetupActions.WS_CONFIG_IS_AVL)

        # If ws_schema is missing add a pending action
        if ws_data.ws_schema is None:
            ws_data.pending_actions.add(WorkspaceSetupActions.WS_IS_AUTHENTICATED)
        else:
            ws_data.pending_actions.discard(WorkspaceSetupActions.WS_IS_AUTHENTICATED)

        # If git_url is missing add a pending action
        if ws_data.ws_schema is None:
            from phiterm.utils.git import get_remote_origin_for_dir

            _remote_origin = get_remote_origin_for_dir(ws_data.ws_root_path)
            if _remote_origin is None:
                ws_data.pending_actions.add(
                    WorkspaceSetupActions.GIT_REMOTE_ORIGIN_IS_AVL
                )
        elif ws_data.ws_schema.git_url is None:
            ws_data.pending_actions.add(WorkspaceSetupActions.GIT_REMOTE_ORIGIN_IS_AVL)
        else:
            ws_data.pending_actions.discard(
                WorkspaceSetupActions.GIT_REMOTE_ORIGIN_IS_AVL
            )

        # logger.debug(f"Required Actions for this workspace: {ws_data.required_actions}")
        # logger.debug(f"Pending Actions for this workspace: {ws_data.pending_actions}")

        # Check how many required_actions are pending
        if len(ws_data.required_actions.intersection(ws_data.pending_actions)) > 0:
            return False, ws_data.pending_actions

        return True, ws_data.pending_actions

    def delete_ws(self, ws_name: str, delete_ws_dir: bool = False) -> bool:
        """Handles Deleting a workspace from the PhiConf"""

        print_info(f"Deleting workspace: {ws_name}")
        print_info(f"--> this does not delete any files, please delete them manually")

        ws_data: Optional[PhiWsData] = self._ws_data_map.pop(ws_name, None)
        if ws_data is None:
            print_error(f"No record of workspace {ws_name}")
            return False

        ws_data_from_path: Optional[PhiWsData]
        if ws_data.ws_root_path is not None:
            ws_data_from_path = self._path_to_ws_data_map.pop(
                ws_data.ws_root_path, None
            )

        # Check if we're deleting the active workspace, if yes, unset the active ws
        if (
            self._active_ws_name is not None
            and ws_data.ws_name is not None
            and self._active_ws_name == ws_data.ws_name
        ):
            print_info(f"Removing {ws_data.ws_name} as the active workspace")
            self._active_ws_name = None

        ws_root_path_deleted: bool = False
        if delete_ws_dir and ws_data.ws_root_path:
            print_info(f"Deleting {str(ws_data.ws_root_path)}")
            ws_root_path_deleted = delete_from_fs(ws_data.ws_root_path)

        # Save the config after deleting workspace
        self.save_config()
        return True

    ######################################################
    ## Get Workspace Data
    ######################################################

    def get_ws_data_by_name(self, ws_name: str) -> Optional[PhiWsData]:
        return self._ws_data_map[ws_name] if ws_name in self._ws_data_map else None

    def get_ws_data_by_path(self, ws_root_path: Path) -> Optional[PhiWsData]:
        return (
            self._path_to_ws_data_map[ws_root_path]
            if ws_root_path in self._path_to_ws_data_map
            else None
        )

    ## Workspace Name
    def get_ws_name_by_path(self, ws_root_path: Path) -> Optional[str]:
        if ws_root_path in self._path_to_ws_data_map:
            return self._path_to_ws_data_map[ws_root_path].ws_name
        return None

    ## Workspace Schema
    def get_ws_schema_by_name(self, ws_name: str) -> Optional[WorkspaceSchema]:
        if ws_name in self._ws_data_map:
            return self._ws_data_map[ws_name].ws_schema
        return None

    def get_ws_schema_by_path(self, ws_root_path: Path) -> Optional[WorkspaceSchema]:
        if ws_root_path in self._path_to_ws_data_map:
            return self._path_to_ws_data_map[ws_root_path].ws_schema
        return None

    ## Workspace Directory
    def get_ws_root_path_by_name(self, ws_name: str) -> Optional[Path]:
        if ws_name in self._ws_data_map:
            return self._ws_data_map[ws_name].ws_root_path
        return None

    ## Workspace Config File Path
    def get_ws_config_file_path_by_name(self, ws_name: str) -> Optional[Path]:
        if ws_name in self._ws_data_map:
            return self._ws_data_map[ws_name].ws_config_file_path
        return None

    ## Workspace Pending Actions
    def get_ws_pending_actions_by_name(
        self, ws_name: str
    ) -> Optional[Set[WorkspaceSetupActions]]:
        if ws_name in self._ws_data_map:
            return self._ws_data_map[ws_name].pending_actions
        return None

    ## Workspace Data
    def get_active_ws_data(self, refresh: bool = False) -> Optional[PhiWsData]:
        if self.active_ws_name is not None and self.active_ws_name in self._ws_data_map:
            if refresh:
                self.refresh_ws_config(self.active_ws_name)
            return self._ws_data_map[self.active_ws_name]
        return None

    def refresh_ws_config(self, ws_name: str) -> None:
        """Refresh the workspace config for a given workspace name"""

        self._add_or_update_ws_data(ws_name=ws_name)
        logger.debug(f"++**++ Config refreshed: {ws_name}")
        self.save_config()

    ######################################################
    ## PhiConf functions
    ######################################################

    def save_config(self):
        # logger.debug(f"Saving config to {str(PHI_CONF_PATH)}")
        pickle_object_to_file(self, PHI_CONF_PATH)

    @classmethod
    def get_saved_conf(cls):
        # logger.debug(f"Reading phidata conf at {PHI_CONF_PATH}")
        if PHI_CONF_PATH.exists():
            # logger.debug(f"{PHI_CONF_PATH} exists")
            if PHI_CONF_PATH.is_file():
                return unpickle_object_from_file(
                    file_path=PHI_CONF_PATH, verify_class=cls
                )
            elif PHI_CONF_PATH.is_dir():
                logger.debug(f"{PHI_CONF_PATH} is a directory, deleting and exiting")
                delete_from_fs(PHI_CONF_PATH)
        return None

    def print_to_cli(self):
        if self.user:
            print_info(f"* User: {self.user.email}")
        if self.active_ws_name:
            print_heading(f"\nActive workspace: {self.active_ws_name}\n")
        else:
            print_info("* No active workspace, run `phi ws init` to create one")
        if len(self._ws_data_map) > 0:
            print_heading("Available workspaces:\n")
            c = 1
            for k, v in self._ws_data_map.items():
                print_info(f"  {c}. Name: {v.ws_name}")
                print_info(f"     Dir: {v.ws_root_path}")
                print_info(f"  -*-\n")
                c += 1
