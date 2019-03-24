
class CommandLineParser:
    def __init__(self, program_name, args):
        self.program_name = program_name
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
    def help(self) -> bool:
        return 'help' in self.args or 'h' in self.args

    @property
    def display(self) -> []:
        return self.args.get('display', None)
