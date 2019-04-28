
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
    def save_prefix(self) -> str:
        return self.get_arg('prefix')
    @property
    def save_postfix(self) -> str:
        return self.get_arg('postfix')
    def save_extra_args(self) -> 'CommandLineParser' :
        return self.remove_arg('save').remove_arg('prefix').remove_arg('postfix')

    @property
    def zip(self) -> str:
        return self.get_arg('zip')
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

