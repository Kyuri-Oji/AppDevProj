from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime
import shelve

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
    eventID = IntegerField('Event ID : ',
                           validators=[DataRequired()],
                           render_kw={'placeholder' : '001'})
    eventType = RadioField('Event Type : ',
                           validators=[DataRequired()],
                           choices=[('S', 'Sports'), ('L', 'Lifestyle'), ('O', 'Others')])
    submit = SubmitField('Create Events')
    
    def validate_eventID(self, eventID):
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
        
        for keys in eventsDict:
            if self.eventID.data == eventsDict[keys].get_eventID():
                raise ValidationError('Event ID already taken!')
            
    
class eventEditForm(FlaskForm):
    editEventID = IntegerField('Enter Event ID to Edit : ',
                               validators=[DataRequired()])
    editEventName = StringField('Edit Event Name : ',
                                validators=[],
                                render_kw={'placeholder' : 'Leave empty if no change.'})
    editEventDesc = TextAreaField('Edit Event Descriptrion : ',
                                  validators=[],
                                  render_kw={'placeholder' : 'Leave empty if no change.'})
    editEventVacancy = IntegerField('Edit Event Vacancy : ',
                               validators=[],
                               render_kw={'placeholder' : 'Leave empty if no change.'})
    editEventDate = DateTimeField('Event End Date : ',
                              validators=[],
                              format='%d-%m-%y',#datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    editEventType = RadioField('Edit Event Type : ',
                               validators=[DataRequired()],
                               choices=[('S', 'Sports'), ('L', 'Lifestyle'), ('O', 'Others')])
    submit = SubmitField('Edit Events')
    
    def validate_eventID(self, editEventID):
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
            
        # if self.editEventID.data not in eventsDict.keys():
        #     raise ValidationError('Event ID not found in Database!')
        
class eventDeleteForm(FlaskForm):
    deleteEventID = IntegerField('Event ID to delete : ', 
                                 validators=[DataRequired()])
    submit = SubmitField('Delete Events')
        