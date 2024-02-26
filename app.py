from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, get_coordinates

from geopy.distance import geodesic

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of flight distance"""
    user_id = session["user_id"]
    update_dist = db.execute("SELECT flight_dist FROM users WHERE id = ?", user_id)
    departures = db.execute("SELECT departure FROM flights WHERE user_id = ?", user_id)
    number = len(departures)
    return render_template("index.html", update_dist = update_dist[0]["flight_dist"], number = number)

@app.route("/record", methods=["GET", "POST"])
@login_required
def record():
    """add a journey"""
    if request.method=="GET":
        return render_template("record.html")
    else:
        city1 = request.form['city1']
        city2 = request.form['city2']
        date = request.form['date']
        if not city1.isalpha() or not city2.isalpha():
            return apology("Please enter valid text for cities")

        coordinates1 = get_coordinates(city1)
        coordinates2 = get_coordinates(city2)
        if not coordinates1 or not coordinates2:
            return apology("please give a name of a city")

        distance = geodesic(coordinates1, coordinates2).kilometers
        if distance == None:
            return apology("sorry, we didn't find it")

        user_id = session["user_id"]

        #user_dist 是一个列表，其中包含一个字典作为其唯一的元素 （db.execute 通常是一个表示查询结果的列表)
        user_dist = db.execute("SELECT flight_dist FROM users WHERE id = ?", user_id)
        #这个字典有一个键 "flight_dist" 赋值给money
        user_dist = user_dist[0]["flight_dist"]
        if user_dist is None:
            user_dist = 0.0

        if distance is None:
            return apology("sorry, we didn't find it")

        update_dist = float(user_dist) + float(distance)
        db.execute("UPDATE users SET flight_dist = ? WHERE id = ?", update_dist, user_id)
        db.execute("INSERT INTO flights (user_id, departure, destination, distance, date) VALUES(?,?,?,?,?)", user_id, city1, city2, distance, date)

        flash("succeed!")
        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of your journey"""
    user_id = session["user_id"]
    flight_db = db.execute("SELECT * FROM flights WHERE user_id = ?", user_id)
    update_dist = db.execute("SELECT flight_dist FROM users WHERE id = ?", user_id)
    return render_template("history.html", flights = flight_db, update_dist = update_dist[0]["flight_dist"])

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/distance", methods=["GET", "POST"])
@login_required
def distance():
    if request.method == "GET":
        return render_template("distance.html")

    else:
        city1 = request.form['city1']
        city2 = request.form['city2']

        coordinates1 = get_coordinates(city1)
        coordinates2 = get_coordinates(city2)
        if not coordinates1 or not coordinates2:
            return apology("please give a name of a city")

        distance = geodesic(coordinates1, coordinates2).kilometers
        if distance == None:
            return apology("sorry, we didn't find it")
        return render_template("distance2.html",city1 = city1, city2 = city2, distance = distance)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET": # display registration form
        return render_template("regis_form.html")
    else:  # insert the new user into users table then log user in
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        #check for possible errors
        if not username:
            return apology("please give a username")
        if not password:
            return apology("please give a password")
        if not confirmation:
            return apology("please confirm password")
        if password != confirmation:
            return apology("password do not match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hash)

        except:
            return apology("username already existed")

        session["user_id"] = new_user

        return redirect("/")

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    """remove a journey"""
    if request.method=="GET":
        user_id = session["user_id"]
        departures = db.execute("SELECT departure FROM flights WHERE user_id = ?", user_id)
        return render_template("remove.html", departures = [row["departure"] for row in departures])
    else:
        city1 = request.form['departure']
        city2 = request.form['destination']
        date = request.form['date']

        coordinates1 = get_coordinates(city1)
        coordinates2 = get_coordinates(city2)

        distance = geodesic(coordinates1, coordinates2).kilometers
        if distance == None:
            return apology("sorry, we didn't find it")

        user_id = session["user_id"]

        #user_dist 是一个列表，其中包含一个字典作为其唯一的元素 （db.execute 通常是一个表示查询结果的列表)
        user_dist = db.execute("SELECT flight_dist FROM users WHERE id = ?", user_id)
        #这个字典有一个键 "flight_dist" 赋值给money
        user_dist = user_dist[0]["flight_dist"]
        if user_dist is None:
            user_dist = 0.0

        if distance is None:
            return apology("sorry, we didn't find it")

        update_dist = float(user_dist) - float(distance)
        db.execute("UPDATE users SET flight_dist = ? WHERE id = ?", update_dist, user_id)
        db.execute("DELETE FROM flights WHERE user_id = ? AND departure = ? AND destination = ? AND distance = ? AND date = ?", user_id, city1, city2, distance, date)

        flash("Removed")
        return redirect("/")

@app.route("/get_destinations_dates", methods=["POST"])
def get_destinations_dates():
    data = request.get_json()
    departure = data['departure']

    # 查询数据库获取目的地和日期
    destinations = db.execute("SELECT destination FROM flights WHERE departure= ?", departure)
    dates = db.execute("SELECT date FROM flights WHERE departure = ?", departure)

    # 返回一个包含目的地和日期的JSON对象
    return jsonify({
        'destinations': [dict(destination = row['destination']) for row in destinations],
        'dates': [dict(date=row['date']) for row in dates]
    })

@app.route("/map")
@login_required
def map_view():
    """Show map page."""

    return render_template("map.html")


@app.route("/get_journey_coordinates")
@login_required
def get_journey_coordinates():
    """Fetch coordinates for the user's journeys."""
    user_id = session["user_id"]
    # Get unique cities from destinations and departures.
    destinations = db.execute("SELECT DISTINCT destination FROM flights WHERE user_id = ?", (user_id,))
    departures = db.execute("SELECT DISTINCT departure FROM flights WHERE user_id = ?", (user_id,))
    cities = {city['destination'] for city in destinations} | {city['departure'] for city in departures}

    # Get coordinates for each city.
    coordinates = []
    for city in cities:
        coords = get_coordinates(city)  # Ensure this function is defined and working.
        if coords:
            coordinates.append({'city': city, 'lat': coords[0], 'lon': coords[1]})

    return jsonify(coordinates)
