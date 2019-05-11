#!/usr/bin/python3
###
### Mockup that simulates trace on MX-One 7.x

from __future__ import absolute_import
import trace_mockup 
import sys

def main_mx7x():
    return trace_mockup.TraceMockup(sys.argv + [u'-mxver', u'7'])

if __name__ == u"__main__":
    main_mx7x()