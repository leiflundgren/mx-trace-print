b'--- artefacts\\mx-trace-helper.py\t(original)'
b'+++ artefacts\\mx-trace-helper.py\t(refactored)'
b'@@ -1,11 +1,14 @@'
b'+from __future__ import with_statement'
b'+from __future__ import absolute_import'
b' import sys'
b' from types import ModuleType'
b'+from io import open'
b' '
b' class MockModule(ModuleType):'
b'     def __init__(self, module_name, module_doc=None):'
b'         ModuleType.__init__(self, module_name, module_doc)'
b"-        if '.' in module_name:"
b"-            package, module = module_name.rsplit('.', 1)"
b"+        if u'.' in module_name:"
b"+            package, module = module_name.rsplit(u'.', 1)"
b'             get_mock_module(package).__path__ = []'
b'             setattr(get_mock_module(package), module, self)'
b' '
b'@@ -24,83 +27,83 @@'
b' '
b' ##===========================================================================##'
b' '
b"-@modulize('command_line_parser')"
b"+@modulize(u'command_line_parser')"
b' def _command_line_parser(__name__):'
b'     ##----- Begin command_line_parser.py -----------------------------------------##'
b'     '
b'-    class CommandLineParser:'
b'-        def __init__(self, program_name:str, args:[str] ):'
b'+    class CommandLineParser(object):'
b'+        def __init__(self, program_name, args ):'
b'             self.program_name = program_name'
b'             self.verbatim_args = args'
b'             self.args = self.parse_command_line(args)'
b'     '
b'         @staticmethod'
b'-        def parse_command_line(argv:[str]) -> None:'
b'+        def parse_command_line(argv):'
b'             args = {}'
b'             i=1'
b'             while i < len(argv):'
b'-                if argv[i][0] == "-":'
b'-                    arg = argv[i].lstrip("-").rstrip().lower()'
b'+                if argv[i][0] == u"-":'
b'+                    arg = argv[i].lstrip(u"-").rstrip().lower()'
b'                     val = []'
b'                     i=i+1'
b'-                    while i < len(argv) and argv[i][0] != "-":'
b'+                    while i < len(argv) and argv[i][0] != u"-":'
b'                         val.append(argv[i].strip())'
b'                         i = i + 1'
b'                     args[arg] = val'
b'             return args'
b'     '
b'         @property'
b'-        def is_empty(self) -> bool:'
b'+        def is_empty(self):'
b'             return self.args.__len__() == 0'
b'     '
b'         @property'
b'-        def help(self) -> bool:'
b"-            return 'help' in self.args or 'h' in self.args"
b'-    '
b'-        @property'
b'-        def display(self) -> []:'
b"-            return self.args.get('display', None)"
b'-    '
b'-        @property'
b'-        def lim(self) -> str:'
b"-            return self.args.get('lim', None)"
b'-        @property'
b'-        def unit(self) -> str:'
b"-            return self.args.get('unit', None)"
b'-        @property'
b'-        def start(self) -> str:'
b"-            return self.args.get('start', None)"
b'-        @property'
b'-        def stop(self) -> str:'
b"-            return self.args.get('stop', None)"
b'-        @property'
b'-        def print(self) -> str:'
b"-            return self.args.get('print', None)"
b'-    '
b'-        @property'
b'-        def print_prefix(self) -> str:'
b"-            return self.args.get('prefix', None)"
b'-        @property'
b'-        def print_postfix(self) -> str:'
b"-            return self.args.get('postfix', None)"
b'-        @property'
b'-        def signo(self) -> str:'
b"-            return self.args.get('signo', None)"
b'-        @property'
b'-        def show(self) -> str:'
b"-            return self.args.get('show', None)"
b'-        @property'
b'-        def signal_from(self) -> str:'
b"-            return self.args.get('from', None)"
b'-        @property'
b'-        def signal_to(self) -> str:'
b"-            return self.args.get('to', None)"
b'-        @property'
b'-        def time_from(self) -> str:'
b"-            return self.args.get('from', None)"
b'-        @property'
b'-        def time_to(self) -> str:'
b"-            return self.args.get('to', None)"
b'+        def help(self):'
b"+            return u'help' in self.args or u'h' in self.args"
b'+    '
b'+        @property'
b'+        def display(self):'
b"+            return self.args.get(u'display', None)"
b'+    '
b'+        @property'
b'+        def lim(self):'
b"+            return self.args.get(u'lim', None)"
b'+        @property'
b'+        def unit(self):'
b"+            return self.args.get(u'unit', None)"
b'+        @property'
b'+        def start(self):'
b"+            return self.args.get(u'start', None)"
b'+        @property'
b'+        def stop(self):'
b"+            return self.args.get(u'stop', None)"
b'+        @property'
b'+        def print(self):'
b"+            return self.args.get(u'print', None)"
b'+    '
b'+        @property'
b'+        def print_prefix(self):'
b"+            return self.args.get(u'prefix', None)"
b'+        @property'
b'+        def print_postfix(self):'
b"+            return self.args.get(u'postfix', None)"
b'+        @property'
b'+        def signo(self):'
b"+            return self.args.get(u'signo', None)"
b'+        @property'
b'+        def show(self):'
b"+            return self.args.get(u'show', None)"
b'+        @property'
b'+        def signal_from(self):'
b"+            return self.args.get(u'from', None)"
b'+        @property'
b'+        def signal_to(self):'
b"+            return self.args.get(u'to', None)"
b'+        @property'
b'+        def time_from(self):'
b"+            return self.args.get(u'from', None)"
b'+        @property'
b'+        def time_to(self):'
b"+            return self.args.get(u'to', None)"
b'         # @property'
b'         # def xxx(self) -> str:'
b"         #     return self.args.get('xxx', None)"
b'@@ -130,7 +133,7 @@'
b'     ##----- End command_line_parser.py -------------------------------------------##'
b'     return locals()'
b' '
b"-@modulize('tools')"
b"+@modulize(u'tools')"
b' def _tools(__name__):'
b'     ##----- Begin tools.py -------------------------------------------------------##'
b'     import sys'
b'@@ -138,45 +141,45 @@'
b'     import os'
b'     import datetime'
b'     '
b'-    def read(file_thing) -> [str]:'
b'+    def read(file_thing):'
b'         if isinstance(file_thing, io.TextIOBase):'
b'             return file_thing.readlines()'
b'-        if isinstance(file_thing, str):'
b"-            if file_thing.count('\\n') > 0:"
b'+        if isinstance(file_thing, unicode):'
b"+            if file_thing.count(u'\\n') > 0:"
b'                 return file_thing # list-thing'
b'             else:'
b'-                with open(file_thing, "r", encoding=\'iso-8859-1\') as f:'
b'+                with open(file_thing, u"r", encoding=u\'iso-8859-1\') as f:'
b'                     return f.readlines()'
b'-        raise ValueError("Cannot read data from " + str(type(file_thing)))'
b'-    '
b'-    def open_file(name) -> io.TextIOBase:'
b'-        return open(name, "r", encoding=\'iso-8859-1\')'
b'+        raise ValueError(u"Cannot read data from " + unicode(type(file_thing)))'
b'+    '
b'+    def open_file(name):'
b'+        return open(name, u"r", encoding=u\'iso-8859-1\')'
b'     '
b'     '
b'     tracelevel = 4'
b'     log_handle = None'
b'     '
b'     def trace(level, *args):'
b'-        def fix_linendings(s: str) -> str:'
b"-            if os.linesep == '\\n':"
b'+        def fix_linendings(s):'
b"+            if os.linesep == u'\\n':"
b'                 return s'
b'             p = 0'
b'             while True:'
b"-                p = s.find('\\n', p+1)"
b"+                p = s.find(u'\\n', p+1)"
b'                 if p<0: break'
b"-                if p>0 and s[p-1] != '\\r':"
b"-                    s = s[:p] + '\\r' + s[p:]"
b"+                if p>0 and s[p-1] != u'\\r':"
b"+                    s = s[:p] + u'\\r' + s[p:]"
b'             return s'
b'     '
b'         def mystr(thing):'
b'             if isinstance(thing, (list, tuple)):'
b'                 msg = []'
b"-                prefix = ''"
b"+                prefix = u''"
b'     '
b'                 if len(thing) <= 4:'
b"-                   separator = ', '"
b"+                   separator = u', '"
b'                 else:'
b'-                   separator = (os.linesep+"   ")'
b'+                   separator = (os.linesep+u"   ")'
b'                    prefix = separator'
b'     '
b'                 for s in thing:'
b'@@ -184,28 +187,28 @@'
b'                 return prefix + separator.join(msg)'
b'     '
b'             elif isinstance(thing, datetime.datetime):'
b'-                return thing.strftime("%Y-%m-%d %H:%M:%S")'
b'+                return thing.strftime(u"%Y-%m-%d %H:%M:%S")'
b'             elif isinstance(thing, datetime.date):'
b'-                return thing.strftime("%Y-%m-%d")'
b'+                return thing.strftime(u"%Y-%m-%d")'
b'             #elif isinstance(thing, bytes):'
b"             #    return bytes.decode('utf-8')"
b'             else:'
b'                 try:'
b'-                    if isinstance(thing, bytes):'
b"-                        s = thing.decode('utf-8')"
b'+                    if isinstance(thing, str):'
b"+                        s = thing.decode(u'utf-8')"
b'                     else:'
b'-                        s = str(thing)'
b'+                        s = unicode(thing)'
b'                     s = fix_linendings(s)'
b'                     return s'
b'                 except UnicodeEncodeError:'
b"-                    return str(thing).encode('ascii', 'ignore')"
b'-                except Exception as ex:'
b"-                    return 'Failed to format thing as string caught ' + str(ex)"
b"+                    return unicode(thing).encode(u'ascii', u'ignore')"
b'+                except Exception, ex:'
b"+                    return u'Failed to format thing as string caught ' + unicode(ex)"
b'     '
b'         #if tracelevel < level:'
b'         #    return'
b'     '
b'-        msg = datetime.datetime.now().strftime("%H:%M:%S: ")'
b'+        msg = datetime.datetime.now().strftime(u"%H:%M:%S: ")'
b'         for thing in args:'
b'             msg += mystr(thing)'
b'     '
b'@@ -213,56 +216,56 @@'
b'         handle = sys.stderr if log_handle is None else log_handle'
b'     '
b'         try:'
b'-            print(msg, file=handle)'
b'+            print >>handle, msg'
b'         except UnicodeEncodeError:'
b"-            print(msg.encode('cp850', errors='replace'), file=handle)"
b'-    '
b'-    def pretty(value,htchar="\\t",lfchar="\\n",indent=0):'
b"+            print >>handle, msg.encode(u'cp850', errors=u'replace')"
b'+    '
b'+    def pretty(value,htchar=u"\\t",lfchar=u"\\n",indent=0):'
b'       if type(value) in [dict]:'
b'-        return "{%s%s%s}"%(",".join(["%s%s%s: %s"%(lfchar,htchar*(indent+1),repr(key),pretty(value[key],htchar,lfchar,indent+1))for key in value]),lfchar,(htchar*indent))'
b'+        return u"{%s%s%s}"%(u",".join([u"%s%s%s: %s"%(lfchar,htchar*(indent+1),repr(key),pretty(value[key],htchar,lfchar,indent+1))for key in value]),lfchar,(htchar*indent))'
b'       elif type(value) in [list,tuple]:'
b'-        return (type(value)is list and"[%s%s%s]"or"(%s%s%s)")%(",".join(["%s%s%s"%(lfchar,htchar*(indent+1),pretty(item,htchar,lfchar,indent+1))for item in value]),lfchar,(htchar*indent))'
b'+        return (type(value)is list andu"[%s%s%s]"oru"(%s%s%s)")%(u",".join([u"%s%s%s"%(lfchar,htchar*(indent+1),pretty(item,htchar,lfchar,indent+1))for item in value]),lfchar,(htchar*indent))'
b'       else:'
b'         return repr(value)'
b'     '
b'     ##----- End tools.py ---------------------------------------------------------##'
b'     return locals()'
b' '
b"-@modulize('settings')"
b"+@modulize(u'settings')"
b' def _settings(__name__):'
b'     ##----- Begin settings.py ----------------------------------------------------##'
b'     import json'
b'     import io'
b'     import tools'
b'     '
b'-    class Settings:'
b'+    class Settings(object):'
b'     '
b'         def __init__(self, settings_file):                '
b'             if isinstance(settings_file, io.TextIOBase):'
b'                 self.data = json.load(settings_file)'
b"-            elif isinstance(settings_file, str) and settings_file.count('\\n') > 1:"
b"+            elif isinstance(settings_file, unicode) and settings_file.count(u'\\n') > 1:"
b'                 self.data = json.load(io.StringIO(settings_file))'
b'-            elif isinstance(settings_file, str):'
b'+            elif isinstance(settings_file, unicode):'
b'                 with tools.open_file(settings_file) as f:'
b'                     self.data = json.load(f)'
b'     '
b'     '
b'     '
b'-        def get_gang(self, name) -> [str] :'
b"-            gangs_list = self.data['gangs']"
b'+        def get_gang(self, name) :'
b"+            gangs_list = self.data[u'gangs']"
b'             for g in gangs_list:'
b"-                if g['name'] == name:"
b"-                    return g['members']"
b"+                if g[u'name'] == name:"
b"+                    return g[u'members']"
b'             return None'
b'     '
b'         '
b'         @property'
b'-        def default_textlevel(self) -> str:'
b'-            return self.data.find(\'default_textlevel\') # none means "default"'
b'-    '
b'-        @property'
b'-        def trace_cmd(self) -> str:'
b"-            return self.data['trace_cmd'] or 'trace'"
b'+        def default_textlevel(self):'
b'+            return self.data.find(u\'default_textlevel\') # none means "default"'
b'+    '
b'+        @property'
b'+        def trace_cmd(self):'
b"+            return self.data[u'trace_cmd'] or u'trace'"
b'     '
b'         '
b'     ##----- End settings.py ------------------------------------------------------##'
b'@@ -277,14 +280,14 @@'
b'     from settings import Settings'
b'     from tools import trace'
b'     '
b'-    class Main:'
b'-        def __init__(self, program_name, argv:[str]) -> None:'
b'+    class Main(object):'
b'+        def __init__(self, program_name, argv):'
b'             self.command_line = CommandLineParser(program_name, argv)'
b'     '
b'         def main(self):'
b'-            trace(1, "placeholder for main method: " + self.command_line.program_name + " args: [ " + ", ".join(self.command_line.verbatim_args)+ " ]")'
b'-    '
b'-    if __name__ == "__main__":'
b'+            trace(1, u"placeholder for main method: " + self.command_line.program_name + u" args: [ " + u", ".join(self.command_line.verbatim_args)+ u" ]")'
b'+    '
b'+    if __name__ == u"__main__":'
b'         Main(sys.argv[0], sys.argv[1:]).main()'
b'     '
b'     ##----- End __main__.py ------------------------------------------------------##'
