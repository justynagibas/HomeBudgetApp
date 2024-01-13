from app import db
from app.database.database import Category, Subcategory, Transactions, Budget
from flask_login import current_user


def get_categories():
    categories_db = db.session.query(Category.name).filter(Category.user_id == current_user.get_id()).all()
    categories = [category[0] for category in categories_db]
    categories.remove("Goals")
    return categories


def get_subcategories(category):
    subcategories_db = (
        db.session.query(Subcategory.name)
        .join(Category)
        .filter(Category.user_id == current_user.get_id(), Category.name == category)
        .all()
    )
    subcategories = [category[0] for category in subcategories_db]
    return subcategories


def add_category(name):
    current_categories = get_categories()
    if name not in current_categories:
        new_category = Category(name=name, user_id=current_user.get_id(), undeletable=False)
        db.session.add(new_category)
        db.session.commit()
        return "Added category successfully", "success"
    return "Category already exists", "error"


def add_subcategory(category, name):
    current_subcategories = get_subcategories(category)
    if name not in current_subcategories:
        category_id = (
            db.session.query(Category.id)
            .filter(Category.user_id == current_user.get_id(), Category.name == category)
            .first()[0]
        )
        new_subcategory = Subcategory(name=name, category_id=category_id)
        db.session.add(new_subcategory)
        db.session.commit()
        return "Added subcategory successfully", "success"
    return "Subcategory already exists", "error"


def remove_category(name):
    category_id = (
        db.session.query(Category.id)
        .filter(Category.name == name, Category.user_id == current_user.get_id(), Category.undeletable == False)
        .first()
    )
    others_id = db.session.query(Category.id).filter(
        Category.name == "Others", Category.user_id == current_user.get_id()
    )
    if category_id is not None:
        subcategories = db.session.query(Subcategory.name).filter(Subcategory.category_id == category_id[0]).all()
        transactions = db.session.query(Transactions.id).filter(Transactions.category_id == category_id[0]).all()
        budgets = db.session.query(Budget.id).filter(Budget.category_id == category_id[0]).all()
        if subcategories is not None:
            for subcategory in subcategories:
                _ = remove_subcategory(name, subcategory[0])
        if transactions is not None:
            for transaction_id in transactions:
                transaction = db.session.get(Transactions, transaction_id[0])
                transaction.category_id = others_id
        if budgets is not None:
            for budget_id in budgets:
                budget = db.session.get(Budget, budget_id[0])
                budget.category_id = others_id
        delete_category = db.session.get(Category, category_id[0])
        db.session.delete(delete_category)
        db.session.commit()
        return "Category deleted successfully", "success"
    return "Category cannot be deleted", "error"


def remove_subcategory(category, name):
    subcategory_id = (
        db.session.query(Subcategory.id)
        .join(Category)
        .filter(Category.name == category, Category.user_id == current_user.get_id(), Subcategory.name == name)
        .first()
    )
    if subcategory_id is not None:
        transactions = db.session.query(Transactions.id).filter(Transactions.subcategory_id == subcategory_id[0]).all()
        if transactions is not None:
            for transaction_id in transactions:
                transaction = db.session.get(Transactions, transaction_id[0])
                transaction.subcategory_id = None
        delete_subcategory = db.session.get(Subcategory, subcategory_id[0])
        db.session.delete(delete_subcategory)
        db.session.commit()
        return "Category deleted successfully", "success"
    return "Category cannot be deleted", "error"
