import unittest
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
        f = self.open_output1()
        parser = ParseDisplayOutput(f)

        self.assertEqual('6.3.3.0.33, 16.3.3.0.33', parser.version)
        self.assertEqual("1", parser.market)

        traces = parser.traces()

        self.assertIsNone(traces[8])
        self.assertEqual('1', traces[1].lim)
        self.assertEqual('all', traces[1].textlevel)
        self.assertEqual('SIPLP', traces[1].unitName)

if __name__ == '__main__':
    unittest.main()