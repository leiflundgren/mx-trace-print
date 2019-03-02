
class CommandGenerator:

    def __init__(self, mx_version):
        self.mx_version = mx_version
        pass


    def add_individual(self, name:str) -> str:
        return 'trace -lim 1 -unit {unit}'.format(unit=name)
    