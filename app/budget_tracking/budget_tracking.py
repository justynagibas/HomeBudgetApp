from app import db
from app.database.database import Category, Budget


def get_budget_categories_names(user_id):
    query = db.session.query(Category.name).filter(Category.user_id == user_id, Category.name != "Income").all()
    if query:
        return [cat[0] for cat in query]
    else:
        return None


def add_budget_entry(form, user_id, entry_type, year, month):
    record = Budget(user_id=user_id, year=year, month=month, amount=form.value.data)

    if entry_type == "income":
        record.category_id = (
            db.session.query(Category.id).filter(Category.name == "Income", Category.user_id == user_id).first()[0]
        )
    elif entry_type == "outcome":
        record.category_id = (
            db.session.query(Category.id)
            .filter(Category.name == form.main_category.data, Category.user_id == user_id)
            .first()[0]
        )
    db.session.add(record)
    db.session.commit()


def get_budget_entries(user_id, year, month):
    return (
        db.session.query(Budget.id, Category.name, Budget.amount, Budget.month, Budget.year)
        .join(Category, Budget.category_id == Category.id)
        .filter(Budget.user_id == user_id, Budget.month == month, Budget.year == year)
        .all()
    )
