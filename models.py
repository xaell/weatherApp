from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class LocationForm(FlaskForm):
    location = StringField(
        "Location",
        validators=[
            DataRequired(message="Please enter a location."),
            Length(min=1, max=100, message="Input is too long"),
        ]
    )
    submit = SubmitField("Submit")