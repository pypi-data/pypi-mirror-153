import sys


def reload_class(instance):
    cls = instance.__class__
    modname = cls.__module__
    del sys.modules[modname]

    module = __import__(modname)
    submodules = modname.split(".")[1:]

    for submodule in submodules:
        module = getattr(module, submodule)

    instance.__class__ = getattr(module, cls.__name__)
