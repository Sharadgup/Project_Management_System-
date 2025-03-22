from flask import Blueprint, render_template, session, redirect, url_for, request, current_app
from datetime import datetime
from bson.objectid import ObjectId
import functools  # ✅ Import functools to use wraps()

dashboard_bp = Blueprint("dashboard", __name__)

# ✅ Fix: Preserve function name using functools.wraps()
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapper

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    mongo = current_app.extensions["pymongo"]
    user_data = mongo.db.users.find_one({"email": session["user"]})
    projects = list(mongo.db.projects.find({}))
    tasks = list(mongo.db.tasks.find({"status": "Active"}))

    return render_template("dashboard.html", user=user_data, projects=projects, tasks=tasks)

@dashboard_bp.route("/projects")
@login_required
def projects():
    mongo = current_app.extensions["pymongo"]
    projects = list(mongo.db.projects.find({}))

    return render_template("projects.html", projects=projects)

@dashboard_bp.route("/tasks")
@login_required
def tasks():
    mongo = current_app.extensions["pymongo"]
    tasks = list(mongo.db.tasks.find({}))

    return render_template("tasks.html", tasks=tasks)

@dashboard_bp.route("/schedule")
@login_required
def schedule():
    return render_template("schedule.html")

@dashboard_bp.route("/reports")
@login_required
def reports():
    return render_template("reports.html")

@dashboard_bp.route("/profile")
@login_required
def profile():
    mongo = current_app.extensions["pymongo"]
    user_data = mongo.db.users.find_one({"email": session["user"]})

    return render_template("profile.html", user=user_data)

@dashboard_bp.route("/update_task", methods=["POST"])
@login_required
def update_task():
    mongo = current_app.extensions["pymongo"]
    task_id = request.form["task_id"]
    new_status = request.form["status"]

    mongo.db.tasks.update_one(
        {"_id": ObjectId(task_id)}, 
        {"$set": {"status": new_status, "updated_at": datetime.now()}}
    )
    
    return redirect(url_for("dashboard.dashboard"))
