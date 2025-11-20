import os

from flask import Flask, flash, redirect, render_template, request, session
# Bring in the Database class from database module
from database.database import Database
from login import login_required, problem
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
print("Current", os.getcwd())
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = Database("recipes.db")

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
    """Show homepage"""
    return render_template("index.html")

@app.route("/cookbook")
@login_required
def cookbook():
    """Show cookbook page"""
    return render_template("cookbook.html")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new recipe"""
    if request.method == "POST":
        # Handle recipe creation logic here
        pass
    return render_template("create.html")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search for recipes"""
    if request.method == "POST":
        # Handle search logic here
        pass
    return render_template("search.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""
    if request.method == "POST":
        # Handle registration logic here
        pass
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in, using the method seen in cs50x/finance"""
    if request.method == "POST":
        # Log out
        session.clear()
        if not request.form.get("username"):
            return problem("Must provide username, sorry.", 403)
        elif not request.form.get("password"):
            return problem("Must provide password, sorry.", 403)
        # Handle login logic here
        pass
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")

@app.route("/problem")
def problem_route():
    """Example problem route"""
    return problem("This is an example problem message.", 400)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)