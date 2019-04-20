
class CommandLineParser:
    def __init__(self, program_name:str, argv:[str] ):
        self.program_name = program_name
        self.original_args = argv
        self.argv = argv
   
    def get_arg(self, name:str, default_value:str = None) -> [str]:
        return CommandLineParser.get_argument(name, self.argv, default_value)

    def replace_arg(self, name:str, val:[str]) -> 'CommandLineParser':
        return CommandLineParser(self.program_name, CommandLineParser.replace_argument(name, self.argv, val))

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
    def get_argument(name:str, argv:[str], default_value:str = None) -> [str]:
        """ Gets the arguments to switch 'name' as a list.
        return: None is not found, otherwise a list. (If name is found but has no arguments, an empty list is returned.) """
        (_start,_stop, args) = CommandLineParser.find_arg_index(name, argv)
        return args if not args is None else default_value

    @staticmethod
    def replace_argument(name:str, argv:[str], val:[str]) -> [str]:
        """ 
            Replaces switch 'name' with the supplied list. 
            :param val:
                list to have no arguments, 
                None to remove the switch all together
            :returns: the updated arguments
        """
        (start,stop, args) = CommandLineParser.find_arg_index(name, argv)
        if start < 0:
            pass
        elif val is None:
            del(args[start:stop])
        else:
            args[start:stop] = val
        return args


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
        return (
                not self.get_arg('help') is None 
                or not self.get_arg('h') is None
        )

    @property
    def display(self) -> []:
        return self.get_arg('display')

    @property
    def lim(self) -> str:
        return self.get_arg('lim')
    @property
    def unit(self) -> str:
        return self.get_arg('unit')
    @property
    def start(self) -> str:
        return self.get_arg('start')
    @property
    def stop(self) -> str:
        return self.get_arg('stop')
    @property
    def print(self) -> str:
        return self.get_arg('print')

    @property
    def print_prefix(self) -> str:
        return self.get_arg('prefix')
    @property
    def print_postfix(self) -> str:
        return self.get_arg('postfix')
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

