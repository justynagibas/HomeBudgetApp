from sqlalchemy import Column, Integer, Sequence, ForeignKey


def create_user_income_categories_table(db):
    class UserIncomeCategories(db.Model):
        __tablename__ = "user_income_category"
        id = Column(Integer, Sequence("seq_user_income_category", start=1), primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        income_category_id = Column(Integer, ForeignKey("income_category.id"), nullable=False)

    return UserIncomeCategories


def create_user_outcome_categories_table(db):
    class UserOutcomeCategories(db.Model):
        __tablename__ = "user_outcome_category"
        id = Column(Integer, Sequence("seq_user_outcome_category", start=1), primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        outcome_category_id = Column(Integer, ForeignKey("outcome_category.id"), nullable=False)

    return UserOutcomeCategories


def create_user_outcome_subcategories_table(db):
    class UserOutcomeSubcategories(db.Model):
        __tablename__ = "user_outcome_subcategory"
        id = Column(Integer, Sequence("seq_user_outcome_subcategory", start=1), primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        outcome_subcategory_id = Column(Integer, ForeignKey("outcome_subcategory.id"), nullable=False)

    return UserOutcomeSubcategories
