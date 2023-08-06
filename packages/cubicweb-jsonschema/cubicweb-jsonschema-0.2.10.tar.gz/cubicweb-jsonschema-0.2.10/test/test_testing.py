"""Tests for "testing" module."""
from __future__ import print_function

from functools import partial
import doctest
import unittest

import webtest

from cubicweb_jsonschema import testing


class WebTestReponseOutputCheckerTC(unittest.TestCase):

    def setUp(self):
        self.checker = testing.WebTestReponseOutputChecker()

    def example(self, want):
        """Return a mock of doctest.Example suitable for output_difference()
        usage.
        """
        return type('Example', (object, ), {'want': want})()

    def test_ok(self):
        got = want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{"id": "1", "login": "alice"}',
        ])
        self.assertTrue(self.checker.check_output(want, got, 0))
        self.assertMultiLineEqual(
            self.checker.output_difference(self.example(want), got, 0), '')

    def test_ok_json_body_prettyformat(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{"id": "1", "login": "alice"}',
        ])
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{',
            '  "id": "1",',
            '  "login": "alice"',
            '}',
        ])
        self.assertTrue(self.checker.check_output(want, got, 0))
        self.assertMultiLineEqual(
            self.checker.output_difference(self.example(want), got, 0), '')

    def test_json_ellipsis_object(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{"id": "1", "login": "alice"}',
        ])
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{'
            '  "id": "...",'
            '  "login": "alice"'
            '}',
        ])
        self.assertFalse(self.checker.check_output(want, got, 0))
        self.assertTrue(self.checker.check_output(want, got, doctest.ELLIPSIS))

    def test_json_ellipsis_list(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '[{"id": "1", "login": "alice"}]',
        ])
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '['
            '  {"id": "...", "login": "alice"}'
            ']',
        ])
        self.assertFalse(self.checker.check_output(want, got, 0))
        self.assertTrue(self.checker.check_output(want, got, doctest.ELLIPSIS))

    def test_bad_json(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{I am invalid JSON!',
        ])
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{"id": "1"}',
        ])
        self.assertFalse(self.checker.check_output(want, got, 0))
        expected = '\n'.join([
            'Actual body is invalid JSON: {I am invalid JSON!',
        ])
        self.assertMultiLineEqual(
            self.checker.output_difference(self.example(want), got, 0),
            expected)

    def test_status_differ(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{"id": "1", "login": "alice"}',
        ])
        want = '\n'.join([
            'Response: 404 Not Found',
            'Content-Type: application/json',
            '{',
            '  "id": "1",',
            '  "login": "alice"',
            '}',
        ])
        self.assertFalse(self.checker.check_output(want, got, 0))
        expected = '\n'.join([
            'Expected status: Response: 404 Not Found',
            'Actual status: Response: 200 OK',
        ])
        self.assertMultiLineEqual(
            self.checker.output_difference(self.example(want), got, 0),
            expected)

    def test_headers_differ(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/octet-stream',
            '{"x": 1}',
        ])
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{"x": 1}',
        ])
        self.assertFalse(self.checker.check_output(want, got, 0))
        expected = '\n'.join([
            'Expected headers: Content-Type: application/json',
            'Actual headers: Content-Type: application/octet-stream',
        ])
        self.assertMultiLineEqual(
            self.checker.output_difference(self.example(want), got, 0),
            expected)

    def test_headers_missing_from_got(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{"x": 1}',
        ])
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            'Link: </schema> rel="describedby"',
            '{"x": 1}',
        ])
        self.assertFalse(self.checker.check_output(want, got, 0))

    def test_headers_extra_in_got(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            'Something: we do not care about',
            '{"x": 1}',
        ])
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{"x": 1}',
        ])
        self.assertTrue(self.checker.check_output(want, got, 0))

    def test_headers_ellipsis(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Location: http://www.example.com/123',
            'Content-Type: application/json',
            '{"x": 1}',
        ])
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            'Location: http://www.example.com/...',
            '{"x": 1}',
        ])
        self.assertFalse(self.checker.check_output(want, got, 0))
        self.assertTrue(self.checker.check_output(want, got, doctest.ELLIPSIS))
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            'Location: http://www.example.org/...',
            '{"x": 1}',
        ])
        self.assertFalse(self.checker.check_output(
            want, got, doctest.ELLIPSIS))

    def test_headers_ellipsis_body_diff(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Location: http://www.example.com/123',
            'Content-Type: application/json',
            '{"id": "1"}',
        ])
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            'Location: http://www.example.com/...',
            '{"id": "2"}',
        ])
        self.assertFalse(self.checker.check_output(
            want, got, doctest.ELLIPSIS))
        difference = self.checker.output_difference(self.example(want), got, 0)
        # Do not check full content until output_difference() handles ELLIPSIS
        # flag.
        self.assertIn('JSON bodies differ', difference)

    def test_json_body_differ(self):
        got = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{"id": "1"}',
        ])
        want = '\n'.join([
            'Response: 200 OK',
            'Content-Type: application/json',
            '{"id": "2"}',
        ])
        self.assertFalse(self.checker.check_output(want, got, 0))
        self.assertFalse(self.checker.check_output(
            want, got, doctest.ELLIPSIS))
        expected = '\n'.join([
            'JSON bodies differ',
            'expected',
            '{',
            '  "id": "2"',
            '}',
            'actual',
            '{',
            '  "id": "1"',
            '}',
            'diff:',
            '{"id": ["2", "1"]}',
        ])
        difference = self.checker.output_difference(self.example(want), got, 0)
        self.assertMultiLineEqual(difference, expected)

    def test_no_content(self):
        got = 'Response: 204 No Content<BLANKLINE><BLANKLINE>'
        want = 'Response: 204 No Content<BLANKLINE>'
        self.assertTrue(self.checker.check_output(want, got, 0))
        got = 'Response: 204 No Content\nFoo: bar\n'
        want = 'Response: 204 No Content\nFoo: bar\n{"x": 1}'
        self.assertFalse(self.checker.check_output(want, got, 0))
        got = 'Response: 204 No Content\nFoo: bar\n{"x": 1}'
        want = 'Response: 204 No Content\nFoo: bar\n<BLANKLINE>'
        self.assertFalse(self.checker.check_output(want, got, 0))

    def test_parse_error(self):
        got = '\n'.join([
            'Response 42',
        ])
        want = '\n'.join([
            'Response: OK',
            'Content-Type: something',
            'bobybody',
        ])
        self.assertFalse(self.checker.check_output(want, got, 0))
        expected = '\n'.join([
            'In expected: not a webtest.TestResponse string', want,
            'In actual: not a webtest.TestResponse string', got,
        ])
        difference = self.checker.output_difference(self.example(want), got, 0)
        self.assertMultiLineEqual(difference, expected)


def unittest_integration_test():
    """Return a DocFileSuite instance using "doctest-example.txt" file with
    a setUp coming from a unittest TestCase.
    """
    class WebTestBaseCase(unittest.TestCase):
        """Base TestCase with a custom setup initializing a webtest
        application.
        """

        def setUp(self):
            def application(environ, start_response):
                body = b'{"a": 1, "b": [1, 2]}'
                headers = [('Content-Type', 'application/json; charset=utf8'),
                           ('Content-Length', str(len(body)))]
                start_response('200 OK', headers)
                return [body]

            self.webapp = webtest.TestApp(application)

    setUp = partial(testing.setUp, cls=WebTestBaseCase,
                    globs_from_testcase=['webapp'])

    return doctest.DocFileSuite(
        'doctest-example.txt', setUp=setUp,
        checker=testing.WebTestReponseOutputChecker())


def load_tests(loader, tests, ignore):
    """unittest discovery callback"""
    tests.addTests(
        unittest_integration_test(),
    )
    tests.addTests(
        doctest.DocTestSuite('cubicweb_jsonschema.testing'),
    )
    return tests


if __name__ == '__main__':
    import unittest
    unittest.main()
