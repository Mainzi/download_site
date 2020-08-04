from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class URLForm(FlaskForm):
    URL = StringField('Your URL', validators=[DataRequired()])
    submit = SubmitField('Parse this URL')


class TaskForm(FlaskForm):
    task_id = StringField('Task id', validators=[DataRequired()])
    submit = SubmitField('Get task status')
