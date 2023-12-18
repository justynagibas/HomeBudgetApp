from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, InputRequired, Optional, NumberRange


class AddCategoryForm(FlaskForm):
    category_name = StringField("Category name:", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Add new main category")


class RemoveCategoryForm(FlaskForm):
    category_name = SelectField("Category name:", choices=[], validators=[DataRequired()])
    submit = SubmitField("Remove main category")


class AddSubcategoryForm(FlaskForm):
    subcategory_name = StringField("Subcategory name:", validators=[DataRequired(), Length(max=100)])
    category_name = HiddenField("Category name:", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Add new subcategory")


class RemoveSubcategoryForm(FlaskForm):
    subcategory_name = SelectField("Subcategory name:", choices=[], validators=[InputRequired()], validate_choice=False)
    category_name = HiddenField("Category name:", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Remove subcategory")
