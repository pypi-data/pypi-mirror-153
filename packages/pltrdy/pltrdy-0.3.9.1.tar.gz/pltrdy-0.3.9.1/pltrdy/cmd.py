#!/usr/bin/env python
"""
    Python wrapper around `wc` command
"""
import subprocess


def run(args):
    if isinstance(args, str):
        args = args.split()

    o = subprocess.run(args, stdout=subprocess.PIPE)
    output = o.stdout.decode("utf-8")
    return output
