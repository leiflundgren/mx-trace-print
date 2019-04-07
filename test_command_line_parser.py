import unittest
from command_line_parser import CommandLineParser
from settings import Settings
import tools 

class TestCommendLineParser(unittest.TestCase):

    def trace(self, lvl, *argv):
        argv = ("TestCommendLineParser: ", ) + argv
        return tools.trace(lvl, argv)
  
    def test_find_arg(self):
        argv = ['progname', '-hej', 'hopp', '-alone', '--bara', 'bra', '-flera', 'arg', 'till', 'denna']
        
        r = CommandLineParser.find_arg_index('finns_Ej', argv)
        self.assertEqual((-1,-1, None), r)

        r = CommandLineParser.find_arg_index('HEJ', argv)
        self.assertEqual((1,2, ['hopp']), r)

        r = CommandLineParser.find_arg_index('flera', argv)
        self.assertEqual((6, 9, ['arg', 'till', 'denna']), r)




if __name__ == '__main__':
    unittest.main()