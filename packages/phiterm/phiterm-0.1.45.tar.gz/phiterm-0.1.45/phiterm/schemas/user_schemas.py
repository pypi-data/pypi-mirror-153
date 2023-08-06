import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from phiterm.enums.user_enums import UserAuthProviderEnum, VersionControlProviderEnum
from phiterm.utils.dttm import dttm_str_to_dttm


######################################################
# User Schemas
# These should match ~/philab/services/zeus/zeus/schemas/user_schemas.py
######################################################
# The UserSchema schema defines the properties which are returned by the zeus API
# Need to be careful that this doesn't contain any sensitive info
class UserSchema(BaseModel):
    username: str
    email: str
    user_auth_provider: UserAuthProviderEnum
    is_active: bool
    is_employee: bool = False
    is_test: bool = False
    version_control_provider: Optional[VersionControlProviderEnum] = None
    id_user: int
    scopes: Optional[List[str]] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    locale: Optional[str] = None
    country_code: Optional[str] = None
    tos_accepted: bool = False
    email_verified: Optional[bool] = False
    create_ts: datetime.datetime
    last_update_ts: Optional[datetime.datetime] = None

    @classmethod
    def from_dict(cls, user_dict: Dict[str, Any]):
        return cls(
            username=user_dict.get("username", None),
            email=user_dict.get("email", None),
            user_auth_provider=UserAuthProviderEnum.from_str(
                user_dict.get("user_auth_provider", None)
            ),
            is_active=user_dict.get("is_valid", None),
            is_employee=user_dict.get("is_employee", None),
            is_test=user_dict.get("is_test", None),
            version_control_provider=VersionControlProviderEnum.from_str(
                user_dict.get("version_control_provider", None)
            ),
            id_user=user_dict.get("id_user", None),
            scopes=user_dict.get("scopes", None),
            name=user_dict.get("name", None),
            first_name=user_dict.get("first_name", None),
            last_name=user_dict.get("last_name", None),
            locale=user_dict.get("locale", None),
            country_code=user_dict.get("country_code", None),
            tos_accepted=user_dict.get("tos_accepted", None),
            email_verified=user_dict.get("email_verified", None),
            create_ts=dttm_str_to_dttm(user_dict.get("create_ts", None)),
            last_update_ts=dttm_str_to_dttm(user_dict.get("last_update_ts", None)),
        )
