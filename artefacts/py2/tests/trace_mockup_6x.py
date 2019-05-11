#!/usr/bin/python3
###
### Mockup that simulates trace on MX-One 6.x

from __future__ import absolute_import
import trace_mockup 

def main_mx6x():
    return trace_mockup.TraceMockup(6)

if __name__ == u"__main__":
    main_mx6x()