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

    