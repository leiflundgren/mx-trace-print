from __future__ import absolute_import
from tools import trace
from tools import tracelevel
from parse_display import ParseDisplayOutput
from command_generator import CommandGenerator

import subprocess 
import sys 

class Executor(object):
    def __init__(self, program, args, trace_cmd_level = 7, trace_result_level = 8):
        self.program = program
        self.args = args
        prog_args = [self.program]
        if not args is None: prog_args += args
        
        trace(trace_cmd_level, u'Executor ' + program + u' ', args)
        try:
            self.result = subprocess.check_output(prog_args)
            if tracelevel >= trace_result_level:
                trace(trace_result_level, self.str_result)
        except subprocess.CalledProcessError, e:
            trace(1, e.cmd, u'failed with ', e.returncode)
            trace(1, e.output)
            sys.exit(e.returncode)

    @property
    def str_result(self):
        return unicode(self.result.decode() if isinstance(self.result, str) else self.result)

