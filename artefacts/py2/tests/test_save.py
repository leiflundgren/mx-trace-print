from __future__ import absolute_import
import unittest
import sys
import re
import io
import os

import tempfile
from itertools import ifilter

PACKAGE_PARENT = u'..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwdu(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from settings import Settings
from parse_display import ParseDisplayOutput
from main import Main
from tools_for_test import captured_output
from tools_for_test import TestSettings
from tools import trace
from tools import tracelevel

class TestSave(unittest.TestCase):
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
        self.tempfolder = tempfile.mkdtemp(prefix=u'test-mxtrace')
        
    # issues save command, checks 
    def run_save(self, save_arg, expected_file_count):
        folder = os.path.join(self.tempfolder, self._testMethodName)
        trace(5, u'Creating ', folder)
        os.mkdir(folder)

        prefix = os.path.join(folder, u'test_trace')

        Main([u'fake_progname', u'-save', save_arg, u'-mxver', u'7', u'-prefix', prefix], settings=self.settings).main()
        
        files = os.listdir(folder)
        trace(3, u'Test ' + self._testMethodName + u" yielded " + unicode(len(files)), u" files:", files)

        if expected_file_count >= 0:
            self.assertEqual(expected_file_count, len(files), msg=u'Expected there to be ' + unicode(expected_file_count) + u" files after test. Got: " + u" ".join(files))
        
        return folder
    

    def assertFileInOutput(self, folder, required):
        files = os.listdir(folder)
        self.assertTrue(ifilter(lambda f: f.find(required), files), msg=u'Expected ' + unicode(required) +u' to be in output')

    def test_save_a_id(self):
        try:
            print u'=================================='
            print u'== test_save_a_id'
            print u' temp folder: ' + self.tempfolder
            print u'=================================='
            folder = self.run_save(u'1', 1)
            self.assertFileInOutput(folder, u'SIPLP')
        except Exception, e: 
                trace(1, u'Test ', self._testMethodName, u' failed: ', unicode(e))
                raise
    def test_save_b_indv(self):
        try:
            print u'=================================='
            print u'== test_print_b_indv'
            print u' temp folder: ' + self.tempfolder
            print u'=================================='
            folder = self.run_save(u'SIPLP', 1)
            self.assertFileInOutput(folder, u'SIPLP')
        except Exception, e: 
                trace(1, u'Test ', self._testMethodName, u' failed: ', unicode(e))
                raise
    def test_save_c_gang(self):
        try:
            print u'=================================='
            print u'== test_print_c_gang'
            print u' temp folder: ' + self.tempfolder
            print u'=================================='
            folder = self.run_save(u'usual', 3)
            self.assertFileInOutput(folder, u'SIPLP')
            self.assertFileInOutput(folder, u'RMP')
            self.assertFileInOutput(folder, u'CMP')
        except Exception, e: 
                trace(1, u'Test ', self._testMethodName, u' failed: ', unicode(e))
                raise
        # #check RMP
        # self.assertTrue(re.search(" Trace ind: *3", result))
        # self.assertTrue(re.search(" Unit name: *RMP", result))

        # #check CMP
        # self.assertTrue(re.search(" Trace ind: *4", result))
        # self.assertTrue(re.search(" Unit name: *CMP", result))
    # pass

if __name__ == u'__main__':
    unittest.main()

    