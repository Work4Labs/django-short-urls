from __future__ import unicode_literals

from django.utils import unittest

from django_short_urls.models import Link


class ValidRandomShortPathsTestCase(unittest.TestCase):
    def test(self):
        self.assertEqual(Link.is_valid_random_short_path("ab2cd"), True)
        self.assertEqual(Link.is_valid_random_short_path("ab2"), True)
        self.assertEqual(Link.is_valid_random_short_path("a234r434g43gb32r"), True)
        self.assertEqual(Link.is_valid_random_short_path("4a"), True)

        self.assertEqual(Link.is_valid_random_short_path("abcd"), False)
        self.assertEqual(Link.is_valid_random_short_path("ge"), False)
        self.assertEqual(Link.is_valid_random_short_path("crap"), False)
        self.assertEqual(Link.is_valid_random_short_path("crap42"), False)
        self.assertEqual(Link.is_valid_random_short_path("abe4abe"), False)
