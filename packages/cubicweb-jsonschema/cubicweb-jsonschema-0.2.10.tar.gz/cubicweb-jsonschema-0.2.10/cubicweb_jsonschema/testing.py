"""doctest utilities"""

from collections import defaultdict
import doctest
import json
import re
import unittest

import jsondiff
from jsondiff.symbols import (
    delete,
    insert,
)
from six import string_types


class ParseError(Exception):
    """Error during example output parsing."""


def _parse_webtest_testresponse(string):
    """Parse a webtest.TestResponse string into a (status, headers, body)
    tuple.

    >>> from webtest import TestResponse
    >>> r = TestResponse(b'{a: 1}', status=200,
    ...                  headerlist=[('Content-Type', 'application/json')])
    >>> _parse_webtest_testresponse(str(r))
    ('Response: 200 OK', [('Content-Type', 'application/json')], '{a: 1}')
    >>> r = TestResponse(b'hello!', status=200,
    ...                  headerlist=[('this', 'that'),
    ...                              ('Host', 'example.fr')])

    >>> _parse_webtest_testresponse(str(r))
    ('Response: 200 OK', [('Host', 'example.fr'), ('This', 'that')], 'hello!')
    >>> r = TestResponse(status=204)
    >>> _parse_webtest_testresponse(str(r))
    ('Response: 204 No Content', [], '')
    >>> r = TestResponse(status=204, headerlist=[('Host', 'example.fr')])
    >>> _parse_webtest_testresponse(str(r))
    ('Response: 204 No Content', [('Host', 'example.fr')], '')
    >>> _parse_webtest_testresponse(
    ...     'Response: 204 No Content<BLANKLINE><BLANKLINE>')
    ('Response: 204 No Content', [], '')
    >>> _parse_webtest_testresponse('ah')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ParseError: not a webtest.TestResponse string
    """
    for newline in ('\n', doctest.BLANKLINE_MARKER):
        try:
            status, rest = string.split(newline, 1)
        except ValueError:
            continue
        else:
            break
    else:
        raise ParseError('not a webtest.TestResponse string')
    if not re.match(r'Response: \d{3} \w+', status):
        raise ParseError('not a webtest.TestResponse string')
    headers = []
    while re.match(r'[a-zA-Z\-]+: [^\n]+\n', rest):
        header, rest = rest.split('\n', 1)
        name, value = header.split(':', 1)
        headers.append((name.strip(), value.strip()))
    body = rest.strip()
    while body.endswith(doctest.BLANKLINE_MARKER):
        body = body[:-len(doctest.BLANKLINE_MARKER)]
    return status, headers, body


def jsondiff_filter_ellipsis(diffobj):
    """Remove keys from `diffobj` if there's an ellipsis in wanted value.

    >>> diffobj = {0: ["...", "123"], 1: [2, 3]}
    >>> jsondiff_filter_ellipsis(diffobj)
    >>> diffobj
    {1: [2, 3]}
    >>> diffobj = {0: ["before...after", "before777after"]}
    >>> jsondiff_filter_ellipsis(diffobj)
    >>> diffobj
    {}
    >>> diffobj = {0: ["before...after", "different"]}
    >>> jsondiff_filter_ellipsis(diffobj)
    >>> diffobj
    {0: ['before...after', 'different']}

    We handle nesting well:

    >>> diffobj = {0: {1: {2: ['a ... number', 'a secret number']}},
    ...            1: ['a', 'b']}
    >>> jsondiff_filter_ellipsis(diffobj)
    >>> diffobj
    {1: ['a', 'b']}
    >>> diffobj = {0: [["..."], ["secret"]]}
    >>> jsondiff_filter_ellipsis(diffobj)
    >>> diffobj
    {}

    Diff structure with "insert" (or "delete") action are ignored:

    >>> diffobj = {0: {delete: {'foo': 'bar'}},
    ...            1: ['...', '666']}
    >>> jsondiff_filter_ellipsis(diffobj)
    >>> diffobj
    {0: {delete: {'foo': 'bar'}}}
    >>> diffobj = {insert: [(0, {'foo': 'bar'})]}
    >>> jsondiff_filter_ellipsis(diffobj)
    >>> diffobj
    {insert: [(0, {'foo': 'bar'})]}

    Marshalled values of these actions are also ignored:
    >>> diffobj = {'$insert': [(0, {'foo': 'bar'})]}
    >>> jsondiff_filter_ellipsis(diffobj)
    >>> diffobj
    {'$insert': [(0, {'foo': 'bar'})]}

    If `diffobj` is a list, it probably means that nothing compares in input,
    so we ignore:

    >>> diffobj = [{'this': 1}, {'that': {'this again': 2}}, {'unrelated': 0}]
    >>> jsondiff_filter_ellipsis(diffobj)
    >>> diffobj
    [{'this': 1}, {'that': {'this again': 2}}, {'unrelated': 0}]
    """
    if isinstance(diffobj, list):
        # Nothing compares?
        return
    for key, diff in list(diffobj.items()):
        if key in (insert, delete):
            continue
        if key in ('$insert', '$delete'):
            continue
        if isinstance(diff, dict):
            jsondiff_filter_ellipsis(diff)
            if not diff:
                del diffobj[key]
        elif isinstance(diff, list):
            want, got = diff
            if isinstance(want, list):
                if len(want) != len(got):
                    continue
                for w, g in zip(want, got):
                    if not doctest._ellipsis_match(w, g):
                        break
                else:
                    del diffobj[key]
            elif isinstance(want, string_types):
                if doctest._ellipsis_match(want, got):
                    del diffobj[key]


def _headerlist_to_dict(headerlist):
    """Convert a list of headers tuples into a dict of lists.

    >>> _headerlist_to_dict([('Location', 'www.example.com')])
    {'Location': ['www.example.com']}
    >>> headers = _headerlist_to_dict([('Location', 'there'), ('Foo', 'bar'),
    ...                                ('Foo', 'baz')])
    >>> list(sorted(headers.items()))
    [('Foo', ['bar', 'baz']), ('Location', ['there'])]
    """
    headers = defaultdict(list)
    for name, value in headerlist:
        headers[name].append(value)
    return dict(headers)


def _headerlist_to_string(headerlist):
    """Convert a list of headers tuples into a multiline string.

    >>> _headerlist_to_string([('Location', 'www.example.com')])
    'Location: www.example.com'
    >>> print(_headerlist_to_string([('Location', 'there'),
    ...                              ('Content-Type', 'application/json')]))
    Location: there
    Content-Type: application/json
    """
    return '\n'.join('{}: {}'.format(name, value)
                     for name, value in headerlist)


class WebTestReponseOutputChecker(doctest.OutputChecker):
    """Output checker for webtest.TestResponse objects."""

    def check_output(self, want, got, optionflags):
        # No super() since doctest.OutputChecker is an old-style class.
        if doctest.OutputChecker.check_output(self, want, got, optionflags):
            return True
        try:
            w_status, w_headers, w_body = _parse_webtest_testresponse(want)
            g_status, g_headers, g_body = _parse_webtest_testresponse(got)
        except ParseError:
            return False
        if w_status != g_status:
            return False
        w_headers = _headerlist_to_dict(w_headers)
        g_headers = _headerlist_to_dict(g_headers)
        # Drop extra headers in "got".
        for hname in list(g_headers):
            if hname not in w_headers:
                del g_headers[hname]
        if g_headers != w_headers:
            if optionflags & doctest.ELLIPSIS:
                for hname, wvalues in w_headers.items():
                    try:
                        gvalues = g_headers[hname]
                    except KeyError:
                        return False
                    for wvalue, gvalue in zip(wvalues, gvalues):
                        if not doctest._ellipsis_match(wvalue, gvalue):
                            return False
            else:
                return False
        if not w_body and g_body:
            return False
        elif not g_body and w_body:
            return False
        elif w_body and g_body:
            try:
                json_want = json.loads(w_body)
                json_got = json.loads(g_body)
            except ValueError:
                return False
            diff = self._filtered_jsondiff(json_want, json_got, optionflags)
            if diff:
                return False
        return True

    @staticmethod
    def _filtered_jsondiff(want, got, optionflags, **kwargs):
        diff = jsondiff.diff(want, got, syntax='symmetric', **kwargs)
        if optionflags & doctest.ELLIPSIS:
            if isinstance(want, list) and isinstance(diff, dict):
                for position, itemdiff in list(diff.items()):
                    jsondiff_filter_ellipsis(itemdiff)
                    if not itemdiff:
                        del diff[position]
            else:
                jsondiff_filter_ellipsis(diff)
        return diff

    def output_difference(self, example, got, optionflags):
        want = example.want
        errors = []
        try:
            w_status, w_headers, w_body = _parse_webtest_testresponse(want)
        except ParseError as exc:
            errors.append('In expected: {!s}\n{}'.format(exc, want))
        try:
            g_status, g_headers, g_body = _parse_webtest_testresponse(got)
        except ParseError as exc:
            errors.append('In actual: {!s}\n{}'.format(exc, got))
        if errors:
            return '\n'.join(errors)
        diff = []
        if w_status != g_status:
            diff.append('Expected status: {}'.format(w_status))
            diff.append('Actual status: {}'.format(g_status))
        if w_headers != g_headers:
            diff.append('Expected headers: {}'.format(
                _headerlist_to_string(w_headers)))
            diff.append('Actual headers: {}'.format(
                _headerlist_to_string(g_headers)))
        if w_body or g_body:
            if not w_body:
                diff.append('Expected body is empty')
            elif not g_body:
                diff.append('Actual body is empty')
            else:
                both_valid = True
                try:
                    w_json = json.loads(w_body)
                except ValueError:
                    diff.append(
                        'Expected body is invalid JSON: {}'.format(w_body))
                    both_valid = False
                try:
                    g_json = json.loads(g_body)
                except ValueError:
                    diff.append(
                        'Actual body is invalid JSON: {}'.format(g_body))
                    both_valid = False
                if both_valid:
                    # Marshal the diff to eliminate jsondiff symbols before
                    # dumping.
                    body_diff = self._filtered_jsondiff(
                        w_json, g_json, optionflags, marshal=True)
                    if body_diff:
                        msg = '\n'.join([
                            'JSON bodies differ',
                            'expected\n{}',
                            'actual\n{}',
                            'diff:\n{}'
                        ])
                        diff.append(msg.format(json.dumps(w_json, indent=2),
                                               json.dumps(g_json, indent=2),
                                               json.dumps(body_diff)))
        return '\n'.join(diff)


def setUp(test, cls=unittest.TestCase, globs_from_testcase=()):
    """set-up function for a doctest that uses the setUp method of `cls` class
    (usually a subclass of unittest.TestCase) and insert attributes of the
    test case instance as "globs" of the DocTest object.
    """
    # unittest(2).TestCase.__init__ takes a string corresponding to one of its
    # method, so create a fake one and cleanup afterwards.
    def fake_test_method(testcase):
        pass

    fakename = '_fake_test'
    assert not hasattr(cls, fakename)
    setattr(cls, fakename, fake_test_method)
    try:
        test._tc = cls(fakename)
        test._tc.setUpClass()
        test._tc.setUp()
        for attrname in globs_from_testcase:
            test.globs[attrname] = getattr(test._tc, attrname)
    finally:
        delattr(cls, fakename)


def tearDown(test):
    """tear-down function performing cleanup actions for a DocTest bound to a
    unittest-like TestCase
    """
    if not hasattr(test, '_tc'):
        return
    test._tc.tearDown()
    test._tc.tearDownClass()


if __name__ == '__main__':
    doctest.testmod()
