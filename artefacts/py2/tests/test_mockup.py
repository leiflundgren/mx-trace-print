from __future__ import with_statement
from __future__ import absolute_import
import os
import unittest
import sys
from contextlib import contextmanager

from io import StringIO

PACKAGE_PARENT = u'..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwdu(), os.path.expanduser(__file__))))
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

    def find_keyword(self, output, key):
        idx = output.find(key)
        if idx < 0:
            self.fail(u"Looked for key '" + key + u"' in output. But not found!\n" + output)
        idx = idx + len(key)
        while unicode(output[idx]).isspace():
            idx = idx + 1
        end = idx
        while not unicode(output[end]).isspace() and not output[end] == u',':
            end = end + 1
        return output[idx:end]

    def test_display(self):
        with captured_output() as (out, err):
            trace_mockup.TraceMockup([u'fake_progname', u'-display', u'-mxver', u'7'])
        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print >>sys.stderr, errout

        output = out.getvalue().strip()
        print output
        self.assertTrue(self.find_keyword(output, u"\n Version:"))
    
    def test_print_id(self):
        with captured_output() as (out, err):
            trace_mockup.TraceMockup([u'fake_progname', u'-print', u'3', u'-mxver', u'7'])
        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print >>sys.stderr, errout

        output = out.getvalue().strip()
        print output
        self.assertTrue(self.find_keyword(output, u"\n Version:"))
        self.assertEqual(u"3", self.find_keyword(output, u"\n Trace ind:"))
        self.assertEqual(u"CMP", self.find_keyword(output, u" Unit name:"))

        end_of_header = output.find(u"\n\n") or output.find(u"\r\n\r\n")
        pos_siplp = output.find(u"SIPLP")
        if pos_siplp > 0:
            self.assertLess(end_of_header, pos_siplp, u"Should not be any SIPLP keyword in output")

    def test_print_indv_SIPLP(self):
        with captured_output() as (out, err):
            trace_mockup.TraceMockup([u'fake_progname', u'-print', u'1', u'-mxver', u'7'])
        errout = err.getvalue()
        if not errout is None and len(errout) > 0:
            print >>sys.stderr, errout
            self.fail(u"Something on stderr")

        output = out.getvalue().strip()
        print output
        self.assertTrue(self.find_keyword(output, u"\n Version:"))
        self.assertEqual(u"1", self.find_keyword(output, u"\n Trace ind:"))
        self.assertEqual(u"SIPLP", self.find_keyword(output, u" Unit name:"))


if __name__ == u'__main__':
    unittest.main()

    