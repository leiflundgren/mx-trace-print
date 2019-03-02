import json
import io
import tools

class Settings:

    def __init__(self, settings_file):                
        if isinstance(settings_file, io.TextIOBase):
            self.data = json.load(settings_file)
        elif isinstance(settings_file, str) and settings_file.count('\n') > 1:
            self.data = json.load(io.StringIO(settings_file))
        elif isinstance(settings_file, str):
            with tools.open_file(settings_file) as f:
                self.data = json.load(f)



    def get_gang(self, name) -> [str] :
        gangs_list = self.data['gangs']
        for g in gangs_list:
            if g['name'] == name:
                return g['members']

    