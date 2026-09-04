from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Topic(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    
    tasks = relationship("AITask", back_populates="topic")

class AITask(Base):
    __tablename__ = "aitask"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="PENDING") # PENDING, PROCESSING, COMPLETED, FAILED
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey("user.id"))
    topic_id = Column(Integer, ForeignKey("topic.id"))
    
    owner = relationship("User")
    topic = relationship("Topic", back_populates="tasks")
