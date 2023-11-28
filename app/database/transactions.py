from sqlalchemy import Column, Integer, String, Double, Date, Sequence, ForeignKey


def create_transactions_table(db):
    class Transaction(db.Model):
        __tablename__ = "transactions"
        id = Column(Integer, Sequence("seq_transactions_id", start=1), primary_key=True)
        transaction_date = Column(Date, nullable=False)
        value = Column(Double, nullable=False)
        category_id = Column(Integer, ForeignKey("category.id"), nullable=True)
        subcategory_id = Column(Integer, ForeignKey("subcategory.id"), nullable=True)
        goal_id = Column(Integer, ForeignKey("goals.id"), nullable=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
        # transaction_type = Column('TransactionType', Enum('Income', 'Expense', name='transaction_type_enum'))
        user_note = Column(String(100), nullable=True)

    return Transaction
