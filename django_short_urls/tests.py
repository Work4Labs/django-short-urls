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

from w4l_http import validate_url

class ValidateUrlTestCase(unittest.TestCase):
    def test(self):
        self.assertEqual(validate_url('http://workfor.us'), (True, None))
        self.assertEqual(validate_url('http://app.work4labs.com/jobs?job_id=42'), (True, None))

        self.assertEqual(validate_url('foobar')[0], False)
        self.assertEqual(validate_url('jobs?job_id=42')[0], False)
        self.assertEqual(validate_url('ftp://work4labs.com')[0], False)
        self.assertEqual(validate_url('http://app:bar@work4labs.com')[0], False)

from valid_redirect_path import get_hash_from, add_parameter

class ValidRedirectPathTestCase(unittest.TestCase):
    def test__get_hash_from(self):
        self.assertEqual(get_hash_from('azertyuiop'), ('azertyuiop', None))
        self.assertEqual(get_hash_from('azerty/uiop'), ('azerty/uiop', None))
        self.assertEqual(get_hash_from('a/z/e/r/t/y/u/i/o/p'), ('a/z/e/r/t/y/u/i/o/p', None))

        self.assertEqual(get_hash_from('some/hash/recruiter'), ('some/hash', 'recruiter'))
        self.assertEqual(get_hash_from('some/hash/share'), ('some/hash', 'share'))
        self.assertEqual(get_hash_from('some/hash/search'), ('some/hash', 'search'))

        self.assertEqual(get_hash_from('some/hashrecruiter'), ('some/hashrecruiter', None))
        self.assertEqual(get_hash_from('some/hashshare'), ('some/hashshare', None))
        self.assertEqual(get_hash_from('some/hashsearch'), ('some/hashsearch', None))

    def test__add_parameter(self):
        self.assertEqual(add_parameter('http://workfor.us', None), 'http://workfor.us')
        self.assertEqual(add_parameter('http://workfor.us', 'toto'), 'http://workfor.us?short_redirect=toto')

        self.assertEqual(
            add_parameter('http://www.theuselessweb.com/', 'search'),
            'http://www.theuselessweb.com/?short_redirect=search'
        )
        self.assertRegexpMatches(
            add_parameter('http://www.theuselessweb.com?a=1&b=2&z=5', 'search'),
            r'^http://www.theuselessweb.com\?.*&short_redirect=search&.*$'
        )
        self.assertEqual(
            add_parameter('http://www.theuselessweb.com?short_redirect=4', 'search'),
            'http://www.theuselessweb.com?short_redirect=search'
        )
