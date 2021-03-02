from flask import Flask, flash, jsonify, redirect, render_template, request, jsonify, make_response, session, flash
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from help import login_required, global_case, local_case
from config.py import App_Secret_Key

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = App_Secret_Key

db = SQL("sqlite:///data.db")

posted = 0

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = session["user_id"]
    global posted
    if request.method == "POST":
        req = request.get_json()
        global country
        country = req["country"]
        global state
        state = req["state"]
        posted = 1
        res = make_response("request recieved", 200)
        return res

    else:
        health = db.execute("SELECT health FROM users WHERE id = :id", id=user)
        health = health[0]["health"]
        test = db.execute("SELECT COVID FROM users WHERE id = :id", id=user)
        test = test[0]["COVID"]
        status = None
        if test == 0:
            status = ["Not Tested", 0]

        elif test == 1:
            status = ["Testing in Progress", 1]

        elif test == 2:
            status = ["Tested NEGATIVE for COVID-19", 2]

        elif test == 3:
            status = ["Tested POSITIVE for COVID-19", 3]

        if posted != 0:
            global_cases = global_case()[0]
            global_deaths = global_case()[1]
            global_recovered = global_case()[2]
            countries = local_case(state, country)
            c_rank = countries[0]["c_rank"]
            c_total = countries[0]["c_total"]
            c_deaths = countries[0]["c_deaths"]
            c_recovered = countries[0]["c_recovered"]
            state_data = countries[1]
            if state_data == 'No Local Data Recovered':
                if health == 1:
                    return render_template("index.html", global_cases=global_cases, global_deaths=global_deaths, global_recovered=global_recovered, country=country, state=state, c_rank=c_rank, c_total=c_total, c_deaths=c_deaths, c_recovered=c_recovered, state_data=state_data, status=status, health=health)
                else:
                    return render_template("index.html", global_cases=global_cases, global_deaths=global_deaths, global_recovered=global_recovered, country=country, state=state, c_rank=c_rank, c_total=c_total, c_deaths=c_deaths, c_recovered=c_recovered, state_data=state_data, status=status)
            else:
                s_rank = countries[1]["s_rank"]
                s_total = countries[1]["s_total"]
                s_deaths = countries[1]["s_deaths"]
                s_recovered = countries[1]["s_recovered"]
                if health == 1:
                    return render_template("index.html", global_cases=global_cases, global_deaths=global_deaths, global_recovered=global_recovered, country=country, state=state, c_rank=c_rank, c_total=c_total, c_deaths=c_deaths, c_recovered=c_recovered, s_rank=s_rank, s_total=s_total, s_deaths=s_deaths, s_recovered=s_recovered, status=status, health=health)
                else:
                    return render_template("index.html", global_cases=global_cases, global_deaths=global_deaths, global_recovered=global_recovered, country=country, state=state, c_rank=c_rank, c_total=c_total, c_deaths=c_deaths, c_recovered=c_recovered, s_rank=s_rank, s_total=s_total, s_deaths=s_deaths, s_recovered=s_recovered, status=status)

        else:
            global_cases = global_case()[0]
            global_deaths = global_case()[1]
            global_recovered = global_case()[2]
            state = None
            return render_template("index.html", global_cases=global_cases, global_deaths=global_deaths, global_recovered=global_recovered, state=state, status=status, health=health)

#register patient, Health providers must contact me to register for safety
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    #if request method is get return the html form
    if request.method == 'GET':
        return render_template('register.html')

    # If request method is post store html form data and check if data is valid. Most of datavalidation is done through html
    else:
        healthcare_provider = request.form.get("health")

        if healthcare_provider:
            message = 'Healthcare Providers must contact "anthony44@rogers.com" to create an account'
            return render_template("error.html", message=message)

        else:
            healthcare_provider = False

        first_name = request.form.get("First Name")
        surname = request.form.get("Surname")
        email = request.form.get("Email")
        password = request.form.get("Password")
        password_confirmed = request.form.get("Confirm Password")

        # Convert first and last name to uppercase before storing in database
        first_name = first_name.upper()
        surname = surname.upper()

        # Check if passwords match
        if password != password_confirmed:
            message = "Passwords do not match"
            return render_template("error.html", message=message)

        else:
            hashed_password = generate_password_hash(password)
            x = db.execute("SELECT email FROM users WHERE email = :email", email=email)
            if x:
                message = "User with same email already exists"
                return render_template("error.html", message=message)
            else:
                db.execute("INSERT INTO users (firstname, surname, email, password, health) VALUES (:firstname, :surname, :email, :password, :health)", firstname=first_name, surname=surname, email=email, password=hashed_password, health=healthcare_provider)

            return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    else:
        healthcare_provider = bool(request.form.get("health"))
        email = request.form.get("Email")
        password = request.form.get("Password")

        x = db.execute("SELECT * FROM users WHERE email = :email", email=email)

        if len(x) != 1:
            message = "No user found!"
            return render_template("error.html", message=message)

        elif not check_password_hash(x[0]["password"], password):
            message = "Incorrect Password"
            return render_template("error.html", message=message)

        elif healthcare_provider != bool(x[0]["health"]):
            if healthcare_provider == 1:
                message = "Can not find Healthcare Provider with associated email"
                return render_template("error.html", message=message)

            else:
                message = "Can not find patient with associated email"
                return render_template("error.html", message=message)

        else:
            session["user_id"] = x[0]["id"]
            return redirect("/")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "GET":
        user = session["user_id"]
        data = db.execute("SELECT * FROM users WHERE id = :id", id=user)
        first_name = data[0]["firstname"]
        surname = data[0]["surname"]
        email = data[0]["email"]
        health = data[0]["health"]
        health_care = None

        if health == 0:
            health_care = "Patient"

        else:
            health_care = "Healthcare Worker"

        return render_template("settings.html", first_name=first_name, surname=surname, email=email, health_care=health_care, health=health)

    else:
        user = session["user_id"]
        data = db.execute("SELECT * FROM users WHERE id = :id", id=user)
        email_list = db.execute("SELECT email FROM users")
        previous_email = email = data[0]["email"]
        email = request.form.get("Email")
        email_confirmed = request.form.get("Email Confirm")

        if email != email_confirmed:
            message = "Email's do not match"
            return render_template("error.html", message=message)

        elif email == previous_email:
            message = "Can't change email to the same email as previous"
            return render_template("error.html", message=message)

        else:
            for x in range(len(email_list)):
                mail = email_list[x]["email"]
                if email == mail:
                    message = "The email adress "'"' + email + '"'" is already in use by another account"
                    return render_template("error.html", message=message)
            db.execute("UPDATE users SET email = :email WHERE id = :id;", email=email, id=user)

        return redirect("/")

@app.route("/forgot", methods=["GET", "POST"])
@login_required
def forgot():
    if request.method == "GET":
        user = session["user_id"]
        data = db.execute("SELECT health FROM users WHERE id = :id", id=user)
        health = data[0]["health"]
        return render_template("forgot.html", health=health)

    else:
        user = session["user_id"]
        data = db.execute("SELECT * FROM users WHERE id = :id", id=user)
        health = data[0]["health"]
        password = request.form.get("Password")
        previous_password = data[0]["password"]
        password_confirmed = request.form.get("Confirm Password")
        password = generate_password_hash(password)
        if not check_password_hash(password, password_confirmed):
            message = "Passwords do not match"
            return render_template("error.html", message=message, health=health)
        elif password == previous_password:
            message = "Can't change password to the same password as previous"
            return render_template("error.html", message=message, health=health)
        else:
            db.execute("UPDATE users SET password = :password WHERE id = :id;", password=password, id=user)
        return redirect("/")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")

@app.route("/patients")
@login_required
def patients():
    user = session["user_id"]
    health = db.execute("SELECT health FROM users WHERE id = :id", id=user)
    health = health[0]["health"]
    data = db.execute("SELECT id, firstname, surname, email, health, COVID FROM users")
    return render_template("patients.html", data=data, health=health)

@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "GET":
        user = session["user_id"]
        health = db.execute("SELECT health FROM users WHERE id = :id", id=user)
        health = health[0]["health"]
        return render_template("update.html", health=health)

    else:
        user = session["user_id"]
        health = db.execute("SELECT health FROM users WHERE id = :id", id=user)
        health = health[0]["health"]
        firstname = request.form.get("Firstname")
        surname = request.form.get("Surname")
        update = request.form.get("update")
        updated_id = request.form.get("updated_id")
        updated_status = request.form.get("updated_status")
        if firstname != None and surname != None:
            firstname = firstname.upper()
            surname = surname.upper()
            names = db.execute("SELECT firstname, surname, email, id, COVID FROM users WHERE firstname = :firstname AND surname = :surname AND health = :health;", firstname=firstname, surname=surname, health=0)
            if len(names) == 1:
                db.execute("UPDATE users SET COVID = :COVID WHERE firstname = :firstname AND surname = :surname AND health = :health;", COVID=update, firstname=firstname, surname=surname, health=0)
                return redirect("/patients")
            elif len(names) == 0:
                message = "No user with that name!"
                return render_template("error.html", message=message)

            else:
                return render_template("updated.html", names=names, health=health)
        elif updated_id != None and updated_status != None:
            db.execute("UPDATE users SET COVID = :COVID WHERE id = :id AND health = :health;", COVID=updated_status, id=updated_id, health=0)
            return redirect("/patients")
        return redirect("/patients")


# ERROR handlers
@app.errorhandler(404)
def not_found(e):
    message = e
    return render_template("error.html", message=message)

@app.errorhandler(500)
def server_error(e):
    message = e
    return render_template("error.html", message=message)

@app.errorhandler(403)
def forbidden(e):
    message = e
    return render_template("error.html", message=message)

@app.errorhandler(405)
def not_allowed(e):
    message = e
    return render_template("error.html", message=message)

@app.errorhandler(408)
def request_timeout(e):
    message = e
    return render_template("error.html", message=message)

@app.errorhandler(502)
def bad_gateway(e):
    message = e
    return render_template("error.html", message=message)

@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)