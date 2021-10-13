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
    # set the current url for the session
    session['url'] = url_for('profile')
    # get the session user from the db
    user = mongo.db.users.find_one({'username': session['user']})
    # get the session users reviews from the db
    user_reviews = list(mongo.db.reviews.find({'username': session['user']}))
    # get the users traveller type based on preffered holiday type
    holiday_type = mongo.db.holiday_type.find_one(
        {'holiday_type': user['holiday_type']})

    return render_template("profile.html", user=user, reviews=user_reviews, traveller_type=holiday_type['traveller_type'])


@app.route("/read_review/<review_id>")
def read_review(review_id):
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    return render_template("read_review.html", review=review, prev_url=session['url'])


@app.route("/write_review", methods=["GET", "POST"])
def write_review():
    if request.method == "POST":
        submit = {
            "username": session["user"],
            "country": request.form.get("country"),
            "location": request.form.get("location"),
            "holiday_type": request.form.get("holiday_type"),
            "holiday_pros": request.form.getlist("holiday_pros"),
            "holiday_cons": request.form.getlist("holiday_cons"),
            "rating": int(request.form.get("rating")),
            "comment": request.form.get("comment"),
            "cost": int(request.form.get("cost")),
            "time_visited": request.form.get("time_visited"),
            "date_reviewed": request.form.get("date_reviewed")
        }
        mongo.db.reviews.insert_one(submit)
        flash('Review Submitted!', category='success')

    curr_date = date.today().strftime("%d %b %Y")
    holiday_type = mongo.db.holiday_type.find()
    pros = list(mongo.db.pros.find())
    cons = list(mongo.db.cons.find())
    return render_template("write_review.html", holiday_type=holiday_type, cons=cons, pros=pros, curr_date=curr_date)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
