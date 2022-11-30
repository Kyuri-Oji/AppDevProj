from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime

class eventCreateForm(FlaskForm):
    eventName = StringField('Event Name :', 
                            validators=[DataRequired(), Length(min = 2, max = 30)])
    eventDesc = TextAreaField('Event Description : ',
                            validators=[DataRequired(), Length(min = 2)])
    eventVacancy = IntegerField('Event Vacancy : ',
                                validators=[DataRequired()])
    eventDate = DateTimeField('Event End Date : ',
                              validators=[DataRequired()],
                              format='%d-%m-%y', default=datetime.now, #datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    submit = SubmitField('Edit Events')