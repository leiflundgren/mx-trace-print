from __future__ import with_statement
from __future__ import absolute_import
import os
import unittest
import sys
import re

PACKAGE_PARENT = u'..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwdu(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from settings import Settings
from parse_display import ParseDisplayOutput
from main import Main
from tools_for_test import captured_output
from tools_for_test import TestSettings

class TestPrint(unittest.TestCase):
    def setUp(self):
        settings_json = u"""
{
    "trace_cmd": "python",
    "trace_args": ["tests/trace_mockup_7x.py"],
    "default_textlevel": "full",
    "gangs": {
        "usual": ["SIPLP", "RMP", "CMP"],
        "csta": ["CSTServer", "ISUS", "CMP", "RMP", "SIPLP"],
        "unusual": ["SIPLP", "MADEUP", "CMP"]        
    },
    "debug_trace_level": 7,
    "debug_trace_commands": 6
}"""        
        self.settings = TestSettings(settings_json)
        
    # issues print command, checks 
    def run_print(self, print_arg, print_output = True, check_siplp_in_output = True ):
        printout = u''
        try:
            with captured_output() as (out, err):
               printout = Main([u'fake_progname', u'-print', print_arg, u'-mxver', u'7'], settings=self.settings).main()
        except:
            print >>sys.stderr, out.getvalue()
            print >>sys.stderr, err.getvalue()
            raise

        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print >>sys.stderr, errout

        output = out.getvalue().strip()
        if print_output:
            print printout
            print output
        if check_siplp_in_output:
            self.assertTrue(output.find(u" Version") >= 0)            
            self.assertTrue(re.search(u" Trace ind: *1", output))
            self.assertTrue(re.search(u" Unit name: *SIPLP", output))

        return output

    def test_print_a_id(self):
        print u'=================================='
        print u'== test_print_a_id'
        print u'=================================='
        self.run_print(u'1')

    def test_print_b_indv(self):
        print u'=================================='
        print u'== test_print_b_indv'
        print u'=================================='
        self.run_print(u'SIPLP')

    def test_print_c_gang(self):
        print u'=================================='
        print u'== test_print_c_gang'
        print u'=================================='
        result = self.run_print(u'usual')

        #check RMP
        self.assertTrue(re.search(u" Trace ind: *3", result))
        self.assertTrue(re.search(u" Unit name: *RMP", result))

        #check CMP
        self.assertTrue(re.search(u" Trace ind: *4", result))
        self.assertTrue(re.search(u" Unit name: *CMP", result))
    # pass

if __name__ == u'__main__':
    unittest.main()

    