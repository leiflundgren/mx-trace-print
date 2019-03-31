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
        def __init__(self, program_name:str, args:[str] ):
            self.program_name = program_name
            self.verbatim_args = args
            self.args = self.parse_command_line(args)
    
        @staticmethod
        def parse_command_line(argv:[str]) -> None:
            args = {}
            i=1
            while i < len(argv):
                if argv[i][0] == "-":
                    arg = argv[i].lstrip("-").rstrip().lower()
                    val = []
                    i=i+1
                    while i < len(argv) and argv[i][0] != "-":
                        val.append(argv[i].strip())
                        i = i + 1
                    args[arg] = val
            return args
    
        @property
        def is_empty(self) -> bool:
            return self.args.__len__() == 0
    
        @property
        def help(self) -> bool:
            return 'help' in self.args or 'h' in self.args
    
        @property
        def display(self) -> []:
            return self.args.get('display', None)
    
        @property
        def lim(self) -> str:
            return self.args.get('lim', None)
        @property
        def unit(self) -> str:
            return self.args.get('unit', None)
        @property
        def start(self) -> str:
            return self.args.get('start', None)
        @property
        def stop(self) -> str:
            return self.args.get('stop', None)
        @property
        def print(self) -> str:
            return self.args.get('print', None)
    
        @property
        def print_prefix(self) -> str:
            return self.args.get('prefix', None)
        @property
        def print_postfix(self) -> str:
            return self.args.get('postfix', None)
        @property
        def signo(self) -> str:
            return self.args.get('signo', None)
        @property
        def show(self) -> str:
            return self.args.get('show', None)
        @property
        def signal_from(self) -> str:
            return self.args.get('from', None)
        @property
        def signal_to(self) -> str:
            return self.args.get('to', None)
        @property
        def time_from(self) -> str:
            return self.args.get('from', None)
        @property
        def time_to(self) -> str:
            return self.args.get('to', None)
        # @property
        # def xxx(self) -> str:
        #     return self.args.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.args.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.args.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.args.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.args.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.args.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.args.get('xxx', None)
        # @property
        # def xxx(self) -> str:
        #     return self.args.get('xxx', None)
    
    
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
    
    def open_file(name) -> io.TextIOBase:
        return open(name, "r", encoding='iso-8859-1')
    
    
    tracelevel = 4
    log_handle = None
    
    def trace(level, *args):
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
        handle = sys.stderr if log_handle is None else log_handle
    
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

@modulize('settings')
def _settings(__name__):
    ##----- Begin settings.py ----------------------------------------------------##
    import json
    import io
    import tools
    
    class Settings:
    
        def __init__(self, settings_file):                
            if isinstance(settings_file, io.TextIOBase):
                self.data = json.load(settings_file)
            elif isinstance(settings_file, str) and settings_file.count('\n') > 1:
                self.data = json.load(io.StringIO(settings_file))
            elif isinstance(settings_file, str):
                with tools.open_file(settings_file) as f:
                    self.data = json.load(f)
    
    
    
        def get_gang(self, name) -> [str] :
            gangs_list = self.data['gangs']
            for g in gangs_list:
                if g['name'] == name:
                    return g['members']
            return None
    
        
        @property
        def default_textlevel(self) -> str:
            return self.data.find('default_textlevel') # none means "default"
    
        @property
        def trace_cmd(self) -> str:
            return self.data['trace_cmd'] or 'trace'
    
        
    ##----- End settings.py ------------------------------------------------------##
    return locals()


def __main__():
    ##----- Begin __main__.py ----------------------------------------------------##
    import sys
    
    from command_line_parser import CommandLineParser
    from settings import Settings
    from tools import trace
    
    class Main:
        def __init__(self, program_name, argv:[str]) -> None:
            self.command_line = CommandLineParser(program_name, argv)
    
        def main(self):
            trace(1, "placeholder for main method: " + self.command_line.program_name + " args: [ " + ", ".join(self.command_line.verbatim_args)+ " ]")
    
    if __name__ == "__main__":
        Main(sys.argv[0], sys.argv[1:]).main()
    
    ##----- End __main__.py ------------------------------------------------------##

__main__()
