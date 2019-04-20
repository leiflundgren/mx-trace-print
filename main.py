import sys

from command_line_parser import CommandLineParser
from command_generator import CommandGenerator
from settings import Settings
from tools import trace
from executor import Executor
from parse_display import ParseDisplayOutput
import io
import os

class Main:
    def __init__(self, program_name, argv:[str], settings:'Settings' = None) -> None:
        self.command_line = CommandLineParser(program_name, argv)
        self.settings = settings or Main.find_settings(self.command_line.settings_file)
        self.parsed_display : ParseDisplayOutput = None
        self.command_generator : CommandGenerator = None

    def set_parsed_display(self, val:ParseDisplayOutput):
        self.parsed_display = val
        self.command_generator = CommandGenerator(val, self.settings)

    def execute(self, args:[str]) -> 'Executor':        
        return Executor(self.settings.trace_cmd, self.settings.trace_args + args, trace_cmd_level=self.settings.debug_trace_commands)

    def execute_all(self, list_of_args:[[str]]):
        if not isinstance(list_of_args, list): raise ValueError("args should be list of command-line-lists, was just " + str(type(list_of_args)))
        if not isinstance(list_of_args[0], list): raise ValueError("args should be list of command-line-lists, was just " + str(type(list_of_args)))

        for args in list_of_args:
            self.execute(args)


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
            self.call_display()
            self.call_start(start_args.split(','), self.command_line.lim, self.command_line.textlevel or self.settings.default_textlevel)

    def expand_to_individuals(self, ids_or_gangs:[str]) -> str:
        return self.settings.expand_to_individuals(ids_or_gangs)

    def call_display(self, args:[str] = []) -> 'ParseDisplayOutput':        
        disp_output = self.execute(['-display'] + args).result
        self.set_parsed_display(ParseDisplayOutput(disp_output))

    def ensure_individuals_exists(self, id_names:[str], lim:str, textlevel:str):
        if len(id_names) == 0 or id_names[0].lower() == 'all':
            id_names = [str(indv) for indv in self.parsed_display.individuals]
        else:
            id_names = self.settings.expand_to_individuals(id_names)
        f = filter(lambda id: self.parsed_display.get_individual(id) is None, id_names)        
        undef_indv = list(f)
        if not undef_indv:
            return
        self.add_individuals(undef_indv, lim, textlevel)

    def add_individuals(self, individuals:[str], lim:str, textlevel:str):
        trace(4, "Adding individuals ", individuals)
        self.execute_all(self.command_generator.add(individuals, lim))

        self.call_display()

        for id in individuals:
            indv = self.parsed_display.get_individual(id)
            if indv is None:
                trace(2, 'Failed to create induvidual ' + id)
                sys.exit(17)
            if indv.textlevel != textlevel:
                self.execute_all(self.command_generator.set_textlevel(id, textlevel))
            

    def call_start(self, args:[str], lim:str, textlevel:str):
        if self.parsed_display is None:
            raise ValueError("Called start when no display parser yet!")
        individuals = self.expand_to_individuals(args)
        self.ensure_individuals_exists(individuals, lim, textlevel)
        start_cmds = self.command_generator.start(individuals)
        for indv_start in start_cmds:
            self.execute(indv_start)
    
    def call_start_individual(self, id_name:str, lim:str):
        
        pass

def foo():
    return 'foo'

def bar():
    return 'bar'

if __name__ == "__main__":
    Main(sys.argv[0], sys.argv[1:]).main()
