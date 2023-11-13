from .category import create_income_category_table, create_outcome_category_table, create_outcome_subcategory_table
from .users import create_users_table
from .user_categories import (
    create_user_income_categories_table,
    create_user_outcome_categories_table,
    create_user_outcome_subcategories_table,
)
from .groups import create_group, create_user_group_table
from .transactions import create_income_history_table, create_outcome_history_table

from app import app, db
from flask_login import UserMixin

Users = create_users_table(db, UserMixin)
Groups = create_group(db)
IncomeCategory = create_income_category_table(db)
OutcomeCategory = create_outcome_category_table(db)
OutcomeSubcategory = create_outcome_subcategory_table(db)
UserGroup = create_user_group_table(db)
OutcomeHistory = create_outcome_history_table(db)
IncomeHistory = create_income_history_table(db)
UserIncomeCategory = create_user_income_categories_table(db)
UserOutcomeCategory = create_user_outcome_categories_table(db)
UserOutcomeSubcategory = create_user_outcome_subcategories_table(db)


def create_tables():
    with app.app_context():
        db.create_all()
