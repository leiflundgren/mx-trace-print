import sys
from types import ModuleType

class MockModule(ModuleType):
    def __init__(self, module_name, module_doc=None):
        ModuleType.__init__(self, module_name, module_doc)
        if '.' in module_name:
            package, module = module_name.rsplit('.', 1)
            get_mock_module(package).__path__ = []
            setattr(get_mock_module(package), module, self)

    def _initialize_(self, module_code):
        self.__dict__.update(module_code(self.__name__))
        self.__doc__ = module_code.__doc__

def get_mock_module(module_name):
    if module_name not in sys.modules:
        sys.modules[module_name] = MockModule(module_name)
    return sys.modules[module_name]

def modulize(module_name, dependencies=[]):
    for d in dependencies: get_mock_module(d)
    return get_mock_module(module_name)._initialize_

##===========================================================================##

@modulize('command_line_parser')
def _command_line_parser(__name__):
    ##----- Begin command_line_parser.py -----------------------------------------##
    
    class CommandLineParser:
        def __init__(self, *arg ):
            if isinstance(arg, str):
                self.program_name = arg
            else:
                self.program_name = arg[0]
                if isinstance(arg[1], list):
                    self.original_args = arg[1]
                else:
                    self.original_args = arg
                self.argv = self.original_args
    
        def get_args(self, name:str, default_value:str = None) -> [str]:
            return CommandLineParser.get_argument(name, self.argv, default_value)
    
        def get_arg(self, name:str, default_value:str = None) -> str:
            arg = self.get_args(name, default_value)
            return None if arg is None or len(arg) == 0 else arg[0]
        
        def has_arg(self, name:str, default_value:str = None) -> bool:
            arg_ls = self.get_args(name, default_value)
            return not arg_ls is None
    
        def replace_arg(self, name:str, val:[str]) -> 'CommandLineParser':
            return CommandLineParser(*CommandLineParser.replace_argument(name, self.argv, val))
    
        def remove_arg(self, *names:[str]) -> 'CommandLineParser':
            cmd = self
            for n in names:
                cmd = cmd.replace_arg(n, None)
            return cmd
    
    
        @staticmethod
        def find_arg_index(name:str, argv:[str]) -> (int,int, [str]):
            """
                Finds between which indices that an argument is
                This makes it possible to replace the argument with seomthing else
                Returns start/stop indices and a list of the arguemnts
            """
            name = name.lower()
            i=1 if len(argv) > 0 and argv[0][0] != '-' else 0
            while i < len(argv):
                if argv[i][0] != "-":
                    i=i+i
                    continue
    
                arg = argv[i].lstrip("-").rstrip().lower()
                val = []
                start = i
                i=i+1
                while i < len(argv) and argv[i][0] != "-":
                    val.append(argv[i].strip())
                    i = i + 1
                if arg == name:
                    return (start, i-1, val)
    
            return (-1, -1, None)
    
        @staticmethod
        def get_argument(name:str, argv:[str], default_value:[str] = None) -> [str]:
            """ Gets the arguments to switch 'name' as a list.
            return: None is not found, otherwise a list. (If name is found but has no arguments, an empty list is returned.) """
            (_start,_stop, args) = CommandLineParser.find_arg_index(name, argv)
            if not args is None:
                return args
            if default_value is None:
                return None
            if isinstance(default_value, list):
                return default_value
            else:
                return [default_value]
    
        @staticmethod
        def replace_argument(name:str, argv:[str], val:[str]) -> [str]:
            """ 
                Replaces switch 'name' with the supplied list. 
                :param val:
                    list with only 'name' to have no arguments, 
                    None to remove the switch all together
                :returns: the updated arguments
            """
            (start,stop, args) = CommandLineParser.find_arg_index(name, argv)
            if start < 0:
                return args
            
            pre = argv[:start] if start > 0 else []
            post = argv[stop+1:] if stop+1 < len(argv) else []
            if val is None or len(val) == 0:
                return pre + post
            else:
                return pre + [val] + post
    
        def set_program_name(self, new_name) -> 'CommandLineParser':
            return CommandLineParser(new_name, self.argv)
    
        @property
        def is_empty(self) -> bool:
            """ Considered empty is only program-name """
            if len(self.argv) == 0:
                return True
            elif len(self.argv) == 1 and self.argv[0][0] != '-': 
                return True # only prog-name
            else:
                return False
    
        @property
        def settings_file(self) -> str:
            return (
                    self.get_arg('settings_file') 
                    or  self.get_arg('settings')
            )
    
        @property
        def help(self) -> bool:
            return self.has_arg('help') or self.has_arg('h')
    
        @property
        def display_settings(self) -> bool:
            return self.has_arg('display_settings') or self.has_arg('display-settings') or self.has_arg('displaysettings')
    
        @property
        def gangs_request(self) -> bool:
            return self.has_arg('gangs') or self.has_arg('gang')
    
    
        @property
        def display(self) -> [str]:
            """
                :return: the optional argument to display [0,1..15]
            """    
            return self.get_args('display')
    
        def display_extra_args(self) -> 'CommandLineParser':
            return self.remove_arg('display')
    
        @property
        def lim(self) -> str:
            return self.get_arg('lim')
        @property
        def unit(self) -> str:
            return self.get_arg('unit')
        @property
        def add(self) -> str:
            return self.get_arg('add')
        def add_extra_args(self) -> 'CommandLineParser':
            return self.remove_arg('add', 'unit', 'lim')
        @property
        def remove(self) -> str:
            return self.get_arg('remove')
        def remove_extra_args(self) -> 'CommandLineParser':
            return self.remove_arg('remove')
        @property
        def start(self) -> str:
            return self.get_arg('start')
    
        def start_extra_args(self) -> 'CommandLineParser' :
            return self.remove_arg('start').remove_arg('lim').remove_arg('textlevel')
    
        @property
        def stop(self) -> str:
            return self.get_arg('stop')
        def stop_extra_args(self) -> 'CommandLineParser' :
            return self.remove_arg('stop').remove_arg('lim')
    
        @property
        def print(self) -> str:
            return self.get_arg('print')
        def print_extra_args(self) -> 'CommandLineParser' :
            return self.remove_arg('print').remove_arg('lim')
    
        @property
        def save(self) -> str:
            return self.get_arg('save')
        @property
        def file_prefix(self) -> str:
            return self.get_arg('prefix')
        @property
        def file_postfix(self) -> str:
            return self.get_arg('postfix')
        def save_extra_args(self) -> 'CommandLineParser' :
            return self.remove_arg('save').remove_arg('prefix').remove_arg('postfix')
    
        @property
        def zip(self) -> [str]:
            return self.get_args('zip')
        def zip_extra_args(self) -> 'CommandLineParser' :
            return self.remove_arg('zip').save_extra_args()
     
        @property
        def signo(self) -> str:
            return self.get_arg('signo')
        @property
        def show(self) -> str:
            return self.get_arg('show')
        @property
        def signal_from(self) -> str:
            return self.get_arg('from')
        @property
        def signal_to(self) -> str:
            return self.get_arg('to')
        @property
        def time_from(self) -> str:
            return self.get_arg('from')
        @property
        def time_to(self) -> str:
            return self.get_arg('to')
        @property
        def textlevel(self) -> str:
            return self.get_arg('textlevel')        
        # @property
        # def xxx(self) -> str:
        #     return self.argv.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.argv.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.argv.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.argv.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.argv.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.argv.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.argv.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.argv.get('xxx', None)
    
    
    ##----- End command_line_parser.py -------------------------------------------##
    return locals()

@modulize('tools')
def _tools(__name__):
    ##----- Begin tools.py -------------------------------------------------------##
    import sys
    import io
    import os
    import datetime
    
    def read(file_thing) -> [str]:
        if isinstance(file_thing, io.TextIOBase):
            return file_thing.readlines()
        if isinstance(file_thing, str):
            if file_thing.count('\n') > 0:
                return file_thing # list-thing
            else:
                with open(file_thing, "r", encoding='iso-8859-1') as f:
                    return f.readlines()
        raise ValueError("Cannot read data from " + str(type(file_thing)))
    
    def open_read_file(name) -> io.TextIOBase:
        return open(name, "r", encoding='iso-8859-1')
    
    
    tracelevel = 4
    log_handle = None
    
    def trace(level:int, *args, file=sys.stdout):
        def fix_linendings(s: str) -> str:
            if os.linesep == '\n':
                return s
            p = 0
            while True:
                p = s.find('\n', p+1)
                if p<0: break
                if p>0 and s[p-1] != '\r':
                    s = s[:p] + '\r' + s[p:]
            return s
    
        def mystr(thing):
            if isinstance(thing, (list, tuple)):
                msg = []
                prefix = ''
    
                if len(thing) <= 4:
                   separator = ', '
                else:
                   separator = (os.linesep+"   ")
                   prefix = separator
    
                for s in thing:
                    msg += [mystr(s)]
                return prefix + separator.join(msg)
    
            elif isinstance(thing, datetime.datetime):
                return thing.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(thing, datetime.date):
                return thing.strftime("%Y-%m-%d")
            #elif isinstance(thing, bytes):
            #    return bytes.decode('utf-8')
            else:
                try:
                    if isinstance(thing, bytes):
                        s = thing.decode('utf-8')
                    else:
                        s = str(thing)
                    s = fix_linendings(s)
                    return s
                except UnicodeEncodeError:
                    return str(thing).encode('ascii', 'ignore')
                except Exception as ex:
                    return 'Failed to format thing as string caught ' + str(ex)
    
        #if tracelevel < level:
        #    return
    
        msg = datetime.datetime.now().strftime("%H:%M:%S: ")
        for thing in args:
            msg += mystr(thing)
    
        msg = msg.rstrip()
        handle = file if not file is None else ( sys.stderr if log_handle is None  else log_handle )
    
        try:
            print(msg, file=handle)
        except UnicodeEncodeError:
            print(msg.encode('cp850', errors='replace'), file=handle)
    
    def pretty(value,htchar="\t",lfchar="\n",indent=0):
      if type(value) in [dict]:
        return "{%s%s%s}"%(",".join(["%s%s%s: %s"%(lfchar,htchar*(indent+1),repr(key),pretty(value[key],htchar,lfchar,indent+1))for key in value]),lfchar,(htchar*indent))
      elif type(value) in [list,tuple]:
        return (type(value)is list and"[%s%s%s]"or"(%s%s%s)")%(",".join(["%s%s%s"%(lfchar,htchar*(indent+1),pretty(item,htchar,lfchar,indent+1))for item in value]),lfchar,(htchar*indent))
      else:
        return repr(value)
    
    ##----- End tools.py ---------------------------------------------------------##
    return locals()

@modulize('parse_display')
def _parse_display(__name__):
    ##----- Begin parse_display.py -----------------------------------------------##
    import io
    from typing import List, Optional
    import tools
    
    class ParseDisplayOutput:
    
        class Individual:
            def __init__(self, dict) -> None:
                self.dict = dict
            def __str__(self) -> str:
                return "{id}: {name} {state}".format(id=self.id, name=self.unit_name, state=self.state)
    
            def get(self, attrName) -> str:
                val = self.dict.get(attrName)
                return ( None if val is None else val.strip() )
    
            @property
            def is_header(self) -> bool:
                return self.dict.find('Version') is not None
    
            @property
            def id(self) -> str:
                return self.get('Trace ind')
    
            @property
            def state(self) -> str:
                return self.get('State')
            @property
            def stored(self) -> str:
                return self.get('Stored')
            @property
            def size(self) -> str:
                return self.get('Size per lim')
         
            @property
            def trace_type(self) -> str:
                return self.get('Type')
            @property
            def rotating(self) -> str:
                return self.get('Rotating')
            @property
            def textlevel(self) -> str:
                return self.get('Textlevel')
            @property
            def lim(self) -> str:
                return self.get('Lim no')
            @property
            def unit_no(self) -> str:
                return self.get('Unit no')
            @property
            def unit_name(self) -> str:
                return self.get('Unit name')
            @property
            def time_mark(self) -> str:
                return self.get('Time mark')
            @property
            def by_user(self) -> str:
                return self.get('by user')
            # @property
            # def (self) -> str:
            #     return self.dict[''].strip()
                        
    
        def __init__(self, source) -> None:
            self.source = tools.read(source)
            if isinstance(self.source, str):
                self.source = self.source.splitlines()
    
            self.individuals : List[ParseDisplayOutput.Individual] = [] 
            parts : List[str] = []
    
            in_header = True
            for line in self.source:
                line = line.strip()
                
                ## skip header, until a line starts with Version
                if in_header:
                    if line.startswith('Version'):
                        in_header = False
                    else:
                        continue
    
                if line.startswith('Version'):
                    mpos = line.index(', Market:')
                    self.version = line[8:mpos].strip()
                    self.market = line[mpos+9:].strip()
                    continue
            
                if line.startswith('First'):
                    last = line.find('Last:')-1
                    while last > 0 and line[last] == ' ':
                        last=last-1
                    if last>0 and line[last] != ',':
                        line = line[:last+1] + ',' + line[last+1:]
                
                if len(line) > 0 :
                    parts.extend(map(str.strip, line.split(',')))
                else:
                    individual = self.parse_individual(parts)
                    if individual is not None:
                        self.individuals.append(individual)
                    parts = []
    
        def __str__(self) -> str:
            return  "\n".join( [str(i) for i in self.individuals ] )
    
        @property
        def first_trace(self) -> str:
            return self.individuals[0].get('First')
        @property
        def last_trace(self) -> str:
            return self.individuals[0].get('Last')
    
    
        def get_individual(self, id) -> 'Individual':
            if isinstance(id, int):
                return self.individuals[id] if id < len(self.individuals) else None
            for ind in self.individuals[1:]: # Avoid header
                if ind.id == id or ind.unit_name == id:
                    return ind
            return None
    
        ### convenience method that returns the id of Individual matching unitname, or None
        def get_id(self, unitname) -> str:
            ind = self.get_individual(unitname)
            return ind.id if not ind is None else None
    
        ## Trace ind:  3, State: setup       , Stored:      0, Size per lim: 5000,  Type     : unit-trace      , Rotating: on , Textlevel: all, Lim no   :   1, Unit no: 0206, Unit name: CMP , Time mark: 2018-12-13 16:46:11 (CET), by user: mxone_admin
        @staticmethod
        def parse_individual(parts) -> 'Individual':
            d = dict(map(str.strip, itm.split(':', 1)) for itm in parts)
            return ParseDisplayOutput.Individual(d) if len(d) > 0 else None
    
    ##----- End parse_display.py -------------------------------------------------##
    return locals()

@modulize('settings')
def _settings(__name__):
    ##----- Begin settings.py ----------------------------------------------------##
    import json
    import io
    import tools
    import os.path
    import re
    
    class Settings:
    
        def __init__(self, settings_file):
            if isinstance(settings_file, io.TextIOBase):
                self.__init__(settings_file.read())
                return
            elif isinstance(settings_file, str) and (settings_file.count('\n') > 1 or not os.path.exists(settings_file) ):
                self.raw_data = settings_file
                trimmed = Settings.trim_json_comments(settings_file)
                self.data = json.load(io.StringIO(trimmed))
                tools.tracelevel = self.debug_trace_level
            elif isinstance(settings_file, str):
                with tools.open_read_file(settings_file) as f:
                    self.__init__(f.read())
                    return
    
        @staticmethod
        def trim_json_comments(data_string):
            result = []
            for line in data_string.split("\n"):
                stripped = line.strip()
                if len(stripped) < 1 or stripped[0:2] == "//":
                    line = "" # remove
                elif line[-1] not in r"\,\"\'":
                    line = re.sub(r"\/\/.*?$", "", line)
                result.append(line)
            return "\n".join(result)
    
        @property
        def gangs(self) -> [{}]:
            return self.data['gangs']
    
        def get_gang(self, name) -> [str]:
            gangs_list = self.gangs
            for g in gangs_list:
                if g['name'] == name:
                    return g['members']
            return None
    
        def expand_to_ids(self, ids_or_gangs:[str]) -> str:
            res = []
            ls = ids_or_gangs if isinstance(ids_or_gangs, list) else [ids_or_gangs]
            for id in ls:
                members = self.get_gang(id) or [id]
                res.extend(members)
            return res
    
    
        @property
        def default_textlevel(self) -> str:
            return self.data.get('default_textlevel', 'default')  # none means "default"
    
        @property
        def trace_cmd(self) -> str:
            return self.data.get('trace_cmd', 'trace')
    
        @property
        def trace_args(self) -> [str]:
            """
                If out trace-command requires some extra prefixed arguments. 
                :returns: list might be empty, but never none
            """
            return self.data.get('trace_args', [])
    
        @property
        def file_prefix(self) -> str:
            """
                Prefix for trace output files
            """
            return self.data.get('file_prefix', 'trace_mx_')
    
        @property
        def file_postfix(self) -> str:
            """
                Postfix for trace output files
            """
            return self.data.get('file_postfix', '.log')
        
        @property
        def file_separators(self) -> str:
            """
                Which separators are allowed
            """
            return self.data.get('file_separators', '-_/=')
    
        @property
        def zip_prefix(self) -> str:
            """
                Prefix for trace output files
            """
            return self.data.get('zip_prefix', self.file_prefix)
    
        @property
        def zip_postfix(self) -> str:
            """
                Postfix for trace output files
            """
            return self.data.get('file_postfix', self.file_postfix)
        @property
        def debug_trace_level(self) -> int:
            return self.data.get('debug_trace_level', 7)
    
        @property
        def debug_trace_commands(self) -> int:
            return self.data.get('debug_trace_commands', 7)
    
        @property
        def debug_trace_output(self) -> int:
            v = self.data.get('debug_trace_output')
            return v is not v is None or self.debug_trace_output
    
    ##----- End settings.py ------------------------------------------------------##
    return locals()

@modulize('command_generator')
def _command_generator(__name__):
    ##----- Begin command_generator.py -------------------------------------------##
    from parse_display import ParseDisplayOutput
    from tools import trace
    from settings import Settings
    import sys
    
    class CommandGenerator:
    
        def __init__(self, display_output:ParseDisplayOutput, settings:'Settings'):
            self.display_output = display_output
            self.mx_version = self.display_output.version
            self.settings = settings
            pass
    
        @property
        def trace_cmd(self) -> str:
            return self.settings.trace_cmd
        @property
        def trace_prefix_args(self) -> [str]:
            return self.settings.trace_args
    
        @staticmethod
        def get_cmd_add_individual(name:str, lim:str) -> [str]:
            lim_switch = [] if lim is None else ['-lim', lim]
            return lim_switch + ['-unit', name]
    
        @staticmethod
        def get_cmd_remove_individual(name:str) -> [str]:
            return ['-remove', name]
    
        @staticmethod
        def get_cmd_set_textlevel(n:str, textlevel:str = 'normal') -> [str]:
            return ['-modify', n, '-textlevel', textlevel]
            
        @staticmethod
        def get_cmd_start(n_list:[str]) -> [str]:
            return ['-start', ",".join(n_list) ]
        @staticmethod
        def get_cmd_stop(n_list:[str]) -> [str]:
            return ['-stop', ",".join(n_list) ]
        @staticmethod
        def get_cmd_clear(n_list:[str]) -> [str]:
            return ['-clear', ",".join(n_list) ]
        
        @staticmethod
        def get_cmd_print(unit_id:str) -> [str]:
            return ['-print', unit_id ]
    
        def expand_names(self, name_or_list) -> [str]:
            def expand_ranges(ls:[str]) -> [str]:
                res = []
                for s in ls:
                    for s2 in s.split(','):
                        dash = s2.find('-')
                        if dash > 0:
                            n1 = s2[:dash]
                            n2 = s2[dash+1:]
                            r = list(map( str, range(int(n1), int(n2)+1)))
                            res += r
                        else:
                            res.append(s2)
                return res
    
    
            res = []
    
            ls = name_or_list if isinstance(name_or_list, list) else [name_or_list]
            ls = expand_ranges(ls)
            for name in ls:
                # if name is not gang, assume unit-name
                gang = self.settings.get_gang(name)
                if not gang is None:
                    res +=self.expand_names(gang)
                else:
                    res.append(name)
            return res
    
        def get_ids_of(self, name_or_list) -> [str]:
            res = []
            for name in self.expand_names(name_or_list):
                ind = self.display_output.get_individual(name)
                if ind is None:
                    trace(2, "Unknown unit '" + name + "', ignored")
                    continue
                res.append(ind.id)
    
            return res
    
        def add_indv(self, name:[str], lim:str = "1", extra_args:[str] = []) -> [str]:
            res = []
            for member in self.settings.expand_to_individuals(name):
                if self.display_output.get_individual(member) is None:               
                    res.append(CommandGenerator.get_cmd_add_individual(member, lim) + extra_args)
    
            return res
    
        def remove(self, name:[str]) -> [str]:
            res = []
            for member in self.settings.expand_to_individuals(name):
                if self.display_output.get_individual(member) is None:               
                    res.append(CommandGenerator.get_cmd_remove_individual(member))
    
            return res
    
        def set_textlevel(self, name:[str], textlevel:str = 'normal') -> [str]:
            res = []
            
            for member in self.settings.expand_to_individuals(name):
                indv = self.display_output.get_individual(member)
                if indv is None:
                    trace(2, "Unknown gang-member '" + member + "' Textlevel not changed")
                    continue
                id = indv.id
                res.append(CommandGenerator.get_cmd_set_textlevel(id, textlevel))
            
            return res 
    
    
        def start(self, name:[str]) -> [str]:
            ids = self.get_ids_of(name)
            return map(lambda i: self.get_cmd_start(i), ids)
    
        def stop(self, name:[str]) -> [str]:
            ids = self.get_ids_of(name)
            return map(lambda i: self.get_cmd_stop(i), ids)
    
        def clear(self, name:[str]) -> [str]:
            ids = self.get_ids_of(name)
            return map(lambda i: self.get_cmd_clear(i), ids)
    
    
        ### Returns a list of tuples(print-cmd, target-filename)
        def save_cmd(self, names:[str], prefix:str = "", postfix:str = ".log", ) -> [(str, str)]:
            def gen_tuple(unitname, id):
                cmd = CommandGenerator.get_cmd_print(id)
                filename = (prefix+sep+unitname+postfix).strip(sep)
                return (cmd, filename)
            
            if self.settings.file_separators.find(prefix[-1]) >= 0:
                sep = prefix[-1]
                prefix = prefix[:-1]
            elif self.settings.file_separators.find(postfix[0]) >= 0:
                sep = postfix[0]
                postfix = postfix[1:]
            else:
                sep = '_'
    
            res = []
    
            for name in self.expand_names(names):
                id = self.display_output.get_id(name)
                if id is None:
                    trace(2, "print_cmd: unknown unit " + name + ", not printed", file=sys.stderr)
                    continue
                res.append(gen_tuple(name, id))
            return res
    
        ### Returns a list print-cmd
        def print_cmd(self, names:[str]) -> [str]:
            res = []
    
            for name in names:
                id = self.display_output.get_id(name)
                if id is None:
                    trace(2, "print_cmd: unknown unit " + name + ", not printed", file=sys.stderr)
                    continue
                cmd = CommandGenerator.get_cmd_print(id)
                res.append(cmd)
            return res
    
    ##----- End command_generator.py ---------------------------------------------##
    return locals()

@modulize('executor')
def _executor(__name__):
    ##----- Begin executor.py ----------------------------------------------------##
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
    
    
    ##----- End executor.py ------------------------------------------------------##
    return locals()

@modulize('main')
def _main(__name__):
    ##----- Begin main.py --------------------------------------------------------##
    import sys
    import io
    import os
    import zipfile
    
    from command_line_parser import CommandLineParser
    from command_generator import CommandGenerator
    from settings import Settings
    from tools import trace
    from executor import Executor
    from parse_display import ParseDisplayOutput
    
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
    
        def execute_all(self, list_of_args:[[str]]) -> str:
            if not isinstance(list_of_args, list): raise ValueError("args should be list of command-line-lists, was just " + str(type(list_of_args)))
            if not isinstance(list_of_args[0], list): raise ValueError("args should be list of command-line-lists, was just " + str(type(list_of_args)))
    
            return "\n".join([self.execute(arg).str_result for arg in list_of_args])
    
    
        @staticmethod 
        def find_settings(file:str = None) -> str:
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
    
            print_args = self.command_line.print
            if not print_args is None:
                trace(3, "print " + print_args)
                self.call_display()
                extra_args = self.command_line.print_extra_args().argv
                printout = self.call_print([print_args], extra_args)
                print(printout)
                return printout
    
            save_args = self.command_line.save
            if not save_args is None:
                prefix=self.command_line.file_prefix or self.settings.save_prefix
                postfix=self.command_line.file_postfix or self.settings.save_postfix
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
    
        def expand_to_ids(self, ids_or_gangs:[str]) -> str:
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
            print(self.settings.raw_data)
            return self.settings.raw_data
    
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
            return self.execute_all(print_cmds + extra_args)
        
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
        Main(sys.argv[0], sys.argv[1:]).main()
    
    ##----- End main.py ----------------------------------------------------------##
    return locals()
