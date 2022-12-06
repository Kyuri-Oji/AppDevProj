from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime

class bookingForm(FlaskForm):
    bookingFacility = RadioField('Facility: ',  
                             validators=[DataRequired()],
                             choices=[])
    bookingDate = DateTimeField('Booking Date: ',
                                validators=[DataRequired()],
                                format='%d-%m-%y', default=datetime.now, #datetime formatting, dafault to current date
                                render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    bookingTimeSlot = DateTimeField('Booking Timeslot: ',
                                    validators=[DataRequired()])
    submit = SubmitField('Book Facility')
    
