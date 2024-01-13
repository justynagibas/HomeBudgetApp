from sqlalchemy import Column, Integer, String, Date, Sequence, ForeignKey, Numeric


def create_transactions_table(db):
    class Transaction(db.Model):
        __tablename__ = "transactions"
        id = Column(Integer, Sequence("seq_transactions_id", start=1), primary_key=True)
        transaction_date = Column(Date, nullable=False)
        value = Column(Numeric(10, 2), nullable=False)
        category_id = Column(Integer, ForeignKey("category.id"), nullable=True)
        subcategory_id = Column(Integer, ForeignKey("subcategory.id"), nullable=True)
        goal_id = Column(Integer, ForeignKey("goals.id"), nullable=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
        user_note = Column(String(100), nullable=True)

    return Transaction
