class InvalidDateError(Exception):
    """ Raised when a cell_type has been identified as DateType but contains an invalid value
    """
    def __init__(self, message):
        self.message = message