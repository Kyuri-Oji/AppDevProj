import random

class Bookings:
     booking_id=""
     def __init__(self,type):
          self.__type=type

     def set_booking_id(self):
          tempList = []
          for i in range(7): # 7-Digit Random
            randomID = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            tempList.append(randomID)
          self.__booking_id="".join(tempList)

     def get_booking_id(self):
          return self.__booking_id

     def get_type(self):
          return self.__type
     
class FacilityBooking:
     def __init__(self,facility,date,timeslot):
          self.__booking_id=""
          self.__facility=facility
          self.__date=date
          self.__timeslot=timeslot

     def set_booking_id(self):
          day,month,year=str(self.__date).split("-")
          facility=self.__facility
          randomID=""
          for i in range(4): # 4-Digit Random
            randomID+=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
          self.__booking_id=day+month+year+facility+randomID
     
     def set_facility(self,facility):
          self.__facility=facility

     def set_date(self,date):
          self.__date=date

     def set_timeslot(self,timeslot):
          self.__timeslot=timeslot

     def get_booking_id(self):
          return self.__booking_id

     def get_facility(self):
          return self.__facility

     def get_date(self):
          return self.__date

     def get_timeslot(self):
          return self.__timeslot