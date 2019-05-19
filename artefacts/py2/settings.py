from __future__ import with_statement
from __future__ import absolute_import
import json
import io
import tools
import os.path
import re

class Settings(object):

    def __init__(self, settings_file):
        if isinstance(settings_file, io.TextIOBase):
            self.__init__(settings_file.read())
            return
        elif isinstance(settings_file, unicode) and (settings_file.count(u'\n') > 1 or not os.path.exists(settings_file) ):
            self.raw_data = settings_file
            trimmed = Settings.trim_json_comments(settings_file)
            self._set_data_object(json.load(io.StringIO(trimmed)))
            tools.tracelevel = self.debug_trace_level
        elif isinstance(settings_file, unicode):
            with tools.open_read_file(settings_file) as f:
                self.__init__(f.read())
                return

    def _set_data_object(self, data_dict):
        self.data = data_dict
        self.add_default(u'default_textlevel', u'default')  # none means "default"
        self.add_default(u'trace_cmd', u'trace')
        self.add_default(u'trace_args', [])
        self.add_default(u'file_prefix', u'trace_mx_')
        self.add_default(u'file_postfix', u'.log')
        self.add_default(u'file_separators', u'-_/=')
        self.add_default(u'zip_prefix', self.file_prefix)
        self.add_default(u'file_postfix', self.file_postfix)
        self.add_default(u'debug_trace_level', 7)
        self.add_default(u'debug_trace_commands', 7)
        self.add_default(u'debug_trace_output', 7)
        if not u'gangs' in self.data:
            self.data[u'gangs'] = {
                u"usual": [u"SIPLP", u"RMP", u"CMP"],
                u"csta": [u"CSTServer", u"ISUS", u"CMP", u"RMP", u"SIPLP"]
            }

    def add_default(self, setting, value):
        if setting not in self.data:
            self.data[setting] = value

    @staticmethod
    def trim_json_comments(data_string):
        result = []
        for line in data_string.split(u"\n"):
            stripped = line.strip()
            if len(stripped) < 1 or stripped[0:2] == u"//":
                line = u"" # remove
            elif line[-1] not in ur"\,\"\'":
                line = re.sub(ur"\/\/.*?$", u"", line)
            result.append(line)
        return u"\n".join(result)

    @property
    def gangs(self):
        return self.data[u'gangs']

    def get_gang(self, name):
        return self.gangs.get(name, None)

    def expand_to_ids(self, ids_or_gangs):
        res = []
        ls = ids_or_gangs if isinstance(ids_or_gangs, list) else [ids_or_gangs]
        for id in ls:
            members = self.get_gang(id) or [id]
            res.extend(members)
        return res


    @property
    def default_textlevel(self):
        return self.data.get(u'default_textlevel', u'default')  # none means "default"

    @property
    def trace_cmd(self):
        return self.data.get(u'trace_cmd', u'trace')

    @property
    def trace_args(self):
        u"""
            If out trace-command requires some extra prefixed arguments. 
            :returns: list might be empty, but never none
        """
        return self.data.get(u'trace_args', [])

    @property
    def file_prefix(self):
        u"""
            Prefix for trace output files
        """
        return self.data.get(u'file_prefix', u'trace_mx_')

    @property
    def file_postfix(self):
        u"""
            Postfix for trace output files
        """
        return self.data.get(u'file_postfix', u'.log')
    
    @property
    def file_separators(self):
        u"""
            Which separators are allowed
        """
        return self.data.get(u'file_separators', u'-_/=')

    @property
    def zip_prefix(self):
        u"""
            Prefix for trace output files
        """
        return self.data.get(u'zip_prefix', self.file_prefix)

    @property
    def zip_postfix(self):
        u"""
            Postfix for trace output files
        """
        return self.data.get(u'file_postfix', self.file_postfix)
    @property
    def debug_trace_level(self):
        return self.data.get(u'debug_trace_level', 7)

    @property
    def debug_trace_commands(self):
        return self.data.get(u'debug_trace_commands', 7)

    @property
    def debug_trace_output(self):
        v = self.data.get(u'debug_trace_output')
        return v is not v is None or self.debug_trace_output
