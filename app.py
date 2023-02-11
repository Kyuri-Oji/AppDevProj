from flask import Flask, render_template, url_for, flash, redirect, request, session
import shelve
from datetime import datetime, date
import secrets
import random

from wtforms.validators import ValidationError
from forms import RegistrationForm, LoginForm, EditForm, userSearchForm
from eventForms import *
from bookingForms import bookingForm, paymentForm
from FacilitiesForm import CreateFacilityForm, EditFacilityForm, SearchFacilityForm

from OOP.userFunction import *
from OOP.eventFunction import *
from OOP.Bookings import *
from OOP.Facilities import *

from modules.search import *
from modules.sort import *
from modules.refreshList import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '8ecce6a32ba6703d10b72f3ccea07175'
app.config["SESSION_PERMANENT"] = False

# Main pages
@app.route('/')
@app.route('/home')
def home():
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
    
    return render_template('index.html', title = 'Home', eventsList = eventsList, eventSports = eventSports, eventLifestyle = eventLifestyle, eventOthers = eventOthers)

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
        userID = str(User.get_random_UID(User))
        userPhoneNo = form.phoneNo.data
        userDateJoined = (User.get_userJoinDate(User)).strftime("%d/%m/%y")
        userPass = form.password.data
        
        userEmailList = []
        userPhoneNoList = []
        for i in dictUsers:
            userInfo = dictUsers.get(i)
            
            userInfoEmail = userInfo.get_email()
            userEmailList.append(userInfoEmail)
            
            userInfoPhoneNo = userInfo.get_phoneNo()
            userPhoneNoList.append(userInfoPhoneNo)
        
        if form.email.data not in userEmailList and form.phoneNo.data not in userPhoneNoList:
            user = User(userName, userFirstName, userLastName, userEmail, userID, userPhoneNo, userDateJoined, userPass)
            dictUsers[user.get_uid()] = user
            db['Users'] = dictUsers
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
        print('Error in User.db test')

    userList = []
    userNameList = []
    userEmailList = []
    userFirstList = []
    userLastList = []
    userPhoneNoList = []
    userDateJoinedList = []
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
        
        userPhoneNo = user.get_phoneNo()
        userPhoneNoList.append(userPhoneNo)
        
        userDateJoined = user.get_dateJoined()
        userDateJoinedList.append(userDateJoined)
        
        userPass = user.get_password()
        user48afe0ac895d0a6229298679.append(userPass)
    
    try:
        loginPhoneNo = int(form.loginField.data)
        loginEmail = None
    except ValueError:
        loginEmail = form.loginField.data
        loginPhoneNo = None
    except:
        print('Error in logging in.')
            
    if form.validate_on_submit():
        if form.loginField.data == 'admin@activeplay.sg' and form.password.data == 'password':
            flash('You have been logged in as an administrator.', 'login')
            userName = "Administrator"
            userID = '0000000'
            userEmail = 'admin@activeplay.sg'
            userFirst = 'Admin'
            userLast = '-'
            session['User'] = [userName, userID, userEmail, userFirst, userLast]
            return redirect(url_for('home'))
        
        elif loginEmail in userEmailList:
            try:
                index = userEmailList.index(form.loginField.data)
            except:
                flash('Login Unsuccessful. Please check Email/Phone Number and Password.', 'danger')
                return redirect(url_for('login'))
            
            if form.password.data == user48afe0ac895d0a6229298679[index]:
                userName = userNameList[index] # Item 0
                userID = userList[index] # Item 1
                userEmail = userEmailList[index] # Item 2
                userFirst = userFirstList[index] # Item 3
                userLast = userLastList[index] # Item 4
                userPhoneNo = userPhoneNoList[index] # Item 5
                userDateJoined = userDateJoinedList[index] # Item 6
                session['User'] = [userName, userID, userEmail, userFirst, userLast, userPhoneNo, userDateJoined]
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check Email/Phone Number and Password.', 'danger')
                return redirect(url_for('login'))
                
        elif loginPhoneNo in userPhoneNoList:
            try:
                index = userPhoneNoList.index(int(form.loginField.data))
            except: 
                flash('Login Unsuccessful. Please check Email/Phone Number and Password.', 'danger')
                return redirect(url_for('login'))
            
            if form.password.data == user48afe0ac895d0a6229298679[index]:
                userName = userNameList[index] # Item 0
                userID = userList[index] # Item 1
                userEmail = userEmailList[index] # Item 2
                userFirst = userFirstList[index] # Item 3
                userLast = userLastList[index] # Item 4
                userPhoneNo = userPhoneNoList[index] # Item 5
                userDateJoined = userDateJoinedList[index] # Item 6
                session['User'] = [userName, userID, userEmail, userFirst, userLast, userPhoneNo, userDateJoined]
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check Email/Phone Number and Password.', 'danger')
                return redirect(url_for('login'))
                
        else:
            flash('Login Unsuccessful. Please check Email/Phone Number and Password.', 'danger')
            return redirect(url_for('login'))
        
    return render_template('login.html', title = 'Login', form=form)

@app.route('/users', methods=['GET', 'POST'])
def users():
    formSearch = userSearchForm()

    if formSearch.validate_on_submit() and request.method == 'POST':
        userSearchData = formSearch.userSearchItem.data
        
        userSearchFunction(userSearchData)
        userUIDList_searchPage = userSearchUIDList # lists from search.py
        userUsernameList_searchPage = userSearchUsernameList
        userFirstNameList_searchPage = userSearchFirstNameList
        userLastNameList_searchPage = userSearchLastNameList
        userEmailList_searchPage = userSearchEmailList
        userPhoneNoList_searchPage = userSearchPhoneNoList
        
        print(userUIDList_searchPage, userUsernameList_searchPage, userFirstNameList_searchPage, userLastNameList_searchPage, userEmailList_searchPage, userPhoneNoList_searchPage)
        
        return render_template('Users/viewUsers.html', formSearch = formSearch,
                               userUIDList_searchPage = userUIDList_searchPage,
                               userUsernameList_searchPage = userUsernameList_searchPage,
                               userFirstNameList_searchPage = userFirstNameList_searchPage,
                               userLastNameList_searchPage = userLastNameList_searchPage,
                               userEmailList_searchPage = userEmailList_searchPage,
                               userPhoneNoList_searchPage = userPhoneNoList_searchPage, 
                               title = userSearchData)
    
    dictsUser ={}
    db = shelve.open('users')
    dictsUser = db['Users']
        
    userList = []
    for users in dictsUser:
        user = dictsUser.get(users)
        userList.append(user)
        
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Users/viewUsers.html', userList = userList, formSearch = formSearch) 
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
        
        currentDateJoined = currentUser.get_dateJoined()
        
        userName = editForm.editUsername.data
        userFirst = editForm.editFirstName.data
        userLast = editForm.editLastName.data
        userEmail = editForm.editEmail.data
        userPass = currentUserPass
        userPhoneNo = editForm.editPhoneNo.data
        userDateJoined = currentDateJoined
        print(userID)
        
        
        user = User(userName, userFirst, userLast, userEmail, userID, userPhoneNo, userDateJoined, userPass)
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
        editForm.editPhoneNo.data = users.get_phoneNo()
        
        
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
@app.route('/account', methods=['GET', 'POST'])
def account():
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
@app.route('/events/selectEventLocation', methods=['GET', 'POST'])
def selectEventLocation():
    formEvents = eventLocationCreateForm()
    
    eventLocationDict = {}
    eventDB = shelve.open('tempEventLocation')
    
    try:
        if 'eventLocation' in eventDB:
            eventLocationDict = eventDB['eventLocation']
        else:
            eventDB['eventLocation'] = eventLocationDict
    except:
        print('An Error Has Occured.')
    
    if formEvents.validate_on_submit() and request.method == 'POST': 

        eventLocation = formEvents.eventLocation.data
        eventLocationDict['location'] = eventLocation
        eventDB['eventLocation'] = eventLocationDict

        return redirect(url_for('createEvent'))
    
    return render_template('Events/eventLocationSelect.html', formEvents = formEvents)

@app.route('/events/createEvents', methods=['GET', 'POST'])
def createEvent():
    refreshFacilityList()
    
    formEvents = eventCreateForm()
    # Before Form Submission
    formEvents.eventVenue.choices = [(facilityIDList[i], f"{facilityUIDList[i]} - {facilityIDList[i]}") for i in range(len(facilityUIDList))] # refreshes the facility list
    
    facilDict = {}
    facilDB = shelve.open('Facilities')
    try:    
        if 'Facilities' in facilDB:
            facilDict = facilDB['Facilities']
        else:
            facilDB['Facilities'] = facilDict
    except:
        print('Error in retrieving facilities.')
            
    eventLocationDict = {}
    eventLocationDB = shelve.open('tempEventLocation')
    try:
        if 'location' in eventLocationDB:
            eventLocationDict = eventLocationDB['location']
        else:
            eventLocationDB['location'] = eventLocationDict
    except:
        print('Location not found.')
        
    facilityLocationList = []
    for events in eventLocationDict:
        event = eventLocationDict.get(events)
        eventLoc = event[0]
        for facility in facilDict:
            facilityLocation = facility.get_fac_loc()
            if facilityLocation == eventLoc:
                facilityLocationList.append(facility)
    print(facilityLocationList)
            
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
        eventDateTime = formEvents.eventDateTime.data
        eventStartDate = formEvents.eventStartDate.data
        eventStartDateTime = formEvents.eventStartDateTime.data
        eventID = formEvents.eventID.data
        eventType = formEvents.eventType.data
        eventLocation = formEvents.eventLocation.data        
        eventVenue = formEvents.eventVenue.data
        eventStatus = formEvents.eventStatus.data    
            
        ce = createEvents(eventName, eventDesc, eventVacancy, eventDate, eventDateTime, eventStartDate, eventStartDateTime, eventID, eventType, eventLocation, eventVenue, eventStatus)
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
    
    facilDict = {}
    facilDB = shelve.open('Facilities')
    try:    
        if 'Facilities' in facilDB:
            facilDict = facilDB['Facilities']
        else:
            facilDB['Facilities'] = facilDict
    except:
        print('Error in retrieving Facilities.')
        
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
        eventDateTime = formEvents.editEventStartDateTime.data
        eventStartDate = formEvents.editEventStartDate.data
        eventStartDateTime = formEvents.editEventStartDateTime.data
        eventID = id
        eventType = formEvents.editEventType.data
        eventLocation = formEvents.editEventLocation.data
        eventVenue = formEvents.editEventVenue.data
        eventStatus = formEvents.editEventStatus.data
        
        if eventID not in eventsDict.keys():
            print('Error.')
            flash('Event ID not found in Event Database.', 'error')
        else:
            ce = createEvents(eventName, eventDesc, eventVacancy, eventDate, eventDateTime, eventStartDate, eventStartDateTime, eventID, eventType, eventLocation, eventVenue, eventStatus)
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
        formEvents.editEventDateTime.data = event.get_eventDateTime()
        formEvents.editEventStartDate.data = event.get_eventStartDate()
        formEvents.editEventStartDateTime.data = event.get_eventStartDateTime()
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
    formSearch = eventSearchForm()
    formSort = eventSortMultipleForm()
    
    if formSearch.validate_on_submit() and request.method == 'POST':
        eventSearchData = formSearch.eventSearchItem.data
        
        eventSearchFunction(eventSearchData)
        
        eventIDList_searchPage = eventSearchIDList # lists from search.py
        eventNameList_searchPage = eventSearchNameList
        eventLocationList_searchPage = eventSearchLocationList
        eventVenueList_searchPage = eventSearchVenueList
        
        print(eventIDList_searchPage, eventNameList_searchPage, eventLocationList_searchPage, eventVenueList_searchPage)
        
        return render_template('Events/eventMain.html', formSearch = formSearch,
                               eventIDList_searchPage = eventIDList_searchPage,
                               eventNameList_searchPage = eventNameList_searchPage,
                               eventLocationList_searchPage = eventLocationList_searchPage,
                               eventVenueList_searchPage = eventVenueList_searchPage,
                               formSort = formSort,
                               title = eventSearchData)
    
    if formSort.validate_on_submit() and request.method == "POST":
        formSortData = formSort.selectData.data
        
        if formSortData == 'sportEvents':
            eventSortBySport()
            eventSportsList_App = eventSportsList
            
            return render_template('Events/eventMain.html', formSearch = formSearch,
                                   formSort = formSort,
                                   eventSportsListDisplay = eventSportsList_App,
                                   title = "Sports")
            
        elif formSortData == 'lifestyleEvents':
            eventSortByLifestyle()
            eventLifestyleList_App = eventLifestyleList
            
            return render_template('Events/eventMain.html', formSearch = formSearch,
                                   formSort = formSort,
                                   eventLifestyleListDisplay = eventLifestyleList_App,
                                   title = "Lifestyle")
            
        elif formSortData == 'otherEvents':
            eventSortByOthers()
            eventOthersList_App = eventOthersList
            
            return render_template('Events/eventMain.html', formSearch = formSearch,
                                   formSort = formSort,
                                   eventOthersListDisplay = eventOthersList_App,
                                   title = "Others")
            
        elif formSortData == 'dateAscending':
            eventSortByTimeAscending()
            eventTimeList = eventListFinalSort
            
            return render_template('Events/eventMain.html', formSearch = formSearch,
                                   formSort = formSort,
                                   eventTimeList = eventTimeList,
                                   title = "Date (Ascending)")
            
        elif formSortData == 'dateDescending':
            eventSortByTimeDescending()
            eventTimeListDescending = eventListFinalSortDescending
            
            return render_template('Events/eventMain.html', formSearch = formSearch,
                                   formSort = formSort,
                                   eventTimeListDescending = eventTimeListDescending,
                                   title = "Date (Descending)")
        
    eventsDict = {}
    eventDB = shelve.open('Events')
    eventsDict = eventDB['Events']
    
    eventsList = []
    for event in eventsDict:
        events = eventsDict.get(event)
        eventsList.append(events)
    print(eventsList)
        
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
            
    return render_template('Events/eventMain.html', eventsList = eventsList,
                           formSort = formSort,
                           formSearch = formSearch)

# _________________________________________________________________________________________________________________________________________________________________________________________
# Might consider removing, leave here first
@app.route('/events/sports', methods=['GET', 'POST'])
def eventsPageSports():  
    formSearch = eventSearchForm()
    formSortEvents = eventSortForm()
    formSortEventsDescending = eventSortFormDescending()
    
    if formSearch.validate_on_submit() and request.method == 'POST':
        eventSearchData = formSearch.eventSearchItem.data
        
        eventSearchFunction(eventSearchData)
        
        eventIDList_searchPage = eventSearchIDList # lists from search.py
        eventNameList_searchPage = eventSearchNameList
        eventLocationList_searchPage = eventSearchLocationList
        eventVenueList_searchPage = eventSearchVenueList
        
        print(eventIDList_searchPage, eventNameList_searchPage, eventLocationList_searchPage, eventVenueList_searchPage)
        
        return render_template('Events/eventMain.html', formSearch = formSearch,
                               eventIDList_searchPage = eventIDList_searchPage,
                               eventNameList_searchPage = eventNameList_searchPage,
                               eventLocationList_searchPage = eventLocationList_searchPage,
                               eventVenueList_searchPage = eventVenueList_searchPage,
                               formSortEvents = formSortEvents,
                               title = eventSearchData)
        
    if formSortEvents.validate_on_submit() and request.method == 'POST':
        eventSortByTimeAscending()
        eventTimeList = eventListFinalSort
        
        return render_template('Events/eventMain.html', formSortEvents = formSortEvents,
                               formSearch=formSearch,
                               eventTimeList=eventTimeList,
                               title="Date (Ascending)")
        
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
  
    return render_template('Events/eventSub/eventSports.html', formSortEvents = formSortEvents,
                           formSortEventsDescending = formSortEventsDescending,
                           formSearch = formSearch,
                           eventsList = eventsList,
                           eventType = eventTypeList,
                           eventSports = eventSports,
                           eventLifestyle = eventLifestyle,
                           eventOthers = eventOthers,
                           eventTypeDict = eventTypeDict)

@app.route('/events/lifestyle', methods=['GET', 'POST'])
def eventsPageLifestyle():
    formSearch = eventSearchForm()
    formSortEvents = eventSortForm()
    formSortEventsDescending = eventSortFormDescending()
    
    if formSearch.validate_on_submit() and request.method == 'POST':
        eventSearchData = formSearch.eventSearchItem.data
        
        eventSearchFunction(eventSearchData)
        
        eventIDList_searchPage = eventSearchIDList # lists from search.py
        eventNameList_searchPage = eventSearchNameList
        eventLocationList_searchPage = eventSearchLocationList
        eventVenueList_searchPage = eventSearchVenueList
        
        print(eventIDList_searchPage, eventNameList_searchPage, eventLocationList_searchPage, eventVenueList_searchPage)
        
        return render_template('Events/eventMain.html', formSearch = formSearch,
                               formSortEventsDescending = formSortEventsDescending,
                               eventIDList_searchPage = eventIDList_searchPage,
                               eventNameList_searchPage = eventNameList_searchPage,
                               eventLocationList_searchPage = eventLocationList_searchPage,
                               eventVenueList_searchPage = eventVenueList_searchPage,
                               formSortEvents = formSortEvents,
                               title = eventSearchData)
        
    if formSortEvents.validate_on_submit() and request.method == 'POST':
        eventSortByTimeAscending()
        eventTimeList = eventListFinalSort
        
        return render_template('Events/eventMain.html', formSortEvents = formSortEvents,
                               formSearch=formSearch,
                               eventTimeList=eventTimeList,
                               title="Date (Ascending)")
        
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
  
    return render_template('Events/eventSub/eventLifestyle.html', formSortEvents = formSortEvents,
                           formSortEventsDescending = formSortEventsDescending,
                           formSearch = formSearch,
                           eventsList = eventsList,
                           eventType = eventTypeList,
                           eventSports = eventSports,
                           eventLifestyle = eventLifestyle,
                           eventOthers = eventOthers,
                           eventTypeDict = eventTypeDict)

@app.route('/events/others', methods=['GET', 'POST'])
def eventsPageOthers():
    formSearch = eventSearchForm()
    formSortEvents = eventSortForm()
    formSortEventsDescending = eventSortFormDescending()
    
    if formSearch.validate_on_submit() and request.method == 'POST':
        eventSearchData = formSearch.eventSearchItem.data
        
        eventSearchFunction(eventSearchData)
        
        eventIDList_searchPage = eventSearchIDList # lists from search.py
        eventNameList_searchPage = eventSearchNameList
        eventLocationList_searchPage = eventSearchLocationList
        eventVenueList_searchPage = eventSearchVenueList
        
        print(eventIDList_searchPage, eventNameList_searchPage, eventLocationList_searchPage, eventVenueList_searchPage)
        
        return render_template('Events/eventMain.html', formSearch = formSearch,
                               eventIDList_searchPage = eventIDList_searchPage,
                               eventNameList_searchPage = eventNameList_searchPage,
                               eventLocationList_searchPage = eventLocationList_searchPage,
                               eventVenueList_searchPage = eventVenueList_searchPage,
                               formSortEvents = formSortEvents,
                               title = eventSearchData)
        
    if formSortEvents.validate_on_submit() and request.method == 'POST':
        eventSortByTimeAscending()
        eventTimeList = eventListFinalSort
        
        return render_template('Events/eventMain.html', formSortEvents = formSortEvents,
                               formSortEventsDescending = formSortEventsDescending,
                               formSearch=formSearch,
                               eventTimeList=eventTimeList,
                               title="Date (Ascending)")
    
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
  
    return render_template('Events/eventSub/eventOthers.html', formSortEvents = formSortEvents,
                           formSortEventsDescending = formSortEventsDescending,
                           formSearch = formSearch,
                           eventsList = eventsList,
                           eventType = eventTypeList,
                           eventSports = eventSports,
                           eventLifestyle = eventLifestyle,
                           eventOthers = eventOthers,
                           eventTypeDict = eventTypeDict)
# Ignore this part
# _________________________________________________________________________________________________________________________________________________________________________________________

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
        eventInfoType = []
        eventDisplayType = []
        
        for i in eventsDict:
            eventID = eventsDict[i].get_eventID()
            print(eventID)
            eventInfoID.append(eventID)
            eventName = eventsDict[i].get_eventName()
            print(eventName)
            eventInfoName.append(eventName)
            eventType = eventsDict[i].get_eventType()
            eventInfoType.append(eventType)
        
        for id in userRegisteredList:
            index = eventInfoID.index(id)
            eventNameIndex = eventInfoName[index]
            eventDisplayName.append(eventNameIndex)
            
            eventTypeIndex = eventInfoType[index]
            eventDisplayType.append(eventTypeIndex)
        
        print(eventDisplayName)
        return render_template('Events/eventRegistered.html', registeredEventList = userRegisteredList, registeredEventName = eventDisplayName, registeredEventType = eventDisplayType)
    else:
        return redirect(url_for('login'))

@app.route('/events/search', methods=['GET', 'POST'])
def eventSearch():
    formEvents = eventSearchForm()
    
    eventIDList_searchPage = []
    eventNameList_searchPage = []
    eventLocationList_searchPage = []
    eventVenueList_searchPage = []
    
    if formEvents.validate_on_submit() and request.method == 'POST':
    
        eventSearchData = formEvents.eventSearchItem.data
        
        eventSearchFunction(eventSearchData)
        
        eventIDList_searchPage = eventSearchIDList # lists from search.py
        eventNameList_searchPage = eventSearchNameList
        eventLocationList_searchPage = eventSearchLocationList
        eventVenueList_searchPage = eventSearchVenueList
        
        print(eventIDList_searchPage, eventNameList_searchPage, eventLocationList_searchPage, eventVenueList_searchPage)
        
        return render_template('Events/eventSearch.html', formEvents = formEvents,
                                eventIDList_searchPage = eventIDList_searchPage,
                                eventNameList_searchPage = eventNameList_searchPage,
                                eventLocationList_searchPage = eventLocationList_searchPage,
                                eventVenueList_searchPage = eventVenueList_searchPage)
    
    return render_template('Events/eventSearch.html', formEvents = formEvents,
                                eventIDList_searchPage = eventIDList_searchPage,
                                eventNameList_searchPage = eventNameList_searchPage,
                                eventLocationList_searchPage = eventLocationList_searchPage,
                                eventVenueList_searchPage = eventVenueList_searchPage)

# Booking functions
@app.route('/bookFacilities', methods=['GET', 'POST'])
def bookingPage():
    formsBooking = bookingForm()
    
    facilDict = {}
    facilDB = shelve.open('Facilities')
    try:    
        if 'Facilities' in facilDB:
            facilDict = facilDB['Facilities']
        else:
            facilDB['Facilities'] = facilDict
    except:
        print('Error in retrieving Facilities.')
        
    facilityIDList = []
    facilityUIDList = []
    for facil in facilDict:
        facils = facilDict.get(facil)
        facilAvailability = facils.get_fac_status()
        if facilAvailability == 'Available':
            facilityUID = facils.get_uniqueID()
            facilityUIDList.append(facilityUID)
            facilityID = facils.get_fac_id()
            facilityIDList.append(facilityUID)

    bookingFacilDict = {}
    bookingFacilDB = shelve.open('BookingFacil')
    try:
        if 'BookingFacil' in bookingFacilDB:
            bookingFacilDict = bookingFacilDB['BookingFacil']
        else:
            bookingFacilDB['BookingFacil'] = bookingFacilDict
    except:
        print('Error in retrieving bookings.')
                
    if 'User' in session:
        userID = session['User'][1]
        if formsBooking.validate_on_submit() and request.method == 'POST':
            bookingsDict = {}
            bookingDB = shelve.open('Bookings')
            try:
                if 'Bookings' in bookingDB:
                    bookingsDict = bookingDB['Bookings']
                else:
                    bookingDB['Bookings'] = bookingsDict
            except:
                print('Error in retrieving bookings')
                
            bookFacil = formsBooking.bookingFacilityID.data                    
            bookDate = formsBooking.bookingDate.data                   
            bookTime = formsBooking.bookingTimeSlot.data
            conflict=False           

            for i in range(bookingFacilDict(keys)):
                ot

            if conflict==False:
                fb = FacilityBooking(bookFacil, bookDate, bookTime)
                fb.set_booking_id()
                bookingUID = fb.get_booking_id()
                #bookingsDict[(bookingUID)] = fb
                #bookingDB['Bookings'] = bookingsDict
                #bookingDB.close()
            
   #u        userBookingInfo = [userID, bookFacil, bookDate, bookTime]
   #         bookingFacilDict[bookingUID[-4:]] = userBookingInfo
   #         print(bookingFacilDict)
   #         bookingFacilDB['BookingFacil'] = bookingFacilDict

                return redirect(url_for('bookingPayment'))

        
        return render_template('Booking/bookingMain.html', formsBooking = formsBooking)
       
    else:
        return redirect(url_for('login'))

def bookingPayment():
    formsPayment = paymentForm()
    if formsPayment.validate_on_submit() and request.method == 'POST':
        payMethod = formsPayment.paymentMethod.data
        cardNum = formsPayment.cardNumber.data
        expireDate = formsPayment.expirationDate.data
        securePIN = formsPayment.securityPIN.data

        bookingFacilDict = {}
        bookingFacilDB = shelve.open('BookingFacil')
        try:
            if 'BookingFacil' in bookingFacilDB:
                bookingFacilDict = bookingFacilDB['BookingFacil']
            else:
                bookingFacilDB['BookingFacil'] = bookingFacilDict
        except:
            print('Error in retrieving bookings.')
            
        bookingUID = fb.get_booking_id()
        bookingFacilDict[(bookingUID)] = fb
        bookingFacilDB['BookingFacil'] = bookingFacilDict
        bookingFacilDB.close()

        if 'User' in session:
            userID = session['User'][1]
            bookingsDict = {}
            bookingDB = shelve.open('Bookings')
            try:
                if 'Bookings' in bookingDB:
                    bookingsDict = bookingDB['Bookings']
                else:
                    bookingDB['Bookings'] = bookingsDict
            except:
                print('Error in retrieving bookings')
            
            bookingsDict[(bookingUID)] = fb
            bookingDB['Bookings'] = bookingsDict
            bookingDB.close()
            
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
            if bookings.get_date()>=date.today():
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

        #bookFacilLoc = formsBooking.bookingFacilityLocation.data
        bookFacil = formsBooking.bookingFacilityID.data
        bookDate = formsBooking.bookingDate.data
        bookTime = formsBooking.bookingTimeSlot.data
        #bookFacil = bookFacilLoc+bookFacilType

        fb = bookingsDict[id]
        fb.set_facility(bookFacil)
        fb.set_date(bookDate)
        fb.set_timeslot(bookTime)
        bookingsDict[fb.get_booking_id()] = fb
        bookingDB['Bookings'] = bookingsDict
        
        bookingDB.close()
        print(bookingsDict.keys())
        
        return redirect(url_for('bookingCurrent'))
    else:
        bookingsDict = {}
        bookingDB = shelve.open('Bookings')
        try:
            if 'Bookings' in bookingDB:
                bookingsDict = bookingDB['Bookings']
            else:
                bookingDB['Bookings'] = bookingsDict
        except:
            print('Error in retrieving bookings.')
            
        booking = bookingsDict.get(id)
        #formsBooking.bookingFacilityLocation.data = booking.get_facility()
        formsBooking.bookingFacilityID.data = booking.get_booking_id()
        formsBooking.bookingDate.data = booking.get_date()
        formsBooking.bookingTimeSlot.data = booking.get_timeslot()

        
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
            if bookings.get_date()>=date.today():
                bookingsList.append(bookings)

        return render_template('Booking/bookingHistory.html', bookingsList=bookingsList)
    else:
        return redirect(url_for('login'))

@app.route('/facilities', methods=['GET', 'POST'])
def facilitiesPage(): #didnt realize the tepmplete lmao
    FacilityFormSearch = SearchFacilityForm()

    if FacilityFormSearch.validate_on_submit() and request.method == 'POST':
        facilitySearchData = FacilityFormSearch.facilitySearchItem.data

        facilitySearchFunction(facilitySearchData)

        facilityIDList_searchPage = facilitySearchIDList
        facilityFac_IDList_searchPage = facilitySearchFac_IDList
        facilityLocationList_searchPage = facilitySearchLocationList
        facilitySlotsList_searchPage = facilitySearchSlotsList

        print(facilityIDList_searchPage,
              facilityFac_IDList_searchPage,
              facilityLocationList_searchPage,
              facilitySlotsList_searchPage)

        return render_template('Facilities/facilitiesMain.html', facilSearchForm = FacilityFormSearch,
                               facilIDList_searchPage = facilityIDList_searchPage,
                               facilFacilityIDList_searchPage = facilityFac_IDList_searchPage,
                               facilLocationList_searchPage = facilityLocationList_searchPage, 
                               facilitySlotsList_searchPage = facilitySlotsList_searchPage,
                               title = facilitySearchData) 

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
    
    return render_template('Facilities/facilitiesMain.html', facilSearchForm = FacilityFormSearch, facilList = facilList, facilLoc = facilLoc)

@app.route('/facilities/facilitiesCreate', methods=['GET', 'POST'])
def createFacilities():
    formsFacil = CreateFacilityForm()
    facilDict = {}
    facilDB = shelve.open('Facilities')
    if formsFacil.validate_on_submit() and request.method == 'POST':   
        try:    
            if 'Facilities' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilities'] = facilDict
        except:
            print('Error in retrieving facilities.')
        # oy alan who lives in a pineapple under the sea
        facilLocation = formsFacil.facility_location.data
        location = facilLocation
        
        facilType = formsFacil.facility_type.data
        type = facilType

        facilID = (str(formsFacil.facility_id.data) + " - " + str(type)) # Hougang Stadium - 53, Sengkang Stadium - 54BD01 - 06
        facilStatus = formsFacil.facility_status.data
        facilSlots = formsFacil.facility_slots.data
        facilRates = ("%.2f" % float(formsFacil.facility_rates.data))

        uniqueID = len(facilDict)
        uniqueID += 1
        uniqueIDCheckList = []
        for i in facilDict:
            uniqueIDCheck = facilDict.get(i)
            uniqueIDCheckList.append(uniqueIDCheck)
            
        if uniqueID in uniqueIDCheckList:
            uniqueID += 1
        
        facil = Facilities(facilID, facilStatus, facilSlots, facilLocation, facilRates ,facilType, uniqueID)
        facilDict[facil.get_uniqueID()] = facil # get id
        facilDB['Facilities'] = facilDict
        
        facilDB.close()
        return redirect(url_for('facilitiesPage'))
    
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Facilities/facilitiesCreate.html', formsFacil = formsFacil)
    else:
        return render_template('404.html')

@app.route('/facilities/facilitiesEdit/', methods=['GET', 'POST'])
def editFacilities():
    formsFacil = EditFacilityForm()
    facilDict = {}
    facilDB = shelve.open('Facilities')
    if formsFacil.validate_on_submit() and request.method == 'POST':  
        try:    
            if 'Facilities' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilities'] = facilDict
        except:
            print('Error in retrieving facilities.')
        
        facilID = formsFacil.edit_facility_id.data
        facilStatus = formsFacil.edit_facility_status.data
        facilSlots = formsFacil.edit_facility_slots.data
        facilLocation = formsFacil.edit_facility_location.data
        facilType = formsFacil.edit_facility_type.data
        facilRates = ("%.2f" % float(formsFacil.facility_rates.data))

        facilityID = str(facilLocation + facilType + facilID)
        
        if facilityID not in facilDict.keys():
            print('Error.')
            flash('Facility ID not found in Facilities Database.')
        else:
            facil = Facilities(facilityID, facilStatus, facilSlots, facilLocation, facilRates, facilType, id)
            facilDict[facil.get_uniqueID()] = facil
            facilDB['Facilities'] = facilDict
    
        return redirect(url_for('facilitiesPage'))
    
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Facilities/facilitiesEdit.html', formsFacil = formsFacil)
    else:
        return render_template('404.html')

@app.route('/facilities/facilitiesEdit/<int:id>', methods=['GET', 'POST'])
def editFacilities2(id):
    formsFacil = EditFacilityForm()
    facilDict = {}
    facilDB = shelve.open('Facilities')
    if formsFacil.validate_on_submit() and request.method == 'POST':  
        try:    
            if 'Facilities' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilities'] = facilDict
        except:
            print('Error in retrieving Facilities.')
        
        facilLocation = formsFacil.edit_facility_location.data
        location = facilLocation
        
        facilType = formsFacil.edit_facility_type.data
        type = facilType
        
        facilID = str(formsFacil.edit_facility_id.data) # Hougang Stadium - 53, Sengkang Stadium - 54BD01 - 06
        facilStatus = formsFacil.edit_facility_status.data
        facilSlots = formsFacil.edit_facility_slots.data
        facilRates = ("%.2f" % float(formsFacil.edit_facility_rates.data))
        
        facil = Facilities(facilID, facilStatus, facilSlots, facilLocation, facilRates, facilType, id)
        facilDict[id] = facil  
        facilDB['Facilities'] = facilDict
        
        facilDB.close()
        return redirect(url_for('facilitiesPage'))
    
    else:
        facilDict = {}
        facilDB = shelve.open('Facilities')
        try:    
            if 'Facilities' in facilDB:
                facilDict = facilDB['Facilities']
            else:
                facilDB['Facilities'] = facilDict
        except:
            print('Error in retrieving Facilities.')
        
        id = int(id)
        if id in facilDict:
            facility = facilDict.get(id)
            print(facility)
            formsFacil.edit_facility_id.data = facility.get_fac_id()
            formsFacil.edit_facility_location.data = facility.get_fac_loc()
            formsFacil.edit_facility_slots.data = facility.get_fac_slots()
            formsFacil.edit_facility_status.data = facility.get_fac_status()
            formsFacil.edit_facility_type.data = facility.get_fac_amt()
            formsFacil.edit_facility_rates.data = facility.get_fac_rate()
            
        else:
            print('An Error Is Here')
    
    if session['User'][0] == 'Administrator' and session['User'][1] == '0000000':
        return render_template('Facilities/facilitiesEdit.html', formsFacil = formsFacil)
    else:
        return render_template('404.html')

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
# 17Jan2023 - No longer is this the 723rd line, we have gone too far off. (1089th line)
# 25/1/2023 - It's only been 8 days..., we gone further (1207th line)
# 27Jan2023 - It's only getting longer. When will our suffering end? (1265th Line)
# 1Feb2023 - It's only geting loonger..... When can i retire? - Alan (1376th Line)
# 10Feb2023 - THE SORT FUNCTION IS WORKING WHEEEEEEE - Alan (1584th Line)