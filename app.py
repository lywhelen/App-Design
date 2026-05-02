from flask import Flask, request
from datetime import timedelta, datetime
from db import db, User, Task
import json

app = Flask(__name__)
db_filename = "game.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False  # set to True to log SQL queries while debugging

db.init_app(app)
with app.app_context():
    db.create_all()


# ── Response helpers ───────────────────────────────────────────────────────────

def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


# ── Users ──────────────────────────────────────────────────────────────────────

@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Create a new user. Currently using name and email.
    """
    body = json.loads(request.data)
    name = body.get("name")
    email = body.get("email")

    if not name or not email:
        return failure_response("name and email are required", 400)

    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return success_response(user.serialize(), 201)


@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    Get a user by ID, including their tasks.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found")
    return success_response(user.serialize())


@app.route("/api/user/", methods=["GET"])
def get_current_user():
    """
    Single-user convenience endpoint — returns the one user in the database.
    The frontend calls this on launch instead of tracking a user ID.
    If no user exists yet, returns 404 so the frontend knows to show setup.
    """
    user = User.query.first()
    if user is None:
        return failure_response("no user found — create one first")
    return success_response(user.serialize())


# ── Tasks ──────────────────────────────────────────────────────────────────────

@app.route("/api/users/<int:user_id>/tasks/", methods=["POST"])
def create_task(user_id):
    """
    Create a task for a user.
    Body: { "title": str, "description": str (opt),
            "priority": int 1-5 (opt), "duration_minutes": int (opt, default 30) }
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found")

    body = json.loads(request.data)
    title = body.get("title")
    if not title:
        return failure_response("title is required", 400)

    duration_minutes = body.get("duration_minutes", 30)

    task = Task(
        title=title,
        description=body.get("description", ""),
        priority=body.get("priority", 1),
        duration=timedelta(minutes=duration_minutes),
        user_id=user_id,
    )
    db.session.add(task)
    db.session.commit()
    return success_response(task.serialize(), 201)


@app.route("/api/users/<int:user_id>/tasks/", methods=["GET"])
def get_tasks(user_id):
    """
    Get all tasks for a user.
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("user not found")
    return success_response([task.serialize() for task in user.tasks])



@app.route("/api/tasks/<int:task_id>/complete/", methods=["PUT"])
def completed_task(task_id):
    """
    changes task completed status and awards points appropriately 
    """
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("task not found")

    if task.completed:
        return failure_response("task is already completed", 400)

    user = User.query.filter_by(id=task.user_id).first()
    if user is None:
        return failure_response("user not found")

    user.complete_task(task)
    user.update_streak()

    db.session.commit()
    return success_response(task.serialize())


@app.route("/api/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    """
    Delete a task by ID.
    """
    task = Task.query.filter_by(id=task_id).first()
    if task is None:
        return failure_response("task not found")
    db.session.delete(task)
    db.session.commit()
    return success_response(task.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
