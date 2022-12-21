from flask import Flask, render_template, url_for, flash, redirect, request, session
import shelve
import secrets

from wtforms.validators import ValidationError
from forms import RegistrationForm, LoginForm, EditForm
from eventForms import eventCreateForm, eventEditForm, eventDeleteForm, eventEditForm2, eventDeleteForm2
from bookingForms import bookingForm, paymentForm
from FacilitiesForm import CreateFacilityForm

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
    
    if editForm.validate_on_submit():
        user = User(userName, userFirst, userLast, userEmail, userID, userPass)
        dictsUser[user.get_uid()] = user
        db['Users'] = dictsUser

        return redirect(url_for('users'))
    
    return render_template('Users/userEdit.html', editForm = editForm)

@app.route('/delete/<id>', methods=['GET', 'POST'])
def deleteUser(id):
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
        eventID = formEvents.eventID.data
        eventType = formEvents.eventType.data
        
        ce = createEvents(eventName, eventDesc, eventVacancy, eventDate, eventID, eventType)
        eventsDict[ce.get_eventID()] = ce
        eventDB['Events'] = eventsDict
        
        eventDB.close()
        
        return redirect(url_for('eventsPage'))
    return render_template('Events/eventCreate.html', formEvents=formEvents)    

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
    return render_template('Events/eventEdit.html', formEvents = formEvents)

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
        eventID = id
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
    return render_template('Events/eventEditDirect.html', formEvents = formEvents)

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
        
    return render_template('Events/eventDelete.html', formEvents=formEvents, ce=createEvents)

@app.route('/events/deleteEvents/<int:id>', methods=['GET', 'POST'])
def deleteEventDirect(id):
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

@app.route('/events', methods=['GET', 'POST'])
def eventsPage():
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
def eventSignup():
    return render_template('Events/eventSignUp.html')

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
            print('Error in retrieving events.')

        bookFacilLoc=formsBooking.bookingFacilityLocation.data
        bookFacil = formsBooking.bookingFacilityID.data
        bookDate = formsBooking.bookingDate.data
        bookTime = formsBooking.bookingTimeSlot.data

        bookFacilID = bookFacilLoc+bookFacil

        fb = FacilityBooking(bookFacilID,bookDate,bookTime)
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

@app.route('/booking/bookingPayment')

@app.route('/booking/bookingCurrent', methods=['GET', 'POST'])
def bookingCurrent():
    bookingsDict = {}
    bookingDB = shelve.open('Bookings')
    bookingsDict = bookingDB['Bookings']

    bookingsList=[]
    for booking in bookingsDict:
        bookings = bookingsDict.get(booking)
        bookingsList.append(bookings)

    return render_template('Booking/bookingCurrent.html')

@app.route('/booking/bookingEdit', methods=['GET', 'POST'])
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
            print('Error in retrieving events.')
        
        bookFacilLoc = formsBooking.bookingFacilityLocation.data
        bookFacil = formsBooking.bookingFacilityID.data
        bookDate = formsBooking.bookingDate.data
        bookTime = formsBooking.bookingTimeSlot.data

        bookFacilID = bookFacilLoc+bookFacil

        fb = bookingsDict[id]
        fb.set_facility(bookFacilID)
        fb.set_date(bookDate)
        fb.set_timeslot(bookTime)
        bookingsDict[id] = fb
        bookingDB['Bookings'] = bookingsDict
        
        bookingDB.close()
        print(bookingsDict.keys())

        return redirect(url_for('bookingCurrent'))
    return render_template('Booking/bookingEdit.html', formsBooking = formsBooking)

@app.route('/booking/bookingHistory')
def bookingHistory():
    bookingsDict = {}
    bookingDB = shelve.open('Bookings')
    bookingsDict = bookingDB['Bookings']
    
    bookingsList=[]
    for booking in bookingsDict:
        bookings = bookingsDict.get(booking)
        bookingsList.append(bookings)

    return render_template('Booking/bookingHistory.html')

@app.route('/facilities')
def facilitiesPage():
    facilDict = {}
    facilDB = shelve.open('Facilities')
    facilDict = facilDB['Facilities']
    
    facilList = []
    for facil in facilDict:
        facilities = facilDict.get(facil)
        facilList.append(facilities)
        
    facilLoc = ['Ang Mo Kio', 'Hougang', 'Macpherson', 'Braddell', 'Seletar', 'Golden Mile']
    
    return render_template('Facilities/facilitiesMain.html', facilList = facilList, facilLoc = facilLoc)

@app.route('/facilities/facilitiesCreate', methods=['GET', 'POST'])
def createFacilities():
    formsFacil = CreateFacilityForm()
    facilDict = {}
    facilDB = shelve.open('Facilities')
    if formsFacil.validate_on_submit() and request.method == 'POST':  
        try:
            if 'Events' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Events'] = facilDict
        except:
            print('Error in retrieving events.')
        
        facilLocation = formsFacil.facility_location.data
        location = facilLocation
        
        facilAmt = formsFacil.facility_amount.data
        amt = facilAmt
        
        facilID = location + amt + str(formsFacil.facility_id.data) # Hougang Stadium - 53, Sengkang Stadium - 54BD01 - 06
        facilName = formsFacil.facility_name.data
        facilStatus = formsFacil.facility_status.data
        facilSlots = formsFacil.facility_slots.data 
        
        
        facil = Facilities(facilID, facilName, facilStatus, facilSlots, facilLocation, facilAmt)
        facilDict[facil.get_fac_id()] = facil
        facilDB['Facilities'] = facilDict
        
        facilDB.close()
        return redirect(url_for('facilitiesPage'))
    return render_template('Facilities/facilitiesCreate.html', formsFacil = formsFacil)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
# 700th line :D