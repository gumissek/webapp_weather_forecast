from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired


class WeatherForm(FlaskForm):
    location = StringField(label='Enter a location to get weather forecast.',validators=[DataRequired()])
    submit = SubmitField(label='Check weather!')

class EmailForm(FlaskForm):
    email = EmailField(label='Enter your email to receive weather info.',validators=[DataRequired()])
    submit = SubmitField(label='Send email')