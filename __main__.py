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
