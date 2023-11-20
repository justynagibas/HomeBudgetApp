from app import login_manager, bcrypt, db
from app.database.database import Users, UserIncomeCategory, UserOutcomeCategory, OutcomeCategory, IncomeCategory


def insert_user(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = Users(user_name=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    db.session.flush()
    db.session.refresh(user)

    # Add default categories to the user
    userId = user.id

    income_default_categories = ["Salary", "Others"]

    outcome_default_categories = [
        "Food",
        "Apartment",
        "Transport",
        "Telecommunication",
        "Health",
        "Clothes",
        "Hygiene",
        "Kids",
        "Entertainment",
        "Others",
        "Debt",
        "Investment",
    ]

    userId = db.session.query(Users).filter(Users.user_name == username).first().id

    for income_category in income_default_categories:
        categoryId = db.session.query(IncomeCategory).filter(IncomeCategory.category_name == income_category).first().id
        user_income_category = UserIncomeCategory(user_id=userId, income_category_id=categoryId)
        db.session.add(user_income_category)

    for outcome_category in outcome_default_categories:
        categoryId = (
            db.session.query(OutcomeCategory).filter(OutcomeCategory.category_name == outcome_category).first().id
        )
        user_outcome_category = UserOutcomeCategory(user_id=userId, outcome_category_id=categoryId)
        db.session.add(user_outcome_category)

    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def check_user_credentials(username, password):
    user = Users.query.filter_by(user_name=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return False
