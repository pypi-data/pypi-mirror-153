#!/usr/bin/env python
import sys
import json


def gen_script(data):
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except BaseException:
            print("data: '%s'" % str(data))
            raise
    tab = "    "
    python_bin = "/usr/bin/env python"
    fct_name = data["name"]
    imports = data.get("import", [])
    args = data.get("args", [])
    kwargs = data.get("kwargs", {})
    all_args = args + ['%s="%s"' % (k, v) for k, v in kwargs.items()]
    all_args_str = ", ".join(all_args)

    def tprint(tlvl, *args, **kwargs):
        args = list(args)
        args[0] = "%s%s" % (tlvl * tab, args[0])
        print(*args, **kwargs)

    print("#!%s" % python_bin)
    for module in imports:
        print("import %s" % module)
    print("\n")
    print("def %s(%s):" % (fct_name, all_args_str))
    tprint(1, "pass\n\n")
    print('if __name__ == "__main__":')
    tprint(1, "import argparse\n")
    tprint(1, "parser = argparse.ArgumentParser()")

    main_args = []
    main_kwargs = []
    for arg in args:
        tprint(1, 'parser.add_argument("%s",' % arg)
        tprint(1, '                    help="")')
        main_args.append("args.%s" % arg)
    for k, v in kwargs.items():
        tprint(
            1, 'parser.add_argument("-%s", "--%s", default="%s",' %
            (k, k, v))
        tprint(1, '                    help="")')
        main_kwargs.append("%s=args.%s" % (k, k))

    main_args_str = ", ".join(main_args + main_kwargs)
    tprint(1, "args = parser.parse_args()\n")
    tprint(1, "%s(%s)" % (fct_name, main_args_str))


def main():
    data = None
    if len(sys.argv) >= 1:
        data = sys.argv[1]

    gen_script(data)


if __name__ == "__main__":
    main()
