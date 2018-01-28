import datetime

from functools import wraps
from luno.exceptions import UnauthorisedResourceException


def requires_authentication(func):
    """Helper function to protect unauthenticated use of private resources"""
    @wraps(func)
    def inner(self, *args, **kwargs):
        if not self._has_auth_details:
            raise UnauthorisedResourceException(f'authentication is required for private resources')
        
        return func(self, *args, **kwargs)
    return inner