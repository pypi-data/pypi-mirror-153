# from typing import Optional
#
# from pak8.app.conf import Pak8AppConf
# from pak8.conf import Pak8Conf
# from phiterm.conf.phi_conf import PhiConf, PhiK8sData, PhiWsData
# from phiterm.utils.common import pprint_heading, pprint_status, pprint_subheading
# from phiterm.utils.log import logger
#
#
# def secho_pak8_service_status(pak8_svc: Pak8AppConf) -> None:
#
#     pprint_subheading("Service: {}".format(pak8_svc.name))
#     pprint_status("Type: {}".format(pak8_svc.type.value))
#     if pak8_svc.args:
#         pprint_status("Args: {}".format(pak8_svc.args))
#
#
# def secho_k8_status(ws_data: PhiWsData, config: PhiConf) -> None:
#
#     ws_pak8_conf: Optional[Pak8Conf] = ws_data.ws_pak8_conf
#
#     pprint_heading("K8s")
#     ws_k8s_data: Optional[PhiK8sData] = ws_data.ws_k8s_data
#     if ws_k8s_data:
#         logger.debug("kubeconfig available: {}".format(ws_k8s_data.kubeconfig_avl))
#         logger.debug("kubeconfig: {}".format(ws_k8s_data.kubeconfig_path))
#
#     # for pak8_svc in ws_pak8_conf.services:
#     #     secho_pak8_service_status(pak8_svc)
#     # resources_dir: Optional[Path] = config.get_k8s_resources_dir_path_by_ws_name(
#     #     ws_data.ws_name
#     # )
#     # if resources_dir:
#     #     pprint_status("Resources Saved to: {}".format(str(resources_dir)))
