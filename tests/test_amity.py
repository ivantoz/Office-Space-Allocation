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



if __name__ == '__main__':
    unittest.main()
