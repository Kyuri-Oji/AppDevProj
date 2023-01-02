from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import shelve

class CreateFacilityForm(FlaskForm):
    facility_id = IntegerField('Facility ID : ', 
                               validators=[DataRequired()], render_kw={'placeholder' : '001'})
    facility_status = SelectField('Facility Status : ', 
                                  validators=[DataRequired()], 
                                  choices=[('', 'Select'), ('Available', 'Available'), ('Unavailable', 'Unavailable')],
default='')
    facility_slots = IntegerField('Facility Slots : ', 
                                  validators=[DataRequired()], 
                                  render_kw={'placeholder' : '0'})
    facility_location = SelectField('Facility Location : ',
                                    validators=[DataRequired()],
                                    choices=[('', 'Select'), ('56', 'Ang Mo Kio'), ('53', 'Hougang'), ('37', 'Macpherson'), ('35', 'Braddell'), ('79', 'Seletar'), ('19', 'Golden Mile')])
    facility_amount = SelectField('Facility Type Amount : ',
                                  validators=[DataRequired()],
                                  choices=[('', 'Select'), ('BD', 'Badminton'), ('BB', 'Basketball'), ('SQ', 'Squash'), ('FB', 'Football'), ('TN', 'Tennis'), ('TT', 'Table Tennis')])
    submit = SubmitField('Submit')
    
    def validate_facilID(self, facilID):
        facilDict = {}
        facilDB = shelve.open('Facilities')
        try:
            if 'Facilities' in facilDB:
                facilDict = facilDB['Events']
            else:
                facilDB['Events'] = facilDict
        except:
            print('Error in retrieving events.')
        
        for keys in facilDict:
            if self.facility_id.data == facilDict[keys].get_fac_id():
                raise ValidationError('Facility ID already taken!')


class EditFacilityForm(FlaskForm):
    edit_facility_id = StringField('Facility ID to edit : ',
                                     validators=[DataRequired()])
    edit_facility_status = SelectField('Edit Facility Status (Leave empty if no changes) : ',
                                     choices=[('', 'Select'), ('Available', 'Available'), ('Unavailable', 'Unavailable')], default='')
    edit_facility_slots = IntegerField('Edit Factility Slots: ',
                                     render_kw={'placeholder' : '0 (Leave empty if no changes'})
    edit_facility_location = SelectField('Facility Location : ',
                                    choices=[('', 'Select'), ('56', 'Ang Mo Kio'), ('53', 'Hougang'), ('37', 'Macpherson'), ('35', 'Braddell'), ('79', 'Seletar'), ('19', 'Golden Mile')])
    edit_facility_amount = SelectField('Facility Type: ',
                                  choices=[('', 'Select'), ('BD', 'Badminton'), ('BB', 'Basketball'), ('SQ', 'Squash'), ('FB', 'Football'), ('TN', 'Tennis'), ('TT', 'Table Tennis')])
    submit = SubmitField('Submit') 