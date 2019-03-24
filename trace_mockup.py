import sys
import io

from tools import trace
from command_line_parser import CommandLineParser

class TraceMockup:
    def __init__(self, mxver: int):
        self.mxver = mxver
        if mxver == 6:
            self.help_file = 'trace-help.output'
            self.display_file = 'trace-display.output'
        elif mxver == 7:
            self.help_file = 'trace-help-7.x.output'
            self.display_file = 'trace-display-7.x.output'
        else:
            raise ValueError("Unknown MX-One version " + str(mxver))

        self.args = CommandLineParser(sys.argv[0], sys.argv[1:])
        if  self.args.help:
            print(self.readfile(self.help_file))
        elif  not self.args.display is None:
            print(self.readfile(self.display_file))
            pass # exit
        else:
            print("args: " + " ".join(sys.argv[1:]))
            pass


    def readfile(self, file:str) -> str:
        with open(file, 'r', encoding='iso-8859-1') as f:
            return str(f.read())


    def parse_command_line(self, argv:[str]) -> None:
        self.args = {}
        i=1
        while i < len(argv):
            if argv[i][0] == "-":
                arg = argv[i].lstrip("-").rstrip().lower()
                val = None
                i=i+1
                if i < len(argv) and argv[i][0] != "-":
                    val = argv[i]
                    i = i + 1
                self.args[arg] = val
            
            
    #print(self.readfile(self.help_file))


