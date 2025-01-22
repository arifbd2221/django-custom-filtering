import sys
from pathlib import Path
# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import unittest
from django.db.models import Q
from filtering import SearchParser


class TestSearchParser(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with allowed fields and a SearchParser instance.
        """
        self.allowed_fields = ['date', 'distance']
        self.parser = SearchParser(self.allowed_fields)

    def test_simple_equality(self):
        """
        Test parsing a simple equality condition.
        """
        phrase = "date eq 2023-01-01"
        expected = Q(date="2023-01-01")
        self.assertEqual(self.parser.parse(phrase), expected)

    def test_and_condition(self):
        """
        Test parsing an AND condition.
        """
        phrase = "date eq 2023-01-01 AND distance gt 20"
        expected = Q(date="2023-01-01") & Q(distance__gt=20)
        self.assertEqual(self.parser.parse(phrase), expected)

    def test_or_condition(self):
        """
        Test parsing an OR condition.
        """
        phrase = "distance gt 20 OR distance lt 10"
        expected = Q(distance__gt=20) | Q(distance__lt=10)
        self.assertEqual(self.parser.parse(phrase), expected)

    def test_nested_conditions(self):
        """
        Test parsing nested conditions with parentheses.
        """
        phrase = "(date eq 2023-01-01) AND ((distance gt 20) OR (distance lt 10))"
        expected = Q(date="2023-01-01") & (Q(distance__gt=20) | Q(distance__lt=10))
        self.assertEqual(self.parser.parse(phrase), expected)

    def test_invalid_field(self):
        """
        Test parsing with an invalid field.
        """
        phrase = "invalid_field eq 10"
        with self.assertRaises(ValueError) as context:
            self.parser.parse(phrase)
        self.assertEqual(str(context.exception), "Field 'invalid_field' is not allowed.")


if __name__ == "__main__":
    unittest.main()