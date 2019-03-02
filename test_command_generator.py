import unittest
from parse_display import ParseDisplayOutput
from command_generator import CommandGenerator

class TestCommendGenerator(unittest.TestCase):

    def setup(self):
        self.display = ParseDisplayOutput("trace-display.output")
        self.cmdgen = CommandGenerator(self.display.version)

    def test_add_ISUS(self):
        isus =  self.display.get_individual('ISUS')
        self.assertIsNone(isus)

        isus_cmd = self.cmdgen.add_individual('ISUS')
        self.assertEqual(isus_cmd, 'trace -lim 1 -unit ISUS')


if __name__ == '__main__':
    unittest.main()