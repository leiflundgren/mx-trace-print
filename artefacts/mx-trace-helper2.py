from __future__ import with_statement
from __future__ import absolute_import
import sys
from types import ModuleType
from io import open

class MockModule(ModuleType):
    def __init__(self, module_name, module_doc=None):
        ModuleType.__init__(self, module_name, module_doc)
        if u'.' in module_name:
            package, module = module_name.rsplit(u'.', 1)
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

@modulize(u'command_line_parser')
def _command_line_parser(__name__):
    ##----- Begin command_line_parser.py -----------------------------------------##
    
    class CommandLineParser(object):
        def __init__(self, program_name, args ):
            self.program_name = program_name
            self.verbatim_args = args
            self.args = self.parse_command_line(args)
    
        @staticmethod
        def parse_command_line(argv):
            args = {}
            i=1
            while i < len(argv):
                if argv[i][0] == u"-":
                    arg = argv[i].lstrip(u"-").rstrip().lower()
                    val = []
                    i=i+1
                    while i < len(argv) and argv[i][0] != u"-":
                        val.append(argv[i].strip())
                        i = i + 1
                    args[arg] = val
            return args
    
        @property
        def is_empty(self):
            return self.args.__len__() == 0
    
        @property
        def help(self):
            return u'help' in self.args or u'h' in self.args
    
        @property
        def display(self):
            return self.args.get(u'display', None)
    
        @property
        def lim(self):
            return self.args.get(u'lim', None)
        @property
        def unit(self):
            return self.args.get(u'unit', None)
        @property
        def start(self):
            return self.args.get(u'start', None)
        @property
        def stop(self):
            return self.args.get(u'stop', None)
        @property
        def print(self):
            return self.args.get(u'print', None)
    
        @property
        def print_prefix(self):
            return self.args.get(u'prefix', None)
        @property
        def print_postfix(self):
            return self.args.get(u'postfix', None)
        @property
        def signo(self):
            return self.args.get(u'signo', None)
        @property
        def show(self):
            return self.args.get(u'show', None)
        @property
        def signal_from(self):
            return self.args.get(u'from', None)
        @property
        def signal_to(self):
            return self.args.get(u'to', None)
        @property
        def time_from(self):
            return self.args.get(u'from', None)
        @property
        def time_to(self):
            return self.args.get(u'to', None)
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

@modulize(u'tools')
def _tools(__name__):
    ##----- Begin tools.py -------------------------------------------------------##
    import sys
    import io
    import os
    import datetime
    
    def read(file_thing):
        if isinstance(file_thing, io.TextIOBase):
            return file_thing.readlines()
        if isinstance(file_thing, unicode):
            if file_thing.count(u'\n') > 0:
                return file_thing # list-thing
            else:
                with open(file_thing, u"r", encoding=u'iso-8859-1') as f:
                    return f.readlines()
        raise ValueError(u"Cannot read data from " + unicode(type(file_thing)))
    
    def open_file(name):
        return open(name, u"r", encoding=u'iso-8859-1')
    
    
    tracelevel = 4
    log_handle = None
    
    def trace(level, *args):
        def fix_linendings(s):
            if os.linesep == u'\n':
                return s
            p = 0
            while True:
                p = s.find(u'\n', p+1)
                if p<0: break
                if p>0 and s[p-1] != u'\r':
                    s = s[:p] + u'\r' + s[p:]
            return s
    
        def mystr(thing):
            if isinstance(thing, (list, tuple)):
                msg = []
                prefix = u''
    
                if len(thing) <= 4:
                   separator = u', '
                else:
                   separator = (os.linesep+u"   ")
                   prefix = separator
    
                for s in thing:
                    msg += [mystr(s)]
                return prefix + separator.join(msg)
    
            elif isinstance(thing, datetime.datetime):
                return thing.strftime(u"%Y-%m-%d %H:%M:%S")
            elif isinstance(thing, datetime.date):
                return thing.strftime(u"%Y-%m-%d")
            #elif isinstance(thing, bytes):
            #    return bytes.decode('utf-8')
            else:
                try:
                    if isinstance(thing, str):
                        s = thing.decode(u'utf-8')
                    else:
                        s = unicode(thing)
                    s = fix_linendings(s)
                    return s
                except UnicodeEncodeError:
                    return unicode(thing).encode(u'ascii', u'ignore')
                except Exception, ex:
                    return u'Failed to format thing as string caught ' + unicode(ex)
    
        #if tracelevel < level:
        #    return
    
        msg = datetime.datetime.now().strftime(u"%H:%M:%S: ")
        for thing in args:
            msg += mystr(thing)
    
        msg = msg.rstrip()
        handle = sys.stderr if log_handle is None else log_handle
    
        try:
            print >>handle, msg
        except UnicodeEncodeError:
            print >>handle, msg.encode(u'cp850', errors=u'replace')
    
    def pretty(value,htchar=u"\t",lfchar=u"\n",indent=0):
      if type(value) in [dict]:
        return u"{%s%s%s}"%(u",".join([u"%s%s%s: %s"%(lfchar,htchar*(indent+1),repr(key),pretty(value[key],htchar,lfchar,indent+1))for key in value]),lfchar,(htchar*indent))
      elif type(value) in [list,tuple]:
        return (type(value)is list andu"[%s%s%s]"oru"(%s%s%s)")%(u",".join([u"%s%s%s"%(lfchar,htchar*(indent+1),pretty(item,htchar,lfchar,indent+1))for item in value]),lfchar,(htchar*indent))
      else:
        return repr(value)
    
    ##----- End tools.py ---------------------------------------------------------##
    return locals()

@modulize(u'settings')
def _settings(__name__):
    ##----- Begin settings.py ----------------------------------------------------##
    import json
    import io
    import tools
    
    class Settings(object):
    
        def __init__(self, settings_file):                
            if isinstance(settings_file, io.TextIOBase):
                self.data = json.load(settings_file)
            elif isinstance(settings_file, unicode) and settings_file.count(u'\n') > 1:
                self.data = json.load(io.StringIO(settings_file))
            elif isinstance(settings_file, unicode):
                with tools.open_file(settings_file) as f:
                    self.data = json.load(f)
    
    
    
        def get_gang(self, name) :
            gangs_list = self.data[u'gangs']
            for g in gangs_list:
                if g[u'name'] == name:
                    return g[u'members']
            return None
    
        
        @property
        def default_textlevel(self):
            return self.data.find(u'default_textlevel') # none means "default"
    
        @property
        def trace_cmd(self):
            return self.data[u'trace_cmd'] or u'trace'
    
        
    ##----- End settings.py ------------------------------------------------------##
    return locals()


def __main__():
    ##----- Begin __main__.py ----------------------------------------------------##
    import sys
    
    from command_line_parser import CommandLineParser
    from settings import Settings
    from tools import trace
    
    class Main(object):
        def __init__(self, program_name, argv):
            self.command_line = CommandLineParser(program_name, argv)
    
        def main(self):
            trace(1, u"placeholder for main method: " + self.command_line.program_name + u" args: [ " + u", ".join(self.command_line.verbatim_args)+ u" ]")
    
    if __name__ == u"__main__":
        Main(sys.argv[0], sys.argv[1:]).main()
    
    ##----- End __main__.py ------------------------------------------------------##

__main__()
