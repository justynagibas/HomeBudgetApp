from app.database.database import Category, Budget, Transactions


def get_user_categories(user_id):
    categories = Category.query.filter_by(user_id=user_id).with_entities(Category.name).all()
    categories = [category[0] for category in categories]
    return categories


def get_user_income_plan(user_id):
    transactions = Budget.query.filter_by(user_id=user_id).with_entities(Budget.amount).all()
    if transactions:
        incomes = [transaction[0] for transaction in transactions if transaction[0] > 0]
        return sum(incomes)
    else:
        return 0


def get_user_outcome_plan(user_id):
    transactions = Budget.query.filter_by(user_id=user_id).with_entities(Budget.amount).all()
    if transactions:
        outcomes = [transaction[0] for transaction in transactions if transaction[0] <= 0]
        return -1 * sum(outcomes)
    else:
        return 0


def get_user_income_actual(user_id):
    transactions = Transactions.query.filter_by(user_id=user_id).with_entities(Transactions.value).all()
    print(transactions)
    if transactions:
        outcomes = [transaction[0] for transaction in transactions if transaction[0] > 0]
        return sum(outcomes)
    else:
        return 0


def get_user_outcome_actual(user_id):
    transactions = Transactions.query.filter_by(user_id=user_id).with_entities(Transactions.value).all()
    if transactions:
        outcomes = [transaction[0] for transaction in transactions if transaction[0] <= 0]
        return -1 * sum(outcomes)
    else:
        return 0
