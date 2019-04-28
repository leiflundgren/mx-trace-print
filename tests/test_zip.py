import unittest
import sys
import re
import io
import os

import tempfile

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from settings import Settings
from parse_display import ParseDisplayOutput
from main import Main
from tools_for_test import captured_output
from tools_for_test import TestSettings
from tools import trace
from tools import tracelevel

class TestZip(unittest.TestCase):
    def setUp(self):
        settings_json = """
{
    "trace_cmd": "python",
    "trace_args": ["tests/trace_mockup_7x.py"],
    "default_textlevel": "full",
    "gangs": [
        {
            "name": "usual",
            "members": ["SIPLP", "RMP", "CMP"]
        },
        {
            "name": "csta",
            "members": ["CSTServer", "ISUS", "CMP", "RMP", "SIPLP"]
        },
        {
            "name": "unusual",
            "members": ["SIPLP", "MADEUP", "CMP"]
        }
    ],
    "debug_trace_level": 7,
    "debug_trace_commands": 6
}"""        
        self.settings = TestSettings(settings_json)
        self.tempfolder = tempfile.TemporaryDirectory('__test-mxtrace')
        
    # issues save command, checks 
    def run_zip(self, save_arg:str, expected_file_count:int) -> str:
        folder = os.path.join(self.tempfolder.name, self._testMethodName)
        trace(5, 'Creating ', folder)
        os.mkdir(folder)

        m = Main('fake_progname', ['-zip', os.path.join(folder, "zipped"), save_arg, '-mxver', '7', '-prefix', 'trace_prefix'], settings=self.settings)
        m.main()
        
        files = os.listdir(folder)
        trace(3, 'Test ' + self._testMethodName + " yielded " + str(len(files)), " files:", files)
        
        return folder
    

    def assertFileInOutput(self, folder:str, required:str):
        files = os.listdir(folder)
        self.assertTrue(filter(lambda f: f.find(required), files), msg='Expected ' + str(required) +' to be in output')

    def test_save_a_id(self):
        try:
            print('==================================')
            print('== test_save_a_id')
            print(' temp folder: ' + self.tempfolder.name)
            print('==================================')
            folder = self.run_zip('1', 1)
            self.assertFileInOutput(folder, 'SIPLP')
        except Exception as e: 
                trace(1, 'Test ', self._testMethodName, ' failed: ', str(e))
                raise
    def test_save_b_indv(self):
        try:
            print('==================================')
            print('== test_print_b_indv')
            print(' temp folder: ' + self.tempfolder.name)
            print('==================================')
            folder = self.run_zip('SIPLP', 1)
            self.assertFileInOutput(folder, 'SIPLP')
        except Exception as e: 
                trace(1, 'Test ', self._testMethodName, ' failed: ', str(e))
                raise
    def test_save_c_gang(self):
        try:
            print('==================================')
            print('== test_print_c_gang')
            print(' temp folder: ' + self.tempfolder.name)
            print('==================================')
            folder = self.run_zip('usual', 3)
            self.assertFileInOutput(folder, 'SIPLP')
            self.assertFileInOutput(folder, 'RMP')
            self.assertFileInOutput(folder, 'CMP')
        except Exception as e: 
                trace(1, 'Test ', self._testMethodName, ' failed: ', str(e))
                raise
        # #check RMP
        # self.assertTrue(re.search(" Trace ind: *3", result))
        # self.assertTrue(re.search(" Unit name: *RMP", result))

        # #check CMP
        # self.assertTrue(re.search(" Trace ind: *4", result))
        # self.assertTrue(re.search(" Unit name: *CMP", result))
    # pass

if __name__ == '__main__':
    unittest.main()

    