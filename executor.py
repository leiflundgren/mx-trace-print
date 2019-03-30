from tools import trace
from parse_display import ParseDisplayOutput
from command_generator import CommandGenerator

from subprocess import Popen, PIPE
 

class Executor:
    def __init__(self, capture_stdout:bool, capture_stderr:bool, print_cmd:bool, program:str, args:[str], body:str) -> str:
        self.program = program
        self.args = args
        sout = PIPE if capture_stdout else None
        serr = PIPE if capture_stderr else None
        if print_cmd: print(program + " " + " ".join(args))
        prog_args = [self.program]
        if not args is None: prog_args += args
        self.process = Popen(prog_args , stdout=sout, stderr=serr)

        trace('Executor ' + program, args)

        self.result = self.process.stdout.read()
        if isinstance(self.result, bytes): self.result = self.result.decode()

        if capture_stdout:
            print(self.result)

        pass


