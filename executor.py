from tools import trace
from tools import tracelevel
from parse_display import ParseDisplayOutput
from command_generator import CommandGenerator

import subprocess 
import sys 

class Executor:
    def __init__(self, program:str, args:[str], trace_cmd_level:int = 7, trace_result_level:int = 8):
        self.program = program
        self.args = args
        prog_args = [self.program]
        if not args is None: prog_args += args
        
        trace(trace_cmd_level, 'Executor ' + program + ' ', args)
        try:
            self.result = subprocess.check_output(prog_args)
            if tracelevel >= trace_result_level:
                trace(trace_result_level, self.str_result)
        except subprocess.CalledProcessError as e:
            trace(1, e.cmd, 'failed with ', e.returncode)
            trace(1, e.output)
            sys.exit(e.returncode)

    @property
    def str_result(self):
        return self.result.decode() if isinstance(self.result, bytes) else self.result

