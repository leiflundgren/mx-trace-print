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
            trimmed = Settings.trim_json_comments(settings_file)
            self.data = json.load(io.StringIO(trimmed))
            tools.tracelevel = self.debug_trace_level
        elif isinstance(settings_file, str):
            with tools.open_read_file(settings_file) as f:
                self.__init__(f.read())
                return

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

    def get_gang(self, name) -> [str]:
        gangs_list = self.data['gangs']
        for g in gangs_list:
            if g['name'] == name:
                return g['members']
        return None

    def expand_to_individuals(self, ids_or_gangs:[str]) -> str:
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
    def save_prefix(self) -> str:
        """
            Prefix for trace output files
        """
        return self.data.get('save_prefix', 'trace_mx_')

    @property
    def save_postfix(self) -> str:
        """
            Postfix for trace output files
        """
        return self.data.get('save_postfix', '.log')
    
    @property
    def save_separators(self) -> str:
        """
            Which separators are allowed
        """
        return self.data.get('save_separators', '-_/=')

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
