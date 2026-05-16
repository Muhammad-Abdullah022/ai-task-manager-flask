from flask import Flask, render_template, request, redirect, url_for
from database import init_db
from models import (
    add_task,
    get_all_tasks,
    mark_task_complete,
    delete_task,
    filter_tasks_by_priority
)

app = Flask(__name__)
init_db()


@app.route("/", methods=["GET"])
def home():
    priority_filter = request.args.get("priority")

    if priority_filter:
        tasks = filter_tasks_by_priority(priority_filter)
    else:
        tasks = get_all_tasks()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    priority = request.form.get("priority")
    deadline = request.form.get("deadline")

    try:
        add_task(title, priority, deadline)
    except ValueError:
        return redirect(url_for("home"))

    return redirect(url_for("home"))


@app.route("/complete/<int:task_id>")
def complete(task_id):
    mark_task_complete(task_id)
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)