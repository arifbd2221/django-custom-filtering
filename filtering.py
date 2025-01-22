import re
from django.db.models import Q



class SearchParser:
    """
    A class to parse a search phrase into a Django Q object.
    """

    def __init__(self, allowed_fields):
        """
        Initialize the parser with allowed fields.
        """
        self.allowed_fields = allowed_fields
        self.operator_mapping = {
            'eq': '',       # Equals
            'ne': '__ne',   # Not equals
            'gt': '__gt',   # Greater than
            'lt': '__lt'    # Less than
        }
        self.token_pattern = re.compile(r'(\(|\)|\band\b|\bor\b|\w+\s(eq|ne|gt|lt)\s[^\s\)]+)', re.IGNORECASE)
    
    def evaluate_expression(self, expression):
        """
        Evaluates a single comparison expression into a Q object.
        """
        # Ensure the expression has exactly three parts: field, operator, value
        parts = re.split(r'\s+', expression)
        if len(parts) != 3:
            raise ValueError(f"Invalid expression: '{expression}'. Expected format: 'field operator value'.")
        
        field, operator, value = re.split(r'\s+', expression, 2)

        # Validate the field
        if field not in self.allowed_fields:
            raise ValueError(f"Field '{field}' is not allowed.")

        # Map the operator to its Django ORM equivalent
        if operator.lower() not in self.operator_mapping:
            raise ValueError(f"Operator '{operator}' is not supported.")
        
        # Convert the value to an appropriate type
        try:
            if value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Keep it as a string if it's not a number
        except Exception as e:
            raise ValueError(f"Invalid value '{value}': {str(e)}")

        lookup = self.operator_mapping[operator.lower()]
        return Q(**{f"{field}{lookup}": value})

    def combine_q_objects(self, sub_q):
        """
        Combines a list of Q objects and operators into a single Q object.
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

    def parse(self, phrase):
        # Tokenize the phrase
        tokens = self.token_pattern.findall(phrase)
        tokens = [t[0] if isinstance(t, tuple) else t for t in tokens]

        if not tokens:
            raise ValueError("Empty or invalid search phrase.")

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
                combined_q = self.combine_q_objects(sub_q)
                stack.append(combined_q)

            elif token in ('and', 'or'):
                stack.append(token)
            else:
                stack.append(self.evaluate_expression(token))
        
        if not stack:
            raise ValueError("Empty or invalid search phrase.")
        
        return self.combine_q_objects(stack)



if __name__ == '__main__':
    allowed_fields = ['date', 'distance']
    search_phrase = "(date eq 2016-05-01) AND ((distance gt 20) OR (distance lt 10))"

    parser = SearchParser(allowed_fields)
    search_filter = parser.parse(search_phrase)

    print(search_filter)