from unittest import TestCase

from versions.compat import basestring


class TestBaseString(TestCase):

    def test(self):
        self.assertTrue(isinstance('foo', basestring))
        self.assertTrue(isinstance(u'foo', basestring))
        self.assertFalse(isinstance(42, basestring))
