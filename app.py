from db import db
from flask import Flask
from flask import request
import json
from db import Task, User
from datetime import datetime, timedelta

app = Flask(__name__)
db_filename = "game.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

#craetes dattabase
db.init_app(app)
with app.app_context():
    db.create_all() #createts aall the tables we will defien in db.py

def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

@app.route("/tasks/<int:task_id>")
def completed_task(task_id):
    """
    chanegs task completed status and awards points appropriately 
    """
    user=User.query.all().first()
    task=Task.query.filter_buy(id=task_id).first()
    if task is None:
        return failure_response("task not found!")
    datetime_completed=datetime.now()
    datetime_started=task.date_started
    interval_end=datetime_started+task.duration
    if datetime_completed.date()==datetime_started.date():
        user.points=user.points+1
        if datetime_completed.time()>= datetime_started.time() and datetime_completed.time()<=interval_end:
            user.streak=user.streak+1
        else:
            user.streak=0
    return success_response(task.serialize())



#add a task, be sure to 





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)