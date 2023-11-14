from sqlalchemy import Column, Integer,  Sequence, ForeignKey, CheckConstraint


def create_income_plan_table(db):
    class IncomePlan(db.Model):
        __tablename__ = "income_plan"
        id = Column(Integer, Sequence("seq_income_plan_id", start=1), primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        income_value = Column(Integer, nullable=False)
        income_category_id = Column(Integer, ForeignKey("income_category.id"), nullable=False)
        year = Column(Integer, nullable=False)
        month = Column(Integer, nullable=False)
        __table_args__ = (
            CheckConstraint("month >= 1"),
            CheckConstraint("month <= 12"),
            CheckConstraint("income_value > 0")
        )
    return IncomePlan


def create_outcome_plan_table(db):
    class OutcomePlan(db.Model):
        __tablename__ = "outcome_plan"
        id = Column(Integer, Sequence("seq_outcome_plan_id", start=1), primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        outcome_value = Column(Integer, nullable=False)
        outcome_category_id = Column(Integer, ForeignKey("outcome_category.id"), nullable=False)
        outcome_subcategory_id = Column(Integer, ForeignKey("outcome_subcategory.id"), nullable=True)
        year = Column(Integer, nullable=False)
        month = Column(Integer, nullable=False)
        __table_args__ = (
            CheckConstraint("month >= 1"),
            CheckConstraint("month  <= 12"),
            CheckConstraint("outcome_value >0")
        )
    return OutcomePlan
