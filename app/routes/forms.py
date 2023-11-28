from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange

from app.database.database import Users, Groups, Category,Subcategory,UserGroup,Transactions,Goals,Budget


class AddGoalForm(FlaskForm):
    name = StringField("Goal Name", validators=[DataRequired()])
    target_amount = IntegerField("Target amount", validators=[DataRequired(), NumberRange(min=1)])
    deadline = DateField('Deadline', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Goal')