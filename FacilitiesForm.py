from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import shelve

class CreateFacilityForm(FlaskForm):
    facility_id = IntegerField('Facility Number : ', 
                               validators=[DataRequired(message="Enter number for the facility.")], render_kw={'placeholder' : '001'})
    facility_status = SelectField('Facility Status : ', 
                                  validators=[DataRequired(message="Enter the number of slots.")], 
                                  choices=[('', 'Select'), ('Available', 'Available'), ('Unavailable', 'Unavailable')],
default='')
    facility_slots = IntegerField('Facility Slots : ', 
                                  validators=[(DataRequired())], 
                                  render_kw={'placeholder' : '0'})
    facility_location = SelectField('Facility Location : ',
                                    validators=[DataRequired()],
                                    choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'), ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    facility_type = SelectField('Facility Type : ',
                                  validators=[DataRequired()],
                                  choices=[('', 'Select'), ('Badminton', 'Badminton'), ('Basketball', 'Basketball'), ('Squash', 'Squash'), ('Football', 'Football'), ('Tennis', 'Tennis'), ('Table Tennis', 'Table Tennis')])
    facility_rates = StringField('Facility Rates ($) : ',
                                  validators=[DataRequired()], render_kw={'placeholder' : '0.00'})
    submit = SubmitField('Submit')

    def validate_facility_slots(self, facility_slots):
        slots = int(self.facility_slots.data)
        if slots < 0:
            raise ValidationError("Slots can not be negative.")
    
    def validate_facility_rates(self, facility_rates):
        rates = (self.facility_rates.data)
        try:
            float(rates)
        except:
            raise ValidationError("Rates must be in numerical values.")

# ur def validates are not a validator in flask, u cant put them inside  the form, jus leave it it works on its own

class EditFacilityForm(FlaskForm):
    edit_facility_id = StringField('Facility Name to edit : ',
                                    validators=[DataRequired()])
    edit_facility_status = SelectField('Edit Facility Status : ',
                                     choices=[('', 'Select'), ('Available', 'Available'), ('Unavailable', 'Unavailable')], default='')
    edit_facility_slots = IntegerField('Edit Factility Slots: ',
                                     render_kw={'placeholder' : '0'})
    edit_facility_location = SelectField('Edit Facility Location : ',
                                    choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'), ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    edit_facility_type = SelectField('Edit Facility Type: ',
                                  choices=[('', 'Select'), ('Badminton', 'Badminton'), ('Basketball', 'Basketball'), ('Squash', 'Squash'), ('Football', 'Football'), ('Tennis', 'Tennis'), ('Table Tennis', 'Table Tennis')])
    edit_facility_rates = StringField('Edit Facility Rates ($) : ',
                                  validators=[DataRequired()], render_kw={'placeholder' : '0.00'})
    submit = SubmitField('Submit') 

    def validator_edit_facility_id(self, edit_faacility_id):
        if len(self.edit_facility_id.data) < 0:
            raise ValidationError('This field is required.')
    
    def validate_edit_facility_rates(self, edit_facility_rates):
        rates = (self.edit_facility_rates.data)
        try:
            float(rates)
        except:
            raise ValidationError("Rates must be in numerical values.")

class SearchFacilityForm(FlaskForm):
    facilitySearchItem = StringField('Search: ',
                                    validators=[DataRequired(message='Search input cannot be empty')])
    submit = SubmitField('Search')