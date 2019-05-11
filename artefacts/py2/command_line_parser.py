
class CommandLineParser(object):
    def __init__(self, arg ):
        self.program_name = arg[0]
        self.original_args = arg
        self.argv = arg[1:]

    def get_args(self, name, default_value = None):
        return CommandLineParser.get_argument(name, self.argv, default_value)

    def get_arg(self, name, default_value = None):
        arg = self.get_args(name, default_value)
        return None if arg is None or len(arg) == 0 else arg[0]
    
    def has_arg(self, name, default_value = None):
        arg_ls = self.get_args(name, default_value)
        return not arg_ls is None

    def replace_arg(self, name, val):
        argv = CommandLineParser.replace_argument(name, self.argv, val)
        return CommandLineParser([self.program_name] + argv)

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
        (start,stop, _args) = CommandLineParser.find_arg_index(name, argv)
        if start < 0:
            return argv
        
        pre = argv[:start] if start > 0 else []
        post = argv[stop+1:] if stop+1 < len(argv) else []
        if val is None or len(val) == 0:
            return pre + post
        else:
            return pre + [val] + post

    def set_program_name(self, new_name):
        return CommandLineParser([new_name] + self.argv[1:])
  
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
        return self.remove_arg(u'print', u'lim')

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

