from app.database.database import Category, Budget, Transactions, Goals


def get_user_income_plan(user_id):
    user_income_cat_id = Category.query.filter_by(user_id=user_id, name="Income").with_entities(Category.id).first()
    transactions = (
        Budget.query.filter_by(user_id=user_id, category_id=user_income_cat_id[0]).with_entities(Budget.amount).all()
    )
    if transactions:
        incomes = [transaction[0] for transaction in transactions]
        return sum(incomes)
    else:
        return 0


def get_user_outcome_plan(user_id):
    user_income_cat_id = Category.query.filter_by(user_id=user_id, name="Income").with_entities(Category.id).first()
    transactions = (
        Budget.query.filter_by(user_id=user_id)
        .filter(Budget.category_id != user_income_cat_id[0])
        .with_entities(Budget.amount)
        .all()
    )
    if transactions:
        outcomes = [transaction[0] for transaction in transactions]
        return sum(outcomes)
    else:
        return 0


def get_user_income_actual(user_id):
    user_income_cat_id = Category.query.filter_by(user_id=user_id, name="Income").with_entities(Category.id).first()
    transactions = (
        Transactions.query.filter_by(user_id=user_id, category_id=user_income_cat_id[0])
        .with_entities(Transactions.value)
        .all()
    )
    if transactions:
        outcomes = [transaction[0] for transaction in transactions]
        return sum(outcomes)
    else:
        return 0


def get_user_outcome_actual(user_id):
    user_income_cat_id = Category.query.filter_by(user_id=user_id, name="Income").with_entities(Category.id).first()
    transactions = (
        Transactions.query.filter_by(user_id=user_id)
        .filter(Transactions.category_id != user_income_cat_id[0])
        .with_entities(Transactions.value)
        .all()
    )
    if transactions:
        outcomes = [transaction[0] for transaction in transactions]
        return sum(outcomes)
    else:
        return 0


def get_categories_data(user_id):
    user_outcome_categories = (
        Category.query.filter_by(user_id=user_id)
        .filter(Category.name != "Income")
        .with_entities(Category.id, Category.name)
        .all()
    )

    output = []

    for category in user_outcome_categories:
        category_transactions = (
            Transactions.query.filter_by(user_id=user_id, category_id=category[0])
            .with_entities(Transactions.value)
            .all()
        )
        category_transactions_sum = float(
            sum([transaction[0] for transaction in category_transactions]) if category_transactions else 0
        )
        category_plans = (
            Budget.query.filter_by(user_id=user_id, category_id=category[0]).with_entities(Budget.amount).all()
        )
        category_plans_sum = float(sum([plan[0] for plan in category_plans]) if category_plans else 0)

        category_percentage = (
            int((category_transactions_sum / category_plans_sum) * 100) if category_plans_sum != 0 else 0
        )

        output.append(
            [
                category[0],
                category[1],
                category_transactions_sum,
                category_plans_sum,
                category_percentage,
            ]
        )

    return output


def get_goals_data(user_id):
    user_goals = (
        Goals.query.filter_by(user_id=user_id)
        .with_entities(Goals.id, Goals.name, Goals.target_amount, Goals.deadline)
        .all()
    )
    print(user_goals)
    output = []

    for id_, name, target, deadline in user_goals:
        goal_transactions = (
            Transactions.query.filter_by(user_id=user_id, goal_id=id_).with_entities(Transactions.value).all()
        )
        print(goal_transactions)
        goal_sum = float(sum([transaction[0] for transaction in goal_transactions]) if goal_transactions else 0)
        goal_percentage = int((goal_sum / target) * 100) if goal_sum != 0 else 0
        output.append(
            [
                name,
                target,
                deadline,
                goal_sum,
                goal_percentage,
            ]
        )
    return output
