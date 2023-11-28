from app import login_manager, bcrypt, db
from app.database.database import Users, Groups, Category,Subcategory,UserGroup,Transactions,Goals,Budget


def insert_user(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = Users(user_name=username, password=hashed_password)
    db.session.add(user)
    db.session.commit() # co to robi?
    db.session.flush()
    db.session.refresh(user)

    # Add default categories to the user
    userId = user.id

    default_categories = ["Income",
        "Food",
        "Apartment",
        "Transport",
        "Telecommunication",
        "Health",
        "Clothes",
        "Hygiene",
        "Kids",
        "Entertainment",
        "Others",
        "Debt",
        "Investment",
    ]

    userId = db.session.query(Users).filter(Users.user_name == username).first().id

    for category in default_categories:
        if category == 'Income':
            record = Category(name=category, user_id=userId, undeletable=True)
        elif category == 'Others':
            record = Category(name=category, user_id=userId, undeletable=True)
        else:
            record = Category(name=category, user_id=userId, undeletable=False)
        db.session.add(record)

    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def check_user_credentials(username, password):
    user = Users.query.filter_by(user_name=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return False
