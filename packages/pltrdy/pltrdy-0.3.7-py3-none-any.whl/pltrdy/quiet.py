import sys
import os

class Quiet:
    def __init__(self, out=None, err=None):
        if out is None:
            out = open(os.devnull, 'w')

        if err is None:
            err = open(os.devnull, 'w')

        self.stdout = None
        self.replace_out = out
        self.stderr = None
        self.replace_err = err

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self.replace_out
        self.stderr = sys.stderr
        sys.stderr = self.replace_err
    
    def __exit__(self, type, value, traceback):
        sys.stdout = self.stdout
        sys.stderr = self.stderr


