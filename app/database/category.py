from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey


def create_income_category_table(db):
    class IncomeCategory(db.Model):
        __tablename__ = "income_category"
        id = Column(Integer, Sequence("seq_income_category_id", start=1), primary_key=True)
        category_name = Column(String, nullable=False)
        undeletable = Column(Boolean, nullable=False)

    return IncomeCategory


def create_outcome_category_table(db):
    class OutcomeCategory(db.Model):
        __tablename__ = "outcome_category"
        id = Column(Integer, Sequence("seq_outcome_category_id", start=1), primary_key=True)
        category_name = Column(String, nullable=False)
        undeletable = Column(Boolean, nullable=False)

    return OutcomeCategory


def create_outcome_subcategory_table(db):
    class OutcomeSubcategory(db.Model):
        __tablename__ = "outcome_subcategory"
        id = Column(Integer, Sequence("seq_outcome_subcategory", start=1), primary_key=True)
        category_name = Column(String, nullable=False)
        outcome_category_id = Column(Integer, ForeignKey("outcome_category.id"), nullable=False)

    return OutcomeSubcategory
