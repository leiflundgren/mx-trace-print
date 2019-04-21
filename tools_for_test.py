
from io import StringIO
import sys
from contextlib import contextmanager

import settings

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestSettings(settings.Settings):

    def __init__(self, settings_json:str):
        settings.Settings.__init__(self, settings_json)
        self.call_count = 0


    @property
    def trace_args(self) -> [str]:
        args = super(TestSettings, self).trace_args
        self.call_count = 1+self.call_count
        return args + ['-call-count', str(self.call_count) ]