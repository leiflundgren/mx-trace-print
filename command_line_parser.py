
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

