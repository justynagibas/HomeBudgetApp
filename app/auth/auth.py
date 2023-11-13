from app import login_manager, bcrypt, db
from app.database.database import Users


def insert_user(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = Users(user_name=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def check_user_credentials(username, password):
    user = Users.query.filter_by(user_name=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return False
