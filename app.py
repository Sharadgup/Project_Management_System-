from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://shardgupta65:Typer%401345@cluster0.sp87qsr.mongodb.net/employeeDB"
app.secret_key = os.urandom(24)

mongo = PyMongo(app)

# Route: Home (Login)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = mongo.db.users.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session["user"] = email
            mongo.db.logs.insert_one({"email": email, "login_time": datetime.now()})
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")

# Route: Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        department = request.form["department"]
        role = request.form["role"]
        join_date = request.form["join_date"]

        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))

        mongo.db.users.insert_one({
            "fullname": fullname,
            "phone": phone,
            "email": email,
            "password": password,
            "department": department,
            "role": role,
            "join_date": join_date
        })
        
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Route: Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        user_data = mongo.db.users.find_one({"email": session["user"]})
        return render_template("dashboard.html", user=user_data)

    return redirect(url_for("login"))

# Route: Logout
@app.route("/logout")
def logout():
    if "user" in session:
        mongo.db.logs.insert_one({"email": session["user"], "logout_time": datetime.now()})
        session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
