import os
import sys
import unittest

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from parse_display import ParseDisplayOutput

class TestStringMethods(unittest.TestCase):

    def open_output1(self):
        f = open("trace-display.output", "r", encoding='iso-8859-1')
        return f

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_parse_display(self):
        with self.open_output1() as f:
            parser = ParseDisplayOutput(f)
            
        self.assertEqual('6.3.3.0.33, 16.3.3.0.33', parser.version)
        self.assertEqual("(1) standard", parser.market)
        self.assertEqual('2019-01-08 12:17:46 (CET)', parser.first_trace)
        self.assertEqual('2019-01-25 20:13:05 (CET)', parser.last_trace)
        individuals = parser.individuals

        id1= individuals[1]
        self.assertEqual('1', id1.lim)
        self.assertEqual('all', id1.textlevel)
        self.assertEqual('SIPLP', id1.unit_name)
        
        id8 = individuals[8]
        self.assertEqual('idle/free', id8.state)

if __name__ == '__main__':
    unittest.main()