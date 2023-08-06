# import datetime
# from pathlib import Path
# from typing import Optional
#
# from pydantic import BaseModel
#
# from pak8.k8s.resources.kubeconfig import Kubeconfig
# from phiterm.conf.constants import PHI_KUBE_DIR
# from phiterm.utils.dttm import current_datetime_utc
# from phiterm.utils.log import logger
#
#
# class PhiK8sData(BaseModel):
#
#     # Set to True if the kubeconfig is available as a resource or in a file
#     # This flag saves us reading a file if the kubeconfig isnt available
#     kubeconfig_avl: bool = False
#     kubeconfig_resource: Optional[Kubeconfig] = None
#     kubeconfig_path: Optional[Path] = None
#     last_update_ts: datetime.datetime = current_datetime_utc()
#
#     @classmethod
#     def create_using_kubeconfig_resource(
#         cls, ws_name: str, kconf_resource: Kubeconfig
#     ) -> Optional["PhiK8sData"]:
#
#         if ws_name is None or kconf_resource is None:
#             return None
#
#         if not PHI_KUBE_DIR.exists():
#             PHI_KUBE_DIR.mkdir(exist_ok=True)
#
#         logger.debug("Creating PhiK8sData")
#         kconf_path: Path = PHI_KUBE_DIR.joinpath(f"{ws_name}_kubeconfig")
#         logger.debug(f"Saving kubeconfig to {str(kconf_path)}")
#         kconf_path.write_text(kconf_resource.json(by_alias=True))
#
#         return cls(
#             kubeconfig_avl=True,
#             kubeconfig_resource=kconf_resource,
#             kubeconfig_path=kconf_path,
#         )
#
#     def update_kubeconfig_resource(self, kconf_resource: Kubeconfig) -> bool:
#
#         if kconf_resource is None:
#             return False
#
#         logger.debug(f"Saving kubeconfig to {str(self.kubeconfig_path)}")
#         self.kubeconfig_resource = kconf_resource
#         if self.kubeconfig_path:
#             self.kubeconfig_path.write_text(kconf_resource.json(by_alias=True))
#             return True
#
#         return False
#
#     def get_kubeconfig(self) -> Optional[Kubeconfig]:
#         if not self.kubeconfig_avl:
#             logger.debug("No Kubeconfig available")
#             return None
#         # TODO: Update this to read from kubeconfig_path if kubeconfig_resource is None
#         return self.kubeconfig_resource
