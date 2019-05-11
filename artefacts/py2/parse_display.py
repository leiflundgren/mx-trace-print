from __future__ import absolute_import
import io
import tools
from itertools import imap

class ParseDisplayOutput(object):

    class Individual(object):
        def __init__(self, dict):
            self.dict = dict
        def __str__(self):
            return u"{id}: {name} {state}".format(id=self.id, name=self.unit_name, state=self.state)

        def get(self, attrName):
            val = self.dict.get(attrName)
            return ( None if val is None else val.strip() )

        @property
        def is_header(self):
            return self.dict.find(u'Version') is not None

        @property
        def id(self):
            return self.get(u'Trace ind')

        @property
        def state(self):
            return self.get(u'State')
        @property
        def stored(self):
            return self.get(u'Stored')
        @property
        def size(self):
            return self.get(u'Size per lim')
     
        @property
        def trace_type(self):
            return self.get(u'Type')
        @property
        def rotating(self):
            return self.get(u'Rotating')
        @property
        def textlevel(self):
            return self.get(u'Textlevel')
        @property
        def lim(self):
            return self.get(u'Lim no')
        @property
        def unit_no(self):
            return self.get(u'Unit no')
        @property
        def unit_name(self):
            return self.get(u'Unit name')
        @property
        def time_mark(self):
            return self.get(u'Time mark')
        @property
        def by_user(self):
            return self.get(u'by user')
        # @property
        # def (self) -> str:
        #     return self.dict[''].strip()
                    

    def __init__(self, source):
        self.source = tools.read(source)
        if isinstance(self.source, unicode):
            self.source = self.source.splitlines()

        parts = [] #List[str] 
        self.individuals  = [] # List['ParseDisplayOutput.Individual'] 

        in_header = True
        for line in self.source:
            line = line.strip()
            
            ## skip header, until a line starts with Version
            if in_header:
                if line.startswith(u'Version'):
                    in_header = False
                else:
                    continue

            if line.startswith(u'Version'):
                mpos = line.index(u', Market:')
                self.version = line[8:mpos].strip()
                self.market = line[mpos+9:].strip()
                continue
        
            if line.startswith(u'First'):
                last = line.find(u'Last:')-1
                while last > 0 and line[last] == u' ':
                    last=last-1
                if last>0 and line[last] != u',':
                    line = line[:last+1] + u',' + line[last+1:]
            
            if len(line) > 0 :
                parts.extend(imap(unicode.strip, line.split(u',')))
            else:
                individual = self.parse_individual(parts)
                if individual is not None:
                    self.individuals.append(individual)
                parts = []

    def __str__(self):
        return  u"\n".join( [unicode(i) for i in self.individuals ] )

    @property
    def is_valid(self):
        return not self.individuals is None

    @property
    def first_trace(self):
        return self.individuals[0].get(u'First')
    @property
    def last_trace(self):
        return self.individuals[0].get(u'Last')


    def get_individual(self, id):
        if isinstance(id, int):
            return self.individuals[id] if id < len(self.individuals) else None
        for ind in self.individuals[1:]: # Avoid header
            if ind.id == id or ind.unit_name == id:
                return ind
        return None

    ### convenience method that returns the id of Individual matching unitname, or None
    def get_id(self, unitname):
        ind = self.get_individual(unitname)
        return ind.id if not ind is None else None

    ## Trace ind:  3, State: setup       , Stored:      0, Size per lim: 5000,  Type     : unit-trace      , Rotating: on , Textlevel: all, Lim no   :   1, Unit no: 0206, Unit name: CMP , Time mark: 2018-12-13 16:46:11 (CET), by user: mxone_admin
    @staticmethod
    def parse_individual(parts):
        d = dict(imap(unicode.strip, itm.split(u':', 1)) for itm in parts)
        return ParseDisplayOutput.Individual(d) if len(d) > 0 else None
