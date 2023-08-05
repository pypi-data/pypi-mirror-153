

def checktype(o, *types):
    for i, t in enumerate(types):
        if isinstance(t, type):
            if isinstance(o, t):
                break

        elif t is None:
            if o is None:
                break

        else:
            raise TypeError(
                f"Invalid type of type {i} during check: {type(t)} instead of "
                f"type, None")
    else:
        raise TypeError(
            f"Invalid type {type(o)}, must be {', '.join(map(str, types))}")
