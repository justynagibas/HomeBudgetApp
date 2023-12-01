from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField, SelectField, Label
from wtforms.validators import DataRequired, Length, InputRequired, Optional

class OutcomeForm(FlaskForm):

    note = StringField("Note:", validators=[DataRequired(), Length(max=100)])
    value = FloatField("Value:", validators=[DataRequired()])
    date = DateField("Date:", validators=[DataRequired()])
    main_category = SelectField("Main category:", choices=[], validators=[InputRequired(), Length(max=100)])
    subcategory = SelectField("Subcategory:", choices=[], validators=[Length(max=100), Optional()],)
    submit = SubmitField("Submit")
class IncomeForm(FlaskForm):

    note = StringField("Note:", validators=[DataRequired(), Length(max=100)])
    value = FloatField("Value:", validators=[DataRequired()])
    date = DateField("Date:", validators=[DataRequired()])
    subcategory = SelectField("Subcategory:", choices=[],  validators=[Optional(), Length(max=100)])
    submit = SubmitField("Submit")