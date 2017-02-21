import unittest
from app.amity import *


class AmityTestCase(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()

    def test_adds_person(self):
        """Test it adds a person to Amity"""
        person_count_before = len(self.amity.all_people)
        self.amity.add_person("cn03", "Ivan", "Kipyegon", "fellow", "y")
        self.assertEqual(len(self.amity.all_people), person_count_before + 1)

    def test_error_adding_person_with_duplicate_employee_number(self):
        """Test it does not add person more than once"""
        self.amity.add_person("CN14", "Chris", "Rock", "staff")
        employee_numbers = [people.employee_number for people in self.amity.all_people]
        self.assertIn("CN14", employee_numbers)
        self.assertEqual(self.amity.add_person("cn14", "Chris", "Rock", "staff"),
                         "sorry, this user already exists.please enter valid employee number")

    def test_add_person_no_office_created(self):
        """Test adding person with no room created"""
        self.assertEqual(self.amity.add_person("cn05", "Sam", "Wanjala", "Fellow"),
                         "sorry, all rooms are full at this time.")

    def test_add_person_no_livingspace_created(self):
        """Testing adding person with no living space created"""
        self.assertEqual(self.amity.add_person("cn05", "Sam", "Wanjala", "Fellow", "Y"),
                         "sorry, all living space rooms are full at this time.")

    def test_add_person_does_not_allocate_fully_occupied_office(self):
        """Testing adding a person to fully occupied office """
        people_list = {"cn01": ["Sam", "wanjala", "Fellow"],
                       "cn02": ["Gideon", "Gitau", "Fellow"],
                       "cn03": ["Charles", "Muthini", "Fellow"],
                       "cn04": ["Roger", "Taracha", "Staff"],
                       "cn05": ["Mahad", "Walusimbi", "Fellow"],
                       "cn06": ["Percila", "Njira", "Staff"],
                       "cn07": ["Bryan", "Rotich", "Fellow"]}
        self.amity.create_room("office", ["Mordor"])
        for empno in people_list:
            assigning_office = self.amity.add_person(empno, people_list[empno][0], people_list[empno][1],
                                                     people_list[empno][2])
        self.assertEqual(assigning_office, "sorry, all rooms are full at this time.")

    def test_add_person_does_not_allocate_more_than_livingspace_capacity(self):
        """Test that adding person does not allocate more than living space maximum capacity"""
        fellow_list = {"cn01": ["Sam", "wanjala", "Fellow"],
                       "cn02": ["Gideon", "Gitau", "Fellow"],
                       "cn03": ["Charles", "Muthini", "Fellow"],
                       "cn04": ["Mahad", "Walusimbi", "Fellow"],
                       "cn05": ["Bryan", "Rotich", "Fellow"]}
        self.amity.create_room("lspace", ["Shell"])
        for empno in fellow_list:
            assigning_living_space = self.amity.add_person(empno, fellow_list[empno][0], fellow_list[empno][1],
                                                           fellow_list[empno][2], wants_accomodation="Y")
        self.assertEqual(assigning_living_space, "sorry, all living space rooms are full at this time.")

    def test_add_person_does_not_allocate_staff_living_space(self):
        """Test add_person does not allocate Living space to a staff member"""
        self.amity.create_room("lspace", ["shell"])
        self.amity.create_room("office", ["valhalla"])
        self.assertEqual(self.amity.add_person("cn01", "Ivan", "Kip", "STAFF", wants_accomodation="Y"),
                         "congratulations Ivan, you have been assigned to VALHALLA office However, Staff members "
                         "Cannot be allocated living space")

    def test_create_multiple_rooms(self):
        """Test creating multiple rooms at once"""
        room_count_before = len(self.amity.all_rooms)
        self.amity.create_room("Office", ["Hogwarts", "Oculus", "Valhalla", "Krypton"])
        self.assertEqual(len(self.amity.all_rooms), room_count_before + 4)

    def test_create_room_with_unknown_room_type(self):
        self.assertEqual(self.amity.create_room("livingspace", ["Shell"]), "sorry, that room_type does not exist")

    def test_office_allocation(self):
        """Test it allocates office space"""
        self.amity.create_room("office", ["Valhalla"])
        self.amity.add_person("CN07", "Ken", "Langat", "Staff")
        for room in self.amity.office_allocations:
            self.assertIn("CN07", self.amity.office_allocations[room])

    def test_add_person_allocates_fellow_livingspace(self):
        """Test that add person allocates a fellow living space if wants accommodation"""
        self.amity.create_room("lspace", ["Shell"])
        self.amity.add_person("CN01", "Gedion", "Gitau", "fellow", wants_accomodation="Y")
        for room in self.amity.lspace_allocations:
            self.assertIn("CN01", self.amity.lspace_allocations[room])

    def test_create_room_added_to_system(self):
        """Test it creates room in Amity"""
        room_count_before = len(self.amity.all_rooms)
        self.amity.create_room("Office", ["Valhalla"])
        room_count_after = len(self.amity.all_rooms)
        self.assertEqual(room_count_after, (room_count_before + 1))

    def test_create_room_return_error_on_duplicate_names(self):
        """Test creating room with same name should return warning"""
        name = ["Hogwarts"]
        self.amity.create_room("office", name)
        expected_msg = "sorry, {} room already exists!please choose another name".format(name[0].upper())
        self.assertEqual(self.amity.create_room("office", name), expected_msg)

    def test_reallocate_person_from_office_to_another(self):
        """Test amity can reallocate a person from one office to another"""
        self.amity.create_room("Office", ["Hogwarts"])
        self.amity.add_person("CN01", "Brian", "Rotich", "staff")
        self.amity.create_room("office", ["Valhalla"])
        self.amity.reallocate_person("CN01", "Valhalla")
        self.assertIn("CN01", self.amity.office_allocations["VALHALLA"])

    def test_reallocate_person_from_livingspace_to_another(self):
        """Test amity can reallocate a person from one livingspace list to another"""
        self.amity.create_room("lspace", ["Shell"])
        self.amity.add_person("CN01", "Brian", "Rotich", "fellow", "Y")
        self.amity.create_room("lspace", ["wing"])
        self.amity.reallocate_person("CN01", "wing")
        self.assertIn("CN01", self.amity.lspace_allocations["WING"])

    def test_reallocate_person_from_unallocated_list(self):
        """Test amity can reallocate a person from one unallocated list to office or livingspace"""
        self.amity.add_person("CN01", "Brian", "Rotich", "fellow", "Y")
        self.amity.create_room("office", ["Oculus"])
        self.amity.create_room("lspace", ["Shell"])
        self.amity.reallocate_person("CN01", "Oculus")
        self.amity.reallocate_person("CN01", "Shell")
        self.assertIn("CN01", self.amity.office_allocations["OCULUS"])
        self.assertIn("CN01", self.amity.lspace_allocations["SHELL"])

    def test_reallocate_person(self):
        """Test amity can reallocate a person from one office to another"""
        self.amity.create_room("Office", ["Hogwarts"])
        self.amity.add_person("CN01", "Brian", "Rotich", "staff")
        self.amity.create_room("office", ["Valhalla"])
        self.assertEqual(self.amity.reallocate_person("CN01", "Valhalla"), "CN01 has been moved to VALHALLA",
                         "should return success message")

    def test_reallocate_person_is_removed_from_unallocated_list(self):
        """Test that a reallocated person is removed from unallocated list"""
        self.amity.add_person("CN02", "John", "Doe", "fellow", "Y")
        self.assertIn("CN02", self.amity.office_unallocated)
        self.assertIn("CN02", self.amity.lspace_unallocated)
        self.amity.create_room("office", ["Oculus"])
        self.amity.create_room("lspace", ["shell"])
        self.amity.reallocate_person("CN02", "Oculus")
        self.amity.reallocate_person("CN02", "shell")
        self.assertNotIn("CN02", self.amity.office_unallocated)
        self.assertNotIn("CN02", self.amity.lspace_unallocated)

    def test_reallocate_person_is_removed_from_old_room(self):
        """Test reallocate person removes person from old room"""
        self.amity.create_room("office", ["Oculus"])
        self.amity.create_room("lspace", ["shell"])
        self.amity.add_person("CN01", "Gideon", "Gitau", "fellow", "Y")
        self.assertIn("CN01", self.amity.office_allocations["OCULUS"])
        self.assertIn("CN01", self.amity.lspace_allocations["SHELL"])
        self.amity.create_room("office", ["Valhalla"])
        self.amity.create_room("lspace", ["Wing"])
        self.amity.reallocate_person("CN01", "Valhalla")
        self.amity.reallocate_person("CN01", "Wing")
        self.assertNotIn("CN01", self.amity.office_allocations["OCULUS"])
        self.assertNotIn("CN01", self.amity.lspace_allocations["SHELL"])
        self.assertIn("CN01", self.amity.office_allocations["VALHALLA"])
        self.assertIn("CN01", self.amity.lspace_allocations["WING"])

    def test_reallocate_person_to_fully_occupied_office_room(self):
        """Test reallocating person to fully maximum number of occupants"""
        self.amity.add_person("cn07", "Brian", "Rotich", "Fellow")
        people_list = {"cn01": ["Sam", "wanjala", "Fellow"],
                       "cn02": ["Gideon", "Gitau", "Fellow"],
                       "cn03": ["Charles", "Muthini", "Fellow"],
                       "cn04": ["Rogers", "Taracha", "Staff"],
                       "cn05": ["Mahad", "Walusimbi", "Fellow"],
                       "cn06": ["Percila", "Njira", "Staff"]}
        self.amity.create_room("office", ["Mordor"])
        for empno in people_list:
            self.amity.add_person(empno, people_list[empno][0], people_list[empno][1], people_list[empno][2])

        self.assertEqual(self.amity.reallocate_person("cn07", "Mordor"), "Sorry the Office is currently fully "
                                                                         "occupied!")

    def test_reallocate_person_to_fully_occupied_livingspace_room(self):
        """Test reallocating person to fully maximum number of occupants"""
        self.amity.add_person("cn05", "Brian", "Rotich", "Fellow", "Y")
        people_list = {"cn01": ["Sam", "wanjala", "Fellow", "Y"],
                       "cn02": ["Gideon", "Gitau", "Fellow", "Y"],
                       "cn03": ["Charles", "Muthini", "Fellow", "Y"],
                       "cn04": ["Rogers", "Taracha", "Fellow", "Y"]}
        self.amity.create_room("lspace", ["Shell"])
        for empno in people_list:
            self.amity.add_person(empno, people_list[empno][0], people_list[empno][1], people_list[empno][2],
                                  people_list[empno][3])

        self.assertEqual(self.amity.reallocate_person("cn05", "Shell"), "Sorry the LivingSpace is currently fully occupied!")

    def test_reallocate_staff_to_living_space(self):
        """test reallocating staff to a living space room"""
        self.amity.create_room("Office", ["Krypton"])
        self.amity.add_person("cn06", "Roger", "Taracha", "staff")
        self.amity.create_room("lspace", ["shell"])
        self.assertEqual(self.amity.reallocate_person("CN06", "shell"), "Sorry you cannot allocate staff living space!")

    def test_reallocate_person_same_room(self):
        """Test reallocating person to same room"""
        self.amity.create_room("office", ["Camelot"])
        self.amity.add_person("CN01", "Percila", "Njira", "Staff")
        self.assertEqual(self.amity.reallocate_person("CN01", 'Camelot'), "The Person is already allocated in the "
                                                                          "requested room")

    def test_reallocate_to_non_existent_room(self):
        """Test reallocating person to non-existent room"""
        self.amity.create_room("office", ["Krypton"])
        self.amity.add_person("CN01", "Percila", "Njira", "Staff")
        new_room = ["Valhalla"]
        unregistered_room_allocation = self.amity.reallocate_person("CN01", new_room[0])
        expected_response = "Room with name {} does not exist".format(new_room[0].upper())
        self.assertEqual(unregistered_room_allocation, expected_response)

    def test_reallocation_of_unregistered_person(self):
        """Test reallocating unregistered person"""
        self.amity.create_room("Office", ["Hogwarts"])
        self.amity.add_person("CN01", "Percila", "Njira", "Staff")
        self.amity.create_room("office", ["Valhalla"])
        misplelled_employer_number = "CNO1"
        self.assertEqual((self.amity.reallocate_person(misplelled_employer_number, "Valhalla")),
                         ("{} does not exist".format(misplelled_employer_number.upper())))

    def test_prints_unallocated_prints_to_file(self):
        """Test print unallocated people to text file"""

        self.amity.add_person("cn05", "Roger", "Taracha", "Fellow")
        self.amity.add_person("cn04", "Mahad", "Walusimbi", "Fellow")
        self.amity.add_person("cn03", "Charles", "Muthini", "Fellow")
        self.amity.add_person("cn02", "Sam", "Wanjala", "Fellow")
        self.amity.add_person("cn01", "Gideon", "Gitau", "Fellow")
        self.amity.print_unallocated('test_print')
        self.assertTrue(os.path.isfile('test_print.txt'))
        os.remove('test_print.txt')

    def test_prints_unallocated_with_all_people_allocated_rooms(self):
        """Test print unallocated people to text file"""
        self.amity.create_room("office", ["Camelot"])
        self.amity.add_person("cn05", "Roger", "Taracha", "Fellow")
        self.amity.add_person("cn04", "Mahad", "Walusimbi", "Fellow")
        self.amity.add_person("cn03", "Charles", "Muthini", "Fellow")
        self.amity.add_person("cn02", "Sam", "Wanjala", "Fellow")
        self.amity.add_person("cn01", "Gideon", "Gitau", "Fellow")
        self.assertEqual(self.amity.print_unallocated(), "All people have been allocated rooms!")

    def test_print_room_with_non_existent_room_name(self):
        """Test printing room with non existent room in amity"""
        name = 'oculus'
        self.assertEqual(self.amity.print_room(name), "The room with the name {} does not exist.".format(name))

    def test_prints_allocations_to_text_file(self):
        """Test printing allocations to text file """
        self.amity.create_room('office', ['valhalla'])
        self.amity.add_person("cn05", "Roger", "Taracha", "Fellow")
        self.amity.add_person("cn04", "Mahad", "Walusimbi", "Fellow")
        self.amity.add_person("cn03", "Charles", "Muthini", "Fellow")
        self.amity.add_person("cn02", "Sam", "Wanjala", "Fellow")
        self.amity.add_person("cn01", "Gideon", "Gitau", "Fellow")
        self.amity.print_allocations('test_print')
        self.assertTrue(os.path.isfile('test_print.txt'))
        os.remove('test_print.txt')

    def test_save_state(self):
        """Test that save state creates database and persist the data to database from memory"""
        self.amity.save_state('test')
        self.assertTrue(os.path.isfile('test.db'))
        os.remove('test.db')

    def test_load_from_file(self):
        """Test adding people fro text file"""
        self.amity.create_room("lspace", ["Shell", "wing"])
        self.amity.create_room("office", ["Valhalla", "Oculus"])
        import os
        path = os.path.realpath("data.txt")
        self.amity.load_people(path)
        self.assertEqual(len(self.amity.fellows_list), 4)
        self.assertEqual(len(self.amity.staff_list), 3)

    def test_load_people_from_non_existent_filename(self):
        """Test loading data from non existen file or filepath"""
        self.amity.create_room("office", ["hogwarts"])
        self.assertEqual(self.amity.load_people('datax.txt'), "Please provide valid a text file name !")

    def test_load_from_empty_file(self):
        """Test loading data from empty text file"""
        self.amity.create_room('office', ["oculus"])
        filename = "empty.txt"
        file = open(filename, "a")
        file.write('')
        self.assertTrue(os.path.isfile(filename))
        self.assertEqual(self.amity.load_people(filename), "The file is empty")
        os.remove(filename)

    def test_load_state_with_non_existent_database(self):
        db_name = 'test.db'
        self.assertFalse(os.path.isfile(db_name))
        self.assertEqual(self.amity.load_state('test.db'), "Database with name {} does not exist".format(db_name))


if __name__ == '__main__':
    unittest.main()
