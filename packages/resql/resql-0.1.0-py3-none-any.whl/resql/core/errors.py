class PydbError(Exception):
    """
    Base class for all exceptions in pydb.
    """
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return "pydb error: " + self.message
    
class PydbInvalidTableName(PydbError):
    """
    Raised when the table name is invalid.
    """
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message
    