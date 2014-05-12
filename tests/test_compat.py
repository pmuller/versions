import sys
from unittest import TestCase

from versions.compat import basestring


class TestBaseString(TestCase):

    def test(self):
        self.assertTrue(isinstance('foo', basestring))
        self.assertFalse(isinstance(42, basestring))

        if sys.version_info[0] == 2:
            self.assertTrue(isinstance(unicode('foo'), basestring))
