"""
Additional helper utils
"""

from datetime import datetime

def validate_types(params):
    """
    Validate types as a list of tuples
    """
    for param, _type in params:
        if not isinstance(param, _type):
            raise TypeError(f'{param} should be of type {_type.__name__} '
                            f'but is instead {type(param)}')


def validate_iso(test_string):
    try:
        datetime.fromisoformat(test_string)
    except ValueError:
        return False
    return True
