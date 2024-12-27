from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class CampusEvent(BaseModel):
    description: str
    timestamp: datetime
    type: Literal["Career", "Sports", "Engineering", "Arts", "Science", "Other"]
    organization: str
    location: str
    image_url: str
    link: str
