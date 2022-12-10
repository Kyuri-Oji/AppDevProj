from flask import Flask, render_template, url_for, flash, redirect, request
import shelve

from forms import RegistrationForm, LoginForm
from wtforms.validators import ValidationError
from eventForms import eventCreateForm, eventEditForm, eventDeleteForm, eventEditForm2, eventDeleteForm2
from bookingForms import bookingForm, paymentForm
from FacilitiesForms import CreateFacilityForm

from OOP.userFunction import *
from OOP.eventFunction import *
from OOP.Bookings import *
from OOP.Facilities import *

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
        userID = User.get_random_UID(None) #DO NOT TOUCH, I REPEAT, DO NOT EVER TOUCH, IT WILL CAUSE A NUCLEAR MELTDOWN
        userPass = form.password.data
        
        user = User(userName, userFirstName, userLastName, userEmail, userID, userPass)
        dictUsers[user.get_random_UID()] = user
        db['Users'] = dictUsers
        
        db.close()
        return redirect(url_for('home'))
    return render_template('registration.html', title = 'Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@activeplay.sg' and form.password.data == 'password':
            flash('You have been logged in as an administrator.', 'login')
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
    return render_template('Events/eventEdit.html', formEvents = formEvents)\

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
    formEvents = eventDeleteForm2()
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
        eventID = id
        
        if eventID not in eventsDict.keys():
            flash('Event ID not found!', 'error')
        else:
            eventsDict.pop(eventID)  
            eventDB['Events'] = eventsDict  
            return redirect(url_for('eventsPage'))
        
    return render_template('Events/eventDelete.html', formEvents=formEvents, ce=createEvents)

@app.route('/events', methods=['GET', 'POST'])
def eventsPage():
    formEventsEdit = eventEditForm()
    eventsDict = {}
    eventDB = shelve.open('Events')
    eventsDict = eventDB['Events']
    
    eventsList = []
    for event in eventsDict:
        events = eventsDict.get(event)
        eventsList.append(events)
        
    eventTypeList = ['Sports', 'Lifestyle', 'Others']
  
    return render_template('Events/eventMain.html', eventsList = eventsList, eventType = eventTypeList, formEventsEdit=formEventsEdit)


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
    
        bookFacil = formsBooking.bookingFacility.data
        bookDate = formsBooking.bookingDate.data
        bookTime = formsBooking.bookingTimeSlot.data

        fb = FacilityBooking(bookFacil,bookDate,bookTime)
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

@app.route('/booking/bookingCurrent')
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
def editBookings():
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
    
        bookFacil = formsBooking.bookingFacility.data
        bookDate = formsBooking.bookingDate.data
        bookTime = formsBooking.bookingTimeSlot.data

        fb = FacilityBooking(bookFacil,bookDate,bookTime)
        bookingsDict[fb.get_booking_id()] = fb
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