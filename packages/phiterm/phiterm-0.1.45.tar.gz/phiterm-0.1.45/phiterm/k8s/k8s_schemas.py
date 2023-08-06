from typing import List, Optional

from pydantic import BaseModel

######################################################
# K8s Schemas
# These should match ~/philab/services/zeus/zeus/schemas/k8s_schemas.py
######################################################


class K8sFilters(BaseModel):
    type_filters: Optional[List[str]] = None
    name_filters: Optional[List[str]] = None
