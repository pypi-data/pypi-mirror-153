from typing import Optional

from .base_model import BaseModel

MODEL_TYPE = "target_community"


class APITargetCommunityFields(BaseModel):
    name: Optional[str] = None
