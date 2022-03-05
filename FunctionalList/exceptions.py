class NoParametersException(Exception):
    """Exception raised when the function passed to a map/filter/find method takes no parameters"""
    pass

class TooManyParametersException(Exception):
    """Exception raised when the function passed to a map/filter/find/reduce method takes too many parameters"""
    pass

class TooFewParametersReduceException(Exception):
    """Exception raised when the function passed to a reduce method takes too few parameters"""
    pass

class NonCallableException(Exception):
    """Exception raised when a non-callable object is passed to a map/filter/reduce/find methode"""
    pass
