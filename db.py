from flask_sqlalchemy import SQLAlchemy

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
        secondary=tasks,
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


class Task(db.Model):
    """
    Assignment model
    """
    __tablename__ = "tasks"