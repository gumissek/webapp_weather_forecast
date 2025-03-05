from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired


class WeatherForm(FlaskForm):
    location = StringField(label='Enter a location to get weather forecast.',validators=[DataRequired()])
    submit = SubmitField(label='Check weather!')