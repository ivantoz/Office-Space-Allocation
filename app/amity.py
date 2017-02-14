from collections import defaultdict
import random
import os
from app.model import Person, Staff, Fellow, Room, Office, LivingSpace
from app.database import Employees, Rooms, create_db, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from sqlalchemy import create_engine


class AmityDefaultDict(defaultdict):
    def __setitem__(self, key, value):
        key = key.upper()
        dict.__setitem__(self, key, value)

    def __getitem__(self, key):
        key = key.upper()
        return dict.__getitem__(self, key)


class Amity(object):
    # TODO add docstring documentation with examples for doctest
    # TODO check that all the logic works

    def __init__(self):
        self.all_people = []
        self.all_rooms = []
        self.office_allocations = AmityDefaultDict(list)
        self.lspace_allocations = AmityDefaultDict(list)
        self.office_unallocated = []
        self.lspace_unallocated = []
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

    def add_person(self, employee_number, first_name, last_name, job_type, wants_accomodation="N"):
        """
        Adds a person to the system and allocates a random room

        :return:

        """

        all_employees_number = [person.employee_number for person in self.all_people]
        print(self.all_people)
        if employee_number in all_employees_number:
            msg = "sorry, this user already exists.please enter valid employee number"
            print(msg)
            return msg
        else:
            if job_type.upper() == "STAFF":

                staff = Staff(employee_number, first_name, last_name, job_type, wants_accomodation)
                self.all_people.append(staff)
                self.staff_list.append(staff)

                allocated_office = self.generate_room("OFFICE")
                if allocated_office is not None:
                    self.office_allocations[allocated_office.room_name].append(employee_number.upper())
                    allocated_office.occupants += 1
                    msg1 = "congratulations {}, you have been assigned to {} office"\
                        .format(first_name, allocated_office.room_name.upper())
                    print(msg1)
                    if wants_accomodation == "Y":
                        msg1 += " However, Staff members Cannot be allocated living space"
                    return msg1
                else:
                    self.office_unallocated.append(employee_number.upper())
                    sorrymsg = "sorry, all rooms are full at this time."
                    print(sorrymsg)
                    return sorrymsg

            elif job_type.upper() == "FELLOW":
                fellow = Fellow(employee_number, first_name, last_name, job_type, wants_accomodation)
                self.all_people.append(fellow)
                self.fellows_list.append(fellow)
                allocated_office = self.generate_room("OFFICE")
                kudosmsg = ''
                if allocated_office is not None:
                    self.office_allocations[allocated_office.room_name].append(employee_number.upper())
                    allocated_office.occupants += 1
                    kudosmsg = "congratulations {}, you have been assigned to {} office"\
                        .format(first_name, allocated_office.room_name.upper())
                    print(kudosmsg)

                else:
                    self.office_unallocated.append(employee_number.upper())
                    kudosmsg = "sorry, all rooms are full at this time."
                    print(kudosmsg)

                if wants_accomodation == "Y":
                    allocated_lspace = self.generate_room("LSPACE")
                    if allocated_lspace is not None:
                        self.lspace_allocations[allocated_lspace.room_name].append(employee_number.upper())
                        allocated_lspace.occupants += 1
                        kudosmsg = "congratulations {}, you have been assigned to {} living space"\
                            .format(first_name, allocated_lspace.room_name)
                        print(kudosmsg)

                    else:
                        person = employee_number.upper()
                        self.lspace_unallocated.append(person)
                        kudosmsg = "sorry, all living space rooms are full at this time."
                        print(kudosmsg)
                return kudosmsg

    def reallocate_person(self, employee_number, new_room):

        """ Reallocate the person with person_identifier to new_room_name. """
        all_employees_numbers = [person.employee_number for person in self.all_people]
        # check if the person exist in amity
        if employee_number.lower() not in all_employees_numbers:
            return "{} does not exist".format(employee_number.upper())

        all_rooms_names = [room.room_name for room in self.all_rooms]
        # check if room exist in amity
        if new_room.lower() not in all_rooms_names:
            return "Room with name {} does not exist".format(new_room.upper())

        rtype = self.check_room_type(new_room)
        current_room = self.check_allocated_room(employee_number, rtype)
        if rtype.upper() == "LSPACE":
            # check whether the person is already in the allocated room
            if employee_number.upper() in self.lspace_allocations[new_room.upper()]:
                return "The Person is already allocated in the requested room"

            new_room_occupant_count = [room.occupants for room in self.all_rooms if room.room_name.lower() == new_room.lower()]

            if current_room is not None:
                if new_room_occupant_count[0] < 4:
                    self.lspace_allocations[current_room.upper()].remove(employee_number.upper())
                    self.lspace_allocations[new_room.upper()].append(employee_number.upper())
                    for room in self.all_rooms:
                        if room.room_name == new_room:
                            room.occupants += 1
                        if room.room_name == current_room:
                            room.occupants -= 1
                    return "{} has been moved to {}".format(employee_number.upper(), new_room)
                else:
                    return "Sorry the LivingSpace is currently fully occupied!"

            else:
                if new_room_occupant_count[0] < 4:
                    for room in self.all_rooms:
                        if room.room_name == new_room:
                            room.occupants += 1
                    self.lspace_unallocated.remove(employee_number.upper())
                    self.lspace_allocations[new_room.upper()].append(employee_number.upper())
                    return "{} has been moved to {}".format(employee_number.upper(), new_room)
                else:
                    return "Sorry the LivingSpace is currently fully occupied!"

        if rtype.upper() == "OFFICE":
            # check whether the person is already in the allocated room
            if employee_number.upper in self.office_allocations[new_room.upper()]:
                return "The Person is already allocated in the requested room"

            new_room_occupant_count = [room.occupants for room in self.all_rooms if
                                       room.room_name.lower() == new_room.lower()]

            if current_room is not None:
                if new_room_occupant_count[0] < 6:
                    for room in self.all_rooms:
                        if room.room_name == new_room:
                            room.occupants += 1
                        if room.room_name == current_room:
                            room.occupants -= 1
                    self.office_allocations[current_room.upper()].remove(employee_number.upper())
                    self.office_allocations[new_room.upper()].append(employee_number.upper())
                    return "{} has been moved to {}".format(employee_number.upper(), new_room)
                else:
                    return "Sorry the Office is currently fully occupied!"

            else:
                if new_room_occupant_count[0] < 6:
                    for room in self.all_rooms:
                        if room.room_name == new_room:
                            room.occupants += 1
                    self.office_allocations.remove(employee_number.upper())
                    self.office_allocations[new_room.upper()].append(employee_number.upper())
                    return "{} has been moved to {}".format(employee_number.upper(), new_room)
                else:
                    return "Sorry the Office is currently fully occupied!"


        # if employee_number.lower() in all_employees_numbers:
        #     rtype = self.check_room_type(new_room)
        #     current_room = self.check_allocated_room(employee_number, rtype)
        #     if rtype is None:
        #         res = "Room with name {} does not exist".format(new_room.upper())
        #         print(res)
        #         return res
        #     elif rtype == 'LSPACE':
        #         if current_room is not None:
        #             self.lspace_allocations[current_room].remove(employee_number.upper())
        #         else:
        #             self.lspace_unallocated.remove(employee_number.upper())
        #         self.lspace_allocations[new_room].append(employee_number.upper())
        #         print("{} has been moved to {}".format(employee_number.upper(), new_room))
        #
        #     elif rtype == 'OFFICE':
        #         if current_room is not None:
        #             self.office_allocations[current_room].remove(employee_number.upper())
        #         else:
        #             self.office_unallocated.remove(employee_number.upper())
        #         self.office_allocations[new_room.upper()].append(employee_number.upper())
        #         print("{} has been moved to {}".format(employee_number.upper(), new_room))
        #
        # else:
        #     return "{} does not exist".format(employee_number.upper())

    def check_room_type(self, name):
        """checks room type allocated to a person"""
        for room in self.all_rooms:
            if name.upper() == room.room_name.upper():
                return room.room_type
        return None

    def check_allocated_room(self, empno, room_type):
        """Checks the room type which person is currently allocated"""
        if room_type.upper() == "LSPACE":
            for room in self.lspace_allocations:
                if empno.upper() in self.lspace_allocations[room]:
                    return room
        elif room_type.upper() == "OFFICE":
            for room in self.office_allocations:
                if empno.upper() in self.office_allocations[room]:
                    return room
        else:
            return None

    def check_employee_job_type(self, empno):
        """Check person job type using employee number"""
        for empnos in self.all_people:
            if empnos.employee_number == empno.lower():
                return empnos.job_type
            else:
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
                        empno = first_name + last_name
                        job_type = person_data[2]
                        try:
                            accomodation = person_data[3]
                        except Exception:
                            accomodation = 'N'

                        self.add_person(empno, first_name, last_name, job_type, accomodation)

                    return "File data added successfully"

        else:
            print("please provide a text file name")

    def print_allocations(self, filename=None):
        """Prints a list of allocations onto the screen. Specifying the optional -o option here outputs the registered
        allocations to a txt file"""

        print("-" * 30 + "\n" + "AMITY OFFICE ALLOCATIONS\n" + "-" * 30 + "\n")
        for office, empnos in self.office_allocations.items():
            print(office.upper())
            print("-" * 30)
            print("\n")
            for empno in empnos:
                firstname = [person.first_name for person in self.all_people if person.employee_number.upper() == empno]
                lastname = [person.last_name for person in self.all_people if person.employee_number.upper() == empno]
                print(firstname[0].upper(), lastname[0].upper(), end=', ')

                if filename:

                    file = open(filename + ".txt", "a")
                    file.write("\n")
                    file.write("-" * 30 + "\n")
                    file.write(office)
                    file.write("\n")
                    file.write("-" * 30 + "\n")
                    file.write(firstname[0].upper() + " " + lastname[0].upper() + ", ")
                    file.write("\n")
                    # for name in self.office_allocations[office]:
                    #     file.write(.upper() + ", ")
                    file.write("\n" + "-" * 30 + "\n")

    def print_unallocated(self, filename=None):
        """Prints a list of unallocated people to the screen. Specifying the -o option here outputs the information to
        the txt file provided"""

        print(self.amity_unallocated)

        print("-" * 30 + "\n" + "AMITY UNALLOCATED\n" + "-" * 30 +"\n")
        if len(self.amity_unallocated) != 0:
            for person in self.amity_unallocated:
                print(person)
        else:
            print("All people have been allocated rooms!")
            if filename:
                file = open(filename + ".txt", "a")
                for person in self.amity_unallocated:
                    file.write(person)

    def print_room(self, room_name):


    def save_state(self, dbname="dbname"):
        pass

    def load_state(self, dbname="dbname"):
        pass









