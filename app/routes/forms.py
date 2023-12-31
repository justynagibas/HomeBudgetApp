from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, IntegerField, StringField, SelectField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from app.database.database import Users, Groups, Category, Subcategory, UserGroup, Transactions, Goals, Budget


class AddGoalForm(FlaskForm):
    name = StringField("Goal Name", validators=[DataRequired()])
    target_amount = IntegerField("Target amount", validators=[DataRequired(), NumberRange(min=1)])
    deadline = DateField("Deadline", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Add Goal")


class AddGoalProgress(FlaskForm):
    name = SelectField("Goal", choices=[])
    amount = IntegerField("Amount", validators=[DataRequired()])
    date = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])
    note = StringField("Note")
    submit = SubmitField("Add Goal Progress")

    def validate_goal_progress(self, name):
        goal = Users.query.filter_by(user_name=name.data).first()
        if not goal:
            raise ValidationError("This Goal does not exist")
