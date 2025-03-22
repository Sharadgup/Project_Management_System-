from flask import render_template, session, redirect, url_for, request
from app import mongo  # Import MongoDB connection
from datetime import datetime

def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    user_data = mongo.db.users.find_one({"email": session["user"]})
    projects = list(mongo.db.projects.find({}))  # Fetch all projects

    return render_template("dashboard.html", user=user_data, projects=projects)

# Update Task Status
def update_task():
    if "user" not in session:
        return redirect(url_for("login"))

    task_id = request.form["task_id"]
    new_status = request.form["status"]

    mongo.db.tasks.update_one({"_id": task_id}, {"$set": {"status": new_status, "updated_at": datetime.now()}})
    
    return redirect(url_for("dashboard"))
