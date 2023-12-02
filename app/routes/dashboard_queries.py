from app.database.database import Category, Budget, Transactions


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


def get_categories_data(user_id):
    user_categories = Category.query.filter_by(user_id=user_id).with_entities(Category.id, Category.name).all()

    output = []

    for category in user_categories:
        category_transactions = (
            Transactions.query.filter_by(user_id=user_id, category_id=category[0])
            .with_entities(Transactions.value)
            .all()
        )
        category_transactions_sum = (
            sum([transaction[0] for transaction in category_transactions if transaction[0] <= 0])
            if category_transactions
            else 0
        )
        category_plans = (
            Budget.query.filter_by(user_id=user_id, category_id=category[0]).with_entities(Budget.amount).all()
        )
        category_plans_sum = sum([plan[0] for plan in category_plans if plan[0] <= 0]) if category_plans else 0

        category_percentage = (
            int(-1 * category_transactions_sum / float(-1 * category_plans_sum) * 100) if category_plans_sum != 0 else 0
        )

        output.append(
            [
                category[0],
                category[1],
                -1 * category_transactions_sum,
                float(-1 * category_plans_sum),
                category_percentage,
            ]
        )

    return output
