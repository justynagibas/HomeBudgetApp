from app import db
from app.database.database import Users, Groups, Category, Subcategory, Transactions

def get_categories(userId, category_type):
    if category_type == "income":
        user_income_categories = db.session.query(Subcategory.name).join(Category).filter(Category.user_id==userId, Category.name=="Income").all()
        return user_income_categories
    elif category_type =="outcome":
        user_outcome_categories = db.session.query(Category.name).filter(Category.user_id==userId).all()
        user_outcome_categories.remove(('Income',))
        user_outcome_dict = {}
        for category_record in user_outcome_categories:
            category_name = category_record[0]
            category_subcategories = db.session.query(Subcategory.name).join(Category).filter(Category.user_id==userId, Category.name==category_name).all()
            user_outcome_dict[category_name] = [subcat_record[0] for subcat_record in category_subcategories]
        return user_outcome_dict


def add_transaction(form, userID, transaction_type):
    subcategory_id = db.session.query(Subcategory.id).filter(Subcategory.name == form.subcategory.data).all()
    if not subcategory_id:
        subcategory_id = None
    else:
        subcategory_id = subcategory_id[0][0]
    record = Transactions(transaction_date = form.date.data, value=form.value.data, subcategory_id=subcategory_id, user_id=userID, user_note=form.note.data)
    if transaction_type == "income":
        record.category_id = db.session.query(Category.id).filter(Category.name=="Income").all()[0][0]
    elif transaction_type == "outcome":
        record.category_id = db.session.query(Category.id).filter(Category.name == form.main_category.data).all()[0][0]

    db.session.add(record)
    db.session.commit()