from app import app, request, db
from flask import render_template, redirect, url_for, flash, request
import sqlalchemy
from app.database import database
from app.auth.auth import insert_user, check_user_credentials, load_user
from flask_login import login_user, current_user, logout_user
from app.auth.auth_forms import SingupForm, LoginForm
from app.transaction_tracking.transaction_forms import OutcomeForm, IncomeForm
from app.transaction_tracking.transaction_tracking import get_categories
from app.database.database import Users, Groups, Category, Subcategory, UserGroup, Transactions, Goals, Budget
import pandas as pd

from app.routes.forms import AddGoalForm, AddGoalProgress


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

@app.route("/transaction_tracking", methods=["GET", "POST"])
def transaction_tracking():
    if current_user.is_authenticated:
        if request.method == 'POST':
            if 'outcome' in request.form.keys():
                form = OutcomeForm()
                main_cat, sub_cat = get_categories(current_user.user_name, 'outcome')
                form.main_category.choices = main_cat
                form.subcategory.choices = sub_cat
                return render_template("transaction_tracking.html", form=form)
            elif 'income' in request.form.keys():
                form = IncomeForm()
                main_cat = get_categories(current_user.user_name, 'income')
                form.main_category.choices = main_cat
                return render_template("transaction_tracking.html", form=form)
            elif 'add' in request.form.keys():
                if form.validate_on_submit():
                    flash("Transaction saved successfully", 'success')
                    return render_template("transaction_tracking.html")
                else:
                    return render_template("transaction_tracking.html", form=form)
        return render_template("transaction_tracking.html")
    else:
        flash("First create account or log in if you have one!")
        return redirect(url_for("login"))


@app.route("/addgoal", methods=["GET", "POST"])
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


@app.route("/addgoalprogress", methods=["GET", "POST"])
def add_goal_progress():
    if not current_user.is_authenticated:
        flash("You need to log in")
        return redirect(url_for("hello"))
    form = AddGoalProgress()
    goals = db.session.query(Goals.id, Goals.name).all()
    print(goals)
    # Update the choices for the dropdown field
    form.name.choices = [(str(goal.id), goal.name) for goal in goals]

    if form.validate_on_submit():
        goal_transaction = Transactions(
            transaction_date=form.date.data,
            value=form.amount.data,
            goal_id=form.name.data,
            user_id=current_user.id,
            user_note=form.date.data,
        )
        db.session.add(goal_transaction)
        db.session.commit()
        flash(f"Goal Progress has been added", "success")
        return render_template("addgoalprogress.html", form=form)
    return render_template("addgoalprogress.html", form=form)


def insert_goal(name, target_amount, deadline, user_id):
    goal = Goals(name=name, target_amount=target_amount, deadline=deadline, user_id=user_id)
    db.session.add(goal)
    db.session.commit()


@app.route("/showgoals", methods=["GET", "POST"])
def show_goals():
    if not current_user.is_authenticated:
        flash("You need to log in")
        return redirect(url_for("hello"))

    goals = db.session.query(Goals.id, Goals.name, Goals.target_amount, Goals.deadline, Goals.user_id)
    transactions = (
        db.session.query(db.func.sum(Transactions.value), Transactions.goal_id)
        .group_by(Transactions.goal_id)
        .order_by(Transactions.goal_id)
        .all()
    )

    # Convert to Pandas DataFrame
    df_progres = pd.DataFrame(transactions, columns=["current_progres", "id"])
    df_goals = pd.DataFrame(goals)

    new_df = pd.merge(df_goals, df_progres, on="id", how="outer")
    # new_df = new_df[new_df['user_id'] == current_user.id]
    return new_df.to_html()


@app.route("/showtransactions", methods=["GET", "POST"])
def show_transactions():
    if not current_user.is_authenticated:
        flash("You need to log in")
        return redirect(url_for("hello"))
    results = db.session.query(
        Transactions.id,
        Transactions.transaction_date,
        Transactions.value,
        Transactions.category_id,
        Transactions.subcategory_id,
        Transactions.goal_id,
        Transactions.user_id,
        Transactions.user_note,
    )

    # Convert to Pandas DataFrame
    df = pd.DataFrame(results)
    return df.to_html()
