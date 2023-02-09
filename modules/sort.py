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
    
    for x in eventListTime: # your sorted list [21 22 23]
        for i in eventsDict: # your current dict
            events = eventsDict.get(i)
            if (events.get_eventStartDate()).strftime(dateFormat) == str(x):
                if events not in eventListFinalSort: # ensure that event object is not repeated
                    eventListFinalSort.append((events))
        
    print(f"Event Sort List : {eventListFinalSort}")


eventListTimeDescending = []
eventListFinalSortDescending = []

def eventSortByTimeDescending():
    eventListTimeDescending.clear()
    eventListFinalSortDescending.clear()
    
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
        eventStartDate = (events.get_eventStartDate())
        
        eventStartDate = int(eventStartDate.strftime(dateFormat))
        
        if eventStartDate not in eventListTimeDescending:
            eventListTimeDescending.append(eventStartDate)
            
    eventListTimeDescendingReverse = sorted(eventListTimeDescending, reverse=True) # reverse not working wtf?
    print(eventListTimeDescendingReverse)
    
    for x in eventListTimeDescendingReverse:
        for i in eventsDict:
            events = eventsDict.get(i)
            if (events.get_eventStartDate()).strftime(dateFormat) == str(x):
                if events not in eventListFinalSortDescending:
                    eventListFinalSortDescending.append(events)
    print(eventListFinalSortDescending)

eventSportsList = []

def eventSortBySport():
    eventSportsList.clear()

    eventsDict = {}
    eventDB = shelve.open('Events')

    try:
        if 'Events' in eventDB:
            eventsDict = eventDB['Events']
        else:
            eventDB['Events'] = eventsDict
    except:
        print('Error in handling database!')

    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Sports' in events.get_eventType():
            eventSportsList.append(events)


eventLifestyleList = []

def eventSortByLifestyle():
    eventLifestyleList.clear()

    eventsDict = {}
    eventDB = shelve.open('Events')

    try:
        if 'Events' in eventDB:
            eventsDict = eventDB['Events']
        else:
            eventDB['Events'] = eventsDict
    except:
        print('Error in handling database!')

    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Lifestyle' in events.get_eventType():
            eventLifestyleList.append(events)


eventOthersList = []

def eventSortByOthers():
    eventOthersList.clear()

    eventsDict = {}
    eventDB = shelve.open('Events')

    try:
        if 'Events' in eventDB:
            eventsDict = eventDB['Events']
        else:
            eventDB['Events'] = eventsDict
    except:
        print('Error in handling database!')

    for event in eventsDict:
        events = (eventsDict.get(event))
        if 'Others' in events.get_eventType():
            eventOthersList.append(events)