from app import db
from app.database.database import Category, Subcategory, Transactions
from sqlalchemy import extract


def get_transaction_categories(userId, category_type):
    if category_type == "income":
        user_income_categories = (
            db.session.query(Subcategory.name)
            .join(Category)
            .filter(Category.user_id == userId, Category.name == "Income")
            .all()
        )
        return user_income_categories
    elif category_type == "outcome":
        user_outcome_categories = db.session.query(Category.name).filter(Category.user_id == userId).all()
        user_outcome_categories.remove(("Income",))
        user_outcome_categories.remove(("Goals",))
        user_outcome_dict = {}
        for category_record in user_outcome_categories:
            category_name = category_record[0]
            category_subcategories = (
                db.session.query(Subcategory.name)
                .join(Category)
                .filter(Category.user_id == userId, Category.name == category_name)
                .all()
            )
            user_outcome_dict[category_name] = [subcat_record[0] for subcat_record in category_subcategories]
        return user_outcome_dict


def add_transaction(form, userID, transaction_type):
    record = Transactions(
        transaction_date=form.date.data, value=form.value.data, user_id=userID, user_note=form.note.data
    )
    if transaction_type == "income":
        record.category_id = (
            db.session.query(Category.id).filter(Category.name == "Income", Category.user_id == userID).all()[0][0]
        )
    elif transaction_type == "outcome":
        record.category_id = (
            db.session.query(Category.id)
            .filter(Category.name == form.main_category.data, Category.user_id == userID)
            .all()[0][0]
        )

    subcategory_id = (
        db.session.query(Subcategory.id)
        .filter(Subcategory.name == form.subcategory.data, Subcategory.category_id == record.category_id)
        .all()
    )
    if not subcategory_id or form.subcategory.data == "No subcategory":
        record.subcategory_id = None
    else:
        record.subcategory_id = subcategory_id[0][0]
    db.session.add(record)
    db.session.commit()


def get_transactions(userId, year, month):
    category_id = db.session.query(Category.id).filter(Category.name == "Goals", Category.user_id == userId).all()[0][0]
    return (
        db.session.query(
            Transactions.id,
            Transactions.transaction_date,
            Transactions.value,
            Category.name,
            Subcategory.name.label("subcategory_name"),
            Transactions.user_note,
        )
        .join(Category, Transactions.category_id == Category.id)
        .outerjoin(Subcategory, Transactions.subcategory_id == Subcategory.id)
        .filter(
            Transactions.user_id == userId,
            Transactions.category_id != category_id,  # remove goal progress transactions
            extract("month", Transactions.transaction_date) == month,
            extract("year", Transactions.transaction_date) == year,
        )
        .all()
    )
