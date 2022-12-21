from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime

def all_numbers(form,field):
    if field.data.isdigit()==False:
        raise ValidationError("Field must be all numbers")

class bookingForm(FlaskForm):
    bookingFacilityLocation = SelectField('Facility Location: ',
                                         validators=[DataRequired()],
                                         choices=[('', 'Select'), ('56', 'Ang Mo Kio'), ('53', 'Hougang'), ('37', 'Macpherson'), ('35', 'Braddell'), ('79', 'Seletar'), ('19', 'Golden Mile')])  
    bookingFacilityID = SelectField('Facility ID: ',  
                                 validators=[DataRequired()],
                                 choices=[('', 'Select'), ('BD1', 'Badminton Court 1'), ('BD2', 'Badminton Court 2'), ('BB1', 'Basketball Court 1')])
    bookingDate = DateTimeField('Booking Date: ',
                                validators=[DataRequired()],
                                format='%d-%m-%y', default=datetime.now, #datetime formatting, dafault to current date
                                render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    bookingTimeSlot = SelectField('Booking Timeslot: ',
                                    validators=[DataRequired()],
                                    choices=[('', 'Select'), ('10am to 11am', '10am to 11am'), ('11am to 12pm', '11am to 12pm'), ('12pm to 1pm', '12pm to 1pm'), ('1pm to 2pm', '1pm to 2pm'), ('2pm to 3pm', '2pm to 3pm'), ('3pm to 4pm', '3pm to 4pm'), ('4pm to 5pm', '4pm to 5pm'), ('5pm to 6pm', '5pm to 6pm'), ('6pm to 7pm', '6pm to 7pm')])
    submit = SubmitField('Continue')

class paymentForm(FlaskForm):
    paymentMethod = SelectField('Payment Method: ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('American Express', 'American Express'), ('Mastercard', 'Mastercard'), ('VISA', 'VISA')])
    cardNumber = StringField('Card Number: ',
                            validators=[DataRequired(), all_numbers, Length(min = 12, max = 12)])
    expirationDate = DateTimeField('Expiration Date: ',
                                validators=[DataRequired()],
                                format='%m-%y', default=datetime.now, #datetime formatting, dafault to current date
                                render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    submit = SubmitField('Book Facility')
    
# Use data from facilitiesdb for choices
# Set restrictions using data from facilitiesdb
# When editting, use data from booking as placeholder