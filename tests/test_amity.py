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

    def test_add_person_duplicate_employee_number(self):
        """Test it does not add person more than once"""
        self.amity.add_person("cn14", "Chris", "Rock", "staff")
        people_names = [people.employee_number for people in self.amity.all_people]
        self.assertIn("cn14", people_names)
        self.assertEqual(self.amity.add_person("cn14", "Chris", "Rock", "staff"),
                         "sorry, this user already exists.please enter valid employee number")

    def test_add_person_no_office_created(self):
        """Test adding person with no room created"""
        self.assertEqual(self.amity.add_person("cn05", "Sam", "Wanjala", "Fellow"),
                         "sorry, all rooms are full at this time.")

    def test_add_person_no_livingspace_created(self):
        self.assertEqual(self.amity.add_person("cn05", "Sam", "Wanjala", "Fellow", "Y"),
                         "sorry, all living space rooms are full at this time.")

    def test_add_person_not_allow_more_than_capacity_office_allocation(self):
        people_list = {"cn01": ["Sam", "wanjala", "Fellow"],
                       "cn02": ["Gideon", "Gitau", "Fellow"],
                       "cn03": ["Charles", "Muthini", "Fellow"],
                       "cn04": ["Rogers", "Taracha", "Staff"],
                       "cn05": ["Mahad", "Walusimbi", "Fellow"],
                       "cn06": ["Percila", "Njira", "Staff"],
                       "cn07": ["Bryan", "Rotich", "Fellow"]}
        self.amity.create_room("office", "Mordor")
        for empno in people_list:
            assigning_office = self.amity.add_person(empno, people_list[empno][0], people_list[empno][1],
                                                     people_list[empno][2])
        self.assertEqual(assigning_office, "sorry, all rooms are full at this time.")

    def test_add_person_not_allow_more_than_capacity_living_space_allocation(self):
        fellow_list = {"cn01": ["Sam", "wanjala", "Fellow"],
                       "cn02": ["Gideon", "Gitau", "Fellow"],
                       "cn03": ["Charles", "Muthini", "Fellow"],
                       "cn04": ["Mahad", "Walusimbi", "Fellow"],
                       "cn05": ["Bryan", "Rotich", "Fellow"]}
        self.amity.create_room("lspace", "Shell")
        for empno in fellow_list:
            assigning_living_space = self.amity.add_person(empno, fellow_list[empno][0], fellow_list[empno][1],
                                                           fellow_list[empno][2], wants_accomodation="Y")
        self.assertEqual(assigning_living_space, "sorry, all living space rooms are full at this time.")

    def test_add_person_does_not_allocate_staff_living_space(self):
        self.amity.create_room("lspace", "shell")
        self.assertEqual(self.amity.add_person("cn01", "Ivan", "Kip", "STAFF", wants_accomodation="Y"),
                         "Staff members Cannot be allocated living space")

    def test_create_multiple_rooms(self):
        room_count_before = len(self.amity.all_rooms)
        self.amity.create_room("Office", "Hogwarts", "Oculus", "Valhalla", "Krypton")
        self.assertEqual(len(self.amity.all_rooms), room_count_before + 4)

    def test_office_allocation(self):
        self.amity.create_room("office", "Valhalla")
        self.amity.add_person("CN07", "Ken", "Langat", "Staff")
        for room in self.amity.office_allocations:
            self.assertIn("CN07", self.amity.office_allocations[room])

    def test_add_person_allocates_fellow_livingspace_with_want_accomadation_option(self):
        self.amity.create_room("lspace", "Shell")
        self.amity.add_person("CN01", "Gedion", "Gitau", "fellow", wants_accomodation="Y")
        for room in self.amity.lspace_allocations:
            self.assertIn("CN01", self.amity.lspace_allocations[room])

    def test_create_room_added_to_system(self):
        room_count_before = len(self.amity.all_rooms)
        self.amity.create_room("Office", "Valhalla")
        room_count_after = len(self.amity.all_rooms)
        self.assertEqual(room_count_after, (room_count_before + 1))

    def test_create_room_return_error_on_duplicate_names(self):
        name = "Hogwarts"
        self.amity.create_room("office", name)
        msg = self.amity.create_room("office", name)
        expected_msg = "sorry, {} room already exists!please choose another name".format(name)
        self.assertEqual(msg, expected_msg)

    def test_reallocate_person(self):
        self.amity.create_room("Office", "Hogwarts")
        self.amity.add_person("Bryan", "staff")
        self.amity.create_room("office", "Valhalla")
        self.amity.reallocate_person("Bryan", "Valhalla")
        self.assertIn("Bryan", self.amity.office_allocations.values())

    def test_person_is_removed_from_old_room(self):
        self.amity.create_room("office", "Oculus")
        self.amity.add_person("CN01", "Gideon", "Gitau", "staff")
        self.assertIn("CN01", self.amity.office_allocations["Oculus"])
        self.amity.create_room("office", "Valhalla")
        self.amity.reallocate_person("CN01", "Valhalla")
        self.assertNotIn("CN01", self.amity.office_allocations["Oculus"])

    def test_prints_unallocated(self):
        self.amity.add_person("cn05", "Roger", "Taracha", "Fellow")
        self.amity.add_person("cn04", "Mahad", "Walusimbi", "Fellow")
        self.amity.add_person("cn03", "Charles", "Muthini", "Fellow")
        self.amity.add_person("cn02", "Sam", "Wanjala", "Fellow")
        self.amity.add_person("cn01", "Gideon", "Gitau", "Fellow")
        self.amity.print_unallocated('test_print')
        self.assertTrue(os.path.isfile('test_print.txt'))
        os.remove('test_print.txt')

    def test_print_room_with_non_existent_room_name(self):
        name = 'oculus'
        self.assertEqual(self.amity.print_room(name), "The room with the name {} does not exist.".format(name))

    def test_prints_allocations_with_filename(self):
        self.amity.create_room('office', 'valhalla')
        self.amity.add_person("cn05", "Roger", "Taracha", "Fellow")
        self.amity.add_person("cn04", "Mahad", "Walusimbi", "Fellow")
        self.amity.add_person("cn03", "Charles", "Muthini", "Fellow")
        self.amity.add_person("cn02", "Sam", "Wanjala", "Fellow")
        self.amity.add_person("cn01", "Gideon", "Gitau", "Fellow")
        self.amity.print_allocations('test_print')
        self.assertTrue(os.path.isfile('test_print.txt'))
        os.remove('test_print.txt')

    def test_save_state(self):
        self.amity.save_state('test.db')
        self.assertTrue(os.path.isfile('test.db'))
        os.remove('test.db')

    def test_reallocate_person_to_fully_occupied_room(self):
        people_list = {"Sam": "Fellow", "Gideon": "Fellow", "Charles": "Fellow", "Rogers": "Staff", "Mahad": "Fellow",
                       "Percila": "Staff"}
        self.amity.create_room("Office", "Kenya")
        for name in people_list:
            self.amity.add_person(name, people_list[name])
        self.amity.add_person("Batian", "Fellow")
        self.assertEqual(self.amity.reallocate_person("Batian7", "Kenya"), "Sorry the office is fully occupied")

    def test_reallocate_staff_to_living_space(self):
        self.amity.create_room("Office", "Longonot")
        self.amity.add_person("chelimo", "Staff")
        self.amity.create_room("lspace", "Shell")
        allocating_staff_living_space = self.amity.reallocate_person("chelimo", "Shell")
        self.assertEqual(allocating_staff_living_space, "Sorry you cannot allocate staff living space")

    def test_reallocate_person_same_room(self):
        self.amity.create_room("office", "Camelot")
        self.amity.add_person("Percila", "Staff")
        already_present = self.amity.reallocate_person("Percila", 'Camelot')
        self.assertEqual(already_present, "The Person is already allocated in the requested room")





if __name__ == '__main__':
    unittest.main()
