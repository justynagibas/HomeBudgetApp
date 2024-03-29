from sqlalchemy import func, extract
from app import db
from app.database.database import Category, Budget, Transactions, Subcategory, Users
from flask_login import current_user
from app.category.manage_category import get_subcategories


def get_category_progress(category_name, this_month, this_year):
    transactions = (
        db.session.query(func.sum(Transactions.value))
        .join(Category)
        .filter(
            Transactions.user_id == current_user.get_id(),
            Category.name == category_name,
            extract("month", Transactions.transaction_date) == this_month,
            extract("year", Transactions.transaction_date) == this_year,
        )
        .first()
    )
    if transactions[0] is not None:
        return float(transactions[0])
    else:
        return 0


def get_category_plan(category_name, this_month, this_year):
    plan = (
        db.session.query(Budget.amount)
        .join(Category)
        .filter(
            Budget.user_id == current_user.get_id(),
            Category.name == category_name,
            Budget.year == this_year,
            Budget.month == this_month,
        )
        .first()
    )
    if plan:
        return float(plan[0])
    else:
        return 0


def get_subcategories_spendings(category_name, this_month, this_year):
    subcategories = get_subcategories(category_name)
    subcategories_spending = (
        db.session.query(Subcategory.name, func.sum(Transactions.value))
        .join(Subcategory)
        .filter(
            Transactions.user_id == current_user.get_id(),
            extract("month", Transactions.transaction_date) == this_month,
            extract("year", Transactions.transaction_date) == this_year,
            Subcategory.name.in_(subcategories),
        )
        .group_by(Subcategory.name)
        .all()
    )
    no_subcategory_speeding = (
        db.session.query(func.sum(Transactions.value))
        .join(Category)
        .filter(
            Transactions.user_id == current_user.get_id(),
            extract("month", Transactions.transaction_date) == this_month,
            extract("year", Transactions.transaction_date) == this_year,
            Category.name == category_name,
            Transactions.subcategory_id == None,
        )
        .first()
    )
    for i in range(len(subcategories_spending)):
        subcategories_spending[i] = list(subcategories_spending[i])
        subcategories_spending[i][1] = float(subcategories_spending[i][1])
    if no_subcategory_speeding[0] is not None:
        subcategories_spending.append(["no assigned subcategory", float(no_subcategory_speeding[0])])
    return subcategories_spending


def get_category_historic_data(category_name, this_year):
    historic_data = []
    for month in range(1, 13):
        month_budget = (
            db.session.query(Budget.amount)
            .join(Category)
            .filter(
                Budget.user_id == current_user.get_id(),
                Category.name == category_name,
                Budget.month == month,
                Budget.year == this_year,
            )
            .first()
        )
        month_spending = (
            db.session.query(func.sum(Transactions.value))
            .join(Category)
            .filter(
                Transactions.user_id == current_user.get_id(),
                Category.name == category_name,
                extract("month", Transactions.transaction_date) == month,
                extract("year", Transactions.transaction_date) == this_year,
            )
            .first()
        )
        if month_budget is not None:
            historic_data.append([month, float(month_budget[0])])
        else:
            historic_data.append([month, 0])
        if month_spending[0] is not None:
            historic_data[month - 1].append(float(month_spending[0]))
        else:
            historic_data[month - 1].append(0)
    return historic_data


def get_subcategories_hirtoric_spedning(category_name, subcategory_name, this_year):
    subcategory_historic_spending = []
    if subcategory_name is not None:
        for month in range(1, 13):
            month_spending = (
                db.session.query(func.sum(Transactions.value))
                .join(Category)
                .join(Subcategory, Transactions.subcategory_id == Subcategory.id)
                .filter(
                    Transactions.user_id == current_user.get_id(),
                    Category.name == category_name,
                    Subcategory.name == subcategory_name,
                    extract("month", Transactions.transaction_date) == month,
                    extract("year", Transactions.transaction_date) == this_year,
                )
                .first()
            )
            if month_spending[0] is not None:
                subcategory_historic_spending.append([month, float(month_spending[0])])
            else:
                subcategory_historic_spending.append([month, 0])
    return subcategory_historic_spending
