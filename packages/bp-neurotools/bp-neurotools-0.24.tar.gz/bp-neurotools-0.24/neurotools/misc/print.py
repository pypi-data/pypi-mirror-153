import warnings

def _get_print(verbose, _print=None):

    # Top behavior should be, if already print
    # init'ed keep that
    if not _print is None:
        return _print

    # Helper for muted print
    if verbose is None:
        return _get_print(verbose=-10)

    def _print(*args, **kwargs):

        if 'level' in kwargs:
            level = kwargs.pop('level')
        else:
            level = 1

        # Skip any print if the verbose is under 0
        if verbose < 0:
            return

        # Use warnings for level = 0
        # If warn, don't also print
        if level == 0:

            # Conv print to str - then warn
            sep = ' '
            if 'sep' in kwargs:
                sep = kwargs.pop('sep')
            as_str = sep.join(str(arg) for arg in args)
            warnings.warn(as_str)

        elif verbose >= level:
            print(*args, **kwargs, flush=True)

    return _print