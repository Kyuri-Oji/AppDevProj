from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime
import time
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
    eventStartDate = DateTimeField('Event Start Date : ',
                              validators=[DataRequired()],
                              format='%d-%m-%y', default=datetime.now, #datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    eventID = IntegerField('Event ID : ',
                           validators=[DataRequired()],
                           render_kw={'placeholder' : '001'})
    eventType = RadioField('Event Type : ',
                           validators=[DataRequired()],
                           choices=[('Sports', 'Sports'), ('Lifestyle', 'Lifestyle'), ('Others', 'Others')])
    eventLocation =  SelectField('Facility Location : ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'), ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    eventVenue = SelectField('Event Venue : ',
                             validators=[DataRequired()],
                             choices=[('', 'Select'), ('Event Hall', 'Event Hall (Max 100 People)'), ('Badminton Court', 'Badminton Court (Max 15 People)')])
    eventStatus = SelectField('Event Status : ',
                              validators=[DataRequired()],
                              choices=[('', 'Select'), ('Active', 'Active'), ('Closed', 'Closed')])
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
        
    def validate_eventVacancy(self, eventVenue):
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
            
        eventVenueList = ['Event Hall', 'Badminton Court']
        eventVenueSpace = [100, 15]
        
        if self.eventVenue.data in eventVenueList:
            index = eventVenueList.index(self.eventVenue.data)
            
            eventVenueMaxVal = eventVenueSpace[index]
            print(eventVenueMaxVal)
            if self.eventVacancy.data > eventVenueMaxVal:
                print(f'Maximum amount of vacancies is {eventVenueMaxVal}')

                raise ValidationError(f'Max Event Vacancies is {eventVenueMaxVal}!')
    
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
    editEventStartDate = DateTimeField('Event Start Date : ',
                              validators=[],
                              format='%d-%m-%y',#datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    editEventType = RadioField('Edit Event Type : ',
                               validators=[DataRequired()],
                               choices=[('Sports', 'Sports'), ('Lifestyle', 'Lifestyle'), ('Others', 'Others')])
    editEventLocation =  SelectField('Facility Location : ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'), ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    editEventVenue = SelectField('Event Venue : ',
                             validators=[DataRequired()],
                             choices=[('', 'Select'), ('Event Hall', 'Event Hall (Max 100 People)'), ('Badminton Court', 'Badminton Court (Max 15 People)')])
    editEventStatus = SelectField('Event Status : ',
                              validators=[DataRequired()],
                              choices=[('', 'Select'), ('Active', 'Active'), ('Closed', 'Closed')])
    submit = SubmitField('Edit Events')

class eventEditForm2(FlaskForm):
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
    editEventStartDate = DateTimeField('Event Start Date : ',
                              validators=[],
                              format='%d-%m-%y',#datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    editEventType = RadioField('Edit Event Type : ',
                               validators=[DataRequired()],
                               choices=[('Sports', 'Sports'), ('Lifestyle', 'Lifestyle'), ('Others', 'Others')])
    editEventLocation =  SelectField('Facility Location : ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'), ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    editEventVenue = SelectField('Event Venue : ',
                             validators=[DataRequired()],
                             choices=[('', 'Select'), ('Event Hall', 'Event Hall (Max 100 People)'), ('Badminton Court', 'Badminton Court (Max 15 People)')])
    editEventStatus = SelectField('Event Status : ',
                              validators=[DataRequired()],
                              choices=[('', 'Select'), ('Active', 'Active'), ('Closed', 'Closed')])
    submit = SubmitField('Edit Events')
        
class eventDeleteForm(FlaskForm):
    deleteEventID = IntegerField('Event ID to delete : ', 
                                 validators=[DataRequired()])
    submit = SubmitField('Delete Events')
    
class eventDeleteForm2(FlaskForm):
    deleteEventID = IntegerField('Event ID to delete : ', 
                                 validators=[DataRequired()],
                                 render_kw={'placeholder' : 'Re-enter ID to delete. (Found in URL)'})
    submit = SubmitField('Delete Events')
    
class eventSignup(FlaskForm):
    eventID = IntegerField('Event ID : ', 
                           validators=[DataRequired()])
    submit = SubmitField('Sign Up')
        