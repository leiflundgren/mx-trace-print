import os
import unittest
import sys
import re

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from settings import Settings
from parse_display import ParseDisplayOutput
from main import Main
from tools_for_test import captured_output
from tools_for_test import TestSettings

class TestPrint(unittest.TestCase):
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
        
    # issues print command, checks 
    def run_print(self, print_arg:str, print_output:bool = True, check_siplp_in_output:bool = True ) -> str:
        printout = ''
        try:
            with captured_output() as (out, err):
               printout = Main('fake_progname', ['-print', print_arg, '-mxver', '7'], settings=self.settings).main()
        except:
            print(out.getvalue(), file=sys.stderr)
            print(err.getvalue(), file=sys.stderr)
            raise

        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print(errout, file=sys.stderr)

        output = out.getvalue().strip()
        if print_output:
            print(printout)
            print(output)
        if check_siplp_in_output:
            self.assertTrue(output.find(" Version") >= 0)            
            self.assertTrue(re.search(" Trace ind: *1", output))
            self.assertTrue(re.search(" Unit name: *SIPLP", output))

        return output

    def test_print_a_id(self):
        print('==================================')
        print('== test_print_a_id')
        print('==================================')
        self.run_print('1')

    def test_print_b_indv(self):
        print('==================================')
        print('== test_print_b_indv')
        print('==================================')
        self.run_print('SIPLP')

    def test_print_c_gang(self):
        print('==================================')
        print('== test_print_c_gang')
        print('==================================')
        result = self.run_print('usual')

        #check RMP
        self.assertTrue(re.search(" Trace ind: *3", result))
        self.assertTrue(re.search(" Unit name: *RMP", result))

        #check CMP
        self.assertTrue(re.search(" Trace ind: *4", result))
        self.assertTrue(re.search(" Unit name: *CMP", result))
    # pass

if __name__ == '__main__':
    unittest.main()

    