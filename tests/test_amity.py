import unittest
from unittest.mock import patch

from app.amity import *


class AmityTestCase(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()

    def test_adds_person(self):
        person_count_before = len(self.amity.all_people)
        self.amity.add_person("Ivan", "fellow", "y")
        person_count_after = len(self.amity.all_people)
        self.assertEqual(person_count_after, person_count_before + 1)

    def test_add_person_duplicate_name(self):
        self.amity.add_person("Chris", "staff")
        people_names = [people.person_name for people in self.amity.all_people]
        self.assertIn("Chris", people_names)
        self.assertEqual(self.amity.add_person("Chris", "staff"),
                         "sorry, this user already exists.please choose another name")

    def test_add_person_no_room(self):
        self.assertEqual(self.amity.add_person("Sam", "Fellow", "Y"), "sorry, all rooms are full at this time.")

    def test_add_person_not_allow_more_than_capacity_office_allocation(self):
        people_list = {"Sam": "Fellow", "Gideon": "Fellow", "Charles": "Fellow", "Rogers": "Staff", "Mahad": "Fellow",
                       "Percila": "Staff", "Brian": "Fellow"}
        self.amity.create_room("office", "Mordor")
        for name in people_list:
            assigning_office = self.amity.add_person(name, people_list[name])
        self.assertEqual(assigning_office, "sorry, all rooms are full at this time.")

    def test_add_person_not_allow_more_than_capacity_living_space_allocation(self):
        fellow_list = {"Sam": "Fellow", "Gideon": "Fellow", "Charles": "Fellow",  "Mahad": "Fellow", "Brian": "Fellow"}
        self.amity.create_room("lspace", "Shell")
        for name in fellow_list:
            assigning_living_space = self.amity.add_person(name, fellow_list[name], wants_accomodation="Y")
        self.assertEqual(assigning_living_space, "sorry, all rooms are full at this time.")

    def test_add_person_does_not_allocate_staff_living_space(self):
        self.assertEqual(self.amity.add_person("Ivan", "STAFF", "Y"), "Cannot allocate staff living space")

    def test_create_multiple_rooms(self):
        room_count_before = len(self.amity.all_rooms)
        self.amity.create_room("Office", "Hogwarts", "Oculus", "Valhalla", "Krypton")
        self.assertEqual(len(self.amity.all_rooms), room_count_before + 4)

    def test_office_allocation(self):
        self.amity.add_person("Ken", "Staff", "Y")
        for room, occupants in self.amity.office_allocations:
            self.assertIn("Ken", self.amity.office_allocations[occupants])

    def test_add_person_allocates_fellow_livingspace_with_want_accomadation_option(self):
        self.amity.add_person("Cheru", "fellow", "Y")
        for room, occupants in self.amity.lspace_allocations:
            self.assertIn("Cheru", self.amity.lspace_allocations[occupants])

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
        self.amity.add_person("Gideon", "staff")
        self.assertIn("Gideon", self.amity.office_allocations["Oculus"])
        self.amity.create_room("office", "Valhalla")
        self.amity.reallocate_person("Gideon", "Valhalla")
        self.assertNotIn("Gideon", self.amity.office_allocations["Oculus"])

    def test_it_prints_unallocated(self):
        self.amity.print_unallocated('test_print')
        self.assertTrue(os.path.isfile('test_print.txt'))
        os.remove('test_print.txt')

    def test_it_saves_state(self):
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

    def test_reallocate_to_non_existent_room(self):
        self.amity.create_room("office", "Krypton")
        self.amity.add_person("Kip", "Fellow")
        new_room = "Valhalla"
        unregistered_room_allocation = self.amity.reallocate_person("Kip", new_room)
        expected_response = "Room with name {} does not exist".format(new_room)
        self.assertEqual(unregistered_room_allocation, expected_response)

    def test_reallocation_of_unregistered_person(self):
        self.amity.create_room("Office", "Hogwarts")
        self.amity.add_person("Bryan", "staff")
        self.amity.create_room("office", "Valhalla")
        person_name = "Bryankip"
        self.assertEqual((self.amity.reallocate_person(person_name, "Valhalla")),
                         ("{} does not exist".format(person_name)))

    def test_load_from_file(self):
        self.amity.create_room("lspace", "Shell", "wing")
        self.amity.create_room("office", "Valhalla", "Oculus")
        path = os.path.realpath("data.txt")
        self.amity.load_people(path)
        self.assertEqual(len(self.amity.fellows_list), 4)
        self.assertEqual(len(self.amity.staff_list), 3)


if __name__ == '__main__':
    unittest.main()
