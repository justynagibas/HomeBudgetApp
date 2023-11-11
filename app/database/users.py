from sqlalchemy import Column, Integer, String, Sequence, CheckConstraint


def create_users_table(db, UserMixin):
    class Users(db.Model, UserMixin):
        __tablename__ = 'users'
        id = Column(Integer, Sequence("seq_users_id", start=1), primary_key=True)
        user_name = Column(String, unique=True, nullable=False)
        password = Column(String, nullable=False)
        __table_args__ = (
            CheckConstraint("LENGTH(user_name) > 3"),
            CheckConstraint("LENGTH(user_name) <= 15"),
            CheckConstraint("LENGTH(password) = 60")
        )
    return Users