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



if __name__ == '__main__':
    unittest.main()
