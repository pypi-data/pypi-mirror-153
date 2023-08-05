#!/usr/bin/env python
import json


def test():
    from gen_script import gen_script

    data = {
        "name": "the_test",
        "args": ["param1", "p2", ],
        "kwargs": {"opt_param1": "value1", "opt_param2": "value2"}
    }

    data_json = json.dumps(data)
    gen_script(data_json)


if __name__ == "__main__":
    test()
