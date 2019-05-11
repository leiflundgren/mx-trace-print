
from __future__ import absolute_import
import os
from io import StringIO
import sys
from contextlib import contextmanager

PACKAGE_PARENT = u'..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwdu(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import settings

@contextmanager
def captured_output(capture_stdout = True, capture_stderr = True):
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        if capture_stdout:
            sys.stdout = new_out
        if capture_stderr:
            sys.stderr = new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestSettings(settings.Settings):

    def __init__(self, settings_json):
        settings.Settings.__init__(self, settings_json)
        self.call_count = 0


    @property
    def trace_args(self):
        args = super(TestSettings, self).trace_args
        self.call_count = 1+self.call_count
        return args + [u'-call-count', unicode(self.call_count) ]