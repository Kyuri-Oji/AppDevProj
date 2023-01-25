class createEvents:
    eventCount = 0
    def __init__(self, eventName, eventDesc, eventVacancy, eventDate, eventStartDate, eventID, eventType, eventLocation, eventVenue, eventStatus):
        self.eventName = eventName
        self.eventDesc = eventDesc
        self.eventVacancy = eventVacancy
        self.eventDate = eventDate
        self.eventStartDate = eventStartDate
        self.eventID = eventID
        self.eventType = eventType
        self.eventLocation = eventLocation
        self.eventVenue = eventVenue
        self.eventStatus = eventStatus
        self.eventCount += 1
        
    def set_eventName(self, eventName):
        self.eventName = eventName
    def get_eventName(self):
        return self.eventName
    
    def set_eventDesc(self, eventDesc):
        self.eventDesc = eventDesc
    def get_eventDesc(self):
        return self.eventDesc
    
    def set_eventVacancy(self, eventVacancy):
        self.eventVacancy = eventVacancy
    def get_eventVacancy(self):
        return self.eventVacancy
    
    def set_eventDate(self, eventDate):
        self.eventDate = eventDate
    def get_eventDate(self):
        return self.eventDate
    
    def set_eventStartDate(self, eventStartDate):
        self.eventStartDate = eventStartDate
    def get_eventStartDate(self):
        return self.eventStartDate
    
    def set_eventID(self, eventID):
        self.eventID = eventID
    def get_eventID(self):
        return self.eventID
    
    def set_eventType(self, eventType):
        self.eventType = eventType
    def get_eventType(self):
        return self.eventType
    
    def set_eventLocation(self, eventLocation):
        self.eventLocation = eventLocation
    def get_eventLocation(self):
        return self.eventLocation
    
    def set_eventVenue(self, eventVenue):
        self.eventVenue = eventVenue
    def get_eventVenue(self):
        return self.eventVenue
    
    def set_eventStatus(self, eventStatus):
        self.eventStatus = eventStatus
    def get_eventStatus(self):
        return self.eventStatus
    
    def __str__(self) -> str:
        s = f'{self.get_eventID()}'
        return s
