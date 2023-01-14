from flask import Flask, render_template, url_for, flash, redirect, request, session
import shelve
import secrets
import random

from wtforms.validators import ValidationError
from forms import RegistrationForm, LoginForm, EditForm
from eventForms import eventCreateForm, eventEditForm, eventDeleteForm, eventEditForm2, eventDeleteForm2
from bookingForms import bookingForm, paymentForm
from FacilitiesForm import CreateFacilityForm, EditFacilityForm

from OOP.userFunction import *
from OOP.eventFunction import *
from OOP.Bookings import *
from OOP.Facilities import *


app = Flask(__name__)
app.config['SECRET_KEY'] = '8ecce6a32ba6703d10b72f3ccea07175'
app.config["SESSION_PERMANENT"] = False

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
        db = shelve.open('users')
        
        try:
            dictUsers = db['Users']
        except:
            print('Error in retrieving users from user.db.')
            
        userName = form.username.data
        userFirstName = form.firstName.data
        userLastName =  form.lastName.data
        userEmail = form.email.data
        userID = str(User.get_random_UID(User)) #DO NOT TOUCH, I REPEAT, DO NOT EVER TOUCH, IT WILL CAUSE A NUCLEAR MELTDOWN
        userPass = form.password.data
        
        user = User(userName, userFirstName, userLastName, userEmail, userID, userPass)
        dictUsers[user.get_uid()] = user
        db['Users'] = dictUsers
        
        db.close()
        return redirect(url_for('home'))
    return render_template('registration.html', title = 'Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    dictsUser ={}
    db = shelve.open('users')
    try:
        dictsUser = db['Users']
    except:
        print('Error in User.db')

    userList = []
    userNameList = []
    userEmailList = []
    userFirstList = []
    userLastList = []
    user48afe0ac895d0a6229298679 = [] # For safety reasons, this isnt called userPassList
    
    for users in dictsUser:
        user = dictsUser.get(users)
        userID = user.get_uid()
        userList.append(userID)

        userName = user.get_username()
        userNameList.append(userName)
        
        userEmail = user.get_email()
        userEmailList.append(userEmail)
        
        userFirst = user.get_firstName()
        userFirstList.append(userFirst)
        
        userLast = user.get_lastName()
        userLastList.append(userLast)
        
        userPass = user.get_password()
        user48afe0ac895d0a6229298679.append(userPass)
        
    print(userList)
    print(userEmailList)
            
    if form.validate_on_submit():
        if form.email.data == 'admin@activeplay.sg' and form.password.data == 'password':
            flash('You have been logged in as an administrator.', 'login')
            userName = "Administrator"
            userID = '0000000'
            userEmail = 'admin@activeplay.sg'
            userFirst = 'Admin'
            userLast = '-'
            session['User'] = [userName, userID, userEmail, userFirst, userLast]
            return redirect(url_for('home'))
        
        elif form.email.data in userEmailList:
            index = userEmailList.index(form.email.data)
            if form.password.data == user48afe0ac895d0a6229298679[index]:
                userName = userNameList[index]
                userID = userList[index]
                userEmail = userEmailList[index]
                userFirst = userFirstList[index]
                userLast = userLastList[index]
                session['User'] = [userName, userID, userEmail, userFirst, userLast]
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password.', 'danger')
            
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
        
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Users/viewUsers.html', userList = userList) 
    else:
        return render_template('404.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def editUser(id):
    editForm = EditForm()
    if editForm.validate_on_submit() and request.method == 'POST':
        dictsUser ={}
        db = shelve.open('users')
        try:
            if 'Users' in db:
                dictsUser = db['Users']
            else:
                db['Users'] = dictsUser
        except:
            print('An Unknown Error Occured')
        print(dictsUser)
        
        userID = id
        
        currentUser = dictsUser.get(userID)
        currentUserPass = currentUser.get_password()
        
        userName = editForm.editUsername.data
        userFirst = editForm.editFirstName.data
        userLast = editForm.editLastName.data
        userEmail = editForm.editEmail.data
        userPass = currentUserPass
        print(userID)
        
        
        user = User(userName, userFirst, userLast, userEmail, userID, userPass)
        dictsUser[user.get_uid()] = user
        db['Users'] = dictsUser

        return redirect(url_for('users'))
    
    else:
        dictsUser ={}
        db = shelve.open('users')
        try:
            if 'Users' in db:
                dictsUser = db['Users']
            else:
                db['Users'] = dictsUser
        except:
            print('An Unknown Error Occured')
        print(dictsUser)
        
        users = dictsUser.get(id)
        editForm.editUsername.data = users.get_username()
        editForm.editFirstName.data = users.get_firstName()
        editForm.editLastName.data = users.get_lastName()
        editForm.editEmail.data = users.get_email()
        
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Users/userEdit.html', editForm = editForm)
    else:
        return render_template('404.html')

@app.route('/delete/<id>', methods=['GET', 'POST'])
def deleteUser(id):
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        dictsUsers = {}
        db = shelve.open('users')
        try:
            if 'Users' in db:
                dictsUsers = db['Users']
            else:
                db['Users'] = dictsUsers
        except:
            print('An Unknown Error Occured.')
            
        userID = id
        dictsUsers.pop(userID)
        db['Users'] = dictsUsers
        
        return redirect(url_for('users'))
    else:
        return render_template('404.html')

# DO NOT TOUCH, NO CLUE WHY IT WORKS, IT JUST DOES - WE DON'T KNOW HOW EITHER - CONSULT BUDDHA @ 404
@app.route('/<user>', methods=['GET', 'POST'])
def account(user):
    form = LoginForm()
    if request.method == 'POST':
        return render_template('Users/userAccount.html', user = session['User'][0]) # TODO: Change how the url looks
    else:
        return redirect(url_for('home'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('User', None)
    session.pop('UserID', None)
    return redirect(url_for('home'))

@app.route('/admin')
def adminWorkspace():
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Users/adminWorkspace.html') 
    else:
        return render_template('404.html')

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
        eventStartDate = formEvents.eventStartDate.data
        eventID = formEvents.eventID.data
        eventType = formEvents.eventType.data
        eventLocation = formEvents.eventLocation.data        
        eventVenue = formEvents.eventVenue.data
        eventStatus = formEvents.eventStatus.data    
            
        ce = createEvents(eventName, eventDesc, eventVacancy, eventDate, eventStartDate, eventID, eventType, eventLocation, eventVenue, eventStatus)
        eventsDict[ce.get_eventID()] = ce
        eventDB['Events'] = eventsDict
        
        return redirect(url_for('eventsPage'))
    
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Events/eventCreate.html', formEvents=formEvents)   
    else:
        return render_template('404.html') 

# EDIT EVENTS ROUTING
@app.route('/events/editEvents', methods=['GET', 'POST'])
def editEvent():
    # DO NOT TOUCH!!!!!!!!
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
        
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Events/eventEdit.html', formEvents = formEvents)
    else:
        return render_template('404.html')

@app.route('/events/editEvents/<int:id>', methods=['GET', 'POST'])
def editEventDirect(id):
    # DO NOT TOUCH!!!!!!!!
    formEvents = eventEditForm2()
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
        eventStartDate = formEvents.editEventStartDate.data
        eventID = id
        eventType = formEvents.editEventType.data
        eventLocation = formEvents.editEventLocation.data
        eventVenue = formEvents.editEventVenue.data
        eventStatus = formEvents.editEventStatus.data
        
        if eventID not in eventsDict.keys():
            print('Error.')
            flash('Event ID not found in Event Database.', 'error')
        else:
            ce = createEvents(eventName, eventDesc, eventVacancy, eventDate, eventStartDate, eventID, eventType, eventLocation, eventVenue, eventStatus)
            eventsDict[ce.get_eventID()] = ce
            eventDB['Events'] = eventsDict
            
            eventDB.close()
            print(eventsDict.keys())
                    
            return redirect(url_for('eventsPage'))
        
    else:
        eventsDict = {}
        eventDB = shelve.open('Events')
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
        
        print(eventsDict)
        event = eventsDict.get(id)
        print(event)
        formEvents.editEventName.data = event.get_eventName()
        formEvents.editEventDesc.data = event.get_eventDesc()
        formEvents.editEventVacancy.data = event.get_eventVacancy()
        formEvents.editEventDate.data = event.get_eventDate()
        formEvents.editEventStartDate.data = event.get_eventStartDate()
        formEvents.editEventType.data = event.get_eventType()
        formEvents.editEventLocation.data = event.get_eventLocation()
        formEvents.editEventVenue.data = event.get_eventVenue()
        formEvents.editEventStatus.data = event.get_eventStatus()
        
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Events/eventEditDirect.html', formEvents = formEvents)
    else:
        return render_template('404.html')

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
            return redirect(url_for('eventsPage'))
        
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Events/eventDelete.html', formEvents=formEvents, ce=createEvents)
    else:
        return render_template('404.html')

@app.route('/events/deleteEvents/<int:id>', methods=['GET', 'POST'])
def deleteEventDirect(id):
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        eventDB = shelve.open('Events')
        eventsDict = {}
        try:
            if 'Events' in eventDB:
                eventsDict = eventDB['Events']
            else:
                eventDB['Events'] = eventsDict
        except:
            print('Error in retrieving events.')
        eventID = id

        eventsDict.pop(eventID)  
        eventDB['Events'] = eventsDict  
        return redirect(url_for('eventsPage'))
    else:
        return render_template('404.html')

@app.route('/events', methods=['GET', 'POST'])
def eventsPage():
    eventsDict = {}
    eventDB = shelve.open('Events')
    eventsDict = eventDB['Events']
    
    eventsList = []
    for event in eventsDict:
        events = eventsDict.get(event)
        eventsList.append(events)
    
    # Please do not touch this, I really have no clue how to solve this if broken.
    eventSports = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Sports' in events.get_eventType():
            eventSports.append(events)
    
    eventLifestyle = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Lifestyle' in events.get_eventType():
            eventLifestyle.append(events)
        
    eventOthers = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Others' in events.get_eventType():
            eventOthers.append(events)
    
    eventTypeList = ['Sports', 'Lifestyle', 'Others']
    eventTypeDict = {'Sports' : eventSports, 'Lifestyle' : eventLifestyle, 'Others' : eventOthers}
    
    
    eventSignUp = []
    eventSignUpDict = {}
    eventSignUpDB = shelve.open('eventSignUp')
    try:
        if 'eventSignUp' in eventSignUpDB:
            eventSignUpDict = eventSignUpDB['eventSignUp']
        else:
            eventSignUpDB['eventSignUp'] = eventSignUpDict
    except:
        print('An Unknown Error Occured.')
    
    eventSignUp = eventSignUpDict
    print(eventSignUp)
            
    return render_template('Events/eventMain.html', eventsList = eventsList, eventType = eventTypeList, eventSports = eventSports, eventLifestyle = eventLifestyle, eventOthers = eventOthers, eventTypeDict = eventTypeDict)

@app.route('/events/sports', methods=['GET', 'POST'])
def eventsPageSports():
    eventsDict = {}
    eventDB = shelve.open('Events')
    eventsDict = eventDB['Events']
    
    eventsList = []
    for event in eventsDict:
        events = eventsDict.get(event)
        eventsList.append(events)
    print(eventsList)
    
    # Please do not touch this, I really have no clue how to solve this if broken.
    eventSports = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Sports' in events.get_eventType():
            eventSports.append(events)
    print(eventSports)
    
    eventLifestyle = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Lifestyle' in events.get_eventType():
            eventLifestyle.append(events)
    print(eventLifestyle)
        
    eventOthers = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Others' in events.get_eventType():
            eventOthers.append(events)
    print(eventOthers)
    
    eventTypeList = ['Sports', 'Lifestyle', 'Others']
    
    eventTypeDict = {'Sports' : eventSports, 'Lifestyle' : eventLifestyle, 'Others' : eventOthers}
  
    return render_template('Events/eventSub/eventSports.html',
                           eventsList = eventsList, eventType = eventTypeList, eventSports = eventSports, eventLifestyle = eventLifestyle, eventOthers = eventOthers, eventTypeDict = eventTypeDict)

@app.route('/events/lifestyle', methods=['GET', 'POST'])
def eventsPageLifestyle():
    eventsDict = {}
    eventDB = shelve.open('Events')
    eventsDict = eventDB['Events']
    
    eventsList = []
    for event in eventsDict:
        events = eventsDict.get(event)
        eventsList.append(events)
    print(eventsList)
    
    # Please do not touch this, I really have no clue how to solve this if broken.
    eventSports = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Sports' in events.get_eventType():
            eventSports.append(events)
    print(eventSports)
    
    eventLifestyle = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Lifestyle' in events.get_eventType():
            eventLifestyle.append(events)
    print(eventLifestyle)
        
    eventOthers = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Others' in events.get_eventType():
            eventOthers.append(events)
    print(eventOthers)
    
    eventTypeList = ['Sports', 'Lifestyle', 'Others']
    
    eventTypeDict = {'Sports' : eventSports, 'Lifestyle' : eventLifestyle, 'Others' : eventOthers}
  
    return render_template('Events/eventSub/eventLifestyle.html',
                           eventsList = eventsList, eventType = eventTypeList, eventSports = eventSports, eventLifestyle = eventLifestyle, eventOthers = eventOthers, eventTypeDict = eventTypeDict)

@app.route('/events/others', methods=['GET', 'POST'])
def eventsPageOthers():
    eventsDict = {}
    eventDB = shelve.open('Events')
    eventsDict = eventDB['Events']
    
    eventsList = []
    for event in eventsDict:
        events = eventsDict.get(event)
        eventsList.append(events)
    print(eventsList)
    
    # Please do not touch this, I really have no clue how to solve this if broken.
    eventSports = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Sports' in events.get_eventType():
            eventSports.append(events)
    print(eventSports)
    
    eventLifestyle = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Lifestyle' in events.get_eventType():
            eventLifestyle.append(events)
    print(eventLifestyle)
        
    eventOthers = []
    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Others' in events.get_eventType():
            eventOthers.append(events)
    print(eventOthers)
    
    eventTypeList = ['Sports', 'Lifestyle', 'Others']
    
    eventTypeDict = {'Sports' : eventSports, 'Lifestyle' : eventLifestyle, 'Others' : eventOthers}
  
    return render_template('Events/eventSub/eventOthers.html',
                           eventsList = eventsList, eventType = eventTypeList, eventSports = eventSports, eventLifestyle = eventLifestyle, eventOthers = eventOthers, eventTypeDict = eventTypeDict)

@app.route('/events/signup/<int:id>', methods=['GET', 'POST'])
def eventSignup(id):
    eventSignUpList = []
    eventSignUpDB = shelve.open('eventSignUp')
    eventSignUpDict = {}
    
    # list the userID under the event ID, find users registered to the event not event registered to the user
    eventID = id
    if 'User' in session:
        userID = session['User'][1]

        try:
            if 'eventSignUp' in eventSignUpDB:
                eventSignUpDict = eventSignUpDB['eventSignUp']
            else:
                eventSignUpDB['eventSignUp'] = eventSignUpDict
        except:
            print('An Unknown Error Occured.')
            
        # Check whether event key already in dictionary
        if eventID in eventSignUpDict.keys():
            eventList = []
            
            for events in eventSignUpDict[eventID]:
                eventList.append(events)
                
            if userID not in eventList:
                eventList.append(userID)
                print(eventList)
                eventSignUpDict[eventID] = eventList
                
                eventSignUpDB['eventSignUp'] = eventSignUpDict
            else:
                print('User already registered!')
        else:
            eventSignUpList.append(userID)
            eventSignUpDict[eventID] = eventSignUpList
            eventSignUpDB['eventSignUp'] = eventSignUpDict
            
        return redirect(url_for('eventsPage'))
    else:
        return redirect(url_for('login'))

@app.route('/events/registered', methods=['GET', 'POST'])
def eventRegistered():
    if 'User' in session:
        userID = session['User'][1]
        eventSignUpDB = shelve.open('eventSignUp')
        eventSignUpDict = {}
        
        try:
            if 'eventSignUp' in eventSignUpDB:
                eventSignUpDict = eventSignUpDB['eventSignUp']
            else:
                eventSignUpDB['eventSignUp'] = eventSignUpDict
        except:
            print('An Unknown Error Occured.')

        userRegisteredList = []
        for events in eventSignUpDict:
            if userID in eventSignUpDict[events]:
                userRegisteredList.append(events)
        print(userRegisteredList)
        
        eventsDict = {}
        eventDB = shelve.open('Events')
        eventsDict = eventDB['Events']

        eventInfoID = []
        eventInfoName = []
        eventDisplayName = []
        for i in eventsDict:
            eventID = eventsDict[i].get_eventID()
            print(eventID)
            eventInfoID.append(eventID)
            eventName = eventsDict[i].get_eventName()
            print(eventName)
            eventInfoName.append(eventName)
        
        for id in userRegisteredList:
            index = eventInfoID.index(id)
            eventNameIndex = eventInfoName[index]
            eventDisplayName.append(eventNameIndex)
        
        print(eventDisplayName)
        return render_template('Events/eventRegistered.html', registeredEventList = userRegisteredList, registeredEventName = eventDisplayName)
    else:
        return redirect(url_for('login'))

# Booking functions
@app.route('/booking', methods=['GET', 'POST'])
def bookingPage():
    formsBooking = bookingForm()
    if formsBooking.validate_on_submit() and request.method == 'POST':
        bookingsDict = {}
        bookingDB = shelve.open('Bookings')
        try:
            if 'Bookings' in bookingDB:
                bookingsDict = bookingDB['Bookings']
            else:
                bookingDB['Bookings'] = bookingsDict
        except:
            print('Error in retrieving bookings.')

        bookFacilLoc = formsBooking.bookingFacilityLocation.data
        bookFacilType = formsBooking.bookingFacilityID.data
        bookDate = formsBooking.bookingDate.data
        bookTime = formsBooking.bookingTimeSlot.data

        bookDate = str(bookDate).split(" ")[0]
        bookFacil = bookFacilLoc+bookFacilType

        fb = FacilityBooking(bookFacil,bookDate,bookTime)
        fb.set_booking_id()
        bookingsDict[fb.get_booking_id()] = fb
        bookingDB['Bookings'] = bookingsDict
        
        bookingDB.close()
        print(bookingsDict.keys())

        return redirect(url_for('bookingPayment'))

    return render_template('Booking/bookingMain.html', formsBooking = formsBooking)

@app.route('/booking/bookingPayment', methods=['GET', 'POST'])
def bookingPayment():
    formsPayment = paymentForm()
    if formsPayment.validate_on_submit() and request.method == 'POST':
        payMethod = formsPayment.paymentMethod.data
        cardNum = formsPayment.cardNumber.data
        expireDate = formsPayment.expirationDate.data

        return redirect(url_for('bookingCurrent'))

    return render_template('Booking/bookingPayment.html', formsPayment = formsPayment)

@app.route('/booking/bookingCurrent', methods=['GET', 'POST'])
def bookingCurrent():
    if 'User' in session:
        userID = session['User'][1]
        bookingsDict = {}
        bookingDB = shelve.open('Bookings')
        bookingsDict = bookingDB['Bookings']
    
        bookingsList=[]
        for booking in bookingsDict:
            bookings = bookingsDict.get(booking)
            bookingsList.append(bookings)

        return render_template('Booking/bookingCurrent.html', bookingsList = bookingsList)
    else:
        return redirect(url_for('login'))

@app.route('/booking/bookingEdit/<id>', methods=['GET', 'POST'])
def editBookings(id):
    formsBooking = bookingForm()
    if formsBooking.validate_on_submit() and request.method == 'POST':
        bookingsDict = {}
        bookingDB = shelve.open('Bookings')
        try:
            if 'Bookings' in bookingDB:
                bookingsDict = bookingDB['Bookings']
            else:
                bookingDB['Bookings'] = bookingsDict
        except:
            print('Error in retrieving bookings.')

        bookFacilLoc = formsBooking.bookingFacilityLocation.data
        bookFacilType = formsBooking.bookingFacilityID.data
        bookDate = formsBooking.bookingDate.data
        bookTime = formsBooking.bookingTimeSlot.data

        bookDate = str(bookDate).split(" ")[0]
        bookFacil = bookFacilLoc+bookFacilType

        fb = bookingsDict[id]
        fb.set_facility(bookFacil)
        fb.set_date(bookDate)
        fb.set_timeslot(bookTime)
        bookingsDict[fb.get_booking_id()] = fb
        bookingDB['Bookings'] = bookingsDict
        
        bookingDB.close()
        print(bookingsDict.keys())

        return redirect(url_for('bookingCurrent'))
    return render_template('Booking/bookingEdit.html', formsBooking = formsBooking)

@app.route('/booking/deleteBooking/<id>', methods=['GET', 'POST'])
def deleteBookings(id):
    bookingsDict = {}
    bookingDB = shelve.open('Bookings')
    try:
        if 'Bookings' in bookingDB:
            bookingsDict = bookingDB['Bookings']
        else:
            bookingDB['Bookings'] = bookingsDict
    except:
        print('Error in retrieving bookings.')

    bookingsDict.pop(id)  
    bookingDB['Bookings'] = bookingsDict

    bookingDB.close()
    print(bookingsDict.keys())

    return redirect(url_for('bookingCurrent'))


@app.route('/booking/bookingHistory')
def bookingHistory():
    if 'User' in session:
        userID = session['User'][1]
        bookingsDict = {}
        bookingDB = shelve.open('Bookings')
        bookingsDict = bookingDB['Bookings']
    
        bookingsList=[]
        for booking in bookingsDict:
            bookings = bookingsDict.get(booking)
            bookingsList.append(bookings)
    
        return render_template('Booking/bookingHistory.html')
    else:
        return redirect(url_for('login'))

@app.route('/facilities')
def facilitiesPage():
    facilDict = {}
    facilDB = shelve.open('Facilities')
    facilDict = facilDB['Facilities']
    print(facilDict)
    
    facilList = []
    for facil in facilDict:
        facilities = facilDict.get(facil)
        facilList.append(facilities)
    print(facilList)
        
    facilLoc = ['Ang Mo Kio', 'Hougang', 'Macpherson', 'Braddell', 'Seletar', 'Golden Mile']
    
    return render_template('Facilities/facilitiesMain.html', facilList = facilList, facilLoc = facilLoc)

@app.route('/facilities/facilitiesCreate', methods=['GET', 'POST'])
def createFacilities():
    formsFacil = CreateFacilityForm()
    facilDict = {}
    facilDB = shelve.open('Facilities')
    if formsFacil.validate_on_submit() and request.method == 'POST':   
        try:    
            if 'Facilites' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilites'] = facilDict
        except:
            print('Error in retrieving facilites.')
        
        facilLocation = formsFacil.facility_location.data
        location = facilLocation
        
        facilType = formsFacil.facility_type.data
        type = facilType
        
        facilID = str(formsFacil.facility_id.data) # Hougang Stadium - 53, Sengkang Stadium - 54BD01 - 06
        facilStatus = formsFacil.facility_status.data
        facilSlots = formsFacil.facility_slots.data
        
        uniqueID = len(facilDict)
        uniqueID += 1
        
        facil = Facilities(facilID, facilStatus, facilSlots, facilLocation, facilType, uniqueID)
        facilDict[facil.get_uniqueID()] = facil # get id
        facilDB['Facilities'] = facilDict
        
        
        facilDB.close()
        return redirect(url_for('facilitiesPage'))
    return render_template('Facilities/facilitiesCreate.html', formsFacil = formsFacil)

@app.route('/facilities/facilitiesEdit/', methods=['GET', 'POST'])
def editFacilities():
    formsFacil = EditFacilityForm()
    facilDict = {}
    facilDB = shelve.open('Facilities')
    if formsFacil.validate_on_submit() and request.method == 'POST':  
        try:    
            if 'Facilites' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilites'] = facilDict
        except:
            print('Error in retrieving facilites.')
        
        facilID = formsFacil.edit_facility_id.data
        facilStatus = formsFacil.edit_facility_status.data
        facilSlots = formsFacil.edit_facility_slots.data
        facilLocation = formsFacil.edit_facility_location.data
        facilType = formsFacil.edit_facility_type.data
        
        facilityID = str(facilLocation + facilType + facilID)
        
        if facilityID not in facilDict.keys():
            print('Error.')
            flash('Facility ID not found in Facilities Database.')
        else:
            facil = Facilities(facilityID, facilStatus, facilSlots, facilLocation, facilType, id)
            facilDict[facil.get_uniqueID()] = facil
            facilDB['Facilities'] = facilDict
    
        return redirect(url_for('facilitiesPage'))
    return render_template('Facilities/facilitiesEdit.html', formsFacil = formsFacil)

@app.route('/facilities/facilitiesEdit/<int:id>', methods=['GET', 'POST'])
def editFacilities2(id):
    formsFacil = EditFacilityForm()
    facilDict = {}
    facilDB = shelve.open('Facilities')
    if formsFacil.validate_on_submit() and request.method == 'POST':  
        try:    
            if 'Facilites' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilites'] = facilDict
        except:
            print('Error in retrieving facilites.')
        
        facilLocation = formsFacil.edit_facility_location.data
        location = facilLocation
        
        facilType = formsFacil.edit_facility_type.data
        type = facilType
        
        facilID = str(formsFacil.edit_facility_id.data) # Hougang Stadium - 53, Sengkang Stadium - 54BD01 - 06
        facilStatus = formsFacil.edit_facility_status.data
        facilSlots = formsFacil.edit_facility_slots.data

        
        facil = Facilities(facilID, facilStatus, facilSlots, facilLocation, facilLocation, id)
        facilDict[id] = facil  
        facilDB['Facilities'] = facilDict
        
        facilDB.close()
        return redirect(url_for('facilitiesPage'))
    
    else:
        facilDict = {}
        facilDB = shelve.open('Facilities')
        try:    
            if 'Facilites' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilites'] = facilDict
        except:
            print('Error in retrieving facilites.')
        
        id = int(id)
        if id in facilDict:
            facility = facilDict.get(id)
            print(facility)
            formsFacil.edit_facility_id.data = facility.get_fac_id()
            formsFacil.edit_facility_location.data = facility.get_fac_loc()
            formsFacil.edit_facility_slots.data = facility.get_fac_slots()
            formsFacil.edit_facility_status.data = facility.get_fac_status()
            formsFacil.edit_facility_type.data = facility.get_fac_amt()
            
        else:
            print('An Error Is Here')
            
    return render_template('Facilities/facilitiesEdit.html', formsFacil = formsFacil)

@app.route('/facilities/facilitiesDelete/<id>', methods=['GET', 'POST'])
def deleteFacilitiesDirect(id):
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        facilDB = shelve.open('Facilities')
        facilDict = {}
        try:
            if 'Facilities' in facilDB:
                facilDict = facilDB['Facilities'] 
            else:
                facilDB['Facilities'] = facilDict
        except:
            print('Error in retrieving Facilities.')
        facilID = int(id)

        facilDict.pop(facilID)  
        facilDB['Facilities'] = facilDict  
        return redirect(url_for('facilitiesPage'))
    else:
        return render_template('404.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
# 723rd line :D