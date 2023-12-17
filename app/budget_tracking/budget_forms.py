from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, Optional, NumberRange


class BudgetOutcomeForm(FlaskForm):
    value = FloatField(
        "Value:", validators=[DataRequired(), NumberRange(min=0, message="Transaction has to be positive!")]
    )
    main_category = SelectField("Main category:", choices=[], validators=[InputRequired(), Length(max=100)])
    submit = SubmitField("Add budget outcome")


class BudgetIncomeForm(FlaskForm):
    value = FloatField(
        "Value:", validators=[DataRequired(), NumberRange(min=0, message="Transaction has to be positive!")]
    )
    submit = SubmitField("Add budget income")
