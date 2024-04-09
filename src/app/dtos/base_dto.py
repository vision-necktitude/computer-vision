from typing import Optional
from pydantic import BaseModel, validator, Field

class BaseDto(BaseModel):
    def __init__(self, **data):
        if "_id" in data:
            data["created_at"] = data["_id"].generation_time
            data["_id"] = str(data["_id"])
        super().__init__(**data)

    id: Optional[str] = Field(
        alias="_id",
    )