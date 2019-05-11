from __future__ import absolute_import
import os
import sys
import unittest
import platform

PACKAGE_PARENT = u'..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwdu(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from executor import Executor
from settings import Settings
from trace_mockup import TraceMockup
import tools 

class TestExecutor(unittest.TestCase):

    def trace(self, lvl, *argv):
        argv = (u"TestExecutor: ", ) + argv
        return tools.trace(lvl, argv)

    def setUp(self):
        self.trace(4, u'setup done')

    def test_hello_world(self):

        if platform.system() == u"Windows":
            executor = Executor(u"cmd", [u"/C", u"echo", u"hello", u"world"])
        else:
            executor = Executor(u"echo", [u"hello", u"world"])
        res = executor.str_result
        self.assertEqual(u"hello world", res.strip())

    #def run_test_mockup(self, mxver:int, prog:str, args:[str]) -> str:
    #    executor = Executor(True, True, True, "trace-mockup")

if __name__ == u'__main__':
    unittest.main()