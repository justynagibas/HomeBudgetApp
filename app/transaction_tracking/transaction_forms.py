from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired

class OutcomeForm(FlaskForm):

    note = StringField("Note:", validators=[DataRequired(), Length(max=100)])
    value = FloatField("Value:", validators=[DataRequired()])
    date = DateField("Date:", validators=[DataRequired()])
    main_category = SelectField("Main category:", choices=[("", "-- select an option --")], validators=[InputRequired(), Length(max=100)], default="")
    subcategory = SelectField("Subcategory:", choices=[("", "-- select an option --")], validators=[InputRequired(), Length(max=100)], default="")
    submit = SubmitField("Submit")

class IncomeForm(FlaskForm):

    note = StringField("Note:", validators=[DataRequired(), Length(max=100)])
    value = FloatField("Value:", validators=[DataRequired()])
    date = DateField("Date:", validators=[DataRequired()])
    main_category = SelectField("Main category:", choices=[],  validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Submit")