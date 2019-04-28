import os
import sys
import unittest
import platform

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from executor import Executor
from settings import Settings
from trace_mockup import TraceMockup
import tools 

class TestExecutor(unittest.TestCase):

    def trace(self, lvl, *argv):
        argv = ("TestExecutor: ", ) + argv
        return tools.trace(lvl, argv)

    def setUp(self):
        self.trace(4, 'setup done')

    def test_hello_world(self) -> None:

        if platform.system() == "Windows":
            executor = Executor("cmd", ["/C", "echo", "hello", "world"])
        else:
            executor = Executor("echo", ["hello", "world"])
        res = executor.str_result
        self.assertEqual("hello world", res.strip())

    #def run_test_mockup(self, mxver:int, prog:str, args:[str]) -> str:
    #    executor = Executor(True, True, True, "trace-mockup")

if __name__ == '__main__':
    unittest.main()