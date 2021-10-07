import os
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

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
            flash("Username already exists!", "danger")
            return redirect(url_for("register"))

        # insert in db if not already existing
        new_user = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password").lower()),
            "holiday_type": request.form.get("holiday").lower(),
            "date_registered": date.today().strftime("%d/%m/%Y")
        }
        mongo.db.users.insert_one(new_user)
        # set the current session user
        session["user"] = request.form.get("username").lower()
        # flash indication
        flash('Registration Successful', category='success')
        # redirect to the users profile
        return redirect(url_for('profile'))

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
            flash('Login Successful', category='success')
            return redirect(url_for('profile'))
        else:
            # flash indication
            flash('Login Failed', category='danger')
            return redirect(url_for('login'))

    return render_template("login.html")


@app.route("/profile")
def profile():
    # get the session user from the db
    user = mongo.db.users.find_one({'username': session['user']})
    # get the session users reviews from the db
    user_reviews = list(mongo.db.reviews.find({'username': session['user']}))
    # get the users traveller type based on preffered holiday type
    holiday_type = mongo.db.holiday_type.find_one(
        {'holiday_type': user['holiday_type']})

    return render_template("profile.html", user=user, reviews=user_reviews, traveller_type=holiday_type['traveller_type'])


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
