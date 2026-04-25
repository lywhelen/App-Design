from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Interval
from datetime import timedelta

db = SQLAlchemy()

class User(db.Model):
    """
    User model
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    streak = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    tasks = db.relationship(
        "Task",
        cascade="delete"
    )

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.email = kwargs.get("email", "")
        self.streak = 0
        self.points = 0


    def serialize(self, include_tasks=True):
        """
        Serialize a user object
        """
        body = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "streak": self.streak,
            "points": self.points
        }
        if include_tasks:
            all_tasks = []
            for task in self.tasks:
                all_tasks.append(task.serialize())
            body["tasks"] = all_tasks
        else:
            body["tasks"] = None
        return body

#notifiications 
class Task(db.Model):
    """
    Assignment model
    """
    __tablename__ = "tasks"
    #id, tiitle, description, priority, estimated time, ocmpleted
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String, nullable=True)
    description=db.Column(db.String, nullable=False)
    priority=db.Column(db.Integer, nullable=True) #scale from 1 to 10
    duration=db.Column(Interval)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description")
        self.priority = kwargs.get("priority", 1)
        self.duration = kwargs.get("duration", timedelta(hours=0, minutes=30))
        self.user_id = kwargs.get("user_id")
        


    def serialize(self, include_tasks=True):
        """
        Serialize a user object
        """
        body = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "duration": self.duration,
            "user_id": self.user_id
        }
        return body




#example for creatigna   new task, new_task=Task(duration=timedelta(hours=2, minutes=30))




