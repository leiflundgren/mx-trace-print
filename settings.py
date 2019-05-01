import json
import io
import tools
import os.path
import re

class Settings:

    def __init__(self, settings_file):
        if isinstance(settings_file, io.TextIOBase):
            self.__init__(settings_file.read())
            return
        elif isinstance(settings_file, str) and (settings_file.count('\n') > 1 or not os.path.exists(settings_file) ):
            self.raw_data = settings_file
            trimmed = Settings.trim_json_comments(settings_file)
            self._set_data_object(json.load(io.StringIO(trimmed)))
            tools.tracelevel = self.debug_trace_level
        elif isinstance(settings_file, str):
            with tools.open_read_file(settings_file) as f:
                self.__init__(f.read())
                return

    def _set_data_object(self, data_dict):
        self.data = data_dict
        self.add_default('default_textlevel', 'default')  # none means "default"
        self.add_default('trace_cmd', 'trace')
        self.add_default('trace_args', [])
        self.add_default('file_prefix', 'trace_mx_')
        self.add_default('file_postfix', '.log')
        self.add_default('file_separators', '-_/=')
        self.add_default('zip_prefix', self.file_prefix)
        self.add_default('file_postfix', self.file_postfix)
        self.add_default('debug_trace_level', 7)
        self.add_default('debug_trace_commands', 7)
        self.add_default('debug_trace_output', 7)
        if not 'gangs' in self.data:
            self.data['gangs'] = {
                "usual": ["SIPLP", "RMP", "CMP"],
                "csta": ["CSTServer", "ISUS", "CMP", "RMP", "SIPLP"]
            }

    def add_default(self, setting:str, value):
        if setting not in self.data:
            self.data[setting] = value

    @staticmethod
    def trim_json_comments(data_string):
        result = []
        for line in data_string.split("\n"):
            stripped = line.strip()
            if len(stripped) < 1 or stripped[0:2] == "//":
                line = "" # remove
            elif line[-1] not in r"\,\"\'":
                line = re.sub(r"\/\/.*?$", "", line)
            result.append(line)
        return "\n".join(result)

    @property
    def gangs(self) -> {}:
        return self.data['gangs']

    def get_gang(self, name) -> [str]:
        return self.gangs.get(name, None)

    def expand_to_ids(self, ids_or_gangs:[str]) -> str:
        res = []
        ls = ids_or_gangs if isinstance(ids_or_gangs, list) else [ids_or_gangs]
        for id in ls:
            members = self.get_gang(id) or [id]
            res.extend(members)
        return res


    @property
    def default_textlevel(self) -> str:
        return self.data.get('default_textlevel', 'default')  # none means "default"

    @property
    def trace_cmd(self) -> str:
        return self.data.get('trace_cmd', 'trace')

    @property
    def trace_args(self) -> [str]:
        """
            If out trace-command requires some extra prefixed arguments. 
            :returns: list might be empty, but never none
        """
        return self.data.get('trace_args', [])

    @property
    def file_prefix(self) -> str:
        """
            Prefix for trace output files
        """
        return self.data.get('file_prefix', 'trace_mx_')

    @property
    def file_postfix(self) -> str:
        """
            Postfix for trace output files
        """
        return self.data.get('file_postfix', '.log')
    
    @property
    def file_separators(self) -> str:
        """
            Which separators are allowed
        """
        return self.data.get('file_separators', '-_/=')

    @property
    def zip_prefix(self) -> str:
        """
            Prefix for trace output files
        """
        return self.data.get('zip_prefix', self.file_prefix)

    @property
    def zip_postfix(self) -> str:
        """
            Postfix for trace output files
        """
        return self.data.get('file_postfix', self.file_postfix)
    @property
    def debug_trace_level(self) -> int:
        return self.data.get('debug_trace_level', 7)

    @property
    def debug_trace_commands(self) -> int:
        return self.data.get('debug_trace_commands', 7)

    @property
    def debug_trace_output(self) -> int:
        v = self.data.get('debug_trace_output')
        return v is not v is None or self.debug_trace_output
