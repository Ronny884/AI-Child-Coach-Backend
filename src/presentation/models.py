from pydantic import BaseModel, EmailStr, Json
from typing import List, Optional, Union, Any
import uuid


class StartData(BaseModel):
    child_id: uuid.UUID
    video_url: str

    class Config:
        arbitrary_types_allowed = True


class ProcessingData(BaseModel):
    child_id: uuid.UUID
    child_voice: bytes

    class Config:
        arbitrary_types_allowed = True
