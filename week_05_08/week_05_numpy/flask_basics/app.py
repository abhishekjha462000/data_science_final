from flask import Flask, render_template, request, redirect
from db import Database

app = Flask(__name__)
dbo = Database()

@app.route("/")
def home():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route("/perform_registration", methods = ["post"])
def perform_registration():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Try to enter the data into the database
    response = dbo.insert(name, email, password)

    if response:
        # This means that the registration was successfull and hence we must go to the login page
        return render_template("login.html", message = "Registration is successfull, you may now proceed to login")
    else:
        # This means that the email was already present in the database and there is no need for registration
        return render_template("register.html", message = "Email already exits. Go to login page")

@app.route("/perform_login", methods = ["post"])
def perform_login():
    email = request.form.get("email")
    password = request.form.get("password")

    response = dbo.search(email, password)

    if response:
        # It means that we found the user in the database
        # we must now show the user profile
        name = dbo.find_user_name(email, password) # we will find a valid name as user is authenticated
        return render_template("profile.html", name = name)
        
    else:
        # It means that we could not find the user in the database
        # we cannot return the user profile
        return render_template("login.html", message = "Email or password is wrong...")

app.run(debug = True)