from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Interval
from datetime import timedelta
from datetime import datetime
from sqlalchemy import Column, DateTime

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

    def calculate_task_points(self, task):
        """
        Point logic for each task where 1 hour = 1 point and the priority (1–10) adds a small bonus
        """
        hours = (task.duration.total_seconds() / 3600) if task.duration else 0
        base_points = hours
        priority_bonus = (task.priority or 0) / 5
        total_points = int(base_points + priority_bonus)
        return max(total_points, 1)



    def complete_task(self, task):
        """
        Awards points when a task is completed with no double cointing
        """
        #no double count
        if task.completed is True:
            return

        points_earned = self.calculate_task_points(task)
        self.points += points_earned
        task.completed = True


    def update_streak(self, completed_today):
        """
        Streak logic where +1 streak if user completed a task today and every 3 days gives +5 points bonus
        """
        if completed_today:
            self.streak += 1
            if self.streak % 3 == 0:
                self.points += 5
        else:
            self.streak = 0
    #maybe +1 if completed int eh same day (no points if not completed in teh same day), but if compelted during time itnerval thats wehn we do +1 to streak, else reset streak
                
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
    completed = db.Column(db.Boolean, default=False)
    date_started=db.Column(DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description")
        self.priority = kwargs.get("priority", 1)
        self.duration = kwargs.get("duration", timedelta(hours=0, minutes=30))
        self.user_id = kwargs.get("user_id")
        self.completed=False
        self.date_started=datetime.now
        


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
            "user_id": self.user_id,
            "completed": self.completed,
            "date_started": self.date_started
        }
        return body
    
    def update_task_completed(self, task):
        "user can update task complete sttaus from false to tru when they finish a  task"





#example for creatigna   new task, new_task=Task(duration=timedelta(hours=2, minutes=30))




