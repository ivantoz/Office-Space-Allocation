from collections import defaultdict
import random
import os
from app.model import Person, Staff, Fellow, Room, Office, LivingSpace


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
        if room_type.upper() in ["LSPACE", "OFFICE"]:
            if len(args) >= 1:
                msg = ''
                for room_name in args:
                    if room_name in all_room_names:
                        msg = "sorry, {} room already exists!please choose another name".format(room_name)
                        print(msg)
                    else:
                        if room_type.upper() == "LSPACE":
                            room = LivingSpace(room_name, room_type)
                            self.all_rooms.append(room)
                            msg = "{} Living Space successfully created".format(room_name)
                            print(msg)
                        elif room_type.upper() == "OFFICE":
                            room = Office(room_name, room_type)
                            self.all_rooms.append(room)
                            msg = "{} Office successfully created".format(room_name)
                            print(msg)
                return msg

            elif len(args) < 1:
                notice = 'A room should have a name'
                print(notice)
                return notice
        else:
            msg = "sorry, that room_type does not exist"
            print(msg)
            return msg

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

        if len(available) > 0:
            return random.choice(available)
        return None

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
                print("{} successfully added to system".format(person_name))

                allocated_office = self.generate_room("OFFICE")
                if allocated_office is not None:
                    self.office_allocations[allocated_office.room_name].append(person_name)
                    allocated_office.occupants += 1
                    msg1 = "congratulations {}, you have been assigned to {} office"\
                        .format(person_name, allocated_office.room_name.upper())
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
                kudosmsg = ''
                if allocated_office is not None:
                    self.office_allocations[allocated_office.room_name].append(person_name.upper())
                    allocated_office.occupants += 1
                    kudosmsg = "congratulations {}, you have been assigned to {} office"\
                        .format(person_name, allocated_office.room_name.upper())
                    print(kudosmsg)


                else:
                    self.amity_unallocated.append(person_name.upper() + "" + job_type)
                    kudosmsg = "sorry, all rooms are full at this time."
                    print(kudosmsg)

                if wants_accomodation == "Y":
                    allocated_lspace = self.generate_room("LSPACE")
                    if allocated_lspace is not None:
                        self.lspace_allocations[allocated_lspace.room_name].append(person_name.upper())
                        allocated_lspace.occupants += 1
                        kudosmsg = "congratulations {}, you have been assigned to {} living space"\
                            .format(person_name, allocated_lspace.room_name)
                        print(kudosmsg)

                    else:
                        person = person_name.upper()
                        self.amity_unallocated.append(person)
                        kudosmsg = "sorry, all rooms are full at this time."
                        print(kudosmsg)
                return kudosmsg

    def reallocate_person(self, person_name, new_room):

        """ Reallocate the person with person_identifier to new_room_name. """
        all_people_names = [person.person_name for person in self.all_people]
        for name in all_people_names:
            if name == person_name:
                if person_name in all_people_names:
                    rtype = self.check_room_type(new_room)
                    current_room = self.check_allocated_room(person_name, rtype)
                    if rtype is None:
                        res = "Room with name {} does not exist".format(new_room)
                        print(res)
                        return res
                    elif rtype == 'LSPACE':
                        if current_room is not None:
                            self.lspace_allocations[current_room].remove(person_name)
                        self.lspace_allocations[new_room].append(person_name)
                        print("{} has been moved to {}".format(person_name, new_room))
                        break
                    elif rtype == 'OFFICE':
                        if current_room is not None:
                            self.office_allocations[current_room].remove(person_name)
                        self.office_allocations[new_room].append(person_name)
                        print("{} has been moved to {}".format(person_name, new_room))
                        break
                else:
                    return "{} does not exist".format(person_name)

    def check_room_type(self, name):
        """checks room allocated to a person"""
        for room in self.all_rooms:
            if name.upper() == room.room_name.upper():
                return room.room_type
        return None

    def check_allocated_room(self, person_name, room_type):
        if room_type == "LSPACE":
            for room in self.lspace_allocations:
                if person_name in self.lspace_allocations[room]:
                    return room
        elif room_type == "OFFICE":
            for room in self.office_allocations:

                if person_name in self.office_allocations[room]:
                    return room
        return None

    def load_people(self, filename):
        """Adds people to rooms from a text file"""

        if os.path.exists(filename):
            with open(filename) as input:

                content = input.readlines()

                if len(content) == 0:
                    return "The file is empty"
                else:
                    for line in content:
                        person_data = line.split()
                        first_name = person_data[0]
                        last_name = person_data[1]
                        full_name = first_name + " " + last_name
                        job_type = person_data[2]
                        try:
                            accomodation = person_data[3]
                        except Exception:
                            accomodation = 'N'

                        self.add_person(full_name, job_type, accomodation)

                    return "File data added successfully"

        else:
            print("please provide a text file name")

    def print_allocations(self, filename=None):
        """prints all allocations"""
        print("-" * 30 + "\n" + "AMITY OFFICE ALLOCATIONS\n" + "-" * 30 + "\n")
        for office, names in self.office_allocations.items():
            print(office.upper())
            print("-" * 30)
            print("\n")
            for name in names:
                print(name)
                print("\n")

                if filename:

                    file = open(filename + ".txt", "a")
                    file.write("\n")
                    file.write("-" * 30 + "\n")
                    file.write(office)
                    file.write("\n")
                    file.write("-" * 30 + "\n")
                    for name in self.office_allocations[office]:
                        file.write(name.upper() + ", ")
                    file.write("\n" + "-" * 30 + "\n")

    def print_unallocated(self, filename=None):
        pass

    def print_room(self):
        pass

    def save_state(self, dbname="dbname"):
        pass

    def load_state(self, dbname="dbname"):
        pass









