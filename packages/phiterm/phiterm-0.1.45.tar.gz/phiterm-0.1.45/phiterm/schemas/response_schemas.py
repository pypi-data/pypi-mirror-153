from typing import List, Optional

from pydantic import BaseModel

from phiterm.enums.response_enums import BackendResponseStatus


class BackendResponse(BaseModel):
    status: BackendResponseStatus = BackendResponseStatus.FAIL
    message: str = "INVALID"
    message_log: Optional[List[str]] = None
