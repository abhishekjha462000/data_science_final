from flask import Flask, render_template, request
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
        return {"name": name, "email": email, "password": password}
    
    return "<h1>You already have an account</h1>"


    


app.run(debug = True)