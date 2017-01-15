from collections import defaultdict
import random

class AmityDefaultDict(defaultdict):
    def __setitem__(self, key, value):
        key = key.upper()
        dict.__setitem__(self, key, value)

    def __getitem__(self, key):
        key = key.upper()
        return dict.__getitem__(self, key)

class Amity(object):

    def __init__(self):
        self.all_people = []
        self.all_rooms = []
        self.office_allocations = AmityDefaultDict(list)
        self.lspace_allocations = AmityDefaultDict(list)
        self.amity_unallocated = []
        self.fellows_list = []
        self.staff_list = []


    def create_room(self, room_type, *args):

        """creates a room not previously in system """
        all_room_names = [room.room_name for room in self.all_rooms]
        msg = ''

        if len(args) >= 1:
            for room_name in args:
                if room_name in all_room_names:
                    msg = "sorry, {} room already exists!please choose another name".format(room_name)
                    print(msg)
                    return msg
                else:
                    if room_type.upper() == "LSPACE":
                        room = LivingSpace(room_name, room_type)
                        self.all_rooms.append(room)
                        msg = "{} Living Space successfully created".format(room_name)
                        print(msg)
                        return msg
                    elif room_type.upper() == "OFFICE":
                        room = Office(room_name, room_type)
                        self.all_rooms.append(room)
                        msg = "{} Office successfully created".format(room_name)
                        print(msg)
                        return msg
                    else:
                        msg = "sorry, that room_type does not exist"
                        print(msg)
                        return msg

        elif len(args) < 1:
            notice = 'A room should have a name'
            print(notice)
            return notice

    def generate_room(self, r_type):
        """returns a list of all rooms not full"""
        available = []
        for room in self.all_rooms:

            if room.room_type.upper() == r_type.upper():
                if room.room_type.upper() == "LSPACE":
                    if room.occupants < room.max_occupants:
                        available.append(room)

                if room.room_type.upper() == "OFFICE":
                    if room.occupants < room.max_occupants:
                        available.append(room)

        if len(available) == 0:
            return None
        else:
            return random.choice(available)




    def add_person(self, person_name, job_type, wants_accomodation="N"):
        """
        Adds a person to the system and allocates a random room

        :return:

        """


        all_people_names = [person.person_name for person in self.all_people]
        if person_name in all_people_names:
            msg = "sorry, this user already exists.please choose another name"
            print(msg)
            return msg
        else:
            if job_type.upper() == "STAFF":
                staff = Staff(person_name, job_type, wants_accomodation)
                self.all_people.append(staff)
                self.staff_list.append(staff)
                print("{} person successfully created".format(person_name))

                allocated_office = self.generate_room("OFFICE")
                if allocated_office is not None:
                    self.office_allocations[allocated_office.room_name].append(person_name)
                    allocated_office.occupants += 1
                    msg1 = "congratulations {}, you have been assigned to {} office".format(person_name, allocated_office.room_name.upper())
                    print(msg1)
                    return msg1
                else:
                    self.amity_unallocated.append(person_name.upper)
                    sorrymsg = "sorry, all rooms are full at this time."
                    print(sorrymsg)
                    return sorrymsg
            elif job_type.upper() == "FELLOW":
                fellow = Fellow(person_name, job_type, wants_accomodation)
                self.all_people.append(fellow)
                self.fellows_list.append(fellow)
                allocated_office = self.generate_room("OFFICE")
                if allocated_office is not None:
                    self.office_allocations[allocated_office.room_name].append(person_name.upper())
                    allocated_office.occupants += 1
                    kudosmsg = "congratulations {}, you have been assigned to {} office".format(person_name, allocated_office.room_name.upper())
                    print(kudosmsg)
                    if wants_accomodation.upper() == "Y":
                        allocated_lspace = self.generate_room("LSPACE")
                        if allocated_lspace is not None:
                            self.lspace_allocations[allocated_lspace.room_name].append(person_name.upper())
                            allocated_lspace.occupants += 1
                            msg3 = "congratulations {}, you have been assigned to {} living space".format(person_name, allocated_lspace.room_name)
                            print(msg3)
                            return msg3
                        else:
                            person = person_name.upper()
                            self.amity_unallocated.append(person)
                            msg4 = "sorry, all rooms are full at this time."
                            print(msg4)
                            return msg4
                    return kudosmsg

                else:
                    self.amity_unallocated.append(person_name.upper() + "" + job_type)
                    sorrymsg2 = "sorry, all rooms are full at this time."
                    print(sorrymsg2)
                    return sorrymsg2

    def reallocate_person(self):
        pass

    def load_people(self):
        pass

    def print_allocations(self):
        pass

    def print_unallocated(self):
        pass

    def print_room(self):
        pass

class Person(object):
    """ Person defines the main attributes and methods common
            to both Fellow and Staff Class """


    def __init__(self, person_name, job_type, wants_accommodation):
        self.person_name = person_name
        self.job_type = job_type
        self.wants_accommodation = wants_accommodation


class Staff(Person):
    def __init__(self, person_name, job_type, wants_accommodation='N'):
        super(Staff, self).__init__(person_name, job_type, wants_accommodation)

class Fellow(Person):
    def __init__(self, person_name, job_type, wants_accommodation='N'):

        super(Fellow, self).__init__(person_name, job_type, wants_accommodation)




class Room(object):

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









