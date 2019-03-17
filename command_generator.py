from parse_display import ParseDisplayOutput
from tools import trace

class CommandGenerator:

    def __init__(self, display_output:ParseDisplayOutput, settings:'Settings'):
        self.display_output = display_output
        self.mx_version = self.display_output.version
        self.settings = settings
        pass

    @property
    def trace_cmd(self) -> str:
        return self.settings.trace_cmd

    @staticmethod
    def get_cmd_add_individual(trace_cmd:str, name:str, lim:str) -> str:
        return '{trace} -lim {lim} -unit {unit}'.format(trace=trace_cmd,unit=name, lim=lim)

    @staticmethod
    def get_cmd_set_textlevel(trace_cmd:str, n:str, textlevel:str = 'normal') -> str:
        return '{trace} -modify {n} -textlevel {textlevel}'.format(trace=trace_cmd,n=n, textlevel=textlevel)
        
    @staticmethod
    def get_cmd_start(trace_cmd:str, n_list:[str]) -> str:
        return '{trace} -start {ns}'.format(trace=trace_cmd,n=",".join(n_list))
    @staticmethod
    def get_cmd_stop(trace_cmd:str, n_list:[str]) -> str:
        return '{trace} -stop {ns}'.format(trace=trace_cmd,n=",".join(n_list))
    @staticmethod
    def get_cmd_clear(trace_cmd:str, n_list:[str]) -> str:
        return '{trace} -clear {ns}'.format(trace=trace_cmd,n=",".join(n_list))
    
    @staticmethod
    def get_cmd_print(trace_cmd:str, unit_id:str) -> str:
        return '{trace} -display {ns}'.format(trace=trace_cmd, ns=unit_id)

    def expand_names(self, name_or_list) -> [str]:
        def expand_ranges(ls:[str]) -> [str]:
            res = []
            for s in ls:
                for s2 in s.split(','):
                    dash = s2.find('-')
                    if dash > 0:
                        n1 = s2[:dash]
                        n2 = s2[dash+1:]
                        r = list(map( str, range(int(n1), int(n2)+1)))
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

    def get_ids_of(self, name_or_list) -> [str]:
        res = []
        for name in self.expand_names(name_or_list):
            ind = self.display_output.get_individual(name)
            if ind is None:
                trace(2, "Unknown unit '" + name + "', ignored")
                continue
            res.append(ind.id)

        return res

    def add(self, name:str, lim:str = "1") -> [str]:
        res = []
        gang = self.settings.get_gang(name)
        # if name is not gang, assume unit-name
        for member in gang or [name]:
            if self.display_output.get_individual(member) is None:
                res.append(CommandGenerator.get_cmd_add_individual(self.trace_cmd, member, lim))

        return res

    def set_textlevel(self, name:str, textlevel:str = 'normal') -> [str]:
        res = []
        # if name is not gang, assume unit-name
        gang = self.settings.get_gang(name) or [name]
        if gang is None:
            trace(2, "Unknown unit/gang '" + name + "' Textlevel not changed")
            return None

        for member in gang or [name]:
            ind = self.display_output.get_individual(member)
            if ind is None:
                trace(2, "Unknown gang-member '" + member + "' Textlevel not changed")
                continue
            
            res.append(CommandGenerator.get_cmd_set_textlevel(ind.id, textlevel))
        
        return res 


    def start(self, name:[str]) -> [str]:
        ids = self.get_ids_of(name)
        return map(self.get_cmd_start, ids)

    def stop(self, name:[str]) -> [str]:
        ids = self.get_ids_of(name)
        return map(self.get_cmd_stop, ids)

    def clear(self, name:[str]) -> [str]:
        ids = self.get_ids_of(name)
        return map(self.get_cmd_clear, ids)



    ### Returns a list of tuples(print-cmd, target-filename)
    def print_cmd(self, names:[str], prefix:str = "", postfix:str = ".log", ) -> [(str, str)]:
        def gen_tuple(unitname, id):
            cmd = CommandGenerator.get_cmd_print(self.trace_cmd, id)
            filename = (prefix+sep+unitname+postfix).strip(sep)
            return (cmd, filename)

        sep = '-' if prefix.find('-') >= 0 or postfix.find('-') >= 0 else '_'
        
        res = []

        for name in self.expand_names(names):
            id = self.display_output.get_id(name)
            if id is None:
                trace(2, "print_cmd: unknown unit " + name + ", not printed")
                continue
            res.append(gen_tuple(name, id))
        return res
