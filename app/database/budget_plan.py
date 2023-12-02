from sqlalchemy import Column, Integer, Sequence, ForeignKey, CheckConstraint


def create_budget_table(db):
    class Budget(db.Model):
        __tablename__ = "budget_plan"
        id = Column(Integer, Sequence("seq_income_plan_id", start=1), primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        amount = Column(Integer, nullable=False)
        category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
        year = Column(Integer, nullable=False)
        month = Column(Integer, nullable=False)
        __table_args__ = (CheckConstraint("month >= 1"), CheckConstraint("month <= 12"))

    return Budget
