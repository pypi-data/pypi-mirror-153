import numpy as np


def equal(x, y, almost=False, epsilon=1e-7):
    if not almost:
        return x == y
    else:
        try:
            return (y - epsilon) <= x <= (y + epsilon)
        except TypeError:
            raise ValueError(
                "Invalid types (%s, %s) for almost comparison"
                % (type(x), type(y)))


def aeq(*args, almost=False, epsilon=1e-7, msg=None, ignore_single=False):
    if ignore_single and len(args) == 1:
        return args[0]

    assert len(args) > 1, (
        "aeq a single element is meaningless (ignore with `ignore_single`")

    if msg is not None:
        msg = "[%s] " % msg
    else:
        msg = ""
    assert all([
        equal(_,
              args[0],
              almost=almost,
              epsilon=epsilon)
        for _ in args[1:]
    ]), (
        "%sArguments are not all equal %s" % (msg, str(args))
    )
    return args[0]

def aaeq(*args, almost=False, epsilon=1e-7, msg=None, ignore_single=False):
    if ignore_single and len(args) == 1:
        return args[0]

    assert len(args) > 1, "aaeq a single element is meaningless, use aeq"
    if msg is not None:
        msg = "[%s] " % msg
    else:
        msg = ""

    aeq(*[len(_) for _ in args], msg="Size mismatch")
    for i, args_i in enumerate(zip(*args)):
        assert all([
            equal(_,
                  args_i[0],
                  almost=almost,
                  epsilon=epsilon)
            for _ in args_i[1:]]
        ), (
            "%sArguments are not all equal at position %d, %s."
            % (msg, i, str(args_i))
        )
    return args[0]


def assert_shapes(*shapes):
    """shapes are iterable of same length
       we assert that for all shape i and dimension j
       shapes[0][j] == shapes[i][j]
    """
    def fix_shape(shape):
        if isinstance(shape, np.ndarray):
            shape = shape.shape
        return shape
    shapes = [fix_shape(s) for s in shapes]

    for i, sizes in enumerate(zip(*shapes)):
        try:
            aeq(*sizes)
        except AssertionError as e:
            shapes_str = ", ".join([
                "[%s]" % (", ".join([
                    str(d) if j != i else "*%d*" % d
                    for j, d in enumerate(s)
                ])) for s in shapes
            ])
            raise AssertionError("Size mismatch on dimension %d: %s"
                                 % (i, shapes_str)) from e


def assert_in(args, args_in):
    for i, arg in enumerate(args):
        for j, arg_in in enumerate(args_in):
            assert arg in arg_in, \
                f"Argument#{i}:{type(arg).__name__}={str(arg)} not in " \
                f"arg_in#{j}:{type(arg_in).__name__}={str(arg_in)}"
