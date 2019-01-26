from typing import List, Optional

class ParseDisplayOutput:

    class Individual:
        def __init__(self, dict) -> None:
            self.dict = dict

        def get(self, attrName):
            return self.dict[attrName].strip()

        @property
        def id(self):
            return self.get('Trace ind')

        @property
        def state(self):
            return self.get('State')
        @property
        def stored(self):
            return self.get('Stored')
        @property
        def size(self):
            return self.get('Size per lim')
     
        @property
        def trace_type(self):
            return self.get('Type')
        @property
        def rotating(self):
            return self.get('Rotating')
        @property
        def textlevel(self):
            return self.get('Textlevel')
        @property
        def lim(self):
            return self.get('Lim no')
        @property
        def unit_no(self):
            return self.get('Unit no')
        @property
        def unit_name(self):
            return self.get('Unit name')
        @property
        def time_mark(self):
            return self.get('Time mark')
        @property
        def by_user(self):
            return self.get('by user')
        # @property
        # def (self):
        #     return self.dict[''].strip()
                    

    def __init__(self, source) -> None:
        self.source = source
        self.individuals : List[ParseDisplayOutput.Individual] = [] 
        parts : List[str] = []

        for line in self.source:
            line = line.strip()
            
            ## skip header if there
            if line.endswith( 'trace -display'):
                continue

            if line.startswith('Version'):
                mpos = line.index(', Market:')
                self.version = line[8:mpos].strip()
                self.market = line[mpos+9:].strip()
                continue
        
            if line.startswith('First'):
                last = line.find('Last:')-1
                while last > 0 and line[last] == ' ':
                    last=last-1
                if last>0 and line[last] != ',':
                    line = line[:last+1] + ',' + line[last+1:]
            
            if len(line) > 0 :
                parts.extend(map(str.strip, line.split(',')))
            else:
                individual = self.parse_individual(parts)
                if individual is not None:
                    self.individuals.append(individual)
                parts = []
        
    @property
    def first_trace(self):
        return self.individuals[0].get('First')
    @property
    def last_trace(self):
        return self.individuals[0].get('Last')

    def get_individual(self, id:str) -> ParseDisplayOutput.Individual:
        return next((ind for ind in self.individuals if ind.id == id), None)

    ## Trace ind:  3, State: setup       , Stored:      0, Size per lim: 5000,  Type     : unit-trace      , Rotating: on , Textlevel: all, Lim no   :   1, Unit no: 0206, Unit name: CMP , Time mark: 2018-12-13 16:46:11 (CET), by user: mxone_admin
    @staticmethod
    def parse_individual(parts) -> dict:
        d = dict(map(str.strip, itm.split(':', 1)) for itm in parts)
        return ParseDisplayOutput.Individual(d) if len(d) > 0 else None
