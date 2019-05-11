from __future__ import with_statement
from __future__ import absolute_import
import sys
import io
import os
from io import open

PACKAGE_PARENT = u'..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwdu(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from tools import trace
from command_line_parser import CommandLineParser

class TraceMockup(object):
    def __init__(self, argv):
        print u" ".join(argv)
        self.args = CommandLineParser(argv)
        self.mxver = int(self.args.get_arg(u'mxver', u'0'))
        if self.mxver == 6:
            self.help_file = u'trace-help.output'
            self.display_file = u'trace-display.output'
            self.print_file = u'trace-print-6x.output'
        elif self.mxver == 7:
            self.help_file = u'trace-help-7.x.output'
            self.display_file = u'trace-display-7.x.output'
            self.print_file = u'trace-print-6x.output' # TODO, change to 7 
        else:
            raise ValueError(u"Unknown MX-One version " + unicode(self.mxver))

        display_args = self.args.display
        print_args = self.args.print_args

        if self.args.help:
            self.print_help()
        elif not display_args is None:
            self.print_display()
        elif not print_args is None:
            self.print_print(print_args)
        else:
            print u"args: " + u" ".join(sys.argv[1:])
            pass

    def print_help(self):
        print self.readfile(self.help_file)

    def print_display(self):
        disp_str = self.readfile(self.display_file)
        cc = self.args.get_arg(u'call-count', 0)
        if int(cc) < 3:
            print disp_str
            return

        # add MADEUP as extra module

        key = u'State: idle/free'
        has_found = False
        for line in disp_str.splitlines():
            if not has_found and line.endswith(key):
                print line[:len(line)-len(key)] + u'State: stopped     , Stored:     75, Size per lim: 5000'
                print u' First: 2019-01-22 16:16:01 (CET) Last: 2019-01-22 16:16:19 (CET)'
                print u' Type     : unit-trace      , Rotating: on , Textlevel: normal'
                print u' Lim no   :   1, Unit no: 4711, Unit name: MADEUP'
                print u' Time mark: 2019-01-22 16:16:32 (CET), by user: mxone_admin'
                print u' Trace stopped by : command (manually stopped)'
                has_found = True
            else:        
                print line

    def readfile(self, file):
        with open(file, u'r', encoding=u'iso-8859-1') as f:
            return unicode(f.read())

    def print_print(self, arg):
        n = -1
        try:
            n = int(arg)
        except:
            raise ValueError(u"Should print individ-id: '" + arg + u"'")
        disp_str = self.readfile(self.print_file)
        unit_name = u''
        if n == 1:
            unit_name = u'SIPLP' # don't change
        elif n == 3: # CMP
            unit_name = u'CMP'
        elif n == 4: # RMP
            unit_name = u'RMP'
        else:
            raise ValueError(u"trace-mockup can only print 1-SIPLP/3:CMP/4:RMP")

        ouput = disp_str.replace(u' Trace ind:  1', u' Trace ind:  ' + unicode(n))
        ouput = ouput.replace(u' Unit name: SIPLP', u' Unit name: ' + unit_name)
        print ouput
        return ouput

    def parse_command_line(self, argv):
        self.args = {}
        i=1
        while i < len(argv):
            if argv[i][0] == u"-":
                arg = argv[i].lstrip(u"-").rstrip().lower()
                val = None
                i=i+1
                if i < len(argv) and argv[i][0] != u"-":
                    val = argv[i]
                    i = i + 1
                self.args[arg] = val
            
            
    #print(self.readfile(self.help_file))


if __name__ == u'__main__':
    TraceMockup([u'trace_mockup_7x.py', u'-call-count', u'3', u'-display', u'-mxver', u'7'])