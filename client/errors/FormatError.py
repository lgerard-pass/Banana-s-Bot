class FormatError(RuntimeError):
    """Exception raised when a command is attempted to be invoked
    from a channel it's not supposed to
    """
    pass