from flask import Blueprint, render_template, session, redirect, url_for, request, current_app
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    mongo = current_app.mongo  # Access MongoDB instance from Flask app
    user_data = mongo.db.users.find_one({"email": session["user"]})
    projects = list(mongo.db.projects.find({}))  # Fetch all projects

    return render_template("dashboard.html", user=user_data, projects=projects)

@dashboard_bp.route("/update_task", methods=["POST"])
def update_task():
    if "user" not in session:
        return redirect(url_for("login"))

    mongo = current_app.mongo
    task_id = request.form["task_id"]
    new_status = request.form["status"]

    mongo.db.tasks.update_one({"_id": task_id}, {"$set": {"status": new_status, "updated_at": datetime.now()}})
    
    return redirect(url_for("dashboard.dashboard"))  # Use blueprint name
