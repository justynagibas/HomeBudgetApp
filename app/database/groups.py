from sqlalchemy import Column, Integer, String, Sequence, ForeignKey


def create_group(db):
    class Group(db.Model):
        __tablename__ = "groups"
        id = Column(Integer, Sequence("seq_groups_id", start=1), primary_key=True)
        name = Column(String, nullable=False)

    return Group


def create_user_group_table(db):
    class UserGroup(db.Model):
        __tablename__ = "user_group"
        id = Column(Integer, Sequence("seq_user_group_id", start=1), primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    return UserGroup
