# from phiterm.utils.enums import ExtendedEnum
#
#
# class GCPProjectStatus(ExtendedEnum):
#
#     ## Deployment States
#
#     # The project has just been created, no action has yet been taken on this
#     # The GCPProjectSchema maintains this status till it is deployed or activated
#     # using activate_gcp_project(), we should try and minimize the projects in this state
#     NEW = "NEW"
#
#     # Project is re-actived after being deactivated
#     REACTIVATED = "REACTIVATED"
#
#     # A deployment for this project has been created
#     # this is a temporary state and instances of this status in the DB imply unsuccessful deployments
#     RELEASE_CREATED = "RELEASE_CREATED"
#     # A GKEClusterSchema for this project has been created, this is also temporary state
#     GKE_CLUSTER_CREATED = "GKE_CLUSTER_CREATED"
#     # We have started to deploy applications, this is also temporary state
#     K8S_APPS_DEPLOYING = "K8S_APPS_DEPLOYING"
#     # K8s Applications are now deployed, this is also temporary state
#     K8S_APPS_DEPLOYED = "K8S_APPS_DEPLOYED"
#     # The deployed K8s Applications are now validated, meaning that the deployment was successful
#     # Majority of our GCPProjects should be in this state
#     ALL_SYSTEMS_RUNNING = "ALL_SYSTEMS_RUNNING"
#
#     # K8s Applications could not be deployed, this is an error state
#     K8S_APPS_DEPLOYMENT_ERROR = "K8S_APPS_DEPLOYMENT_ERROR"
#
#     ## Shutdown states
#
#     GKE_CLUSTER_DELETE_REQUEST = "GKE_CLUSTER_DELETE_REQUEST"
#     GKE_CLUSTER_DELETED = "GKE_CLUSTER_DELETED"
#
#     # Project is requested to be shutdown
#     DEACTIVATE_REQUEST = "DEACTIVATE_REQUEST"
#     # Project is shutdown
#     DEACTIVATED = "DEACTIVATED"
#
#     UNSPECIFIED = "UNSPECIFIED"
#
#
# class GCPOperationType(ExtendedEnum):
#     """Currently supported GCP Operations."""
#
#     # Operation types from GKE
#     # https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1beta1/projects.locations.operations#Operation.Type
#     GKE_CREATE_CLUSTER = "GKE_CREATE_CLUSTER"
#     GKE_DELETE_CLUSTER = "GKE_DELETE_CLUSTER"
#     GKE_TYPE_UNSPECIFIED = "GKE_TYPE_UNSPECIFIED"
#     GKE_UPGRADE_MASTER = "GKE_UPGRADE_MASTER"
#     GKE_UPGRADE_NODES = "GKE_UPGRADE_NODES"
#     GKE_REPAIR_CLUSTER = "GKE_REPAIR_CLUSTER"
#     GKE_UPDATE_CLUSTER = "GKE_UPDATE_CLUSTER"
#     GKE_CREATE_NODE_POOL = "GKE_CREATE_NODE_POOL"
#     GKE_DELETE_NODE_POOL = "GKE_DELETE_NODE_POOL"
#     GKE_SET_NODE_POOL_MANAGEMENT = "GKE_SET_NODE_POOL_MANAGEMENT"
#     GKE_AUTO_REPAIR_NODES = "GKE_AUTO_REPAIR_NODES"
#     GKE_AUTO_UPGRADE_NODES = "GKE_AUTO_UPGRADE_NODES"
#     GKE_SET_LABELS = "GKE_SET_LABELS"
#     GKE_SET_MASTER_AUTH = "GKE_SET_MASTER_AUTH"
#     GKE_SET_NODE_POOL_SIZE = "GKE_SET_NODE_POOL_SIZE"
#     GKE_SET_NETWORK_POLICY = "GKE_SET_NETWORK_POLICY"
#     GKE_SET_MAINTENANCE_POLICY = "GKE_SET_MAINTENANCE_POLICY"
