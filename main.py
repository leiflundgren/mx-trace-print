#!/usr/bin/python

import sys
import io
import os
import json
import zipfile


from command_line_parser import CommandLineParser
from command_generator import CommandGenerator
from settings import Settings
from tools import trace
from executor import Executor
from parse_display import ParseDisplayOutput
import tools

class Main:

    help_str = \
"""
trace-helper, can call and group calls to MX-trace.
If starting something not yet defined, it is auto-defined.
Possible to start/stop/print on name, not only ID.
Possible to configure groups if units, all listening to the same name
Switches not used by this program should be passed down to trace

  Many settings have default values, change ~/.mx-trace.json
  -display_settings to output current settings-file

  -gangs Prints which gangs are defined

  -add indivuduals_or_gang   (same as -unit in trace)
  -remove indivuduals_or_gang   
  -start indivuduals_or_gang 
  -stop indivuduals_or_gang 
  -clear indivuduals_or_gang   
  -print indivuduals_or_gang   
  -save indivudual_or_gang -prefix trace -postfix log
        Print all the individuals to separate files, with specified prefix/postfix. (Prefix might include paths)
  -zip output_file.zip indivudual_or_gang
        Like save, but generate 1 zip file with all traces

  If specifying many individuals/gangs, separate with space

"""    

    def __init__(self, argv:[str], settings:'Settings' = None) -> None:
        self.command_line = CommandLineParser(argv)
        self.settings = settings or Main.find_settings(self.command_line.settings_file)
        # No type hints on variables, as py3to2 doesn't handle them
        #self.parsed_display = ParseDisplayOutput(io.StringIO(''))
        self.parsed_display = None
        self.command_generator = None
        # self.command_generator: 'CommandGenerator' = None
        # self.command_generator = CommandGenerator(self.parsed_display, self.settings)

    def set_parsed_display(self, val:ParseDisplayOutput):
        self.parsed_display = val
        self.command_generator = CommandGenerator(val, self.settings)

    def execute(self, args:[str]) -> 'Executor':        
        if not isinstance(args, list): 
            raise ValueError('Arguments should be list, not: ' + str(args))
        return Executor(self.settings.trace_cmd, self.settings.trace_args + args, trace_cmd_level=self.settings.debug_trace_commands)

    def execute_all(self, list_of_args:[[str]], extra_args:[str]=[]) -> str:
        if not isinstance(list_of_args, list): raise ValueError("args should be list of command-line-lists, was just " + str(type(list_of_args)))
        if not isinstance(list_of_args[0], list): raise ValueError("args should be list of command-line-lists, was just " + str(type(list_of_args)))

        return "\n".join([self.execute(arg + extra_args).str_result for arg in list_of_args])


    @staticmethod 
    def find_settings(file:str = None) -> str:
        ex = None
        files = filter(None, [
            file,            
            os.path.join( os.path.dirname(os.path.realpath(__file__)), 'settings.json'),
            os.path.join( os.path.expanduser("~"), '.mx-trace', 'settings.json'),
            os.path.join( os.path.expanduser("~"), '.mx-trace.json')
        ])
        for f in files:
            if os.path.exists(f):
                try:
                    return Settings(f)
                except BaseException as ex:
                    trace(3, "Failed to open settings from " + f + ": " + str(ex))                    

        trace(3, "Failed to open settings from any known file " + "\n   " + "\n   ".join(files) )
        return Settings("{\n}") # Return empty settings
            

    def main(self) -> str:
        trace(7, "main method: " + self.command_line.program_name + " args: [ " + ", ".join(self.command_line.original_args)+ " ]")

        display_settings = self.command_line.display_settings
        if  display_settings:
            return self.call_display_settings()

        if self.command_line.gangs_request:
            return self.call_display_gangs()

        help_args = self.command_line.help
        if help_args:
            return self.call_help()
        display_args = self.command_line.display
        if not display_args is None:
            trace(3, "display " + " ".join(display_args), file=sys.stderr)
            self.call_display(display_args + self.command_line.display_extra_args().argv)
            print(self.parsed_display)
            return

        add_args = self.command_line.add
        if not add_args is None:
            trace(3, "add " + " ".join(add_args))
            self.call_display()
            add_extra_args = self.command_line.add_extra_args().argv
            self.call_add(add_args.split(','), self.command_line.lim, self.command_line.textlevel or self.settings.default_textlevel, add_extra_args)
            return

        remove_args = self.command_line.remove
        if not remove_args is None:
            trace(3, "remove " + " ".join(remove_args))
            self.call_display()
            remove_extra_args = self.command_line.remove_extra_args().argv
            self.call_remove(remove_args.split(','), remove_extra_args)
            return


        start_args = self.command_line.start
        if not start_args is None:
            trace(3, "start " + " ".join(start_args))
            self.call_display()
            start_extra_args = self.command_line.start_extra_args().argv
            self.call_start(start_args.split(','), self.command_line.lim, self.command_line.textlevel or self.settings.default_textlevel, start_extra_args)
            return

        stop_args = self.command_line.stop
        if not stop_args is None:
            trace(3, "stop " + " ".join(stop_args))
            self.call_display()
            self.call_stop(stop_args.split(','), self.command_line.stop_extra_args().argv)
            return

        print_args = self.command_line.print_args
        if not print_args is None:
            trace(3, "print " + print_args)
            self.call_display()
            extra_args = self.command_line.print_extra_args().argv
            printout = self.call_print([print_args], extra_args)
            print(printout)
            return printout

        save_args = self.command_line.save
        if not save_args is None:
            prefix=tools.expand_string( self.command_line.file_prefix or self.settings.file_prefix)
            postfix=tools.expand_string(self.command_line.file_postfix or self.settings.file_postfix)
            trace(3, "save " + save_args , ", prefix=" , prefix , ", postfix=" , postfix)
            self.call_display()
            self.call_save(save_args.split(','), prefix, postfix)
            return

        zip_args = self.command_line.zip
        if not zip_args is None:
            prefix = self.command_line.file_prefix or self.settings.zip_prefix
            postfix = self.command_line.file_postfix or self.settings.zip_postfix
            zip_file = zip_args[0]
            _ignored , file_extension = os.path.splitext(zip_file)
            if len(file_extension) == 0:
                zip_file = zip_file.rstrip('.') + '.zip' 
            individuals = zip_args[1:]
            trace(3, "zip ", individuals, " to ", zip_file , ", prefix=" , prefix , ", postfix=" , postfix)
            self.call_display()
            self.call_zip(individuals, zip_file, prefix, postfix)
            return

        trace(2, 'Unknown command, calling trace verbatim for all individuals')
        self.call_display()
        self.call_unknown_command()
        return

    def expand_to_ids(self, ids_or_gangs:[str]) -> [str]:
        if isinstance(ids_or_gangs, str): # Handle if list forgotten
            ids_or_gangs = [ids_or_gangs]
        list_of_lists = [ iog.split(',') for iog in ids_or_gangs]
        ids_or_gangs =  [val for sublist in list_of_lists for val in sublist]

        if len(ids_or_gangs) == 0 or ids_or_gangs[0].lower() == 'all':
            return [str(indv) for indv in self.parsed_display.individuals]
        else:
            return self.settings.expand_to_ids(ids_or_gangs)

    def get_existing_ids(self, id_names:[str]) -> [str]:
        return map( lambda indv: indv.id, self.get_existing_indivuduals(id_names))
        # if len(id_names) == 0 or id_names[0].lower() == 'all':
        #     id_names = [str(indv) for indv in self.parsed_display.individuals]
        # else:
        #     id_names = self.settings.expand_to_ids(id_names)
        # return list(filter(lambda id: not self.parsed_display.get_individual(id) is None, id_names))

    def get_existing_indivuduals(self, id_names:[str]) -> ['ParseDisplayOutput.Individual']:
        if len(id_names) == 0 or id_names[0].lower() == 'all':
            id_names = [str(indv) for indv in self.parsed_display.individuals]
        else:
            id_names = self.settings.expand_to_ids(id_names)
        individuals = map(lambda id: self.parsed_display.get_individual(id), id_names)
        return [x for x in individuals if x is not None]
        #return list(filter(lambda indv: not self.parsed_display.get_individual(id) is None, id_names))

    def get_non_existing_individuals(self, id_names:[str]) -> [str]:
        if len(id_names) == 0 or id_names[0].lower() == 'all':
            id_names = [str(indv) for indv in self.parsed_display.individuals]
        else:
            id_names = self.settings.expand_to_ids(id_names)
        return list(filter(lambda id: self.parsed_display.get_individual(id) is None, id_names))

    def ensure_individuals_exists(self, id_names:[str], lim:str, textlevel:str, extra_args:[str]):
        self.add_individuals(self.get_non_existing_individuals(id_names), lim, textlevel, extra_args)
 
    def call_display_gangs(self) -> str:        
        res = "\n".join( [ (g['name'] + ": " + ", ".join(g['members'])) for g in self.settings.gangs])
        print(res)
        return res


    def call_display_settings(self) -> str:
        j = json.dumps(self.settings.data, sort_keys=True, indent=4)
        print(j)
        return j

    def call_help(self) -> str:
        print(Main.help_str)
        return Main.help_str

    def call_display(self, args:[str] = []) -> 'ParseDisplayOutput':
        disp_output = self.execute(['-display'] + args).str_result
        self.set_parsed_display(ParseDisplayOutput(disp_output))


    def add_individuals(self, individuals:[str], lim:str, textlevel:str, extra_args:[str]):
        trace(4, "Adding individuals ", individuals)
        self.execute_all(self.command_generator.add_indv(individuals, lim, extra_args))

        self.call_display()

        for id in individuals:
            indv = self.parsed_display.get_individual(id)
            if indv is None:
                trace(2, 'Failed to create induvidual ' + id)
                sys.exit(17)
            if indv.textlevel != textlevel:
                self.execute_all(self.command_generator.set_textlevel(id, textlevel))
            
    def call_add(self, args:[str], lim:str, textlevel:str, extra_args:[str] = []):
        if self.parsed_display is None:
            raise ValueError("Called start when no display parser yet!")
        individuals = self.expand_to_ids(args)
        self.ensure_individuals_exists(individuals, lim, textlevel, extra_args)

    def call_remove(self, args:[str], extra_args:[str] = []):
        if self.parsed_display is None:
            raise ValueError("Called start when no display parser yet!")
        existing = self.get_existing_ids(self.expand_to_ids(args))
        remove_cmds = self.command_generator.remove(existing)
        for indv_stop in remove_cmds:
            self.execute(indv_stop + extra_args)
    
    def call_start(self, args:[str], lim:str, textlevel:str, extra_args:[str] = []):
        self.call_add(args, lim, textlevel)
        individuals = self.expand_to_ids(args)
        start_cmds = self.command_generator.start(individuals)
        for indv_start in start_cmds:
            self.execute(indv_start + extra_args)
    
    def call_stop(self, args:[str], extra_args:[str] = []):
        if self.parsed_display is None:
            raise ValueError("Called stop when no display parser yet!")
        individuals = self.expand_to_ids(args)
        existing = self.get_existing_ids(individuals)
        stop_cmds = self.command_generator.stop(existing)
        for indv_stop in stop_cmds:
            self.execute(indv_stop + extra_args)

    def call_print(self, args:[str], extra_args:[str] = []) -> str:
        if self.parsed_display is None:
            raise ValueError("Called print when no display parser yet!")
        individuals = self.expand_to_ids(args)
        existing = filter(lambda id: not self.parsed_display.get_individual(id) is None, individuals)        
        print_cmds = self.command_generator.print_cmd(existing)
        return self.execute_all(print_cmds, extra_args)
    
    def call_save(self, args:[str], prefix, postfix, extra_args:[str] = []) -> str:
        if self.parsed_display is None:
            raise ValueError("Called print when no display parser yet!")
        individuals_names = self.expand_to_ids(args)
        individuals = map(lambda id: self.parsed_display.get_individual(id), individuals_names)
        
        existing_individuals = self.get_existing_ids(individuals)
        
        # extra_args = self.command_line.get_non_save()

        for indv in existing_individuals:
            (print_cmd, filename) = self.command_generator.save_cmd([indv.unit_name], prefix, postfix)[0]        
            trace(3, 'printing ' + indv.id + "/" + indv.unit_name + " to " + filename)
            ex = self.execute(print_cmd)
            with io.open(filename, "w", encoding="latin-1") as fil:
                fil.write(ex.str_result + extra_args)
            
    def call_zip(self, args:[str], zipfilename, prefix, postfix, extra_args:[str] = []) -> str:
        if not isinstance(args, list): 
            raise ValueError('Should be called with list of individuals')
        if self.parsed_display is None:
            raise ValueError("Called print when no display parser yet!")
        individuals_names = self.expand_to_ids(args)
        
        existing_individuals = self.get_existing_indivuduals(individuals_names)
        
        # extra_args = self.command_line.get_non_zip()

        with zipfile.ZipFile(zipfilename, "w") as z:
            for indv in existing_individuals:
                (print_cmd, filename) = self.command_generator.save_cmd([indv.unit_name], prefix, postfix)[0]        
                trace(3, 'printing ' + indv.id + "/" + indv.unit_name + " to " + filename)
                ex = self.execute(print_cmd)
                
                z.writestr(filename, ex.result)

        trace(5, "Wrote to " + zipfilename)
        try:
            trace(5, "Size became " + str(os.path.getsize(zipfilename)))
        except:
            trace(1, "Failed to save data to " + zipfilename)

    
    def expand_first_gang_in_commandline(self, args):
        for i, a in enumerate(args):
            expanded = self.expand_to_ids(a)
            if len(expanded) > 1:                
                pre = args[:i] if i > 0 else []
                post = args[i+1:] if i+1 < len(args) else []
                return [ pre + [indv] + post for indv in expanded ]
        return [args]

    

    def call_unknown_command(self):
        def find_gang() -> (int, [str]):
            for i, a in enumerate(self.command_line.argv[1:]):
                gang = self.expand_to_ids(a)
                if len(gang) > 0:
                    pre = self.command_line.argv[:i] if i > 0 else []
                    post = self.command_line.argv[i+1:] if i+1 < len(self.command_line.argv) else []
                    return [ pre + [indv] + post for indv in gang ]
            return None

        gang_expanded = find_gang() or self.command_line.argv[1:]
        for a in gang_expanded:
            trace(4, a)
            self.execute(a)

if __name__ == "__main__":
    Main(sys.argv).main()
