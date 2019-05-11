from __future__ import with_statement
from __future__ import absolute_import
import os
import sys
import unittest
from io import open

PACKAGE_PARENT = u'..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwdu(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from parse_display import ParseDisplayOutput

class TestStringMethods(unittest.TestCase):

    def open_output1(self):
        f = open(u"trace-display.output", u"r", encoding=u'iso-8859-1')
        return f

    def test_upper(self):
        self.assertEqual(u'foo'.upper(), u'FOO')

    def test_isupper(self):
        self.assertTrue(u'FOO'.isupper())
        self.assertFalse(u'Foo'.isupper())

    def test_split(self):
        s = u'hello world'
        self.assertEqual(s.split(), [u'hello', u'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_parse_display(self):
        with self.open_output1() as f:
            parser = ParseDisplayOutput(f)
            
        self.assertEqual(u'6.3.3.0.33, 16.3.3.0.33', parser.version)
        self.assertEqual(u"(1) standard", parser.market)
        self.assertEqual(u'2019-01-08 12:17:46 (CET)', parser.first_trace)
        self.assertEqual(u'2019-01-25 20:13:05 (CET)', parser.last_trace)
        individuals = parser.individuals

        id1= individuals[1]
        self.assertEqual(u'1', id1.lim)
        self.assertEqual(u'all', id1.textlevel)
        self.assertEqual(u'SIPLP', id1.unit_name)
        
        id8 = individuals[8]
        self.assertEqual(u'idle/free', id8.state)

if __name__ == u'__main__':
    unittest.main()