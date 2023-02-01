from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from datetime import datetime
import time
import shelve

facilDict = {}
facilDB = shelve.open('Facilities')
try:    
    if 'Facilites' in facilDB:
        facilDict = facilDB['Facilities']
    else:
        facilDB['Facilites'] = facilDict
except:
    print('Error in retrieving facilites.')

facilIDList = []
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
        
print(facilityUIDList)
print(facilityIDList)

class eventLocationCreateForm(FlaskForm):
    eventLocation =  SelectField('Facility Location : ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'),
                                         ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    
    submit = SubmitField('Next ')

class eventCreateForm(FlaskForm):
    eventName = StringField('Event Name :', 
                            validators=[DataRequired(), Length(min = 2, max = 30)])
    eventDesc = TextAreaField('Event Description : ',
                            validators=[DataRequired(), Length(min = 2)])
    eventVacancy = IntegerField('Event Vacancy : ',
                                validators=[DataRequired()])
    eventDate = DateTimeField('Event End Date : ',
                              validators=[DataRequired()],
                              format='%d-%m-%y %H:%M:%S', default=datetime.now, #datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    eventStartDate = DateTimeField('Event Start Date : ',
                              validators=[DataRequired()],
                              format='%d-%m-%y %H:%M:%S', default=datetime.now, #datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    eventID = IntegerField('Event ID : ',
                           validators=[DataRequired(message="This field is required."), NumberRange(min=1000, max=9999)],
                           render_kw={'placeholder' : '001'})
    eventType = RadioField('Event Type : ',
                           validators=[DataRequired()],
                           choices=[('Sports', 'Sports'), ('Lifestyle', 'Lifestyle'), ('Others', 'Others')])
    eventLocation =  SelectField('Facility Location : ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'), ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    eventVenue = SelectField('Event Venue : ',
                             validators=[DataRequired()],
                             choices=[(facilityIDList[i], f"{facilityUIDList[i]} - {facilityIDList[i]}") for i in range(len(facilityUIDList))])
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
        facilitySlotsList = []
        for facil in facilDict:
            facils = facilDict.get(facil)
            facilAvailability = facils.get_fac_status()
            if facilAvailability == 'Available':             
                facilityID = facils.get_fac_id()
                facilityIDList.append(facilityID)
                
                facilitySlots = facils.get_fac_slots()
                facilitySlotsList.append(facilitySlots)
                
        eventVenueChosen = self.eventVenue.data
        eventVacancyChosen = self.eventVacancy.data
        if eventVenueChosen in facilityIDList:
            index = facilityIDList.index(eventVenueChosen)
            if eventVacancyChosen > facilitySlotsList[index]:
                raise ValidationError(f'Max Event Vacancies is {facilitySlotsList[index]}!')
            
        print(facilityIDList)
        
    def validate_eventDate(self, eventDate): # Dont touch this.
        dateFormat = "%d%m%y%H%M%S"
        
        startDate = (self.eventStartDate.data)
        startDateData = startDate.strftime(dateFormat)
        print(f'Start Date : {startDate}')
        
        endDate = (self.eventDate.data)
        endDateData = endDate.strftime(dateFormat)
        print(f'End Date : {endDate}')
        
        if int(endDateData) < int(startDateData):
            print('Please work man')
            raise ValidationError('End Date cannot be before Start Date')
            
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
                              format='%d-%m-%y %H:%M:%S',#datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    editEventStartDate = DateTimeField('Event Start Date : ',
                              validators=[],
                              format='%d-%m-%y %H:%M:%S',#datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    editEventType = RadioField('Edit Event Type : ',
                               validators=[DataRequired()],
                               choices=[('Sports', 'Sports'), ('Lifestyle', 'Lifestyle'), ('Others', 'Others')])
    editEventLocation =  SelectField('Facility Location : ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'), ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    editEventVenue = SelectField('Event Venue : ',
                             validators=[DataRequired()],
                             choices=[(facilityIDList[i], f"{facilityUIDList[i]} - {facilityIDList[i]}") for i in range(len(facilityUIDList))])
    editEventStatus = SelectField('Event Status : ',
                              validators=[DataRequired()],
                              choices=[('', 'Select'), ('Active', 'Active'), ('Closed', 'Closed')])
    submit = SubmitField('Edit Events')

class eventEditForm2(FlaskForm):
    editEventName = StringField('Edit Event Name : ',
                                validators=[DataRequired()],
                                render_kw={'placeholder' : 'Leave empty if no change.'})
    editEventDesc = TextAreaField('Edit Event Descriptrion : ',
                                  validators=[DataRequired()],
                                  render_kw={'placeholder' : 'Leave empty if no change.'})
    editEventVacancy = IntegerField('Edit Event Vacancy : ',
                               validators=[DataRequired()],
                               render_kw={'placeholder' : 'Leave empty if no change.'})
    editEventDate = DateTimeField('Event End Date : ',
                              validators=[DataRequired()],
                              format='%d-%m-%y %H:%M:%S',#datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    editEventStartDate = DateTimeField('Event Start Date : ',
                              validators=[DataRequired()],
                              format='%d-%m-%y %H:%M:%S',#datetime formatting, dafault to current date
                              render_kw={'placeholder' : 'DD-MM-YY'}) #adds a placeholder
    editEventType = RadioField('Edit Event Type : ',
                               validators=[DataRequired()],
                               choices=[('Sports', 'Sports'), ('Lifestyle', 'Lifestyle'), ('Others', 'Others')])
    editEventLocation =  SelectField('Facility Location : ',
                                validators=[DataRequired()],
                                choices=[('', 'Select'), ('Ang Mo Kio', 'Ang Mo Kio'), ('Hougang', 'Hougang'), ('Macpherson', 'Macpherson'), ('Braddell', 'Braddell'), ('Seletar', 'Seletar'), ('Golden Mile', 'Golden Mile')])
    editEventVenue = SelectField('Event Venue : ',
                             validators=[DataRequired()],
                             choices=[(facilityIDList[i], f"{facilityUIDList[i]} - {facilityIDList[i]}") for i in range(len(facilityUIDList))])
    editEventStatus = SelectField('Event Status : ',
                              validators=[DataRequired()],
                              choices=[('', 'Select'), ('Active', 'Active'), ('Closed', 'Closed')])
    submit = SubmitField('Edit Events')
    
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
        facilitySlotsList = []
        for facil in facilDict:
            facils = facilDict.get(facil)
            facilAvailability = facils.get_fac_status()
            if facilAvailability == 'Available':             
                facilityID = facils.get_fac_id()
                facilityIDList.append(facilityID)
                
                facilitySlots = facils.get_fac_slots()
                facilitySlotsList.append(facilitySlots)
                
        eventVenueChosen = self.eventVenue.data
        eventVacancyChosen = self.eventVacancy.data
        if eventVenueChosen in facilityIDList:
            index = facilityIDList.index(eventVenueChosen)
            if eventVacancyChosen > facilitySlotsList[index]:
                raise ValidationError(f'Max Event Vacancies is {facilitySlotsList[index]}!')
        
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
        
class eventSearchForm(FlaskForm):
    eventSearchItem = StringField('Search : ',
                                  validators=[DataRequired(message='Search input cannot be empty')])
    submit = SubmitField('Search')