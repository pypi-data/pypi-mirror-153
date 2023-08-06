from phiterm.utils.enums import ExtendedEnum


class ReleaseType(ExtendedEnum):
    CREATE_GKE_CLUSTER = "CREATE_GKE_CLUSTER"
    DELETE_GKE_CLUSTER = "DELETE_GKE_CLUSTER"
