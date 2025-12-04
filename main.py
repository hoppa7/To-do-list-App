from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]=(f'postgresql://'
                                       f'{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}'
                                       f'@localhost:{os.getenv("DB_PORT")}/todoapp')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, task):
        self.task = task


@app.route("/")
def index():
    todos = Todo.query.order_by(Todo.id).all()
    return render_template('index.html', todos=todos)

@app.route("/add", methods=['POST'])
def add_task():
    task = request.form.get('task')

    if not task:
        return "Task is required", 400

    new_todo = Todo(task)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete", methods=['POST'])
def delete_task():
    task_id = request.form.get('task_id')

    if not task_id:
        return "Task ID is required", 400

    todo = Todo.query.get(task_id)
    if not todo:
        return "Task not found", 404

    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/check", methods=['POST'])
def check_task():
    task_id = request.form.get('task_id')

    if not task_id:
        return "Task ID is required", 400

    todo = Todo.query.get(task_id)
    if not todo:
        return "Task not found",
    todo.completed = not todo.completed
    db.session.commit()

    return redirect(url_for("index"))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)