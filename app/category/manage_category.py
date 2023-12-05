from app import db
from app.database.database import Category, Subcategory
from flask_login import current_user


def get_categories():
    categories_db = db.session.query(Category.name).filter(
        Category.user_id == current_user.get_id()
    ).all()
    categories = [category[0] for category in categories_db]
    return categories


def get_subcategories(category):
    subcategories_db = db.session.query(Subcategory.name).join(Category).filter(
        Category.user_id == current_user.get_id(),
        Category.name == category
    ).all()
    subcategories = [category[0] for category in subcategories_db]
    return subcategories


def add_category(name):
    current_categories = get_categories()
    if name not in current_categories:
        new_category = Category(category_name=name, user_id=current_user.get_id(), undeletable=False)
        db.session.add(new_category)
        db.session.commit()
    else:
        pass # wysłać komunika że chujowe


def add_subcategory(category, name):
    current_subcategories = get_subcategories(category)
    if name not in current_subcategories:
        category_id = db.session.query(Category.id).filter(
            Category.user_id == current_user.get_id(),
            Category.name == category).first()[0]
        new_subcategory = Subcategory(name=name, category_id=category_id)
        db.session.add(new_subcategory)
        db.session.commit()
    else:
        pass # wysłać komunika że chujowe


def remove_category(name):
    pass

def remove_subcategory(name):
    pass