class createEvents:
    eventCount = 0
    def __init__(self, eventName, eventDesc, eventVacancy, eventDate, eventID, eventType):
        self.eventName = eventName
        self.eventDesc = eventDesc
        self.eventVacancy = eventVacancy
        self.eventDate = eventDate
        self.eventID = eventID
        self.eventType = eventType
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

    def set_eventID(self, eventID):
        self.eventID = eventID
    def get_eventID(self):
        return self.eventID
    
    def set_eventType(self, eventType):
        self.eventType = eventType
    def get_eventType(self):
        return self.eventType
    
    def __str__(self) -> str:
        s = f'ID:{self.get_eventID()} - {self.get_eventName()} | {self.get_eventID()}'
        return s