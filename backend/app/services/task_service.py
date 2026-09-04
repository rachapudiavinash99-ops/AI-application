from sqlalchemy.orm import Session
from app.models.task import AITask, Topic
from app.services.ai_provider import get_ai_provider

class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_provider = get_ai_provider()

    def process_task(self, task_id: int):
        task = self.db.query(AITask).filter(AITask.id == task_id).first()
        if not task:
            return
            
        task.status = "PROCESSING"
        self.db.commit()
        
        try:
            # Here we would use task.description or other fields as prompt
            prompt = f"Topic: {task.topic.name}. Task: {task.title}. Description: {task.description}"
            result = self.ai_provider.generate_content(prompt)
            
            task.result = result
            task.status = "COMPLETED"
        except Exception as e:
            task.status = "FAILED"
            task.result = f"Error: {str(e)}"
            
        self.db.commit()
        return task
