import os
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from operator import itemgetter


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
    session.clear()
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


@app.route("/logout")
def logout():
    session.clear()
    flash("Logout Succesful")
    return redirect(url_for('login'))


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
    session.pop('_flashes', None)
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


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    session.pop('_flashes', None)
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
        mongo.db.reviews.update({"_id": ObjectId(review_id)}, submit)
        flash('Review Updated!', category='success')

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    seasons = ["spring", "summer", "autumn", "winter"]
    holiday_type = mongo.db.holiday_type.find()
    pros = list(mongo.db.pros.find())
    cons = list(mongo.db.cons.find())
    return render_template("edit_review.html", review=review, seasons=seasons, holiday_type=holiday_type, cons=cons, pros=pros, prev_url=session['url'])


@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.delete_one({"_id": ObjectId(review_id)})
    flash("Review Successfully Deleted!", category="success")
    return redirect(url_for('profile'))


@app.route("/charts")
def charts():
    # extract reviews from database
    reviews = list(mongo.db.reviews.find())

    # extract all countries reviewed
    countries = extract_all_reviewed_countries(reviews)

    # extract all locations reviewed
    locations = extract_all_reviewed_locations(reviews)

    # calculate best rated countries
    avg_ratings = avg_ratings_per_country(countries, reviews)
    avg_ratings = sorted(avg_ratings, key=itemgetter(
        'avg_rating'), reverse=True)

    # calculate best locations for food
    avg_ratings_food = avg_ratings_per_location_with_food(locations, reviews)
    avg_ratings_food = sorted(avg_ratings_food, key=itemgetter(
        'avg_rating'), reverse=True)

    # calculate the cheapest locations
    avg_costs = avg_cost_rating_per_location(locations, reviews)
    avg_costs = sorted(avg_costs, key=itemgetter(
        'avg_cost'))

    # trim the data (max 10 items should be sent to front end)

    return render_template("charts.html", avg_ratings=avg_ratings, avg_ratings_food=avg_ratings_food, avg_costs=avg_costs)


@app.route("/reviews/<data>")
def reviews(data):
    # extract reviews from database
    reviews = list(mongo.db.reviews.find())

    # extract all countries reviewed
    countries = extract_all_reviewed_countries(reviews)

    # extract all locations reviewed
    locations = extract_all_reviewed_locations(reviews)

    if data in countries:
        specific_reviews = list(
            mongo.db.reviews.find({'country': data.lower()}))

    else:
        specific_reviews = mongo.db.reviews.find({'location': data.lower()})

    return render_template('reviews.html', data=data, reviews=specific_reviews)


def extract_all_reviewed_locations(reviews):
    locations = []
    for review in reviews:
        review_location = review['location'].lower()
        if review_location not in locations:
            locations.append(review_location)
    # print(locations)
    return locations


def extract_all_reviewed_countries(reviews):
    countries = []
    for review in reviews:
        review_country = review['country'].lower()
        if review_country not in countries:
            countries.append(review_country)
    return countries


def avg_cost_rating_per_location(locations, reviews):

    # init dict for storing avg_ratings per country
    avg_ratings = []

    # start loop to cycle through every possible location that has been reviewed
    for location in locations:
        location_rating = {}
        location_count = 0
        costs = []

        # find all reviews which have the location being checked and also have food as a pro
        for review in reviews:
            if review['location'].lower() == location:
                costs.append(review['cost'])
                location_count += 1

        # if there were some cases found add them to the return value
        if costs:
            location_rating['location'] = location
            location_rating['avg_cost'] = round(sum(costs)/len(costs))
            location_rating['total_reviews'] = location_count
            avg_ratings.append(location_rating)

    return avg_ratings


def avg_ratings_per_location_with_food(locations, reviews):

    # init dict for storing avg_ratings per country
    avg_ratings = []

    # start loop to cycle through every possible location that has been reviewed
    for location in locations:
        location_rating = {}
        location_count = 0
        ratings = []

        # find all reviews which have the location being checked and also have food as a pro
        for review in reviews:
            if review['location'].lower() == location and "food" in review["holiday_pros"]:
                ratings.append(review['rating'])
                location_count += 1

        # if there were some cases found add them to the return value
        if ratings:
            location_rating['location'] = location
            location_rating['avg_rating'] = sum(ratings)/len(ratings)
            location_rating['total_reviews'] = location_count
            avg_ratings.append(location_rating)

    return avg_ratings


def avg_ratings_per_country(countries, reviews):
    # init dict for storing avg_ratings per country
    avg_ratings = []

    for country in countries:
        country_rating = {}
        country_count = 0
        # init a list for storing reviews for country
        ratings = []
        for review in reviews:
            review_country = review['country'].lower()
            if review_country == country:
                ratings.append(review['rating'])
                country_count += 1
        # add results to dictionary of data
        country_rating['country'] = country
        country_rating['avg_rating'] = sum(ratings)/len(ratings)
        country_rating['total_reviews'] = country_count
        # add dict to list of dicts
        avg_ratings.append(country_rating)

    return avg_ratings


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
