#!/usr/bin/python3
###
### Mockup that simulates trace on MX-One 7.x

import trace_mockup 
import sys

def main_mx7x():
    return trace_mockup.TraceMockup(sys.argv + ['-mxver', '7'])

if __name__ == "__main__":
    main_mx7x()