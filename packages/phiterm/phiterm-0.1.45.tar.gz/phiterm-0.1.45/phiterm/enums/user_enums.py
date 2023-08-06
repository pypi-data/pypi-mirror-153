from phiterm.utils.enums import ExtendedEnum


class UserAuthProviderEnum(ExtendedEnum):
    TEST = "TEST"
    MANUAL = "MANUAL"
    EMAIL_PASS = "EMAIL_PASS"
    GOOGLE = "GOOGLE"
    GITHUB = "GITHUB"


class VersionControlProviderEnum(ExtendedEnum):
    GITHUB = "GITHUB"
    GITLAB = "GITLAB"
    BITBUCKET = "BITBUCKET"
