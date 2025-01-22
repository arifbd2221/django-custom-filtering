import re
from django.db.models import Q



def evaluate_expression(expression):
        # Mapping of operators
        operator_mapping = {
            'eq': '',       # Equals
            'ne': '__ne',   # Not equals
            'gt': '__gt',   # Greater than
            'lt': '__lt'    # Less than
        }
        field, operator, value = re.split(r'\s+', expression, 2)

        # Mapping the operator to its Django ORM equivalent
        lookup = operator_mapping[operator.lower()]
        return Q(**{f"{field}{lookup}": value})


def parse_search_phrase(allowed_fields, phrase):
    """
    This function Parses a search phrase and converts it into a Django Q object.

    :param allowed_fields: List of allowed fields for filtering. eg: date, distance
    :param phrase: The search phrase string.
    :return: A Q object representing the filters.
    """

    # tokenizing search phrases
    token_pattern = re.compile(r'(\(|\)|\band\b|\bor\b|\w+\s(eq|ne|gt|lt)\s[^\s\)]+)', re.IGNORECASE)

    tokens = token_pattern.findall(phrase)
    # tokens=[('(', ''), ('date eq 2016-05-01', 'eq'), (')', ''), ('AND', ''), ('(', ''), ('(', ''), ('distance gt 20', 'gt'), (')', ''), ('OR', ''), ('(', ''), ('distance lt 10', 'lt'), (')', ''), (')', '')]

    # formatting tokens to string
    tokens = [t[0] if isinstance(t, tuple) else t for t in tokens]




if __name__ == '__main__':
    allowed_fields = ['date', 'distance']
    search_phrase = "(date eq 2016-05-01) AND ((distance gt 20) OR (distance lt 10))"

    parse_search_phrase(allowed_fields, search_phrase)