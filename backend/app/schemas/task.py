from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TopicBase(BaseModel):
    name: str
    description: Optional[str] = None

class Topic(TopicBase):
    id: int
    class Config:
        from_attributes = True

class AITaskCreate(BaseModel):
    title: str
    description: str
    topic_id: int

class AITask(BaseModel):
    id: int
    title: str
    description: str
    status: str
    result: Optional[str]
    created_at: datetime
    topic_id: int
    owner_id: int

    class Config:
        from_attributes = True
