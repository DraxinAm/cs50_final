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
db = Database("database/recipes.db")

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
    cards = db.list_recipe(session["user_id"])
    return render_template("index.html", cards=cards, card_number=len(cards))

# https://flask.palletsprojects.com/en/stable/quickstart/ (I borrowed the variable rules modul from this link)
@app.route('/recipe/<int:recipe_id>')
def show_post(recipe_id):
    # Show the recipe with the given id, the id is an integer
    info, tags, ingredients, steps = db.return_recipe_info(recipe_id)
    return render_template("recipe.html", info=info, tags=tags, ingredients=ingredients, steps=steps)

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
        # Handle recipe title, desc logic here
        recipe_title = request.form.get("recipe_title")
        if not recipe_title:
            return problem("Must add title")
        description = request.form.get("recipe_description")
        if not description:
            return problem("Must add description")
        # Handle cooktime and servings
        cooktime = request.form.get("time")
        if not cooktime or int(cooktime) < 0:
            return problem("Must give integer minutes")
        servings = request.form.get("servings")
        if not servings or int(servings) < 0:
            return problem("Must give whole and positive servings")
        # Insert into table
        db.insert_recipes(session["user_id"], recipe_title, description, cooktime, servings)
        # Handle tags
        tags = []
        for i in range(3):
            if request.form.get(f"tags{i}"):
                tags.append(request.form.get(f"tags{i}"))
        # Insert into table
        db.insert_tags(recipe_title, tags)
        # Handle ingredients
        ingredients = []
        for i in range(15):
            amount = request.form.get(f"amount{i}")
            unit = request.form.get(f"unit{i}")
            name = request.form.get(f"name{i}")
            if name and amount and unit:
                ingredient = {
                    "amount" : amount,
                    "unit" : unit,
                    "name" : name
                }
                ingredients.append(ingredient)
        # Insert into table
        db.insert_ingredients(recipe_title, ingredients)
        # Handle the steps
        steps = []
        for i in range(10):
            step = request.form.get(f"step{i}")
            if step:
                steps.append(step)
        # Insert into table
        db.insert_steps(recipe_title, steps)
        return redirect("/")
    else:
        return render_template("create.html")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search for recipes"""
    if request.method == "POST":
        # Handle search logic here
        search = request.form.get("search")
        diet = request.form.get("diet")
        print(search)
        print(diet)
        if request.form.get("search"):
            # Select from table and return that
            recipe_title = request.form.get("search")
            cards = db.search(recipe_title)
            # Search for recipe_title, desc, time, servings, tags, ingredients, steps
            return render_template("index.html", cards=cards, card_number=len(cards))
        if request.form.get("diet"):
            # Select from table and return that
            return redirect("/list")
        if search and diet:
            return problem("Sorry, you can only choose one")
    else:
        return render_template("search.html")

@app.route("/list", methods=["GET", "POST"])
@login_required
def list():
    """List the cards for the found recipes"""
    cards = db.list_recipe(session["user_id"])
    return render_template("index.html", cards=cards, card_number=len(cards))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""
    if request.method == "POST":
        # Handle registration logic here
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return problem("Sorry, password and confirmation must match")
        if not username:
            return problem("Sorry, must give username")
        if not password:
            return problem("Sorry, must give password")
        if not confirmation:
            return problem("Sorry, must give confirmation for password")
        password = generate_password_hash(password)
        try:
            db.insert_username_and_password(username, password)
        except ValueError:
            return problem("Sorry that username is taken")
        return render_template("login.html")
    else:
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
        user = db.get_user_by_username(request.form.get("username"))
        password = request.form.get("password")
        hash = str(user["hash"])
        if not check_password_hash(hash, password):
            return problem("Sorry, wrong password")
        session["user_id"] = user["id"]
        return redirect("/")
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