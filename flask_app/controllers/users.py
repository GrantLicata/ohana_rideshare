from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models import ride
from flask_bcrypt import Bcrypt
from pprint import pprint
bcrypt = Bcrypt(app)

# ||| Applicaiton Root ||| -> Most likely to be login & registration
@app.route("/")
def index():
    return render_template("login.html")

# ||| Application Entry Point ||| -> Home page following authentication
@app.route('/dashboard')
def profile():
    if session == {}:
        return redirect('/')
    ride_instance = ride.Ride.get_all_rides_driver_and_rider()
    request_instance = ride.Ride.get_all_rides_and_rider()
    return render_template("dashboard.html", all_rides = ride_instance, all_requests = request_instance)

#||| Basic Registration ||| -> Generating a new user and giving them access to the application
@app.route('/register', methods=["POST"])
def register():
    print("---> Form data:", request.form)
    if not User.validate_user(request.form): 
        return redirect('/')
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.save(data)
    return redirect("/dashboard")

# ||| Basic Login ||| -> Accepts and validates both the users email and password
@app.route('/login', methods=['POST'])
def login():
    print("---> Form data:", request.form)
    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")

# ||| Basic Logout ||| -> Session data is cleared
@app.route('/logout')
def clear_session():
    session.clear()
    print("||-- Session should be clear --|| <> Session is:", session)
    return render_template("login.html")

# Ride request form page
@app.route('/rides/new')
def new_ride_form():
    return render_template("request_ride.html")

# Ride request form page
@app.route('/rides/edit/<int:id>')
def edit_ride_form(id):
    return render_template("update_ride.html", ride_object = ride.Ride.get_all_ride(id))

# Ride request form page
@app.route('/rides/detail/<int:id>')
def ride_details(id):
    data = {
        "id": id
    }
    return render_template("details.html", ride_object = ride.Ride.get_all_ride(data))

# Ride request submit
@app.route('/ride/create', methods=["POST"])
def create():
    print("---> Form data:", request.form)
    data = {
        "destination": request.form["destination"],
        "pick_up_location" : request.form["pick_up_location"],
        "date": request.form["date"],
        "details": request.form["details"],
        "user2_id": session["user_id"]
    }
    ride.Ride.save_ride(data)
    return redirect('/dashboard')

# Ride request submit
@app.route('/ride/edit', methods=["POST"])
def update():
    print("---> Form data:", request.form)
    data = {
        "pick_up_location" : request.form["pick_up_location"],
        "details": request.form["details"],
        "ride_id": request.form["ride_id"]
    }
    ride.Ride.update_ride(data)
    return redirect('/dashboard')

# Ride request submit
@app.route('/ride/delete', methods=["POST"])
def delete_ride():
    print("---> Form data:", request.form)
    data = {
        "id" : request.form["ride_id"]
    }
    ride.Ride.delete(data)
    return redirect('/dashboard')

# Ride request submit
@app.route('/ride/assign', methods=["POST"])
def assign_driver():
    print("---> Form data:", request.form)
    data = {
        "driver_id": request.form["driver_id"],
        "ride_id": request.form["ride_id"]
    }
    ride.Ride.assign_driver(data)
    return redirect('/dashboard')

