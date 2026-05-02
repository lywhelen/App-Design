from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Interval
from datetime import timedelta, datetime, date
from sqlalchemy import Column, DateTime, Date

db = SQLAlchemy()


class User(db.Model):
    """
    User model
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    streak = db.Column(db.Integer, nullable=False, default=0)
    points = db.Column(db.Integer, nullable=False, default=0)
    last_completed_date = db.Column(Date, nullable=True)

    tasks = db.relationship("Task", cascade="delete")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.email = kwargs.get("email", "")
        self.streak = 0
        self.points = 0
        self.last_completed_date = None

    def calculate_task_points(self, task):
        """
        30 min = 1 point + priority bonus (priority / 5), minimum 1 pt.
        """
        half_hours = (task.duration.total_seconds() / 1800) if task.duration else 0
        base_points = half_hours
        priority_bonus = (task.priority or 0) / 5
        total_points = int(base_points + priority_bonus)
        return max(total_points, 1)

    def complete_task(self, task):
        """
        Awards points when a task is completed. Guards against double-counting.
        """
        if task.completed is True:
            return
        points_earned = self.calculate_task_points(task)
        self.points += points_earned
        task.completed = True

    def update_streak(self):
        """
        Streak logic:
        - +1 streak if user completed a task today.
        - Resets to 1 if more than 1 day has elapsed since last completion.
        - Every 3 days awards +5 bonus points.
        - Updates last_completed_date to today.
        """
        today = date.today()

        if self.last_completed_date is None:
            # first-ever completion — streak defaults to 0, increment to 1
            self.streak += 1
        elif self.last_completed_date == today:
            return
        elif (today - self.last_completed_date).days == 1:
            # consecutive day
            self.streak += 1
        else:
            # gap > 1 day — reset
            self.streak = 1

        # streak bonus every 3 consecutive days
        if self.streak % 3 == 0:
            self.points += 5

        self.last_completed_date = today

    def serialize(self, include_tasks=True):
        """
        Serialize a user object.
        """
        body = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "streak": self.streak,
            "points": self.points,
            "last_completed_date": self.last_completed_date.isoformat() if self.last_completed_date else None,
        }
        if include_tasks:
            body["tasks"] = [task.serialize() for task in self.tasks]
        else:
            body["tasks"] = None
        return body


class Task(db.Model):
    """
    Task model — one study task belonging to a user.
    """
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    priority = db.Column(db.Integer, nullable=True)  # is it integer rly? 
    duration = db.Column(Interval)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_started = db.Column(DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.priority = kwargs.get("priority", 1)
        self.duration = kwargs.get("duration", timedelta(minutes=30))
        self.user_id = kwargs.get("user_id")
        self.completed = False
        self.date_started = datetime.now()

    def serialize(self):
        """
        Serialize a task. duration → duration_seconds (int), date_started → ISO string.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "duration_minutes": int(self.duration.total_seconds() / 60) if self.duration else None,
            "user_id": self.user_id,
            "completed": self.completed,
            "date_started": self.date_started.isoformat() if self.date_started else None
        }

'''
class Track(db.Model):
    """
    Track model — one completed ring (fully-filled study session).
    Persisted permanently in the user's Album.
    """
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    completed_at = db.Column(DateTime, default=datetime.utcnow)
    total_points_earned = db.Column(db.Integer, nullable=False, default=0)
    # Color string used by the frontend to style the album groove (e.g. "gold", "blue", "red")
    color = db.Column(db.String, nullable=False, default="gold")

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.completed_at = datetime.utcnow()
        self.total_points_earned = kwargs.get("total_points_earned", 0)
        self.color = kwargs.get("color", "gold")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_points_earned": self.total_points_earned,
            "color": self.color,
        }
'''