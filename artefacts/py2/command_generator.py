from __future__ import absolute_import
from parse_display import ParseDisplayOutput
from tools import trace
from settings import Settings
import sys
from itertools import imap

class CommandGenerator(object):

    def __init__(self, display_output, settings):
        self.display_output = display_output
        self.mx_version = self.display_output.version
        self.settings = settings
        pass

    @property
    def trace_cmd(self):
        return self.settings.trace_cmd
    @property
    def trace_prefix_args(self):
        return self.settings.trace_args

    @staticmethod
    def get_cmd_add_individual(name, lim):
        lim_switch = [] if lim is None else [u'-lim', lim]
        return lim_switch + [u'-unit', name]

    @staticmethod
    def get_cmd_remove_individual(name):
        return [u'-remove', name]

    @staticmethod
    def get_cmd_set_textlevel(n, textlevel = u'normal'):
        return [u'-modify', n, u'-textlevel', textlevel]
        
    @staticmethod
    def get_cmd_start(n_list):
        return [u'-start', u",".join(n_list) ]
    @staticmethod
    def get_cmd_stop(n_list):
        return [u'-stop', u",".join(n_list) ]
    @staticmethod
    def get_cmd_clear(n_list):
        return [u'-clear', u",".join(n_list) ]
    
    @staticmethod
    def get_cmd_print(unit_id):
        return [u'-print', unit_id ]

    def expand_names(self, name_or_list):
        def expand_ranges(ls):
            res = []
            for s in ls:
                for s2 in s.split(u','):
                    dash = s2.find(u'-')
                    if dash > 0:
                        n1 = s2[:dash]
                        n2 = s2[dash+1:]
                        r = list(imap( unicode, xrange(int(n1), int(n2)+1)))
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

    def get_ids_of(self, name_or_list):
        res = []
        for name in self.expand_names(name_or_list):
            ind = self.display_output.get_individual(name)
            if ind is None:
                trace(2, u"Unknown unit '" + name + u"', ignored")
                continue
            res.append(ind.id)

        return res

    def add_indv(self, name, lim = u"1", extra_args = []):
        res = []
        for member in self.settings.expand_to_ids(name):
            if self.display_output.get_individual(member) is None:               
                res.append(CommandGenerator.get_cmd_add_individual(member, lim) + extra_args)

        return res

    def remove(self, name):
        res = []
        for member in self.settings.expand_to_ids(name):
            if self.display_output.get_individual(member) is None:               
                res.append(CommandGenerator.get_cmd_remove_individual(member))

        return res

    def set_textlevel(self, name, textlevel = u'normal'):
        res = []
        
        for member in self.settings.expand_to_ids(name):
            indv = self.display_output.get_individual(member)
            if indv is None:
                trace(2, u"Unknown gang-member '" + member + u"' Textlevel not changed")
                continue
            id = indv.id
            res.append(CommandGenerator.get_cmd_set_textlevel(id, textlevel))
        
        return res 


    def start(self, name):
        ids = self.get_ids_of(name)
        return imap(lambda i: self.get_cmd_start(i), ids)

    def stop(self, name):
        ids = self.get_ids_of(name)
        return imap(lambda i: self.get_cmd_stop(i), ids)

    def clear(self, name):
        ids = self.get_ids_of(name)
        return imap(lambda i: self.get_cmd_clear(i), ids)


    ### Returns a list of tuples(print-cmd, target-filename)
    def save_cmd(self, names, prefix = u"", postfix = u".log", ):
        def gen_tuple(unitname, id):
            cmd = CommandGenerator.get_cmd_print(id)
            filename = (prefix+sep+unitname+postfix).strip(sep)
            return (cmd, filename)
        
        if self.settings.file_separators.find(prefix[-1]) >= 0:
            sep = prefix[-1]
            prefix = prefix[:-1]
        elif self.settings.file_separators.find(postfix[0]) >= 0:
            sep = postfix[0]
            postfix = postfix[1:]
        else:
            sep = u'_'

        res = []

        for name in self.expand_names(names):
            id = self.display_output.get_id(name)
            if id is None:
                trace(2, u"print_cmd: unknown unit " + name + u", not printed", file=sys.stderr)
                continue
            res.append(gen_tuple(name, id))
        return res

    ### Returns a list print-cmd
    def print_cmd(self, names):
        res = []

        for name in names:
            id = self.display_output.get_id(name)
            if id is None:
                trace(2, u"print_cmd: unknown unit " + name + u", not printed", file=sys.stderr)
                continue
            cmd = CommandGenerator.get_cmd_print(id)
            res.append(cmd)
        return res
