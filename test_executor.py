import unittest
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
        executor = Executor(True, True, False, "echo", ["hello world"], None)
        res = executor.result
        self.assertEqual("hello world", str(res).strip())

    #def run_test_mockup(self, mxver:int, prog:str, args:[str]) -> str:
    #    executor = Executor(True, True, True, "trace-mockup")

if __name__ == '__main__':
    unittest.main()