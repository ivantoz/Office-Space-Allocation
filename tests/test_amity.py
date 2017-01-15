import unittest

from app.model import *


class AmityTestCase(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.person = Person()
        self.fellow = Fellow()
        self.staff = Staff()



    def test_adds_person(self):
        pass

    def test_add_person_to_fully_occupied_room(self):
        pass

    def test_add_person_missing_person_name(self):
        pass

    def test_add_person_missing_job_type(self):
        pass

    def test_add_person_no_room(self):
        pass

    def test_add_person_not_allow_more_than_capacity(self):
        pass

    def test_add_person_allocates_room(self):
        pass

    def test_add_person_allocates_fellow_livingspace_with_want_accomadation_option(self):
        pass


    def test_add_person_does_not_allocate_staff_living_space(self):
        pass

    def test_create_multiple_rooms(self):
        self.assertEqual(self.amity.create_room("OFFICE", "Hogwarts", "Valhalla", "Oculus"),
                         "Hogwarts Office successfully created")

    def test_create_room_duplicate_names(self):
        name = "Hogwarts"
        self.amity.create_room("office", name)
        r_names = [r.room_name for r in self.amity.all_rooms]
        self.assertIn(name, r_names)
        msg = self.amity.create_room("office", name)
        expected_msg = "sorry, {} room already exists!please choose another name".format(name)
        self.assertEqual(msg, expected_msg)

    def test_create_room_input_string_type(self):
        pass

    def test_create_room_no_input(self):
        pass

    def test_reallocate_person_wihtout_person_identifier(self):
        pass

    def test_reallocate_person_without_room_name_input(self):
        pass

    def test_reallocate_person_does_not_want_accomadation(self):
        pass

    def test_reallocate_staff_to_living_space(self):
        pass

    def test_reallocate_to_unregistered_room(self):
        pass

    def  test_reallocation_of_unregistered_person(self):
        pass

    def test_print_registered_allocation_to_text(self):
        pass

    def test_it_prints_allocations(self):
        pass

    def test_it_prints_unaloccated_people(self):
        pass

    def test_it_prints_unallocated_people_to_text(self):
        pass

    def test_print_existing_room(self):
        pass

    def test_print_room_occupants(self):
        pass

    def test_commit_rooms(self):
        pass

    def test_commit_people(self):
        pass

    def test_load_people(self):
        pass

    def test_load_rooms(self):
        pass
















if __name__ == '__main__':
    unittest.main()
