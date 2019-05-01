from __future__ import with_statement
from __future__ import absolute_import
import sys
from types import ModuleType
from io import open
from itertools import imap
from itertools import ifilter

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
        def __init__(self, *arg ):
            if isinstance(arg, unicode):
                self.program_name = arg
            else:
                self.program_name = arg[0]
                if isinstance(arg[1], list):
                    self.original_args = arg[1]
                else:
                    self.original_args = arg
                self.argv = self.original_args
    
        def get_args(self, name, default_value = None):
            return CommandLineParser.get_argument(name, self.argv, default_value)
    
        def get_arg(self, name, default_value = None):
            arg = self.get_args(name, default_value)
            return None if arg is None or len(arg) == 0 else arg[0]
        
        def has_arg(self, name, default_value = None):
            arg_ls = self.get_args(name, default_value)
            return not arg_ls is None
    
        def replace_arg(self, name, val):
            return CommandLineParser(*CommandLineParser.replace_argument(name, self.argv, val))
    
        def remove_arg(self, *names):
            cmd = self
            for n in names:
                cmd = cmd.replace_arg(n, None)
            return cmd
    
    
        @staticmethod
        def find_arg_index(name, argv):
            u"""
                Finds between which indices that an argument is
                This makes it possible to replace the argument with seomthing else
                Returns start/stop indices and a list of the arguemnts
            """
            name = name.lower()
            i=1 if len(argv) > 0 and argv[0][0] != u'-' else 0
            while i < len(argv):
                if argv[i][0] != u"-":
                    i=i+i
                    continue
    
                arg = argv[i].lstrip(u"-").rstrip().lower()
                val = []
                start = i
                i=i+1
                while i < len(argv) and argv[i][0] != u"-":
                    val.append(argv[i].strip())
                    i = i + 1
                if arg == name:
                    return (start, i-1, val)
    
            return (-1, -1, None)
    
        @staticmethod
        def get_argument(name, argv, default_value = None):
            u""" Gets the arguments to switch 'name' as a list.
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
        def replace_argument(name, argv, val):
            u""" 
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
    
        def set_program_name(self, new_name):
            return CommandLineParser(new_name, self.argv)
    
        @property
        def is_empty(self):
            u""" Considered empty is only program-name """
            if len(self.argv) == 0:
                return True
            elif len(self.argv) == 1 and self.argv[0][0] != u'-': 
                return True # only prog-name
            else:
                return False
    
        @property
        def settings_file(self):
            return (
                    self.get_arg(u'settings_file') 
                    or  self.get_arg(u'settings')
            )
    
        @property
        def help(self):
            return self.has_arg(u'help') or self.has_arg(u'h')
    
        @property
        def display_settings(self):
            return self.has_arg(u'display_settings') or self.has_arg(u'display-settings') or self.has_arg(u'displaysettings')
    
        @property
        def gangs_request(self):
            return self.has_arg(u'gangs') or self.has_arg(u'gang')
    
    
        @property
        def display(self):
            u"""
                :return: the optional argument to display [0,1..15]
            """    
            return self.get_args(u'display')
    
        def display_extra_args(self):
            return self.remove_arg(u'display')
    
        @property
        def lim(self):
            return self.get_arg(u'lim')
        @property
        def unit(self):
            return self.get_arg(u'unit')
        @property
        def add(self):
            return self.get_arg(u'add')
        def add_extra_args(self):
            return self.remove_arg(u'add', u'unit', u'lim')
        @property
        def remove(self):
            return self.get_arg(u'remove')
        def remove_extra_args(self):
            return self.remove_arg(u'remove')
        @property
        def start(self):
            return self.get_arg(u'start')
    
        def start_extra_args(self) :
            return self.remove_arg(u'start').remove_arg(u'lim').remove_arg(u'textlevel')
    
        @property
        def stop(self):
            return self.get_arg(u'stop')
        def stop_extra_args(self) :
            return self.remove_arg(u'stop').remove_arg(u'lim')
    
        @property
        def print_args(self):
            return self.get_arg(u'print')
        def print_extra_args(self) :
            return self.remove_arg(u'print').remove_arg(u'lim')
    
        @property
        def save(self):
            return self.get_arg(u'save')
        @property
        def file_prefix(self):
            return self.get_arg(u'prefix')
        @property
        def file_postfix(self):
            return self.get_arg(u'postfix')
        def save_extra_args(self) :
            return self.remove_arg(u'save').remove_arg(u'prefix').remove_arg(u'postfix')
    
        @property
        def zip(self):
            return self.get_args(u'zip')
        def zip_extra_args(self) :
            return self.remove_arg(u'zip').save_extra_args()
     
        @property
        def signo(self):
            return self.get_arg(u'signo')
        @property
        def show(self):
            return self.get_arg(u'show')
        @property
        def signal_from(self):
            return self.get_arg(u'from')
        @property
        def signal_to(self):
            return self.get_arg(u'to')
        @property
        def time_from(self):
            return self.get_arg(u'from')
        @property
        def time_to(self):
            return self.get_arg(u'to')
        @property
        def textlevel(self):
            return self.get_arg(u'textlevel')        
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
    
    def open_read_file(name):
        return open(name, u"r", encoding=u'iso-8859-1')
    
    
    tracelevel = 4
    log_handle = None
    
    def trace(level, *args, **_3to2kwargs):
        if 'file' in _3to2kwargs: file = _3to2kwargs['file']; del _3to2kwargs['file']
        else: file = sys.stdout
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
        handle = file if not file is None else ( sys.stderr if log_handle is None  else log_handle )
    
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

@modulize(u'parse_display')
def _parse_display(__name__):
    ##----- Begin parse_display.py -----------------------------------------------##
    import io
    from typing import List, Optional
    import tools
    
    class ParseDisplayOutput(object):
    
        class Individual(object):
            def __init__(self, dict):
                self.dict = dict
            def __str__(self):
                return u"{id}: {name} {state}".format(id=self.id, name=self.unit_name, state=self.state)
    
            def get(self, attrName):
                val = self.dict.get(attrName)
                return ( None if val is None else val.strip() )
    
            @property
            def is_header(self):
                return self.dict.find(u'Version') is not None
    
            @property
            def id(self):
                return self.get(u'Trace ind')
    
            @property
            def state(self):
                return self.get(u'State')
            @property
            def stored(self):
                return self.get(u'Stored')
            @property
            def size(self):
                return self.get(u'Size per lim')
         
            @property
            def trace_type(self):
                return self.get(u'Type')
            @property
            def rotating(self):
                return self.get(u'Rotating')
            @property
            def textlevel(self):
                return self.get(u'Textlevel')
            @property
            def lim(self):
                return self.get(u'Lim no')
            @property
            def unit_no(self):
                return self.get(u'Unit no')
            @property
            def unit_name(self):
                return self.get(u'Unit name')
            @property
            def time_mark(self):
                return self.get(u'Time mark')
            @property
            def by_user(self):
                return self.get(u'by user')
            # @property
            # def (self) -> str:
            #     return self.dict[''].strip()
                        
    
        def __init__(self, source):
            self.source = tools.read(source)
            if isinstance(self.source, unicode):
                self.source = self.source.splitlines()
    
            parts = [] #List[str] 
            self.individuals  = [] # List['ParseDisplayOutput.Individual'] 
    
            in_header = True
            for line in self.source:
                line = line.strip()
                
                ## skip header, until a line starts with Version
                if in_header:
                    if line.startswith(u'Version'):
                        in_header = False
                    else:
                        continue
    
                if line.startswith(u'Version'):
                    mpos = line.index(u', Market:')
                    self.version = line[8:mpos].strip()
                    self.market = line[mpos+9:].strip()
                    continue
            
                if line.startswith(u'First'):
                    last = line.find(u'Last:')-1
                    while last > 0 and line[last] == u' ':
                        last=last-1
                    if last>0 and line[last] != u',':
                        line = line[:last+1] + u',' + line[last+1:]
                
                if len(line) > 0 :
                    parts.extend(imap(unicode.strip, line.split(u',')))
                else:
                    individual = self.parse_individual(parts)
                    if individual is not None:
                        self.individuals.append(individual)
                    parts = []
    
        def __str__(self):
            return  u"\n".join( [unicode(i) for i in self.individuals ] )
    
        @property
        def first_trace(self):
            return self.individuals[0].get(u'First')
        @property
        def last_trace(self):
            return self.individuals[0].get(u'Last')
    
    
        def get_individual(self, id):
            if isinstance(id, int):
                return self.individuals[id] if id < len(self.individuals) else None
            for ind in self.individuals[1:]: # Avoid header
                if ind.id == id or ind.unit_name == id:
                    return ind
            return None
    
        ### convenience method that returns the id of Individual matching unitname, or None
        def get_id(self, unitname):
            ind = self.get_individual(unitname)
            return ind.id if not ind is None else None
    
        ## Trace ind:  3, State: setup       , Stored:      0, Size per lim: 5000,  Type     : unit-trace      , Rotating: on , Textlevel: all, Lim no   :   1, Unit no: 0206, Unit name: CMP , Time mark: 2018-12-13 16:46:11 (CET), by user: mxone_admin
        @staticmethod
        def parse_individual(parts):
            d = dict(imap(unicode.strip, itm.split(u':', 1)) for itm in parts)
            return ParseDisplayOutput.Individual(d) if len(d) > 0 else None
    
    ##----- End parse_display.py -------------------------------------------------##
    return locals()

@modulize(u'settings')
def _settings(__name__):
    ##----- Begin settings.py ----------------------------------------------------##
    import json
    import io
    import tools
    import os.path
    import re
    
    class Settings(object):
    
        def __init__(self, settings_file):
            if isinstance(settings_file, io.TextIOBase):
                self.__init__(settings_file.read())
                return
            elif isinstance(settings_file, unicode) and (settings_file.count(u'\n') > 1 or not os.path.exists(settings_file) ):
                self.raw_data = settings_file
                trimmed = Settings.trim_json_comments(settings_file)
                self.data = json.load(io.StringIO(trimmed))
                tools.tracelevel = self.debug_trace_level
            elif isinstance(settings_file, unicode):
                with tools.open_read_file(settings_file) as f:
                    self.__init__(f.read())
                    return
    
        @staticmethod
        def trim_json_comments(data_string):
            result = []
            for line in data_string.split(u"\n"):
                stripped = line.strip()
                if len(stripped) < 1 or stripped[0:2] == u"//":
                    line = u"" # remove
                elif line[-1] not in ur"\,\"\'":
                    line = re.sub(ur"\/\/.*?$", u"", line)
                result.append(line)
            return u"\n".join(result)
    
        @property
        def gangs(self):
            return self.data[u'gangs']
    
        def get_gang(self, name):
            gangs_list = self.gangs
            for g in gangs_list:
                if g[u'name'] == name:
                    return g[u'members']
            return None
    
        def expand_to_ids(self, ids_or_gangs):
            res = []
            ls = ids_or_gangs if isinstance(ids_or_gangs, list) else [ids_or_gangs]
            for id in ls:
                members = self.get_gang(id) or [id]
                res.extend(members)
            return res
    
    
        @property
        def default_textlevel(self):
            return self.data.get(u'default_textlevel', u'default')  # none means "default"
    
        @property
        def trace_cmd(self):
            return self.data.get(u'trace_cmd', u'trace')
    
        @property
        def trace_args(self):
            u"""
                If out trace-command requires some extra prefixed arguments. 
                :returns: list might be empty, but never none
            """
            return self.data.get(u'trace_args', [])
    
        @property
        def file_prefix(self):
            u"""
                Prefix for trace output files
            """
            return self.data.get(u'file_prefix', u'trace_mx_')
    
        @property
        def file_postfix(self):
            u"""
                Postfix for trace output files
            """
            return self.data.get(u'file_postfix', u'.log')
        
        @property
        def file_separators(self):
            u"""
                Which separators are allowed
            """
            return self.data.get(u'file_separators', u'-_/=')
    
        @property
        def zip_prefix(self):
            u"""
                Prefix for trace output files
            """
            return self.data.get(u'zip_prefix', self.file_prefix)
    
        @property
        def zip_postfix(self):
            u"""
                Postfix for trace output files
            """
            return self.data.get(u'file_postfix', self.file_postfix)
        @property
        def debug_trace_level(self):
            return self.data.get(u'debug_trace_level', 7)
    
        @property
        def debug_trace_commands(self):
            return self.data.get(u'debug_trace_commands', 7)
    
        @property
        def debug_trace_output(self):
            v = self.data.get(u'debug_trace_output')
            return v is not v is None or self.debug_trace_output
    
    ##----- End settings.py ------------------------------------------------------##
    return locals()

@modulize(u'command_generator')
def _command_generator(__name__):
    ##----- Begin command_generator.py -------------------------------------------##
    from parse_display import ParseDisplayOutput
    from tools import trace
    from settings import Settings
    import sys
    
    class CommandGenerator(object):
    
        def __init__(self, display_output, settings):
            self.display_output = display_output
            self.mx_version = self.display_output.version
            self.settings = settings
            pass
    
        @property
        def trace_cmd(self):
            return self.settings.trace_cmd
        @property
        def trace_prefix_args(self):
            return self.settings.trace_args
    
        @staticmethod
        def get_cmd_add_individual(name, lim):
            lim_switch = [] if lim is None else [u'-lim', lim]
            return lim_switch + [u'-unit', name]
    
        @staticmethod
        def get_cmd_remove_individual(name):
            return [u'-remove', name]
    
        @staticmethod
        def get_cmd_set_textlevel(n, textlevel = u'normal'):
            return [u'-modify', n, u'-textlevel', textlevel]
            
        @staticmethod
        def get_cmd_start(n_list):
            return [u'-start', u",".join(n_list) ]
        @staticmethod
        def get_cmd_stop(n_list):
            return [u'-stop', u",".join(n_list) ]
        @staticmethod
        def get_cmd_clear(n_list):
            return [u'-clear', u",".join(n_list) ]
        
        @staticmethod
        def get_cmd_print(unit_id):
            return [u'-print', unit_id ]
    
        def expand_names(self, name_or_list):
            def expand_ranges(ls):
                res = []
                for s in ls:
                    for s2 in s.split(u','):
                        dash = s2.find(u'-')
                        if dash > 0:
                            n1 = s2[:dash]
                            n2 = s2[dash+1:]
                            r = list(imap( unicode, xrange(int(n1), int(n2)+1)))
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
    
        def get_ids_of(self, name_or_list):
            res = []
            for name in self.expand_names(name_or_list):
                ind = self.display_output.get_individual(name)
                if ind is None:
                    trace(2, u"Unknown unit '" + name + u"', ignored")
                    continue
                res.append(ind.id)
    
            return res
    
        def add_indv(self, name, lim = u"1", extra_args = []):
            res = []
            for member in self.settings.expand_to_individuals(name):
                if self.display_output.get_individual(member) is None:               
                    res.append(CommandGenerator.get_cmd_add_individual(member, lim) + extra_args)
    
            return res
    
        def remove(self, name):
            res = []
            for member in self.settings.expand_to_individuals(name):
                if self.display_output.get_individual(member) is None:               
                    res.append(CommandGenerator.get_cmd_remove_individual(member))
    
            return res
    
        def set_textlevel(self, name, textlevel = u'normal'):
            res = []
            
            for member in self.settings.expand_to_individuals(name):
                indv = self.display_output.get_individual(member)
                if indv is None:
                    trace(2, u"Unknown gang-member '" + member + u"' Textlevel not changed")
                    continue
                id = indv.id
                res.append(CommandGenerator.get_cmd_set_textlevel(id, textlevel))
            
            return res 
    
    
        def start(self, name):
            ids = self.get_ids_of(name)
            return imap(lambda i: self.get_cmd_start(i), ids)
    
        def stop(self, name):
            ids = self.get_ids_of(name)
            return imap(lambda i: self.get_cmd_stop(i), ids)
    
        def clear(self, name):
            ids = self.get_ids_of(name)
            return imap(lambda i: self.get_cmd_clear(i), ids)
    
    
        ### Returns a list of tuples(print-cmd, target-filename)
        def save_cmd(self, names, prefix = u"", postfix = u".log", ):
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
                sep = u'_'
    
            res = []
    
            for name in self.expand_names(names):
                id = self.display_output.get_id(name)
                if id is None:
                    trace(2, u"print_cmd: unknown unit " + name + u", not printed", file=sys.stderr)
                    continue
                res.append(gen_tuple(name, id))
            return res
    
        ### Returns a list print-cmd
        def print_cmd(self, names):
            res = []
    
            for name in names:
                id = self.display_output.get_id(name)
                if id is None:
                    trace(2, u"print_cmd: unknown unit " + name + u", not printed", file=sys.stderr)
                    continue
                cmd = CommandGenerator.get_cmd_print(id)
                res.append(cmd)
            return res
    
    ##----- End command_generator.py ---------------------------------------------##
    return locals()

@modulize(u'executor')
def _executor(__name__):
    ##----- Begin executor.py ----------------------------------------------------##
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
            return self.result.decode() if isinstance(self.result, str) else self.result
    
    
    ##----- End executor.py ------------------------------------------------------##
    return locals()

@modulize(u'main')
def _main(__name__):
    ##----- Begin main.py --------------------------------------------------------##
    #!/usr/bin/python
    
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
    
    class Main(object):
    
        help_str = \
    u"""
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
    
        def __init__(self, program_name, argv, settings = None):
            self.command_line = CommandLineParser(program_name, argv)
            self.settings = settings or Main.find_settings(self.command_line.settings_file)
            self.parsed_display = u'ParseDisplayOutput' = None # ("")
            self.command_generator = CommandGenerator(self.parsed_display, self.settings)
    
        def set_parsed_display(self, val):
            self.parsed_display = val
            self.command_generator = CommandGenerator(val, self.settings)
    
        def execute(self, args):        
            return Executor(self.settings.trace_cmd, self.settings.trace_args + args, trace_cmd_level=self.settings.debug_trace_commands)
    
        def execute_all(self, list_of_args):
            if not isinstance(list_of_args, list): raise ValueError(u"args should be list of command-line-lists, was just " + unicode(type(list_of_args)))
            if not isinstance(list_of_args[0], list): raise ValueError(u"args should be list of command-line-lists, was just " + unicode(type(list_of_args)))
    
            return u"\n".join([self.execute(arg).str_result for arg in list_of_args])
    
    
        @staticmethod 
        def find_settings(file = None):
            ex = None
            files = [
                file,            
                os.path.join( os.path.dirname(os.path.realpath(__file__)), u'settings.json'),
                os.path.join( os.path.expanduser(u"~"), u'.mx-trace', u'settings.json'),
                os.path.join( os.path.expanduser(u"~"), u'.mx-trace.json')
            ] 
            for f in files:
                if not f is None and os.path.exists(f):
                    try:
                        return Settings(f)
                    except BaseException, ex:
                        trace(3, u"Failed to open settings from " + f + u": " + unicode(ex))                    
    
            trace(3, u"Failed to open settings from any known file " + u"\n   " + u"\n   ".join(files) )
            return Settings(u"{\n}") # Return empty settings
                
    
        def main(self):
            trace(7, u"main method: " + self.command_line.program_name + u" args: [ " + u", ".join(self.command_line.original_args)+ u" ]")
    
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
                trace(3, u"display " + u" ".join(display_args), file=sys.stderr)
                self.call_display(display_args + self.command_line.display_extra_args().argv)
                print self.parsed_display
                return
    
            add_args = self.command_line.add
            if not add_args is None:
                trace(3, u"add " + u" ".join(add_args))
                self.call_display()
                add_extra_args = self.command_line.add_extra_args().argv
                self.call_add(add_args.split(u','), self.command_line.lim, self.command_line.textlevel or self.settings.default_textlevel, add_extra_args)
                return
    
            remove_args = self.command_line.remove
            if not remove_args is None:
                trace(3, u"remove " + u" ".join(remove_args))
                self.call_display()
                remove_extra_args = self.command_line.remove_extra_args().argv
                self.call_remove(remove_args.split(u','), remove_extra_args)
                return
    
    
            start_args = self.command_line.start
            if not start_args is None:
                trace(3, u"start " + u" ".join(start_args))
                self.call_display()
                start_extra_args = self.command_line.start_extra_args().argv
                self.call_start(start_args.split(u','), self.command_line.lim, self.command_line.textlevel or self.settings.default_textlevel, start_extra_args)
                return
    
            stop_args = self.command_line.stop
            if not stop_args is None:
                trace(3, u"stop " + u" ".join(stop_args))
                self.call_display()
                self.call_stop(stop_args.split(u','), self.command_line.stop_extra_args().argv)
                return
    
            print_args = self.command_line.print_args
            if not print_args is None:
                trace(3, u"print " + print_args)
                self.call_display()
                extra_args = self.command_line.print_extra_args().argv
                printout = self.call_print([print_args], extra_args)
                print printout
                return printout
    
            save_args = self.command_line.save
            if not save_args is None:
                prefix=self.command_line.file_prefix or self.settings.save_prefix
                postfix=self.command_line.file_postfix or self.settings.save_postfix
                trace(3, u"save " + save_args , u", prefix=" , prefix , u", postfix=" , postfix)
                self.call_display()
                self.call_save(save_args.split(u','), prefix, postfix)
                return
    
            zip_args = self.command_line.zip
            if not zip_args is None:
                prefix = self.command_line.file_prefix or self.settings.zip_prefix
                postfix = self.command_line.file_postfix or self.settings.zip_postfix
                zip_file = zip_args[0]
                _ignored , file_extension = os.path.splitext(zip_file)
                if len(file_extension) == 0:
                    zip_file = zip_file.rstrip(u'.') + u'.zip' 
                individuals = zip_args[1:]
                trace(3, u"zip ", individuals, u" to ", zip_file , u", prefix=" , prefix , u", postfix=" , postfix)
                self.call_display()
                self.call_zip(individuals, zip_file, prefix, postfix)
                return
    
            trace(2, u'Unknown command, calling trace verbatim for all individuals')
            self.call_display()
            self.call_unknown_command()
            return
    
        def expand_to_ids(self, ids_or_gangs):
            if isinstance(ids_or_gangs, unicode): # Handle if list forgotten
                ids_or_gangs = [ids_or_gangs]
            list_of_lists = [ iog.split(u',') for iog in ids_or_gangs]
            ids_or_gangs =  [val for sublist in list_of_lists for val in sublist]
    
            if len(ids_or_gangs) == 0 or ids_or_gangs[0].lower() == u'all':
                return [unicode(indv) for indv in self.parsed_display.individuals]
            else:
                return self.settings.expand_to_ids(ids_or_gangs)
    
        def get_existing_ids(self, id_names):
            return imap( lambda indv: indv.id, self.get_existing_indivuduals(id_names))
            # if len(id_names) == 0 or id_names[0].lower() == 'all':
            #     id_names = [str(indv) for indv in self.parsed_display.individuals]
            # else:
            #     id_names = self.settings.expand_to_ids(id_names)
            # return list(filter(lambda id: not self.parsed_display.get_individual(id) is None, id_names))
    
        def get_existing_indivuduals(self, id_names):
            if len(id_names) == 0 or id_names[0].lower() == u'all':
                id_names = [unicode(indv) for indv in self.parsed_display.individuals]
            else:
                id_names = self.settings.expand_to_ids(id_names)
            individuals = imap(lambda id: self.parsed_display.get_individual(id), id_names)
            return [x for x in individuals if x is not None]
            #return list(filter(lambda indv: not self.parsed_display.get_individual(id) is None, id_names))
    
        def get_non_existing_individuals(self, id_names):
            if len(id_names) == 0 or id_names[0].lower() == u'all':
                id_names = [unicode(indv) for indv in self.parsed_display.individuals]
            else:
                id_names = self.settings.expand_to_ids(id_names)
            return list(ifilter(lambda id: self.parsed_display.get_individual(id) is None, id_names))
    
        def ensure_individuals_exists(self, id_names, lim, textlevel, extra_args):
            self.add_individuals(self.get_non_existing_individuals(id_names), lim, textlevel, extra_args)
     
        def call_display_gangs(self):        
            res = u"\n".join( [ (g[u'name'] + u": " + u", ".join(g[u'members'])) for g in self.settings.gangs])
            print res
            return res
    
    
        def call_display_settings(self):
            print self.settings.raw_data
            return self.settings.raw_data
    
        def call_help(self):
            print Main.help_str
            return Main.help_str
    
        def call_display(self, args = []):
            disp_output = self.execute([u'-display'] + args).str_result
            self.set_parsed_display(ParseDisplayOutput(disp_output))
    
    
        def add_individuals(self, individuals, lim, textlevel, extra_args):
            trace(4, u"Adding individuals ", individuals)
            self.execute_all(self.command_generator.add_indv(individuals, lim, extra_args))
    
            self.call_display()
    
            for id in individuals:
                indv = self.parsed_display.get_individual(id)
                if indv is None:
                    trace(2, u'Failed to create induvidual ' + id)
                    sys.exit(17)
                if indv.textlevel != textlevel:
                    self.execute_all(self.command_generator.set_textlevel(id, textlevel))
                
        def call_add(self, args, lim, textlevel, extra_args = []):
            if self.parsed_display is None:
                raise ValueError(u"Called start when no display parser yet!")
            individuals = self.expand_to_ids(args)
            self.ensure_individuals_exists(individuals, lim, textlevel, extra_args)
    
        def call_remove(self, args, extra_args = []):
            if self.parsed_display is None:
                raise ValueError(u"Called start when no display parser yet!")
            existing = self.get_existing_ids(self.expand_to_ids(args))
            remove_cmds = self.command_generator.remove(existing)
            for indv_stop in remove_cmds:
                self.execute(indv_stop + extra_args)
        
        def call_start(self, args, lim, textlevel, extra_args = []):
            self.call_add(args, lim, textlevel)
            individuals = self.expand_to_ids(args)
            start_cmds = self.command_generator.start(individuals)
            for indv_start in start_cmds:
                self.execute(indv_start + extra_args)
        
        def call_stop(self, args, extra_args = []):
            if self.parsed_display is None:
                raise ValueError(u"Called stop when no display parser yet!")
            individuals = self.expand_to_ids(args)
            existing = self.get_existing_ids(individuals)
            stop_cmds = self.command_generator.stop(existing)
            for indv_stop in stop_cmds:
                self.execute(indv_stop + extra_args)
    
        def call_print(self, args, extra_args = []):
            if self.parsed_display is None:
                raise ValueError(u"Called print when no display parser yet!")
            individuals = self.expand_to_ids(args)
            existing = ifilter(lambda id: not self.parsed_display.get_individual(id) is None, individuals)        
            print_cmds = self.command_generator.print_cmd(existing)
            return self.execute_all(print_cmds + extra_args)
        
        def call_save(self, args, prefix, postfix, extra_args = []):
            if self.parsed_display is None:
                raise ValueError(u"Called print when no display parser yet!")
            individuals_names = self.expand_to_ids(args)
            individuals = imap(lambda id: self.parsed_display.get_individual(id), individuals_names)
            
            existing_individuals = self.get_existing_ids(individuals)
            
            # extra_args = self.command_line.get_non_save()
    
            for indv in existing_individuals:
                (print_cmd, filename) = self.command_generator.save_cmd([indv.unit_name], prefix, postfix)[0]        
                trace(3, u'printing ' + indv.id + u"/" + indv.unit_name + u" to " + filename)
                ex = self.execute(print_cmd)
                with io.open(filename, u"w", encoding=u"latin-1") as fil:
                    fil.write(ex.str_result + extra_args)
                
        def call_zip(self, args, zipfilename, prefix, postfix, extra_args = []):
            if not isinstance(args, list): 
                raise ValueError(u'Should be called with list of individuals')
            if self.parsed_display is None:
                raise ValueError(u"Called print when no display parser yet!")
            individuals_names = self.expand_to_ids(args)
            
            existing_individuals = self.get_existing_indivuduals(individuals_names)
            
            # extra_args = self.command_line.get_non_zip()
    
            with zipfile.ZipFile(zipfilename, u"w") as z:
                for indv in existing_individuals:
                    (print_cmd, filename) = self.command_generator.save_cmd([indv.unit_name], prefix, postfix)[0]        
                    trace(3, u'printing ' + indv.id + u"/" + indv.unit_name + u" to " + filename)
                    ex = self.execute(print_cmd)
                    
                    z.writestr(filename, ex.result)
    
            trace(5, u"Wrote to " + zipfilename)
            try:
                trace(5, u"Size became " + unicode(os.path.getsize(zipfilename)))
            except:
                trace(1, u"Failed to save data to " + zipfilename)
    
        
        def expand_first_gang_in_commandline(self, args):
            for i, a in enumerate(args):
                expanded = self.expand_to_ids(a)
                if len(expanded) > 1:                
                    pre = args[:i] if i > 0 else []
                    post = args[i+1:] if i+1 < len(args) else []
                    return [ pre + [indv] + post for indv in expanded ]
            return [args]
    
        
    
        def call_unknown_command(self):
            def find_gang():
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
    
    if __name__ == u"__main__":
        Main(sys.argv[0], sys.argv[1:]).main()
    
    ##----- End main.py ----------------------------------------------------------##
    return locals()
