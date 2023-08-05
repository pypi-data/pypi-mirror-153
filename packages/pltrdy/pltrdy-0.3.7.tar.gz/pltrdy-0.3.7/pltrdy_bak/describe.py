import sys


def binsize(o):
    import dill
    return len(dill.dumps(o))


def has_module(module_name):
    return module_name in sys.modules


def is_torch_tensor(o):
    if has_module("torch"):
        import torch

        if isinstance(o, torch.Tensor):
            return True
    return False


def tab_print(*args, sep="        ", lvl=0, **kwargs):
    args = list(args)
    if lvl > 0:
        tabs = sep * lvl
        args[0] = tabs + args[0]
    print(*args, **kwargs)


def describe(o, max_elements=20, max_depth=100, depth=1, file=sys.stdout,
             report_size=False):
    def _print(*args, **kwargs):
        print(*args, **kwargs, file=file)

    next_kwargs = {
        "max_elements": max_elements,
        "max_depth": (max_depth - 1),
        "depth": (depth + 1),
        "file": file,
        "report_size": report_size,
    }

    lines = []

    if report_size:
        size = binsize(o)
        size_str = ", binsize: %d o" % size
    else:
        size_str = ""

    if max_depth == 0:
        _print("(max depth reached)")
        return

    if isinstance(o, dict):
        keys = o.keys()
        n = len(o)
        _print("Dict (len: %d%s)" % (n, size_str))
        if n <= max_elements:
            try:
                keys = sorted(o.keys())
            except TypeError:
                keys = sorted(o.keys(), key=lambda e: str(e))

            for k in keys:
                v = o[k]
                tab_print("%s:" % k, lvl=depth, end=" ", file=file)
                describe(v, **next_kwargs)
        else:
            tab_print("(too many elements to show, %d > %d)"
                      % (n, max_elements), lvl=depth, file=file)
    elif isinstance(o, list) or isinstance(o, tuple):

        n = len(o)
        _print("%s (len: %d%s)" % (type(o), n, size_str))
        if n <= max_elements:
            for i, v in enumerate(o):
                tab_print("#%d:" % i, lvl=depth, end=" ", file=file)
                describe(v, **next_kwargs)
        else:
            tab_print("(too many elements to show, %d > %d)"
                      % (n, max_elements), lvl=depth, file=file)
    elif is_torch_tensor(o):
        tensor_shape = str(list(o.size()))
        tensor_type = str(o.type())

        _print("%s: %s%s" % (tensor_type, tensor_shape, size_str))
    else:
        _print("%s%s" % (repr(o), size_str))


def describe_str(*args, **kwargs):
    from io import StringIO
    s = StringIO()
    describe(*args, file=s, **kwargs)

    return s.getvalue()


def describe_lines(*args, **kwargs):
    return describe_str(*args, **kwargs).split("\n")
