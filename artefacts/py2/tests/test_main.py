from __future__ import with_statement
from __future__ import absolute_import
import os
import unittest
import sys
import re

PACKAGE_PARENT = u'..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwdu(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from parse_display import ParseDisplayOutput

from settings import Settings
from main import Main
from tools_for_test import captured_output
from tools_for_test import TestSettings

class TestMain(unittest.TestCase):
   

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

    def test_print_SIPLP(self):
        with captured_output() as (out, err):
            Main([u'fake_progname', u'-print', u'SIPLP', u'-mxver', u'7', u'-hello', u'world'], self.settings).main()

        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print >>sys.stderr, errout
            self.fail(u"Something on stderr")

        output = out.getvalue().strip()
        print output
        self.assertTrue(output.find(u"-hello world") >= 0)
        self.assertTrue(output.find(u" Version") >= 0)
        self.assertTrue(output.find(u" Trace ind:  1") >= 0)
        self.assertTrue(output.find(u" Unit name: SIPLP") >= 0)

    # def test_main_start(self):
       
    #     # test display
    #     # main = Main('test_main', [ "-display"], settings)
    #     # main.main()

    #     main = Main('test_main', [ "-display", "unusual", '-hello', 'world'], self.settings)
    #     main.main()


    pass

if __name__ == u'__main__':
    unittest.main()

    