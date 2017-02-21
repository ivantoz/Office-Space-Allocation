from collections import defaultdict
import random
import os
from app.model import  Staff, Fellow, Office, LivingSpace
from app.database import Employees, Rooms, create_db, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from sqlalchemy import create_engine
from app.utilities import bcolors


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
        self.office_unallocated = []
        self.lspace_unallocated = []
        self.fellows_list = []
        self.staff_list = []

    def create_room(self, room_type, room_name):

        """creates a room not previously in system """
        all_room_names = [room.room_name for room in self.all_rooms]
        msg = ''
        if room_type.upper() in ["LSPACE", "OFFICE"]:
            if room_name:
                msg = ''
                for room_name in room_name:

                    if room_name.upper() in all_room_names:
                        msg = "sorry, {} room already exists!please choose another name".format(room_name.upper())
                        return msg
                    else:
                        if room_type.upper() == "LSPACE":
                            room = LivingSpace(room_name.upper(), room_type.upper())
                            self.all_rooms.append(room)
                            msg = "{} Living Space successfully created".format(room_name.upper())
                            print(msg)
                        elif room_type.upper() == "OFFICE":
                            room = Office(room_name.upper(), room_type.upper())
                            self.all_rooms.append(room)
                            msg = "{} Office successfully created".format(room_name.upper())
                            print(msg)
                return msg
            notice = 'A room should have a name'
            return notice
        else:
            return "sorry, that room_type does not exist"

    def generate_room(self, room_type):
        """returns a list of all rooms not full"""
        available = []
        for room in self.all_rooms:

            if room.room_type == room_type.upper():
                if room.room_type == "LSPACE" and room.occupants < room.max_occupants:
                    available.append(room)

                if room.room_type == "OFFICE" and room.occupants < room.max_occupants:
                    available.append(room)

        if available:
            return random.choice(available)
        return None

    def add_person(self, employee_number, first_name, last_name, job_type, wants_accomodation="N"):
        """
        Adds a person to the system and allocates a random room

        :return:

        """

        all_employees_number = [person.employee_number for person in self.all_people]
        if employee_number.upper() in all_employees_number:
            msg = "sorry, this user already exists.please enter valid employee number"
            return msg
        else:
            if job_type.upper() == "STAFF":

                staff = Staff(employee_number.upper(), first_name.upper(), last_name.upper(), job_type.upper(),
                              wants_accomodation.upper())
                self.all_people.append(staff)
                self.staff_list.append(staff)

                allocated_office = self.generate_room("OFFICE")
                if allocated_office:
                    self.office_allocations[allocated_office.room_name].append(employee_number.upper())
                    allocated_office.occupants += 1
                    msg1 = "congratulations {}, you have been assigned to {} office"\
                        .format(first_name, allocated_office.room_name.upper())
                    print(msg1)
                    if wants_accomodation.upper() == "Y":
                        msg1 += " However, Staff members Cannot be allocated living space"
                    return msg1
                else:
                    self.office_unallocated.append(employee_number.upper())
                    sorrymsg = "sorry, all rooms are full at this time."
                    print(sorrymsg)
                    return sorrymsg

            elif job_type.upper() == "FELLOW":
                fellow = Fellow(employee_number.upper(), first_name.upper(), last_name.upper(), job_type.upper(),
                                wants_accomodation.upper())
                self.all_people.append(fellow)
                self.fellows_list.append(fellow)
                allocated_office = self.generate_room("OFFICE")
                kudosmsg = ''
                if allocated_office:
                    self.office_allocations[allocated_office.room_name].append(employee_number.upper())
                    allocated_office.occupants += 1
                    kudosmsg = "congratulations {}, you have been assigned to {} office"\
                        .format(first_name, allocated_office.room_name.upper())
                else:
                    self.office_unallocated.append(employee_number.upper())
                    kudosmsg = "sorry, all rooms are full at this time."

                if wants_accomodation.upper() == "Y":
                    allocated_lspace = self.generate_room("LSPACE")
                    if allocated_lspace:
                        self.lspace_allocations[allocated_lspace.room_name].append(employee_number.upper())
                        allocated_lspace.occupants += 1
                        kudosmsg = "congratulations {}, you have been assigned to {} living space"\
                            .format(first_name, allocated_lspace.room_name)

                    else:
                        person = employee_number.upper()
                        self.lspace_unallocated.append(person)
                        kudosmsg = "sorry, all living space rooms are full at this time."
                return kudosmsg

    def reallocate_person(self, employee_number, new_room):

        """ Reallocate the person with person_identifier to new_room_name. """
        all_employees_numbers = [person.employee_number for person in self.all_people]
        # check if the person exist in amity
        if employee_number.upper() not in all_employees_numbers:
            return "{} does not exist".format(employee_number.upper())

        all_rooms_names = [room.room_name for room in self.all_rooms]
        # check if room exist in amity
        if new_room.upper() not in all_rooms_names:
            return "Room with name {} does not exist".format(new_room.upper())

        room_type = self.check_room_type(new_room.upper())
        current_room = self.check_allocated_room(employee_number.upper(), room_type.upper())
        job_type = self.check_employee_job_type(employee_number)
        if room_type.upper() == "LSPACE":
            # check if trying to reallocate staff to Livingspace
            if job_type.upper() == "STAFF":
                return "Sorry you cannot allocate staff living space!"
            # check whether the person is already in the allocated room
            if employee_number.upper() in self.lspace_allocations[new_room.upper()]:
                return "The Person is already allocated in the requested room"
            new_room_occupant_count = [room.occupants for room in self.all_rooms if room.room_name ==
                                       new_room.upper()]
            if current_room:
                if new_room_occupant_count[0] < 4:
                    self.lspace_allocations[current_room.upper()].remove(employee_number.upper())
                    self.lspace_allocations[new_room.upper()].append(employee_number.upper())
                    for room in self.all_rooms:
                        if room.room_name == new_room.upper():
                            room.occupants += 1
                        if room.room_name == current_room:
                            room.occupants -= 1
                    return "{} has been moved to {}".format(employee_number.upper(), new_room.upper())
                return "Sorry the LivingSpace is currently fully occupied!"

            else:
                if new_room_occupant_count[0] < 4:
                    for room in self.all_rooms:
                        if room.room_name == new_room.upper():
                            room.occupants += 1
                    self.lspace_unallocated.remove(employee_number.upper())
                    self.lspace_allocations[new_room.upper()].append(employee_number.upper())
                    return "{} has been moved to {}".format(employee_number.upper(), new_room.upper())
                return "Sorry the LivingSpace is currently fully occupied!"

        if room_type.upper() == "OFFICE":
            # check whether the person is already in the allocated room
            if employee_number.upper() in self.office_allocations[new_room.upper()]:
                return "The Person is already allocated in the requested room"
            new_room_occupant_count = [room.occupants for room in self.all_rooms if
                                       room.room_name == new_room.upper()]
            if current_room:
                if new_room_occupant_count[0] < 6:
                    for room in self.all_rooms:
                        if room.room_name == new_room.upper():
                            room.occupants += 1
                        if room.room_name == current_room:
                            room.occupants -= 1
                    self.office_allocations[current_room.upper()].remove(employee_number.upper())
                    self.office_allocations[new_room.upper()].append(employee_number.upper())
                    return "{} has been moved to {}".format(employee_number.upper(), new_room.upper())
                return "Sorry the Office is currently fully occupied!"

            else:
                if new_room_occupant_count[0] < 6:
                    for room in self.all_rooms:
                        if room.room_name == new_room.upper():
                            room.occupants += 1
                    self.office_unallocated.remove(employee_number.upper())
                    self.office_allocations[new_room.upper()].append(employee_number.upper())
                    return "{} has been moved to {}".format(employee_number.upper(), new_room.upper())
                return "Sorry the Office is currently fully occupied!"

    def check_room_type(self, name):
        """checks room type allocated to a person"""
        for room in self.all_rooms:
            if name.upper() == room.room_name:
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
        return None

    def check_employee_job_type(self, empno):
        """Check person job type using employee number"""
        for empnos in self.all_people:
            if empnos.employee_number == empno.upper():
                return empnos.job_type
            return None

    def load_people(self, filename):
        """Adds people to rooms from a text file"""

        if os.path.exists(filename):
            with open(filename) as inputfl:

                content = inputfl.readlines()
                if not content:
                    return "The file is empty"
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

                    self.add_person(empno.upper(), first_name.upper(), last_name.upper(), job_type.upper(),
                                    accomodation.upper())

                return "File data added successfully"
        return "Please provide valid a text file name !"

    def print_allocations(self, filename=None):
        """Prints a list of allocations onto the screen. Specifying the optional -o option here outputs the registered
        allocations to a txt file"""
        if self.office_allocations or self.lspace_allocations:
            output = ""
            output += '\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC
            heading = 'AMITY OFFICE ALLOCATIONS'
            output += '\n\n\t\t\t\t\t' + bcolors.HEADER + bcolors.BOLD + heading.upper() + '\n' + bcolors.ENDC
            output += '\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC + '\n'
            if filename:
                file = open(filename + ".txt", "a")
                file.write('\t' + "-" * 50 + '\n\t\t\t\t\t' + heading.upper() + '\n\t' + "-" * 50 + "\n")
            for office, empnos in self.office_allocations.items():
                output += '\n\t' + bcolors.OKGREEN + office + bcolors.ENDC + "\n"
                names = ''
                for empno in empnos:
                    firstname = [person.first_name for person in self.all_people if person.employee_number.upper() == empno]
                    lastname = [person.last_name for person in self.all_people if person.employee_number.upper() == empno]
                    names += firstname[0].capitalize() + " " + lastname[0].capitalize() + ", "
                output += '\n\t' + bcolors.OKBLUE + names + bcolors.ENDC
                output += '\n\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC + '\n'

                if filename:
                    file = open(filename + ".txt", "a")
                    file.write('\n')
                    file.write('\t' + office + "\n")
                    file.write('\t' + names)
                    file.write('\n\t' + "_" * 50 + "\n")
            output += '\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC
            heading = 'AMITY LIVING SPACE ALLOCATIONS'
            output += '\n\n\t\t\t\t\t' + bcolors.HEADER + bcolors.BOLD + heading.upper() + '\n' + bcolors.ENDC
            output += '\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC + '\n'
            for lspace, empnos in self.lspace_allocations.items():
                output += '\n\t' + bcolors.OKGREEN + lspace + bcolors.ENDC + '\n'
                lspace_names = ''
                for empno in empnos:
                    firstname = [person.first_name for person in self.all_people if person.employee_number.upper() == empno]
                    lastname = [person.last_name for person in self.all_people if person.employee_number.upper() == empno]
                    lspace_names += firstname[0].capitalize() + " " + lastname[0].capitalize() + ", "
                output += '\n\t' + bcolors.OKBLUE + lspace_names + bcolors.ENDC
                output += '\n\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC + '\n'

                if filename:
                    file = open(filename + ".txt", "a")
                    file.write("\n")
                    file.write('\t' + lspace + "\n")
                    file.write('\t' + lspace_names)
                    file.write('\n\t' + "_" * 50 + "\n")

            return output
        return "No person allocated room yet!"

    def print_unallocated(self, filename=None):
        """Prints a list of unallocated people to the screen. Specifying the -o option here outputs the information to
        the txt file provided"""

        if self.office_unallocated or self.lspace_unallocated:
            output = ""
            output += '\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC
            heading = 'UNALLOCATED OFFICE'
            output += '\n\n\t\t\t\t\t' + bcolors.HEADER + bcolors.BOLD + heading.upper() + '\n' + bcolors.ENDC
            output += '\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC + '\n'
            names = ''
            for employee_number in self.office_unallocated :
                firstname = [person.first_name for person in self.all_people if person.employee_number.upper() == employee_number]
                lastname = [person.last_name for person in self.all_people if person.employee_number.upper() == employee_number]
                names += firstname[0].capitalize() + " " + lastname[0].capitalize() + ", "
            output += '\n\t' + bcolors.OKBLUE + names + bcolors.ENDC
            output += '\n\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC
            heading2 = 'UNALLOCATED LIVING SPACE'
            output += '\n\n\t\t\t\t\t' + bcolors.HEADER + bcolors.BOLD + heading2.upper() + '\n' + bcolors.ENDC
            output += '\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC + '\n'
            lspace_names = ''
            for employee_numb in self.lspace_unallocated:
                fname = [person.first_name for person in self.all_people if
                             person.employee_number.upper() == employee_numb]
                lname = [person.last_name for person in self.all_people if
                            person.employee_number.upper() == employee_numb]
                lspace_names += fname[0].capitalize() + " " + lname[0].capitalize() + ", "
            output += '\n\t' + bcolors.OKBLUE + lspace_names + bcolors.ENDC
            output += '\n\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC + '\n'
            if filename:
                file = open(filename + ".txt", "a")
                file.write("-" * 50 + "\n" + " " * 15 + "UNALLOCATED OFFICE\n" + "-" * 50 + "\n")
                file.write(names)
                file.write("\n")
                file.write("-" * 50 + "\n" + " " * 15 + "UNALLOCATED LIVING SPACE\n" + "-" * 50 + "\n")
                file.write(lspace_names)
                file.close()
            return output
        return "No one in the unallocated list!"

    def print_room(self, room_name):
        """Prints  the names of all the people in room_name on the screen."""

        all_rooms_names = [room.room_name for room in self.all_rooms]
        if room_name.upper() in all_rooms_names:
            output = ''
            for room in self.all_rooms:
                if room_name.upper() == room.room_name:
                    output += '\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC
                    output += '\n\n\t\t\t\t\t' + bcolors.HEADER + bcolors.BOLD + room_name.upper() + '\n' + bcolors.ENDC
                    output += '\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC + '\n'
                    if room.room_type == 'lspace'.upper():
                        if room_name.upper() in self.lspace_allocations:
                            empnos = self.lspace_allocations[room_name.upper()]
                            if len(empnos):
                                names = ''
                                for empno in empnos:
                                    firstname = [person.first_name for person in self.all_people if
                                                 person.employee_number.upper() == empno]
                                    lastname = [person.last_name for person in self.all_people if
                                                person.employee_number.upper() == empno]
                                    names += firstname[0].capitalize() + " " + lastname[0].capitalize() + ", "

                                output += '\n\t' + bcolors.OKBLUE + names + bcolors.ENDC
                                output += '\n\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC + '\n'
                            else:
                                output += "No one is allocated to {} room".format(room_name)

                    elif room.room_type == 'office'.upper():
                        if room_name.upper() in self.office_allocations:
                            empnos = self.office_allocations[room_name.upper()]
                            if len(empnos):
                                lspace_names = ''
                                for empno in empnos:
                                    firstname = [person.first_name for person in self.all_people if
                                                 person.employee_number.upper() == empno]
                                    lastname = [person.last_name for person in self.all_people if
                                                person.employee_number.upper() == empno]
                                    lspace_names += firstname[0].capitalize() + " " + lastname[0].capitalize() + ", "

                                output += '\n\t' + bcolors.OKBLUE + lspace_names + bcolors.ENDC
                                output += '\n\t' + bcolors.HEADER + bcolors.UNDERLINE + ' ' * 55 + bcolors.ENDC + '\n'
                            else:
                                output += "No one is allocated to {} room".format(room_name)

            return output
        return "The room with the name {} does not exist.".format(room_name)

    def save_state(self, dbname=None):
        """ Persists all the data stored in the app to a SQLite database. Specifying the --db parameter explicitly
        stores the data in the sqlite_database specified"""
        engine = create_db(dbname)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        items = select([Rooms])
        result = session.execute(items)

        database_rooms_list = [item.room_name for item in result]
        for room in self.all_rooms:
            if room.room_name not in database_rooms_list:
                new_room = Rooms(room_name=room.room_name,
                                 room_type=room.room_type,
                                 occupants=room.occupants,
                                 max_occupants=room.max_occupants)
                session.add(new_room)
                session.commit()

        people = select([Employees])
        response = session.execute(people)

        dbempno_list = [item.person_number for item in response]
        print("saving state....")
        for person in self.all_people:
            list_index = self.all_people.index(person)
            empno = self.all_people[list_index].employee_number
            if empno not in dbempno_list:
                office_allocated = self.check_allocated_room(empno.upper(), 'OFFICE')
                if office_allocated is None:
                    office_allocated = 'N'
                lspace_allocated = self.check_allocated_room(empno.upper(), 'LSPACE')
                if lspace_allocated is None:
                    lspace_allocated = 'N'
                person_fname = self.all_people[list_index].first_name
                person_lname = self.all_people[list_index].last_name
                person_job_type = self.all_people[list_index].job_type
                wants_accommodation = self.all_people[list_index].wants_accommodation
                new_person = Employees(employee_number=empno,
                                       first_name=person_fname,
                                       last_name=person_lname,
                                       job_type=person_job_type,
                                       wants_accommodation=wants_accommodation,
                                       lspace_allocated=lspace_allocated,
                                       office_allocated=office_allocated)
                session.add(new_person)
                session.commit()

    def load_state(self, dbname):
        """Loads data from a database into the application."""
        if os.path.exists(dbname):
            try:
                engine = create_engine('sqlite:///' + dbname)
                Session = sessionmaker(bind=engine)
                session = Session()

                people = session.query(Employees).all()
                rooms = session.query(Rooms).all()
                all_rooms_names = [room.room_name for room in self.all_rooms]
                for room in rooms:
                    if room.room_name not in all_rooms_names:
                        if room.room_type.upper() == "LSPACE":
                            lspace = LivingSpace(room.room_name.upper(), room.room_type.upper())
                            lspace.occupants = room.occupants
                            self.all_rooms.append(lspace)
                        elif room.room_type.upper() == "OFFICE":
                            office = Office(room.room_name.upper(), room.room_type.upper())
                            office.occupants = room.occupants
                            self.all_rooms.append(office)
                all_people_numbers = [person.employee_number for person in self.all_people]
                for person in people:
                    if person.employee_number not in all_people_numbers:
                        if person.job_type.upper() == "FELLOW":
                            fellow = Fellow(person.employee_number.upper(), person.first_name.upper(), person.last_name.upper(),
                                            person.job_type.upper(), person.wants_accommodation.upper())

                            self.all_people.append(fellow)
                            self.fellows_list.append(fellow)
                            if person.lspace_allocated.upper() == "N":
                                if person.employee_number.upper() not in self.lspace_unallocated:
                                    self.lspace_unallocated.append(person.employee_number.upper())
                            else:
                                self.lspace_allocations[person.lspace_allocated].append(person.employee_number.upper())

                            if person.office_allocated.upper() == "N":
                                if person.employee_number.upper() not in self.office_unallocated:
                                    self.office_unallocated.append(person.employee_number.upper())
                            else:
                                self.office_allocations[person.office_allocated].append(person.employee_number.upper())

                        elif person.job_type.upper() == "STAFF":
                            staff = Staff(person.employee_number.upper(), person.first_name.upper(), person.last_name.upper(),
                                          person.job_type.upper(), person.wants_accommodation.upper())
                            self.all_people.append(staff)
                            self.staff_list.append(staff)
                            if person.office_allocated.upper() == "N":
                                if person.employee_number.upper() not in self.office_unallocated:
                                    self.office_unallocated.append(person.employee_number.upper())
                            else:
                                self.office_allocations[person.office_allocated].append(person.employee_number.upper())
                return "loading data from {} done".format(dbname)
            except:
                return "There was error loading from database"

        return "Database with name {} does not exist".format(dbname)











