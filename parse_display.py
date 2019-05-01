import io
import tools

class ParseDisplayOutput:

    class Individual:
        def __init__(self, dict) -> None:
            self.dict = dict
        def __str__(self) -> str:
            return "{id}: {name} {state}".format(id=self.id, name=self.unit_name, state=self.state)

        def get(self, attrName) -> str:
            val = self.dict.get(attrName)
            return ( None if val is None else val.strip() )

        @property
        def is_header(self) -> bool:
            return self.dict.find('Version') is not None

        @property
        def id(self) -> str:
            return self.get('Trace ind')

        @property
        def state(self) -> str:
            return self.get('State')
        @property
        def stored(self) -> str:
            return self.get('Stored')
        @property
        def size(self) -> str:
            return self.get('Size per lim')
     
        @property
        def trace_type(self) -> str:
            return self.get('Type')
        @property
        def rotating(self) -> str:
            return self.get('Rotating')
        @property
        def textlevel(self) -> str:
            return self.get('Textlevel')
        @property
        def lim(self) -> str:
            return self.get('Lim no')
        @property
        def unit_no(self) -> str:
            return self.get('Unit no')
        @property
        def unit_name(self) -> str:
            return self.get('Unit name')
        @property
        def time_mark(self) -> str:
            return self.get('Time mark')
        @property
        def by_user(self) -> str:
            return self.get('by user')
        # @property
        # def (self) -> str:
        #     return self.dict[''].strip()
                    

    def __init__(self, source) -> None:
        self.source = tools.read(source)
        if isinstance(self.source, str):
            self.source = self.source.splitlines()

        parts = [] #List[str] 
        self.individuals  = [] # List['ParseDisplayOutput.Individual'] 

        in_header = True
        for line in self.source:
            line = line.strip()
            
            ## skip header, until a line starts with Version
            if in_header:
                if line.startswith('Version'):
                    in_header = False
                else:
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

    def __str__(self) -> str:
        return  "\n".join( [str(i) for i in self.individuals ] )

    @property
    def is_valid(self) -> bool:
        return not self.individuals is None

    @property
    def first_trace(self) -> str:
        return self.individuals[0].get('First')
    @property
    def last_trace(self) -> str:
        return self.individuals[0].get('Last')


    def get_individual(self, id) -> 'Individual':
        if isinstance(id, int):
            return self.individuals[id] if id < len(self.individuals) else None
        for ind in self.individuals[1:]: # Avoid header
            if ind.id == id or ind.unit_name == id:
                return ind
        return None

    ### convenience method that returns the id of Individual matching unitname, or None
    def get_id(self, unitname) -> str:
        ind = self.get_individual(unitname)
        return ind.id if not ind is None else None

    ## Trace ind:  3, State: setup       , Stored:      0, Size per lim: 5000,  Type     : unit-trace      , Rotating: on , Textlevel: all, Lim no   :   1, Unit no: 0206, Unit name: CMP , Time mark: 2018-12-13 16:46:11 (CET), by user: mxone_admin
    @staticmethod
    def parse_individual(parts) -> 'Individual':
        d = dict(map(str.strip, itm.split(':', 1)) for itm in parts)
        return ParseDisplayOutput.Individual(d) if len(d) > 0 else None
