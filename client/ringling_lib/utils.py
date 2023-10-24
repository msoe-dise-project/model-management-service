"""
Copyright 2023 MSOE DISE Project
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
    """
    Validate if a string is valid iso format
    """
    try:
        datetime.fromisoformat(test_string)
    except ValueError:
        return False
    return True
