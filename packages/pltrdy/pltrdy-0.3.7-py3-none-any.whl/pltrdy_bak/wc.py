#!/usr/bin/env python
"""
    Python wrapper around `wc` command
"""
import subprocess


def linecount(path):
    return wordcount(path, args="-l")


def wordcount(path, args=["-w"]):
    o = subprocess.run(["wc"] + args + [path], stdout=subprocess.PIPE)
    wc = int(o.stdout.decode('utf-8').split()[0])
    return wc
