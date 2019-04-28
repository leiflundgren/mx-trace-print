import os
import unittest
import sys
from contextlib import contextmanager

from io import StringIO

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import trace_mockup 

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestMockup(unittest.TestCase):

    def find_keyword(self, output:str, key:str) -> str:
        idx = output.find(key)
        if idx < 0:
            self.fail("Looked for key '" + key + "' in output. But not found!\n" + output)
        idx = idx + len(key)
        while str(output[idx]).isspace():
            idx = idx + 1
        end = idx
        while not str(output[end]).isspace() and not output[end] == ',':
            end = end + 1
        return output[idx:end]

    def test_display(self):
        with captured_output() as (out, err):
            trace_mockup.TraceMockup(['fake_progname', '-display', '-mxver', '7'])
        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print(errout, file=sys.stderr)

        output = out.getvalue().strip()
        print(output)
        self.assertTrue(self.find_keyword(output, "\n Version:"))
    
    def test_print_id(self):
        with captured_output() as (out, err):
            trace_mockup.TraceMockup(['fake_progname', '-print', '3', '-mxver', '7'])
        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print(errout, file=sys.stderr)

        output = out.getvalue().strip()
        print(output)
        self.assertTrue(self.find_keyword(output, "\n Version:"))
        self.assertEqual("3", self.find_keyword(output, "\n Trace ind:"))
        self.assertEqual("CMP", self.find_keyword(output, " Unit name:"))

        end_of_header = output.find("\n\n") or output.find("\r\n\r\n")
        pos_siplp = output.find("SIPLP")
        if pos_siplp > 0:
            self.assertLess(end_of_header, pos_siplp, "Should not be any SIPLP keyword in output")

    def test_print_indv_SIPLP(self):
        with captured_output() as (out, err):
            trace_mockup.TraceMockup(['fake_progname', '-print', '1', '-mxver', '7'])
        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print(errout, file=sys.stderr)
            self.fail("Something on stderr")

        output = out.getvalue().strip()
        print(output)
        self.assertTrue(self.find_keyword(output, "\n Version:"))
        self.assertEqual("1", self.find_keyword(output, "\n Trace ind:"))
        self.assertEqual("SIPLP", self.find_keyword(output, " Unit name:"))


if __name__ == '__main__':
    unittest.main()

    