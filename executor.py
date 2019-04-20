from tools import trace
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
        
        trace(trace_cmd_level, 'Executor ' + program, args)
        try:
            self.result = subprocess.check_output(prog_args)
            if isinstance(self.result, bytes): self.result = self.result.decode()
            trace(trace_result_level, self.result)
        except subprocess.CalledProcessError as e:
            trace(1, e.cmd, 'failed with ', e.returncode)
            trace(1, e.output)
            sys.exit(e.returncode)


