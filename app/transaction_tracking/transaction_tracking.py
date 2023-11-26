from app import db
from app.database.database import Users, UserIncomeCategory, UserOutcomeCategory, \
    UserOutcomeSubcategory, IncomeCategory, OutcomeCategory, OutcomeSubcategory

def get_categories(username, category_type):
    userId = db.session.query(Users).filter(Users.user_name == username).first().id
    if userId:
        if category_type == "income":
            user_income_categories = db.session.query(IncomeCategory.category_name).join(UserIncomeCategory).filter_by(user_id=userId).all()
            return user_income_categories
        elif category_type =="outcome":
            user_outcome_categories = db.session.query(OutcomeCategory.category_name).join(UserOutcomeCategory).filter_by(user_id=userId).all()
            user_outcome_subcategories = db.session.query(OutcomeSubcategory.category_name).join(UserOutcomeSubcategory).filter_by(user_id=userId).all()
            return user_outcome_categories, user_outcome_subcategories
    return None