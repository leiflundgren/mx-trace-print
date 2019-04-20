import unittest
from parse_display import ParseDisplayOutput

from settings import Settings
from main import Main

class TestMain(unittest.TestCase):
    class TestSettings(Settings):

        def __init__(self, settings_json:str):
            Settings.__init__(self, settings_json)
            self.call_count = 0


        @property
        def trace_args(self) -> [str]:
            args = super(TestMain.TestSettings, self).trace_args
            self.call_count = 1+self.call_count
            return args + ['-call-count', str(self.call_count) ]


    def test_main_start(self):
        settings_json = """
{
    "trace_cmd": "python",
    "trace_args": ["trace_mockup_7x.py"],
    "default_textlevel": "full",
    "gangs": [
        {
            "name": "usual",
            "members": ["SIPLP", "RMP", "CMP"]
        },
        {
            "name": "csta",
            "members": ["CSTServer", "ISUS", "CMP", "RMP", "SIPLP"]
        },
        {
            "name": "unusual",
            "members": ["SIPLP", "MADEUP", "CMP"]
        }
    ],
    "debug_trace_level": 7,
    "debug_trace_commands": 6
}"""        
        settings = self.TestSettings(settings_json)

        # test display
        # main = Main('test_main', [ "-display"], settings)
        # main.main()

        main = Main('test_main', [ "-start", "unusual"], settings)
        main.main()


    pass

if __name__ == '__main__':
    unittest.main()

    