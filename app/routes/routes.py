import json

from app import app, request, db
from flask import render_template, redirect, url_for, flash, request, jsonify
import sqlalchemy
from app.auth.auth import insert_user, check_user_credentials, load_user
from flask_login import login_user, current_user, logout_user
from app.auth.auth_forms import SingupForm, LoginForm
from app.transaction_tracking.transaction_forms import TransOutcomeForm, TransIncomeForm
from app.transaction_tracking.transaction_tracking import get_transaction_categories, add_transaction, get_transactions
from app.budget_tracking.budget_forms import BudgetIncomeForm, BudgetOutcomeForm
from app.budget_tracking.budget_tracking import get_budget_categories_names, add_budget_entry, get_budget_entries
from app.category.manage_category import (
    add_category,
    add_subcategory,
    remove_category,
    remove_subcategory,
    get_subcategories,
    get_categories,
)
from app.category.category_forms import AddCategoryForm, AddSubcategoryForm, RemoveSubcategoryForm, RemoveCategoryForm
from app.database.database import Users, Groups, Category, Subcategory, UserGroup, Transactions, Goals, Budget
from app.routes.dashboard_queries import (
    get_user_monthly_budget_sums,
    get_user_monthly_transaction_sums,
    get_user_monthly_category_outcomes,
    get_goals_data,
)
import pandas as pd
from datetime import datetime, date
import calendar

from app.routes.forms import AddGoalForm, AddGoalProgress


this_date = datetime.now().strftime("%B, %Y")
this_month = date.today().month  # TODO: make this changeable in nav
this_year = date.today().year  # TODO: make this changeable in nav


@app.route("/")
@app.route("/hello")
def hello():
    if not current_user.is_authenticated:
        return render_template("hello.html")
    else:
        return redirect(url_for("home"))


@app.route("/home")
def home():
    percent_of_month = round((date.today().day / calendar.monthrange(date.today().year, date.today().month)[1]) * 100)

    user_income_plan, user_outcome_plan = get_user_monthly_budget_sums(current_user.get_id(), this_month, this_year)
    user_planned_balance = user_income_plan - user_outcome_plan

    user_income_actual, user_outcome_actual = get_user_monthly_transaction_sums(
        current_user.get_id(), this_month, this_year
    )

    user_actual_balance = user_income_actual - user_outcome_actual

    already_spent_percentage = round(user_outcome_actual / user_income_actual * 100) if user_income_actual != 0 else 0

    user_categories_data = get_user_monthly_category_outcomes(current_user.get_id(), this_month, this_year)

    return render_template(
        "home.html",
        month_progress=percent_of_month,
        this_date=this_date,
        already_spent=already_spent_percentage,
        income_plan=user_income_plan,
        outcome_plan=user_outcome_plan,
        balance_plan=user_planned_balance,
        income_actual=user_income_actual,
        outcome_actual=user_outcome_actual,
        balance_actual=user_actual_balance,
        categories_data=user_categories_data,
    )


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
        results = get_transactions(current_user.id, this_year, this_month)
        # Convert to Pandas DataFrame
        df = pd.DataFrame(results)
        form_outcome = TransOutcomeForm(prefix="outcome")
        out_cat_dict = get_transaction_categories(current_user.id, "outcome")
        form_outcome.main_category.choices += [cat for cat in out_cat_dict.keys()]
        selected_cat = form_outcome.main_category.data if form_outcome.main_category.data else "Food"
        form_outcome.subcategory.choices += [subcat for subcat in out_cat_dict.get(selected_cat, [])]
        form_income = TransIncomeForm(prefix="income")
        subcat_in = get_transaction_categories(current_user.id, "income")
        form_income.subcategory.choices += [cat[0] for cat in subcat_in]
        if request.method == "POST":
            if form_outcome.submit.data:
                if form_outcome.validate():
                    add_transaction(form_outcome, current_user.id, "outcome")
                    flash("Outcome added successfully!", "success")
                    return redirect(url_for("transaction_tracking"))
            elif form_income.submit.data:
                if form_income.validate():
                    add_transaction(form_income, current_user.id, "income")
                    flash("Income added successfully!", "success")
                    return redirect(url_for("transaction_tracking"))
        return render_template(
            "transaction_tracking.html", form_outcome=form_outcome, form_income=form_income, transactions=df
        )

    else:
        flash("First create account or log in if you have one!")
        return redirect(url_for("login"))


@app.route("/budget_tracking", methods=["GET", "POST"])
def budget_tracking():
    if current_user.is_authenticated:
        outcome_cat_names = get_budget_categories_names(current_user.id)
        form_outcome = BudgetOutcomeForm(prefix="outcome")
        form_outcome.main_category.choices += outcome_cat_names

        form_income = BudgetIncomeForm(prefix="income")

        budget_entries = pd.DataFrame(get_budget_entries(current_user.id, this_year, this_month))
        print(budget_entries)

        if request.method == "POST":
            if form_outcome.submit.data:
                if form_outcome.validate():
                    add_budget_entry(form_outcome, current_user.id, "outcome", this_year, this_month)
                    flash("Budget outcome added successfully!", "success")
                    return redirect(url_for("budget_tracking"))
            elif form_income.submit.data:
                if form_income.validate():
                    add_budget_entry(form_income, current_user.id, "income", this_year, this_month)
                    flash("Budget income added successfully!", "success")
                    return redirect(url_for("budget_tracking"))

        return render_template(
            "budget_tracking.html", form_outcome=form_outcome, form_income=form_income, budget_entries=budget_entries
        )

    else:
        flash("First create account or log in if you have one!")
        return redirect(url_for("login"))


@app.route("/get_second_field_options", methods=["POST"])
def get_second_field_options():
    selected_cat = request.form.get("selected_value")

    # Use the selected value to determine the new options for the second field
    # Replace this logic with your own based on your requirements
    out_cat_dict = get_transaction_categories(current_user.id, "outcome")
    subcategory_choices = [subcat for subcat in out_cat_dict.get(selected_cat, [])]

    # Return the new options as JSON
    return jsonify(subcategory_choices)


@app.route("/delete-record", methods=["POST"])
def delete_record():
    id_, record_type = json.loads(request.data).values()
    if record_type.lower() == "transaction":
        delete_transaction = db.session.get(Transactions, id_)
        db.session.delete(delete_transaction)
        db.session.commit()
        flash("Transaction deleted successfully!", "success")
    elif record_type.lower() == "budget":
        delete_budget_entry = db.session.get(Budget, id_)
        db.session.delete(delete_budget_entry)
        db.session.commit()
        flash("Budget plan entry deleted successfully!", "success")
    elif record_type.lower() == "goal":
        goal_entry = db.session.get(Goals, id_)
        goal_transactions = (
            Transactions.query.filter_by(user_id=current_user.get_id(), goal_id=id_)
            .with_entities(Transactions.value)
            .all()
        )
        goal_sum = float(sum([transaction[0] for transaction in goal_transactions]) if goal_transactions else 0)

        record = Transactions(
            transaction_date=datetime.now().strftime("%d/%m/%Y"),
            value=goal_sum,
            category_id=db.session.query(Category.id)
            .filter(Category.name == "Income", Category.user_id == current_user.get_id())
            .all()[0][0],
            user_id=current_user.get_id(),
            user_note=f"Income from closing Goal: {goal_entry.name}",
        )
        db.session.add(record)
        goal_entry.goal_finished = True
        db.session.commit()
        flash(f"Goal plan entry deleted successfully! \n Added Income {goal_sum}", "success")
    else:
        flash("Something went wrong!", "danger")
    return jsonify({})


@app.route("/addgoal", methods=["GET", "POST"])
def goals():
    if not current_user.is_authenticated:
        flash("You need to log in")
        return redirect(url_for("hello"))
    form = AddGoalForm()
    user_goals_data = get_goals_data(current_user.get_id())

    if form.validate_on_submit():
        active_user_goals = (
            Goals.query.filter_by(user_id=current_user.get_id())
            .filter(Goals.goal_finished != True)
            .with_entities(Goals.name)
            .all()
        )
        if (str(form.name.data),) in active_user_goals:
            flash("Invalid goal name", "danger")
        else:
            insert_goal(form.name.data, form.target_amount.data, form.deadline.data, current_user.id)
            flash(f"New Goal has been added", "success")
        return redirect("addgoal")
    return render_template("addgoal.html", form=form, goals_data=user_goals_data)


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
    goals = (
        db.session.query(Goals.id, Goals.name)
        .filter_by(user_id=current_user.get_id())
        .filter(Goals.goal_finished != True)
        .all()
    )
    # Update the choices for the dropdown field
    form.name.choices = [(str(goal.id), goal.name) for goal in goals]

    goals_transactions = get_goals_transactions(current_user.get_id())
    goals_transactions = pd.DataFrame(goals_transactions)
    if form.validate_on_submit():
        goal_transaction = Transactions(
            transaction_date=form.date.data,
            value=form.amount.data,
            goal_id=form.name.data,
            user_id=current_user.id,
            user_note=form.note.data,
        )
        db.session.add(goal_transaction)
        db.session.commit()
        flash(f"Goal Progress has been added", "success")
        return redirect("addgoalprogress")
    return render_template("addgoalprogress.html", form=form, transactions=goals_transactions)


def get_goals_transactions(user_id):
    return (
        db.session.query(
            Transactions.id,
            Transactions.transaction_date,
            Transactions.value,
            Goals.name,
            Transactions.goal_id,
            Transactions.user_note,
        )
        .join(Goals, Transactions.goal_id == Goals.id)
        .filter(Transactions.user_id == user_id)
        # TODO: Do we want to display transaction history for completed Goals?
        # .filter(Goals.goal_finished != True)
        .all()
    )


@app.route("/categories", methods=["GET", "POST"])
def category_page():
    categories = get_categories()
    add_category_form = AddCategoryForm(prefix="addcat")
    remove_category_form = RemoveCategoryForm(prefix="remcat")
    add_subcategory_form = AddSubcategoryForm(prefix="addsubcat")
    remove_subcategory_form = RemoveSubcategoryForm(prefix="remsubcat")
    remove_category_form.category_name.choices = categories
    if request.method == "POST":
        if add_category_form.submit.data:
            if add_category_form.validate():
                message, status = add_category(add_category_form.category_name.data)
                flash(message, status)
                return redirect(url_for("category_page"))
        if remove_category_form.submit.data:
            if remove_category_form.validate():
                message, status = remove_category(remove_category_form.category_name.data)
                flash(message, status)
                return redirect(url_for("category_page"))
        if add_subcategory_form.submit.data:
            if add_subcategory_form.validate():
                message, status = add_subcategory(
                    add_subcategory_form.category_name.data, add_subcategory_form.subcategory_name.data
                )
                flash(message, status)
                return redirect(url_for("category_page"))
        if remove_subcategory_form.submit.data:
            if remove_subcategory_form.validate():
                message, status = remove_subcategory(
                    remove_subcategory_form.category_name.data, remove_subcategory_form.subcategory_name.data
                )
                flash(message, status)
                return redirect(url_for("category_page"))
    return render_template(
        "category.html",
        data=categories,
        add_category_form=add_category_form,
        add_subcategory_form=add_subcategory_form,
        remove_categgory_form=remove_category_form,
        remove_subcategory_form=remove_subcategory_form,
    )


@app.route("/get_subcategory_field_options", methods=["POST"])
def get_subcategory_field_options():
    selected_cat = request.form.get("selected_value")

    # Use the selected value to determine the new options for the second field
    # Replace this logic with your own based on your requirements
    subcategory_choices = get_subcategories(selected_cat)

    # Return the new options as JSON
    return jsonify(subcategory_choices)
