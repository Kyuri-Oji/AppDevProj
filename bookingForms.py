from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from datetime import date, datetime

import shelve

def all_numbers(form,field):
    if field.data.isdigit()==False:
        raise ValidationError("Field must be all numbers")

facilDict = {}
facilDB = shelve.open('Facilities')
try:    
    if 'Facilites' in facilDB:
        facilDict = facilDB['Facilities']
    else:
        facilDB['Facilites'] = facilDict
except:
    print('Error in retrieving facilites.')
    
facilityIDList = []
facilityUIDList = []
for facil in facilDict:
    facils = facilDict.get(facil)
    facilAvailability = facils.get_fac_status()
    if facilAvailability == 'Available':
        facilityUID = facils.get_uniqueID()
        facilityUIDList.append(facilityUID)
        facilityID = facils.get_fac_id()
        facilityIDList.append(facilityID)
            
class bookingForm(FlaskForm):
    bookingFacilityLocation = SelectField('Facility Location: ',
                                         validators=[DataRequired()],
                                         choices=[('', 'Select'), ('56', 'Ang Mo Kio'), ('53', 'Hougang'), ('37', 'Macpherson'), ('35', 'Braddell'), ('79', 'Seletar'), ('19', 'Golden Mile')])  
    bookingFacilityID = SelectField('Facility ID: ',  
                                 validators=[DataRequired()],
                                 choices=[(facilityIDList[i], f"{facilityUIDList[i]} - {facilityIDList[i]}") for i in range(len(facilityUIDList))])
    bookingDate = DateField('Booking Date: ',
                                validators=[InputRequired()],
                                # format='%d/%m/%y',
                                render_kw={'placeholder' : 'DD-MM-YY'})
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
    expirationDate = DateField('Expiration Date: ',
                                validators=[DataRequired()],
                                render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    submit = SubmitField('Book Facility')
    
# Use data from facilitiesdb for choices
# Set restrictions using data from facilitiesdb
# When editting, use data from booking as placeholder