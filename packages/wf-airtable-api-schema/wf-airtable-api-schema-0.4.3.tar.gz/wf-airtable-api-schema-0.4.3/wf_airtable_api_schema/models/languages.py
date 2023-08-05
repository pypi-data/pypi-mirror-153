from typing import Optional

from .base_model import BaseModel

MODEL_TYPE = "language"


class CreateAPILanguagesFields(BaseModel):
    language: Optional[str] = None
    is_primary_language: Optional[bool] = None


class APILanguagesFields(CreateAPILanguagesFields):
    full_name: Optional[str] = None
    language_dropdown: Optional[str] = None
    language_other: Optional[str] = None
