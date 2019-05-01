import sys
import io
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from tools import trace
from command_line_parser import CommandLineParser

class TraceMockup:
    def __init__(self, argv:[str]):
        print(" ".join(argv))
        self.args = CommandLineParser(argv)
        self.mxver = int(self.args.get_arg('mxver', '0'))
        if self.mxver == 6:
            self.help_file = 'trace-help.output'
            self.display_file = 'trace-display.output'
            self.print_file = 'trace-print-6x.output'
        elif self.mxver == 7:
            self.help_file = 'trace-help-7.x.output'
            self.display_file = 'trace-display-7.x.output'
            self.print_file = 'trace-print-6x.output' # TODO, change to 7 
        else:
            raise ValueError("Unknown MX-One version " + str(self.mxver))

        display_args = self.args.display
        print_args = self.args.print_args

        if self.args.help:
            self.print_help()
        elif not display_args is None:
            self.print_display()
        elif not print_args is None:
            self.print_print(print_args)
        else:
            print("args: " + " ".join(sys.argv[1:]))
            pass

    def print_help(self):
        print(self.readfile(self.help_file))

    def print_display(self):
        disp_str = self.readfile(self.display_file)
        cc = self.args.get_arg('call-count', 0)
        if int(cc) < 3:
            print(disp_str)
            return

        # add MADEUP as extra module

        key = 'State: idle/free'
        has_found = False
        for line in disp_str.splitlines():
            if not has_found and line.endswith(key):
                print(line[:len(line)-len(key)] + 'State: stopped     , Stored:     75, Size per lim: 5000')
                print(' First: 2019-01-22 16:16:01 (CET) Last: 2019-01-22 16:16:19 (CET)')
                print(' Type     : unit-trace      , Rotating: on , Textlevel: normal')
                print(' Lim no   :   1, Unit no: 4711, Unit name: MADEUP')
                print(' Time mark: 2019-01-22 16:16:32 (CET), by user: mxone_admin')
                print(' Trace stopped by : command (manually stopped)')
                has_found = True
            else:        
                print(line)

    def readfile(self, file:str) -> str:
        with open(file, 'r', encoding='iso-8859-1') as f:
            return str(f.read())

    def print_print(self, arg:str) -> str:
        n = -1
        try:
            n = int(arg)
        except:
            raise ValueError("Should print individ-id: '" + arg + "'")
        disp_str = self.readfile(self.print_file)
        unit_name = ''
        if n == 1:
            unit_name = 'SIPLP' # don't change
        elif n == 3: # CMP
            unit_name = 'CMP'
        elif n == 4: # RMP
            unit_name = 'RMP'
        else:
            raise ValueError("trace-mockup can only print 1-SIPLP/3:CMP/4:RMP")

        ouput = disp_str.replace(' Trace ind:  1', ' Trace ind:  ' + str(n))
        ouput = ouput.replace(' Unit name: SIPLP', ' Unit name: ' + unit_name)
        print(ouput)
        return ouput

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


if __name__ == '__main__':
    TraceMockup(['trace_mockup_7x.py', '-call-count', '3', '-display', '-mxver', '7'])