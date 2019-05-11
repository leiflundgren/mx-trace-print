from __future__ import absolute_import
import unittest
import os
import sys

PACKAGE_PARENT = u'..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwdu(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from parse_display import ParseDisplayOutput
from command_generator import CommandGenerator
from settings import Settings
import tools 

class TestCommendGenerator(unittest.TestCase):

    def trace(self, lvl, *argv):
        argv = (u"TestCommendGenerator: ", ) + argv
        return tools.trace(lvl, argv)

    def setUp(self):
        self.settings = Settings(u'settings.json')
        self.display = ParseDisplayOutput(u"trace-display.output")
        self.cmdgen = CommandGenerator(self.display, self.settings)
        self.trace(4, u'setup done')


        print self.cmdgen.add_indv(u'csta')

    def test_expand(self):
        self.assertListEqual([u'1',u'2',u'3'], self.cmdgen.expand_names(u'1,2,3'))
        self.assertListEqual([u'1',u'2',u'3',u'5'], self.cmdgen.expand_names(u'1-3,5'))
        self.assertListEqual([u'SIPLP', u'RMP', u'CMP'], self.cmdgen.expand_names(u'usual'))
        self.assertListEqual([u'SIPLP', u'RMP', u'CMP', u'extra'], self.cmdgen.expand_names(u'usual,extra'))
        self.assertListEqual([u'SIPLP', u'RMP', u'CMP', u'extra'], self.cmdgen.expand_names([u'usual,extra']))
        self.assertListEqual([u'SIPLP', u'RMP', u'CMP', u'extra'], self.cmdgen.expand_names([u'usual',u'extra']))

    def test_add_ISUS(self):
        isus =  self.display.get_individual(u'ISUS')
        self.assertIsNone(isus)

        isus_cmd = self.cmdgen.add_indv(u'ISUS', u'4')
        self.trace(u"add(ISUS) cmd ", isus_cmd)
        self.assertTrue(isinstance(isus_cmd, list))
        self.assertEqual(1, len(isus_cmd))
        self.assertEqual(u' '.join(isus_cmd[0]), u'-lim 4 -unit ISUS')

    def test_add_csta_gang(self):
        gang_cmd = self.cmdgen.add_indv(u'csta')
        self.assertIn(u'-lim 1 -unit ISUS'.split(u' '), gang_cmd)
        # self.assertIn('trace -lim 1 -unit CSTServer', gang_cmd)
        self.assertNotIn([u'-lim', u'1', u'-unit', u'SIPLP'], gang_cmd)

    def test_set_textlevel(self):
        set_cmd = self.cmdgen.set_textlevel(u'SIPLP', u'full')
        self.trace(3, set_cmd)

    def test_print_usual(self):
        self.trace(3, u'Printing buffers for usual gang: SIPLP, RMP, CMP')
        cmd = self.cmdgen.save_cmd(self.settings.expand_to_ids([u'usual']), u'sample_')
        for args, fname in cmd:
            self.trace(3, u"    " + u", ".join(args) + u"  filename:" + fname)
        self.assertEqual(3, len(cmd))
        self.assertEqual(u'sample_SIPLP.log', cmd[0][1])





if __name__ == u'__main__':
    unittest.main()