from __future__ import absolute_import
import os
import sys
import unittest

PACKAGE_PARENT = u'..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwdu(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from command_line_parser import CommandLineParser
from settings import Settings
import tools 

class TestCommendLineParser(unittest.TestCase):

    def trace(self, lvl, *argv):
        argv = (u"TestCommendLineParser: ", ) + argv
        return tools.trace(lvl, argv)
  
    def test_find_arg(self):
        argv = [u'progname', u'-hej', u'hopp', u'-alone', u'--bara', u'bra', u'-flera', u'arg', u'till', u'denna']
        
        r = CommandLineParser.find_arg_index(u'finns_Ej', argv)
        self.assertEqual((-1,-1, None), r)

        r = CommandLineParser.find_arg_index(u'HEJ', argv)
        self.assertEqual((1,2, [u'hopp']), r)

        r = CommandLineParser.find_arg_index(u'flera', argv)
        self.assertEqual((6, 9, [u'arg', u'till', u'denna']), r)

        cmd = CommandLineParser(argv)
        self.assertEqual(u'hopp', cmd.get_arg(u'hej'))
        self.assertEqual([u'arg', u'till', u'denna'], cmd.get_args(u'flera'))
        self.assertEqual(u'arg', cmd.get_arg(u'flera'))

    def test_remove_arg(self):
        argv = [u'progname', u'-hej', u'hopp', u'-alone', u'--bara', u'bra', u'-flera', u'arg', u'till', u'denna']

        r = CommandLineParser(argv)
        self.assertIn(u'-hej', r.argv)
        self.assertIn(u'hopp', r.argv)

        r_no_hej = r.remove_arg(u'hej')
        self.assertNotIn(u'-hej', r_no_hej.argv)
        self.assertNotIn(u'hopp', r_no_hej.argv)

if __name__ == u'__main__':
    unittest.main()