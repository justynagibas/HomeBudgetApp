from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey, Date, Numeric


def create_category_table(db):
    class Category(db.Model):
        __tablename__ = "category"
        id = Column(Integer, Sequence("seq_income_category_id", start=1), primary_key=True)
        name = Column(String, nullable=False)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        undeletable = Column(Boolean, nullable=False)

    return Category


def create_subcategory_table(db):
    class Subcategory(db.Model):
        __tablename__ = "subcategory"
        id = Column(Integer, Sequence("seq_outcome_subcategory", start=1), primary_key=True)
        name = Column(String, nullable=False)
        category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    return Subcategory


def create_goals_table(db):
    class Goal(db.Model):
        __tablename__ = "goals"
        id = Column(Integer, Sequence("seq_goals", start=1), primary_key=True)
        name = Column(String, nullable=False)
        target_amount = Column(Numeric(10, 2))
        deadline = Column(Date)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        goal_finished = Column(Boolean, nullable=False, default=False)

    return Goal
