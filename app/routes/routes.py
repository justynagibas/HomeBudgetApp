import sqlalchemy

from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.database import database
from app.auth.auth import insert_user, check_user_credentials, load_user
from flask_login import login_user, current_user, logout_user
from app.auth.auth_forms import SingupForm, LoginForm
from app.database.database import *
import pandas as pd

from app.routes.forms import AddGoalForm


@app.route("/")
@app.route("/hello")
def hello():
    if not current_user.is_authenticated:
        return render_template("hello.html")
    else:
        return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        flash("You need to log out before you can create a new account.")
        return redirect(url_for("hello"))
    form = SingupForm()
    if form.validate_on_submit():
        insert_user(form.login.data, form.password.data)
        flash(f"Your account has been created!. You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for("hello"))
    form = LoginForm()
    if form.validate_on_submit():
        user = check_user_credentials(form.login.data, form.password.data)
        if user:
            login_user(user)
            flash(f"Successfully logged in as {current_user.user_name}.")
            return redirect(url_for("hello"))
        else:
            flash("Login failed. Please check username and password.", "danger")
    return render_template("login.html", form=form, user=current_user)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out.")
    else:
        flash("You need to log in before you can log out")
    return redirect(url_for("hello"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

@app.route("/addgoal", methods=['GET', 'POST'])
def goals():
    if not current_user.is_authenticated:
        flash("You need to log in")
        return redirect(url_for("hello"))
    form = AddGoalForm()
    if form.validate_on_submit():
        insert_goal(form.name.data, form.target_amount.data, form.deadline.data, current_user.id)
        flash(f"New Goal has been added", "success")
        return render_template("addgoal.html", form=form)
    return render_template("addgoal.html", form=form)

def insert_goal(name, target_amount, deadline, user_id):
    goal = Goals(name=name, target_amount=target_amount, deadline=deadline, user_id=user_id)
    db.session.add(goal)
    db.session.commit()

@app.route("/showgoals", methods=['GET', 'POST'])
def show_goals():
    if not current_user.is_authenticated:
        flash("You need to log in")
        return redirect(url_for("hello"))
    results = db.session.query(Goals.name, Goals.target_amount,Goals.deadline,Goals.user_id)
    # Convert to Pandas DataFrame
    df = pd.DataFrame(results)
    return df.to_html()