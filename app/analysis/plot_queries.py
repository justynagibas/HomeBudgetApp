from sqlalchemy import func

from app import db
from app.database.database import Category, Budget, Transactions, Subcategory
from flask_login import current_user
from app.category.manage_category import get_subcategories


def get_category_progress(category_name):
    transactions = db.session.query(Transactions.id).join(Category).filter(
        Transactions.user_id == current_user.get_id(),
        Category.name == category_name
        ).all()
    if transactions:
        incomes = [transaction[0] for transaction in transactions]
        return sum(incomes)
    else:
        return 0


def get_category_plan(category_name):
    plan = db.session.query(Budget.amount).join(Category).filter(
        Category.name == category_name,
        Budget.year == 2023,
        Budget.month == 12
    ).first()
    if plan:
        return plan[0]
    else:
        return 0

def get_subcategories_spendings(category_name):
    subcategories = get_subcategories(category_name)
    subcategories_spending = db.session.query(Subcategory.name, func.sum(Transactions.value)).join(Subcategory).filter(
        Transactions.user_id == current_user.get_id(),
        Subcategory.name.in_(subcategories)
    ).group_by(Subcategory.name).all()
    for i in range(len(subcategories_spending)):
        subcategories_spending[i] = list(subcategories_spending[i])
        subcategories_spending[i][1] = float(subcategories_spending[i][1])
    return  subcategories_spending