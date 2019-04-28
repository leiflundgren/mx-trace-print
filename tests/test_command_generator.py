import unittest
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from parse_display import ParseDisplayOutput
from command_generator import CommandGenerator
from settings import Settings
import tools 

class TestCommendGenerator(unittest.TestCase):

    def trace(self, lvl, *argv):
        argv = ("TestCommendGenerator: ", ) + argv
        return tools.trace(lvl, argv)

    def setUp(self):
        self.settings = Settings('settings.json')
        self.display = ParseDisplayOutput("trace-display.output")
        self.cmdgen = CommandGenerator(self.display, self.settings)
        self.trace(4, 'setup done')


        print(self.cmdgen.add('csta'))

    def test_expand(self):
        self.assertListEqual(['1','2','3'], self.cmdgen.expand_names('1,2,3'))
        self.assertListEqual(['1','2','3','5'], self.cmdgen.expand_names('1-3,5'))
        self.assertListEqual(['SIPLP', 'RMP', 'CMP'], self.cmdgen.expand_names('usual'))
        self.assertListEqual(['SIPLP', 'RMP', 'CMP', 'extra'], self.cmdgen.expand_names('usual,extra'))
        self.assertListEqual(['SIPLP', 'RMP', 'CMP', 'extra'], self.cmdgen.expand_names(['usual,extra']))
        self.assertListEqual(['SIPLP', 'RMP', 'CMP', 'extra'], self.cmdgen.expand_names(['usual','extra']))

    def test_add_ISUS(self):
        isus =  self.display.get_individual('ISUS')
        self.assertIsNone(isus)

        isus_cmd = self.cmdgen.add('ISUS', '4')
        self.trace("add(ISUS) cmd ", isus_cmd)
        self.assertTrue(isinstance(isus_cmd, list))
        self.assertEqual(1, len(isus_cmd))
        self.assertEqual(' '.join(isus_cmd[0]), '-lim 4 -unit ISUS')

    def test_add_csta_gang(self):
        gang_cmd = self.cmdgen.add('csta')
        self.assertIn('-lim 1 -unit ISUS'.split(' '), gang_cmd)
        # self.assertIn('trace -lim 1 -unit CSTServer', gang_cmd)
        self.assertNotIn(['-lim', '1', '-unit', 'SIPLP'], gang_cmd)

    def test_set_textlevel(self):
        set_cmd = self.cmdgen.set_textlevel('SIPLP', 'full')
        self.trace(3, set_cmd)

    def test_print_usual(self):
        self.trace(3, 'Printing buffers for usual gang: SIPLP, RMP, CMP')
        cmd = self.cmdgen.save_cmd(self.settings.expand_to_individuals(['usual']), 'sample_')
        for args, fname in cmd:
            self.trace(3, "    " + ", ".join(args) + "  filename:" + fname)
        self.assertEqual(3, len(cmd))
        self.assertEqual('sample_SIPLP.log', cmd[0][1])





if __name__ == '__main__':
    unittest.main()