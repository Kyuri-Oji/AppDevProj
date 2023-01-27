import shelve
import random
import datetime

dictUsers = {}
db = shelve.open('users', 'c')

try:
    dictUsers = db['Users']
except:
    print('Error in retrieving users from user.db.')

class User:
    def __init__(self, username, firstName, lastName, email, uid, phoneNo, dateJoined, password):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.uid = uid
        self.phoneNo = phoneNo
        self.dateJoined = dateJoined
        self.password = password
        
    def set_firstName(self, firstName):
        self.firstName = firstName
    def get_firstName(self):
        return self.firstName
    
    def set_uid(self, uid):
        self.uid = uid
    def get_uid(self):
        return self.uid
        
    def set_lastName(self, lastName):
        self.lastName = lastName
    def get_lastName(self):
        return self.lastName

    def set_username(self, username):
        self.username = username
    def get_username(self):
        return self.username
    
    def set_email(self, email):
        self.email = email
    def get_email(self):
        return self.email

    def set_phoneNo(self, phoneNo):
        self.phoneNo = phoneNo
    def get_phoneNo(self):
        return self.phoneNo
    
    def set_dateJoined(self, dateJoined):
        self.dateJoined = dateJoined
    def get_dateJoined(self):
        return self.dateJoined
        
    def set_password(self, password):
        self.password = password
    def get_password(self):
        return self.password

    def get_random_UID(self):
        tempList = []
        for i in range(7): # 7-Digit Random
            randomID = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            tempList.append(randomID)
            
        if str(tempList) not in db:
            return "".join(tempList)
        
        else:
            while True:
                tempList = []
                for i in range(7): # 7-Digit Random
                    randomID = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
                    tempList.append(randomID)
                    
                if str(tempList) not in db:
                    return "".join(tempList)
                break

    def get_userJoinDate(self):
        userDateJoined = datetime.date.today()
        return userDateJoined