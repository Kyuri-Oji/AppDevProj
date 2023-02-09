import shelve
from datetime import *

from OOP.userFunction import *
from OOP.eventFunction import *
from OOP.Bookings import *
from OOP.Facilities import *

eventListTime = []
eventListFinalSort = []

def eventSortByTimeAscending():
    eventListTime.clear()
    eventListFinalSort.clear()
    
    eventsDict = {}
    eventDB = shelve.open('Events')
    
    try:
        if 'Events' in eventDB:
            eventsDict = eventDB['Events']
        else:
            eventDB['Events'] = eventsDict
    except:
        print('Error in handling database!')
        
    dateFormat = "%Y%m%d"
        
    for i in eventsDict:
        events = eventsDict.get(i)
        eventTime = events.get_eventStartDate()
        
        eventTime = int(eventTime.strftime(dateFormat))
        
        if eventTime not in eventListTime:
            eventListTime.append(eventTime)
            eventListTime.sort()
    
    print(f"Event Time List : {eventListTime}")
    
    for x in eventListTime:
        for i in eventsDict:
            events = eventsDict.get(i)
            if (events.get_eventStartDate()).strftime(dateFormat) == str(x):
                if events not in eventListFinalSort: # ensure that event object is not repeated
                    eventListFinalSort.append((events))
        
    print(f"Event Sort List : {eventListFinalSort}")
