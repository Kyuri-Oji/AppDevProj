from flask import Flask, render_template, url_for, flash, redirect, request
import shelve

from forms import RegistrationForm, LoginForm
from wtforms.validators import ValidationError
from eventForms import eventCreateForm, eventEditForm, eventDeleteForm

from OOP.userFunction import *
from OOP.eventFunction import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '8ecce6a32ba6703d10b72f3ccea07175'

# Main pages
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title = 'Home')

@app.route('/contact')
@app.route('/about')
def contact():
    return render_template('forms.html')

@app.route('/overview')
def overview():
    return render_template('overview.html', title = 'Overview')

# User Functions
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        
        dictUsers = {}
        db = shelve.open('users', 'c')
        
        try:
            dictUsers = db['Users']
        except:
            print('Error in retrieving users from user.db.')
            
        userName = form.username.data
        userFirstName = form.firstName.data
        userLastName =  form.lastName.data
        userEmail = form.email.data
        userID = User.set_uid(0, len(dictUsers))
        userPass = form.password.data
        
        def __str__():
            return f'{User.set_uid}'
        
        user = User(userName, userFirstName, userLastName, userEmail, userID, userPass)
        dictUsers[user.get_uid()] = user
        db['Users'] = dictUsers
        
        db.close()

        flash(f'Account created for {form.username.data}!', '')
        return redirect(url_for('home'))
    return render_template('registration.html', title = 'Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', '')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title = 'Login', form=form)

@app.route('/users')
def users():
    dictsUser ={}
    db = shelve.open('users')
    dictsUser = db['Users']
    
    userList = []
    for users in dictsUser:
        user = dictsUser.get(users)
        userList.append(user)
        
    return render_template('Users/viewUsers.html', userList = userList)
    
# Event Functions
@app.route('/events/createEvents', methods=['GET', 'POST'])
def createEvent():
    formEvents = eventCreateForm()
    if formEvents.validate_on_submit() and request.method == 'POST':  
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
                     
        eventName = formEvents.eventName.data
        eventDesc = formEvents.eventDesc.data
        eventVacancy = formEvents.eventVacancy.data
        eventDate = formEvents.eventDate.data
        eventID = formEvents.eventID.data
        eventType = formEvents.eventType.data
        
        ce = createEvents(eventName, eventDesc, eventVacancy, eventDate, eventID, eventType)
        eventsDict[ce.get_eventID()] = ce
        eventDB['Events'] = eventsDict
        
        eventDB.close()
        
        return redirect(url_for('eventsPage'))
    return render_template('Events/eventCreate.html', formEvents=formEvents)    

@app.route('/events/editEvents', methods=['GET', 'POST'])
def editEvent():
    formEvents = eventEditForm()
    if formEvents.validate_on_submit() and request.method == 'POST':
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
            
        eventName = formEvents.editEventName.data
        eventDesc = formEvents.editEventDesc.data
        eventVacancy = formEvents.editEventVacancy.data
        eventDate = formEvents.editEventDate.data
        eventID = formEvents.editEventID.data
        eventType = formEvents.editEventType.data
        
        if eventID not in eventsDict.keys():
            print('Error.')
            flash('Event ID not found in Event Database.', 'error')
        else:
            ce = createEvents(eventName, eventDesc, eventVacancy, eventDate, eventID, eventType)
            eventsDict[ce.get_eventID()] = ce
            eventDB['Events'] = eventsDict
            
            eventDB.close()
            print(eventsDict.keys())
                    
            return redirect(url_for('eventsPage'))
    return render_template('Events/eventEdit.html', formEvents = formEvents)

@app.route('/events/deleteEvents', methods=['GET', 'POST'])
def deleteEvent():
    formEvents = eventDeleteForm()
    if formEvents.validate_on_submit() and request.method == 'POST':
        eventDB = shelve.open('Events')
        eventsDict = {}
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
        eventID = formEvents.deleteEventID.data
        
        if eventID not in eventsDict.keys():
            flash('Event ID not found!', 'error')
        else:
            eventsDict.pop(eventID)  
            eventDB['Events'] = eventsDict  
        
    return render_template('Events/eventDelete.html', formEvents=formEvents)

@app.route('/events')
def eventsPage():
    eventsDict = {}
    eventDB = shelve.open('Events')
    eventsDict = eventDB['Events']
    
    eventsList = []
    for event in eventsDict:
        events = eventsDict.get(event)
        eventsList.append(events)
    
    return render_template('Events/eventMain.html', eventsList = eventsList)

# Booking functions
@app.route('/booking')
def bookingPage():
    eventsDict = {}
    eventDB = shelve.open('Events')
    eventsDict = eventDB['Events']
    
    eventsList = []
    for event in eventsDict:
        events = eventsDict.get(event)
        eventsList.append(events)

    return render_template('Booking/bookingMain.html')

@app.route('/booking/bookingPayment')

@app.route('/booking/bookingCurrent')
def bookingCurrent():
    return render_template('Booking/bookingCurrent.html')

@app.route('/facilities')
def facilitiesPage():
    return render_template('Facilities/facilitiesMain.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)