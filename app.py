import os
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


if os.path.exists('env.py'):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def landing():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    holiday_type = mongo.db.holiday_type.find()
    if request.method == "POST":
        # check if the username is already registered in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # give a message if already exists
        if existing_user:
            return redirect(url_for("register"))
        # insert in db if not already existing
        new_user = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password").lower()),
            "holiday_type": request.form.get("holiday").lower()
        }
        mongo.db.users.insert_one(new_user)
        # set the current session user
        session["user"] = request.form.get("username").lower()
        # flash indication

        # redirect to the users profile
        flash("Registered Successfully!")

    # direct to the profile page and session cookie set up for user
    return render_template("register.html", holiday_type=holiday_type)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if the username is already registered in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # check if the hashed password matches the password on the database
        if check_password_hash(existing_user["password"], request.form.get("password")):
            # set the current sessions user
            session["user"] = request.form.get("username").lower()
            # flash indication
            flash("Login Success")
            return redirect(url_for('login'))
        else:
            # flash indication
            flash("Login Failed")
            return redirect(url_for('login'))

    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
