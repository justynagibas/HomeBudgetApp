from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, Optional, NumberRange


class TransOutcomeForm(FlaskForm):
    note = StringField("Note:", validators=[Length(max=100)])
    value = FloatField(
        "Value:", validators=[DataRequired(), NumberRange(min=0, message="Transaction has to be positive!")]
    )
    date = StringField("Date:", validators=[DataRequired()])
    main_category = SelectField("Main category:", choices=[], validators=[InputRequired(), Length(max=100)])
    subcategory = SelectField(
        "Subcategory:",
        choices=["No subcategory"],
        validators=[Length(max=100), Optional()],
    )
    submit = SubmitField("Add new outcome")


class TransIncomeForm(FlaskForm):
    note = StringField("Note:", validators=[Length(max=100)])
    value = FloatField(
        "Value:", validators=[DataRequired(), NumberRange(min=0, message="Transaction has to be positive!")]
    )
    date = StringField("Date:", validators=[DataRequired()])
    subcategory = SelectField("Subcategory:", choices=["No subcategory"], validators=[Optional(), Length(max=100)])
    submit = SubmitField("Add new income")
