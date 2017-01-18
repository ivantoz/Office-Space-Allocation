import unittest

from app.model import *


class AmityTestCase(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.amity.all_people = []
        self.amity.all_rooms = []
        self.amity.office_allocations = defaultdict(list)
        self.amity.lspace_allocations = defaultdict(list)
        self.amity.fellows_list = []
        self.amity.staff_list = []



    def test_adds_person(self):
        self.amity.add_person("Ivan", "fellow", "y")
        self.assertEqual(len(self.amity.all_people), 1)

    def test_add_person_duplicate_name(self):
        self.amity.add_person("Chris", "staff")
        people_names = [people.person_name for people in self.amity.all_people]
        self.assertIn("Chris", people_names)
        msg = self.amity.add_person("Chris", "staff")
        self.assertEqual(msg, "sorry, this user already exists.please choose another name")

    def test_add_person_no_room(self):
        self.assertEqual(self.amity.add_person("Sam", "Fellow", "Y"), "sorry, all rooms are full at this time.")

    def test_add_person_not_allow_more_than_capacity(self):
        self.assertEqual(True, False)

    def test_add_person_does_not_allocate_staff_living_space(self):
        self.assertEqual((self.amity.add_person("Ivan", "STAFF", "Y")), "Cannot allocate staff living space")

    def test_create_multiple_rooms(self):
        room_name = ["Hogwarts", "Oculus", "Valhalla", "Krypton"]
        room_count = len(room_name)
        for room in room_name:
            self.amity.create_room("Office", room)

        self.assertEqual(len(self.amity.all_rooms), room_count)

    def test_office_allocation(self):
        self.amity.add_person("Ken", "Staff", "Y")
        for room, occupants in self.amity. office_allocations:
            self.assertIn("Ken", self.amity.office_allocations[occupants])

    def test_add_person_allocates_fellow_livingspace_with_want_accomadation_option(self):
        self.amity.add_person("Cheru", "fellow", "Y")
        for room, occupants in self.amity.lspace_allocations:
            self.assertIn("Cheru", self.amity.lspace_allocations[occupants])

    def test_create_room_added_to_system(self):
        self.amity.create_room("Office", "Valhalla")
        self.assertEqual(len(self.amity.all_rooms), 1)

    def test_create_room_duplicate_names(self):
        name = "Hogwarts"
        self.amity.create_room("office", name)
        r_names = [r.room_name for r in self.amity.all_rooms]
        self.assertIn(name, r_names)
        msg = self.amity.create_room("office", name)
        expected_msg = "sorry, {} room already exists!please choose another name".format(name)
        self.assertEqual(msg, expected_msg)

    def test_reallocate_person(self):
        self.amity.create_room("Office", "Hogwarts")
        self.amity.add_person("Bryan", "staff")
        print(self.amity.office_allocations)
        self.amity.reallocate_person("Bryan", "Hogwarts")
        self.assertIn("Bryan", self.amity.office_allocations["Hogwarts"])

    def test_reallocate_person_without_person_identifier(self):
        self.assertEqual(True, False)

    def test_reallocate_person_without_room_name_input(self):
        self.assertEqual(True, False)

    def test_reallocate_person_does_not_want_accomodation(self):
        self.assertEqual(True, False)

    def test_reallocate_staff_to_living_space(self):
        self.assertEqual(True, False)

    def test_reallocate_to_unregistered_room(self):
        self.assertEqual(True, False)

    def test_reallocation_of_unregistered_person(self):
        self.assertEqual(True, False)

    def test_print_registered_allocation_to_text(self):
        self.assertEqual(True, False)

    def test_it_prints_allocations(self):
        self.assertEqual(True, False)

    def test_it_prints_unaloccated_people(self):
        self.assertEqual(True, False)

    def test_it_prints_unallocated_people_to_text(self):
        self.assertEqual(True, False)

    def test_print_existing_room(self):
        self.assertEqual(True, False)

    def test_print_room_occupants(self):
        self.assertEqual(True, False)

    def test_commit_rooms(self):
        self.assertEqual(True, False)

    def test_commit_people(self):
        self.assertEqual(True, False)

    def test_load_from_file(self):
        self.amity.create_room("lspace", "Shell", "wing")
        self.amity.create_room("office", "Valhalla", "Oculus")
        path = os.path.realpath("data.txt")
        self.amity.load_people(path)
        self.assertEqual(len(self.amity.fellows_list), 4)
        self.assertEqual(len(self.amity.staff_list), 3)

    def test_load_rooms(self):
        self.assertEqual(True, False)
















if __name__ == '__main__':
    unittest.main()
