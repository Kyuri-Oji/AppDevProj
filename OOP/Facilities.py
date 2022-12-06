class Facilities:
    fac_count = 0

    def __init__(self, fac_name, fac_status, fac_slots):
        self.__fac_name = fac_name
        self.__fac_status = fac_status
        self.__fac_slots = fac_slots

    def set_fac_name(self, fac_name):
        self.__fac_name = fac_name

    def set_fac_status(self, fac_status):
        self.__fac_status = fac_status

    def set_fac_slots(self, fac_slots):
        self.__fac_slots = fac_slots

    def get_fac_name(self):
        return self.__fac_name

    def get_fac_status(self):
        return self.__fac_status

    def get_fac_slots(self):
        return self.__fac_slots
