# Django Custom Filtering

A Python utility for parsing complex search phrases and converting them into Django ORM `Q` objects. This utility is designed to handle dynamic filtering in Django-based projects by supporting complex query operations, including logical operators (`AND`, `OR`) and comparison operators (`eq`, `ne`, `gt`, `lt`).

## Features

- **Logical Operators**: Supports `AND` and `OR`.
- **Comparison Operators**:
  - `eq`: Equals
  - `ne`: Not equals
  - `gt`: Greater than
  - `lt`: Less than
- **Nested Conditions**: Handles parentheses for precedence.
- **Validation**: Ensures fields used in queries are part of the allowed fields.

## Prerequisites

- Python 3.8 or higher.
- Django installed in your environment.

## File Structure

```How to use
from filtering import SearchParser
allowed_fields = ['date', 'distance']
search_phrase = "(date eq 2023-01-01) AND ((distance gt 20) OR (distance lt 10))"

parser = SearchParser(allowed_fields)
search_filter = parser.parse(search_phrase)

