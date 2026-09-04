from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.task import AITask, Topic
from app.models.user import User
from app.schemas.task import AITask as AITaskSchema, AITaskCreate, Topic as TopicSchema
from app.services.task_service import TaskService

router = APIRouter()

@router.get("/topics", response_model=List[TopicSchema])
def read_topics(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    return db.query(Topic).all()

@router.post("/tasks", response_model=AITaskSchema)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: AITaskCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    topic = db.query(Topic).filter(Topic.id == task_in.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    task = AITask(
        title=task_in.title,
        description=task_in.description,
        topic_id=task_in.topic_id,
        owner_id=current_user.id,
        status="PENDING"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Process task synchronously for this initial implementation
    # In production, use Celery or BackgroundTasks
    task_service = TaskService(db)
    task_service.process_task(task.id)
    
    db.refresh(task)
    return task

@router.get("/tasks", response_model=List[AITaskSchema])
def read_tasks(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    return db.query(AITask).filter(AITask.owner_id == current_user.id).offset(skip).limit(limit).all()
