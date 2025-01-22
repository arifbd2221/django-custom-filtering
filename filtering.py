import re

def parse_search_phrase(allowed_fields, phrase):
    """
    This function Parses a search phrase and converts it into a Django Q object.

    :param allowed_fields: List of allowed fields for filtering. eg: date, distance
    :param phrase: The search phrase string.
    :return: A Q object representing the filters.
    """

    # tokenizing search phrases
    token_pattern = re.compile(r'(\(|\)|\band\b|\bor\b|\w+\s(eq|ne|gt|lt)\s[^\s\)]+)', re.IGNORECASE)

    # Mapping of operators
    operator_mapping = {
        'eq': '',       # Equals
        'ne': '__ne',   # Not equals
        'gt': '__gt',   # Greater than
        'lt': '__lt'    # Less than
    }

    tokens = token_pattern.findall(phrase)
    print(f"{tokens=}") # tokens=[('(', ''), ('date eq 2016-05-01', 'eq'), (')', ''), ('AND', ''), ('(', ''), ('(', ''), ('distance gt 20', 'gt'), (')', ''), ('OR', ''), ('(', ''), ('distance lt 10', 'lt'), (')', ''), (')', '')]




if __name__ == '__main__':
    allowed_fields = ['date', 'distance']
    search_phrase = "(date eq 2016-05-01) AND ((distance gt 20) OR (distance lt 10))"

    parse_search_phrase(allowed_fields, search_phrase)