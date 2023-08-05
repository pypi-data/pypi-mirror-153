from .console import Console


__console = None


def get_console(**kwargs) -> Console:
    '''
    Gets the current global console instance. If there is none, then it creates it with the given
    arguments.

    ## Params

    kwargs = keyword arguments for initializing the global console in case there is none. (refer to
    `Console` for more information on valid keyword arguments).

    ## Returns

    returns the global console instance
    '''
    global __console

    if __console is None:
        __console = Console(**kwargs)

    return __console


def set_console(**kwargs):
    '''
    Sets the global console instance with the given attributes.

    ## Params

    kwargs = keyword arguments for initializing the global console. (refer to `Console` for more
    information on valid keyword arguments).
    '''
    global __console

    new_console = Console(**kwargs)

    if __console is None:
        __console = new_console
    else:
        __console.__dict__ = new_console.__dict__
