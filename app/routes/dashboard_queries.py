from app.database.database import Category, Budget, Transactions, Goals
from app import db
from sqlalchemy import extract


def get_user_monthly_budget_sums(user_id, this_month, this_year):
    income_query = (
        db.session.query(Budget.amount)
        .filter(
            Budget.user_id == user_id, Category.name == "Income", Budget.month == this_month, Budget.year == this_year
        )
        .join(Category, Category.id == Budget.category_id)
        .all()
    )
    income_query = [entry[0] for entry in income_query]
    budget_income_sum = sum(income_query)

    outcome_query = (
        db.session.query(Budget.amount)
        .filter(
            Budget.user_id == user_id, Category.name != "Income", Budget.month == this_month, Budget.year == this_year
        )
        .join(Category, Category.id == Budget.category_id)
        .all()
    )
    outcome_query = [entry[0] for entry in outcome_query]
    budget_outcome_sum = sum(outcome_query)
    return budget_income_sum, budget_outcome_sum


def get_user_monthly_transaction_sums(user_id, this_month, this_year):
    income_query = (
        db.session.query(Transactions.value)
        .filter(
            Transactions.user_id == user_id,
            Category.name == "Income",
            extract("month", Transactions.transaction_date) == this_month,
            extract("year", Transactions.transaction_date) == this_year,
        )
        .join(Category, Category.id == Transactions.category_id)
        .all()
    )
    income_query = [entry[0] for entry in income_query]
    trans_income_sum = sum(income_query)

    outcome_query = (
        db.session.query(Transactions.value)
        .filter(
            Transactions.user_id == user_id,
            Category.name != "Income",
            extract("month", Transactions.transaction_date) == this_month,
            extract("year", Transactions.transaction_date) == this_year,
        )
        .join(Category, Category.id == Transactions.category_id)
        .all()
    )
    outcome_query = [entry[0] for entry in outcome_query]
    trans_outcome_sum = sum(outcome_query)
    return trans_income_sum, trans_outcome_sum


def get_user_monthly_category_outcomes(user_id, this_month, this_year):
    user_outcome_categories = (
        Category.query.filter_by(user_id=user_id)
        .filter(Category.name != "Income")
        .with_entities(Category.id, Category.name)
        .all()
    )

    output = []

    for category in user_outcome_categories:
        category_transactions = (
            db.session.query(Transactions.value)
            .filter(
                Transactions.user_id == user_id,
                Transactions.category_id == category[0],
                extract("month", Transactions.transaction_date) == this_month,
                extract("year", Transactions.transaction_date) == this_year,
            )
            .all()
        )
        category_transactions_sum = float(
            sum([transaction[0] for transaction in category_transactions]) if category_transactions else 0
        )

        category_budgets = db.session.query(Budget.amount).filter(
            Budget.user_id == user_id,
            Budget.category_id == category[0],
            Budget.month == this_month,
            Budget.year == this_year,
        )
        category_plans_sum = float(sum([plan[0] for plan in category_budgets]) if category_budgets else 0)

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
    output = []

    for id_, name, target, deadline in user_goals:
        goal_transactions = (
            Transactions.query.filter_by(user_id=user_id, goal_id=id_).with_entities(Transactions.value).all()
        )
        goal_sum = float(sum([transaction[0] for transaction in goal_transactions]) if goal_transactions else 0)
        goal_percentage = int((goal_sum / target) * 100) if goal_sum != 0 else 0
        output.append([name, target, deadline, goal_sum, goal_percentage])
    return output
