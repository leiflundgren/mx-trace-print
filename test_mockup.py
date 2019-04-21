import unittest
import sys
from contextlib import contextmanager

from io import StringIO

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

    def test_display(self):
        with captured_output() as (out, err):
            trace_mockup.TraceMockup(['fake_progname', '-display', '-mxver', '7'])
        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print(errout, file=sys.stderr)

        output = out.getvalue().strip()
        print(output)
        self.assertTrue(output.find("\n Version") >= 0)
    
    def test_print_id(self):
        with captured_output() as (out, err):
            trace_mockup.TraceMockup(['fake_progname', '-print', '3', '-mxver', '7'])
        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print(errout, file=sys.stderr)

        output = out.getvalue().strip()
        print(output)
        self.assertTrue(output.find("\n Version") >= 0)            
        self.assertTrue(output.find("\n Trace ind: 3") >= 0)
        self.assertTrue(output.find(" Unit name: CMP") >= 0)

    def test_print_indv_SIPLP(self):
        with captured_output() as (out, err):
            trace_mockup.TraceMockup(['fake_progname', '-print', 'SIPLP', '-mxver', '7'])
        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print(errout, file=sys.stderr)
            self.fail("Something on stderr")

        output = out.getvalue().strip()
        print(output)
        self.assertTrue(output.find("\n Version") >= 0)            
        self.assertTrue(output.find("\n Trace ind: 1") >= 0)
        self.assertTrue(output.find(" Unit name: SIPLP") >= 0)

if __name__ == '__main__':
    unittest.main()

    