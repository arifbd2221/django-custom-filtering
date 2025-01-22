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


def combine_q_objects(sub_q):
    """
    Combines a list of Q objects and operators (sub_q) into a single Q object.
    """
    combined_q = sub_q.pop(0)
    while sub_q:
        operator = sub_q.pop(0)
        next_q = sub_q.pop(0)
        if operator == 'or':
            combined_q |= next_q
        elif operator == 'and':
            combined_q &= next_q
        else:
            raise ValueError(f"Invalid logical operator: {operator}")
    return combined_q


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

    stack = []
    for token in tokens:
        token = token.strip().lower()

        if token == '(':
            stack.append(token)
        elif token == ')':
            sub_q = []
            while stack and stack[-1] != '(':
                sub_q.insert(0, stack.pop())
            stack.pop()  # Remove the '('
            combined_q = combine_q_objects(sub_q)
            stack.append(combined_q)

        elif token in ('and', 'or'):
            stack.append(token)
        else:
            stack.append(evaluate_expression(token))
    
    # Combine remaining tokens in the stack
    return combine_q_objects(stack)
    


if __name__ == '__main__':
    allowed_fields = ['date', 'distance']
    search_phrase = "(date eq 2016-05-01) AND ((distance gt 20) OR (distance lt 10))"

    print(parse_search_phrase(allowed_fields, search_phrase))