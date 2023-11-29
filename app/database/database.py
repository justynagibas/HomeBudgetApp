from .category import create_category_table, create_subcategory_table, create_goals_table
from .users import create_users_table
from .groups import create_group, create_user_group_table
from .transactions import create_transactions_table
from .budget_plan import create_budget_table

from app import app, db
from flask_login import UserMixin

Users = create_users_table(db, UserMixin)
Groups = create_group(db)
Category = create_category_table(db)
Subcategory = create_subcategory_table(db)
UserGroup = create_user_group_table(db)
Transactions = create_transactions_table(db)
Goals = create_goals_table(db)
Budget = create_budget_table(db)


def create_tables():
    with app.app_context():
        db.create_all()
