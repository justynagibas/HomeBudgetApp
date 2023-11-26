from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class OutcomeForm(FlaskForm):
    note = StringField("Description of your expense", validators=[DataRequired(), Length(max=100)])
    value = DecimalField("Value your expense", validators=[DataRequired()])
    date = DateField("Date of making expense", validators=[DataRequired()])
    main_category = StringField("Main category of your expense", validators=[DataRequired(), Length(max=100)])
    subcategory = StringField("Subcategory of your expense", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Submit")

    #TODO: add necessary validators

class IncomeForm(FlaskForm):
    note = StringField("Description of your expense", validators=[DataRequired(), Length(max=100)])
    value = DecimalField("Value your expense", validators=[DataRequired()])
    date = DateField("Date of making expense", validators=[DataRequired()])
    main_category = StringField("Main category of your expense", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Submit")