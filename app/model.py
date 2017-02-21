
class Person(object):
    """ Person defines the main attributes and methods common
            to both Fellow and Staff Class """
    def __init__(self, employee_no, first_name, last_name, job_type, wants_accommodation):
        self.employee_number = employee_no
        self.first_name = first_name
        self.last_name = last_name
        self.job_type = job_type
        self.wants_accommodation = wants_accommodation


class Staff(Person):
    def __init__(self, employee_number, first_name, last_name, job_type, wants_accommodation='N'):
        super(Staff, self).__init__(employee_number, first_name, last_name, job_type, wants_accommodation)


class Fellow(Person):
    def __init__(self, employee_number, first_name, last_name, job_type, wants_accommodation='N'):
        super(Fellow, self).__init__(employee_number, first_name, last_name, job_type, wants_accommodation)


class Room(object):
    """Room defines the main attributes and methods common
            to both Office and LivingSpace Class"""

    def __init__(self, room_name, room_type=None, max_occupants=None,
                 occupants=None):
        self.room_name = room_name
        self.room_type = room_type
        self.occupants = occupants
        self.max_occupants = max_occupants


class Office(Room):
    def __init__(self, room_name, room_type):
        super(Office, self).__init__(room_name,  room_type=room_type, max_occupants=6, occupants=0)


class LivingSpace(Room):
    def __init__(self, room_name, room_type):
        super(LivingSpace, self).__init__(room_name,  room_type=room_type, max_occupants=4, occupants=0)

