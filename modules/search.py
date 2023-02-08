import shelve

from OOP.userFunction import *
from OOP.eventFunction import *
from OOP.Bookings import *
from OOP.Facilities import *

eventSearchIDList = []
eventSearchNameList = []
eventSearchLocationList = []
eventSearchVenueList = []
    
def eventSearchFunction(searchItem):
    eventSearchIDList.clear() # clears the list on new search
    eventSearchNameList.clear()
    eventSearchLocationList.clear()
    eventSearchVenueList.clear()

    eventsDict = {}
    eventDB = shelve.open('Events')
    
    try:
        if 'Events' in eventDB:
            eventsDict = eventDB['Events']
        else:
            eventDB['Events'] = eventsDict
    except:
        print('Error in handling database!')
    
    try:
        searchData = int(searchItem)
        print('searchItem is an integer')
    except:
        searchData = str(searchItem).lower()
        print('searchItem is a string')
            
    for event in eventsDict:
        events = eventsDict.get(event)
        
        if isinstance(searchData, int): # finally knew what isinstance is omg
            if searchData == events.get_eventID(): # TODO: search entry change to int
                eventSearchIDList.append(events)
        elif isinstance(searchData, str):
            if searchData == events.get_eventName() or searchData in str(events.get_eventName()).lower() :
                eventSearchNameList.append(events)
            elif searchData == events.get_eventLocation() or searchData in str(events.get_eventLocation()).lower():
                eventSearchLocationList.append(events)
            elif searchData == events.get_eventVenue() or searchData in str(events.get_eventVenue()).lower():
                eventSearchVenueList.append(events)

    print(eventSearchIDList)
    print(eventSearchNameList)
    print(eventSearchLocationList)
    print(eventSearchVenueList)

# User search function
userSearchUIDList = []
userSearchUsernameList = []
userSearchFirstNameList = []
userSearchLastNameList = []
userSearchEmailList = []
userSearchPhoneNoList = []

def userSearchFunction(searchItem):
    userSearchUIDList.clear()
    userSearchUsernameList.clear()
    userSearchFirstNameList.clear()
    userSearchLastNameList.clear()
    userSearchEmailList.clear()
    userSearchPhoneNoList.clear()
    
    userDict = {}
    userDB = shelve.open('users')
    
    try:
        if 'Users' in userDB:
            userDict = userDB['Users']
        else:
            userDB['Users'] = userDict
    except:
        print('Error in handling database!')
        
    try:
        searchData = int(searchItem)
        print('searchItem is an integer')
    except:
        searchData = str(searchItem).lower()
        print('searchItem is a string')
        
    for users in userDict:
        user = userDict.get(users)
        
        if isinstance(searchData, int):
            if searchData == user.get_phoneNo():
                userSearchPhoneNoList.append(user)
        elif isinstance(searchData, str):
            if searchData == user.get_uid() or searchData in str(user.get_uid()).lower():
                userSearchUIDList.append(user)
            elif searchData == user.get_firstName() or searchData in str(user.get_firstName()).lower():
                userSearchFirstNameList.append(user)
            elif searchData == user.get_lastName() or searchData in str(user.get_lastName()).lower():
                userSearchLastNameList.append(user)
            elif searchData == user.get_email() or searchData in str(user.get_email()).lower():
                userSearchEmailList.append(user)
        
    print(userSearchPhoneNoList)
    print(userSearchUIDList)
    print(userSearchFirstNameList)
    print(userSearchLastNameList)
    print(userSearchEmailList)

# Facility Search Function
facilitySearchIDList = []
facilitySearchFac_IDLIst = []
facilitySearchLocationList = []
facilitySearchStatusList = []
facilitySearchSlotsLIst = []
facilitySearchRatesList = []

def facilitySearchFunction(searchItem):
    facilitySearchIDList.clear()
    facilitySearchFac_IDLIst.clear()
    facilitySearchLocationList.clear()
    facilitySearchStatusList.clear()
    facilitySearchSlotsLIst.clear()
    facilitySearchRatesList.clear()

    facilDict = {}
    facilDB = shelve.open('Facilites')

    try:
        if 'Facilities' in facilDB:
            facilDict = facilDB['Facilites']
        else:
            facilDB['Facilities'] = facilDict
    except:
        print('Error in handling database!')