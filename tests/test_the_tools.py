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

class Test_Tools(unittest.TestCase):

    def trace(self, lvl, *argv):
        argv = ("Test_Tools: ", ) + argv
        return tools.trace(lvl, argv)

    def setUp(self):
        pass


    def test_expand_string(self):
        def assertExpandedSomething(s:str):
            expanded = tools.expand_string(s)
            self.assertNotEqual(s, expanded)
        self.assertEqual('', tools.expand_string(''))
        self.assertEqual('hej', tools.expand_string('hej'))
        
        assertExpandedSomething('prefix_${USERNAME}_end')
        #assertExpandedSomething('prefix_$USERNAME_end')
        assertExpandedSomething('prefix_${DATETIME}_end')
        assertExpandedSomething('prefix_${DATE}')
        assertExpandedSomething('prefix_${TIME}_end')
        #assertExpandedSomething('$DATETIME')



if __name__ == '__main__':
    unittest.main()