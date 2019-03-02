from parse_display import ParseDisplayOutput

class CommandGenerator:

    def __init__(self, display_output:ParseDisplayOutput, settings:'Settings'):
        self.display_output = display_output
        self.mx_version = self.display_output.version
        self.settings = settings
        pass

    @staticmethod
    def add_individual(name:str) -> str:
        return 'trace -lim 1 -unit {unit}'.format(unit=name)
    
    def add_gang(self, name:str) -> [str]:
        res = []
        gang = self.settings.get_gang(name)
        for member in gang:
            if self.display_output.get_individual(member) is None:
                res.append(self.add_individual(member))

        return res