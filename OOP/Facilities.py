class Facilities:
    fac_count = 0

    def __init__(self, fac_id, fac_name, fac_status, fac_slots, fac_loc, fac_amt):
        Facilities.fac_count += 1
        self.__fac_id = fac_id
        self.__fac_name = fac_name
        self.__fac_status = fac_status
        self.__fac_slots = fac_slots
        self.__fac_loc = fac_loc
        self.__fac_amt = fac_amt

    def set_fac_id(self, fac_id):
        self.__fac_id = fac_id

    def set_fac_name(self, fac_name):
        self.__fac_name = fac_name

    def set_fac_status(self, fac_status):
        self.__fac_status = fac_status

    def set_fac_slots(self, fac_slots):
        self.__fac_slots = fac_slots

    def set_fac_loc(self, fac_loc):
        self.__fac_loc = fac_loc
    
    def set_fac_amt(self, fac_amt):
        self.__fac_amt = fac_amt

    def get_fac_id(self):
        return self.__fac_id

    def get_fac_name(self):
        return self.__fac_name

    def get_fac_status(self):
        return self.__fac_status

    def get_fac_slots(self):
        return self.__fac_slots
    
    def get_fac_loc(self):
        return self.__fac_loc
    
    def get_fac_amt(self):
        return self.__fac_amt
