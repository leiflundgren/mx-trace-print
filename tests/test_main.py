import os
import unittest
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from parse_display import ParseDisplayOutput

from settings import Settings
from main import Main
from tools_for_test import captured_output
from tools_for_test import TestSettings

class TestMain(unittest.TestCase):
   

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

    def run_print(self, print_arg:str):
        with captured_output() as (out, err):
            Main('fake_progname', ['-print', print_arg, '-mxver', '7']).main()

        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print(errout, file=sys.stderr)
            self.fail("Something on stderr")

        output = out.getvalue().strip()
        print(output)
        self.assertTrue(output.find("\n Version") >= 0)            
        self.assertTrue(output.find("\n Trace ind: 1") >= 0)
        self.assertTrue(output.find(" Unit name: SIPLP") >= 0)

    def test_main_start(self):
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
        settings = TestSettings(settings_json)

        # test display
        # main = Main('test_main', [ "-display"], settings)
        # main.main()

        main = Main('test_main', [ "-start", "unusual"], settings)
        main.main()


    pass

if __name__ == '__main__':
    unittest.main()

    