import unittest

import trace_mockup 

class TestMockup(unittest.TestCase):

    def test_display(self):
        trace_mockup.TraceMockup(['fake_progname', '-display', '-mxver', '7'])


    pass

if __name__ == '__main__':
    unittest.main()

    