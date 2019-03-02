import unittest
from parse_display import ParseDisplayOutput
from command_generator import CommandGenerator
from settings import Settings

class TestCommendGenerator(unittest.TestCase):

    def setUp(self):
        self.settings = Settings('settings.json')
        self.display = ParseDisplayOutput("trace-display.output")
        self.cmdgen = CommandGenerator(self.display, self.settings)
        print('setup done')

    def test_add_ISUS(self):
        isus =  self.display.get_individual('ISUS')
        self.assertIsNone(isus)

        isus_cmd = self.cmdgen.add_individual('ISUS')
        self.assertEqual(isus_cmd, 'trace -lim 1 -unit ISUS')

    def test_add_csta_gang(self):
        gang_cmd = self.cmdgen.add_gang('csta')
        self.assertIn('trace -lim 1 -unit ISUS', gang_cmd)
        # self.assertIn('trace -lim 1 -unit CSTServer', gang_cmd)
        self.assertNotIn('trace -lim 1 -unit SIPLP', gang_cmd)

if __name__ == '__main__':
    unittest.main()