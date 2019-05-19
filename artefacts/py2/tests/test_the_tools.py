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

class Test_Tools(unittest.TestCase):

    def trace(self, lvl, *argv):
        argv = (u"Test_Tools: ", ) + argv
        return tools.trace(lvl, argv)

    def setUp(self):
        if  not u'USERNAME' in os.environ :
            os.environ[u'USERNAME'] = u'N/A'
        if  not u'NON_EXISTING_ENV' in os.environ :
            os.environ[u'NON_EXISTING_ENV'] = u'yes'
        


    def test_expand_string(self):
        def assertExpandedSomething(s):
            expanded = tools.expand_string(s)
            self.assertNotEqual(s, expanded)
        self.assertEqual(u'', tools.expand_string(u''))
        self.assertEqual(u'hej', tools.expand_string(u'hej'))
        self.assertTrue(u"USERNAME" in os.environ)
        self.assertTrue(u"NON_EXISTING_ENV" in os.environ)

        assertExpandedSomething(u'prefix_${USERNAME}_end')
        #assertExpandedSomething('prefix_$USERNAME_end')
        assertExpandedSomething(u'prefix_${DATETIME}_end')
        assertExpandedSomething(u'prefix_${DATE}')
        assertExpandedSomething(u'prefix_${TIME}_end')
        #assertExpandedSomething('$DATETIME')



if __name__ == u'__main__':
    unittest.main()