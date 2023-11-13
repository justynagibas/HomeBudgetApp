from sqlalchemy import Column, Integer, String, Double, Date, Sequence, ForeignKey


def create_income_history_table(db):
    class IncomeHistory(db.Model):
        __tablename__ = "income_history"
        id = Column(Integer, Sequence("seq_income_history_id", start=1), primary_key=True)
        transaction_date = Column(Date, nullable=False)
        value = Column(Double, nullable=False)
        category_id = Column(Integer, ForeignKey("income_category.id"), nullable=False)
        user_note = Column(String(100), nullable=True)

    return IncomeHistory


def create_outcome_history_table(db):
    class OutcomeHistory(db.Model):
        __tablename__ = "outcome_history"
        id = Column(Integer, Sequence("seq_outcome_history_id", start=1), primary_key=True)
        transaction_date = Column(Date, nullable=False)
        value = Column(Double, nullable=False)
        category_id = Column(Integer, ForeignKey("outcome_category.id"), nullable=False)
        subcategory_id = Column(Integer, ForeignKey("outcome_subcategory.id"), nullable=True)
        user_note = Column(String(100), nullable=True)

    return OutcomeHistory
