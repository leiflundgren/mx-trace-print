import sys

from command_line_parser import CommandLineParser
from settings import Settings
from tools import trace
from executor import Executor
from parse_display import ParseDisplayOutput
import io
import os

class Main:
    def __init__(self, program_name, argv:[str]) -> None:
        self.command_line = CommandLineParser(program_name, argv)
        self.settings = Main.find_settings(self.command_line.settings_file)
        self.parsed_display = None

    @staticmethod 
    def find_settings(file: str = None) -> str:
        ex = None
        files = [
            file,            
            os.path.join( os.path.dirname(os.path.realpath(__file__)), 'settings.json'),
            os.path.join( os.path.expanduser("~"), '.mx-trace', 'settings.json'),
            os.path.join( os.path.expanduser("~"), '.mx-trace.json')
        ] 
        for f in files:
            if not f is None and os.path.exists(f):
                try:
                    return Settings(f)
                except BaseException as ex:
                    trace(3, "Failed to open settings from " + f + ": " + str(ex))                    

        trace(3, "Failed to open settings from any known file " + "\n   " + "\n   ".join(files) )
        return Settings("{\n}") # Return empty settings
            

    def main(self):
        trace(1, "placeholder for main method: " + self.command_line.program_name + " args: [ " + ", ".join(self.command_line.original_args)+ " ]")
        display_args = self.command_line.display
        if not display_args is None:
            self.call_display(display_args)
            print(self.parsed_display)
            return

        start_args = self.command_line.start
        if not start_args is None:
            self.call_display(start_args)
            self.call_start(start_args)

    def call_display(self, args:[str]) -> 'ParseDisplayOutput':
        executor = Executor(True, False, self.settings.debug_print_commands, self.settings.trace_cmd, self.settings.trace_args + ['-display'] + args, None)
        if self.settings.debug_print_output:
            trace(4, executor.result)        
        self.parsed_display = ParseDisplayOutput(executor.result)

    def call_start(self, args:[str]):
        if self.parsed_display is None:
            raise ValueError("Called start when no display parser yet!")
        raise NotImplementedError('Start is not implmemented yet')
        

if __name__ == "__main__":
    Main(sys.argv[0], sys.argv[1:]).main()
