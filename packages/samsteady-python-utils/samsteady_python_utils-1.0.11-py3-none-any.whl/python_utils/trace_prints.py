import traceback
import sys

class TracePrints(object):
    def __init__(self):
        self.stdout = sys.stdout
        self.ignore_print = False
    def write(self, s):
        if self.ignore_print:
            self.ignore_print = False
            return
        # self.stdout.write("Writing %r\n" % s)
        stack = traceback.format_stack()
        last_line = ""
        for line in stack:
            if "traceback.format_stack" in line:
                break
            last_line = line
        self.stdout.write(last_line)
        self.stdout.write(s + "\n---------\n")
        self.ignore_print = True