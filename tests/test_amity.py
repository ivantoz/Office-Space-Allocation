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



if __name__ == '__main__':
    unittest.main()
