class UserAlreadyExists(Exception):
    """Raise when try create new user already created"""

class ApiUnavailable(Exception):
    """Raise when consume external API fail"""