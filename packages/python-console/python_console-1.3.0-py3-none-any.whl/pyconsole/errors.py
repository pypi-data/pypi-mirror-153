class KeyboardWarning(Warning):
    '''
    Base class for keyboard auto-corrected warnings.
    '''
    pass


class TracebackWarning(Warning):
    '''
    Base class for traceback related warnings.
    '''
    pass


class KeyNotFoundError(Exception):
    '''
    The key is not on the keyboard register.
    '''
    pass
