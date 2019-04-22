import unittest
import sys
import re
import io
import os

import tempfile

from settings import Settings
from parse_display import ParseDisplayOutput
from main import Main
from tools_for_test import captured_output
from tools_for_test import TestSettings
from tools import trace
from tools import tracelevel

class TestSave(unittest.TestCase):
    def setUp(self):
        settings_json = """
{
    "trace_cmd": "python",
    "trace_args": ["trace_mockup_7x.py"],
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
        self.tempfolder = tempfile.TemporaryDirectory('test-mxtrace')
        
    # issues save command, checks 
    def run_save(self, save_arg:str, expected_file_count:int) -> str:
        folder = os.path.join(self.tempfolder, self._testMethodName)
        trace(5, 'Creating ', folder)
        os.mkdir(folder)

        prefix = os.path.join(folder, 'test_trace')

        Main('fake_progname', ['-save', save_arg, '-mxver', '7', '-prefix', prefix], settings=self.settings).main()
        
        if expected_file_count >= 0:
            self.assertEqual(expected_file_count, len(os.listdir(folder)), msg='Expected there to be ' + str(expected_file_count) + " files after test. Got: " + " ".join(os.listdir(folder)))
        
        return folder

    def test_save_a_id(self):
        print('==================================')
        print('== test_save_a_id')
        print('==================================')
        folder = self.run_save('1', 1)

    def test_print_b_indv(self):
        print('==================================')
        print('== test_print_b_indv')
        print('==================================')
        folder = self.run_save('SIPLP', 1)

    def test_print_c_gang(self):
        print('==================================')
        print('== test_print_c_gang')
        print('==================================')
        folder = self.run_save('usual', 3)

        # #check RMP
        # self.assertTrue(re.search(" Trace ind: *3", result))
        # self.assertTrue(re.search(" Unit name: *RMP", result))

        # #check CMP
        # self.assertTrue(re.search(" Trace ind: *4", result))
        # self.assertTrue(re.search(" Unit name: *CMP", result))
    # pass

if __name__ == '__main__':
    unittest.main()

    