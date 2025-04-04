from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)

# ✅ MongoDB Configuration
app.config["MONGO_URI"] = "mongodb+srv://shardgupta65:Typer%401345@cluster0.sp87qsr.mongodb.net/employeeDB"
app.secret_key = os.urandom(24)

# ✅ Initialize PyMongo once and register it in Flask extensions
mongo = PyMongo(app)
app.extensions["mongo"] = mongo  # Explicitly store PyMongo

# ✅ Import routes AFTER initializing Mongo
from dashboard_routes import dashboard_bp  

# ✅ Register Blueprint
app.register_blueprint(dashboard_bp)

# ✅ Home (Login) Route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = mongo.db.users.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session["user"] = email
            
            # ✅ Store login time in logs collection
            mongo.db.logs.insert_one({
                "email": email,
                "action": "login",
                "timestamp": datetime.now()
            })
            
            return redirect(url_for("dashboard.dashboard_home"))  
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")

# ✅ Register Route
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

# ✅ Dashboard Route
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        user_data = mongo.db.users.find_one({"email": session["user"]})
        return render_template("dashboard.html", user=user_data)

    return redirect(url_for("login"))

# ✅ Logout Route
@app.route("/logout")
def logout():
    if "user" in session:
        # ✅ Store logout time in logs collection
        mongo.db.logs.insert_one({
            "email": session["user"],
            "action": "logout",
            "timestamp": datetime.now()
        })
        
        session.pop("user", None)
    
    return redirect(url_for("login"))

# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
