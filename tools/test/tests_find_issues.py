import unittest

from tools.find_issues import _get_issues


class TestFindIssues(unittest.TestCase):
    def setUp(self):
        self.lines = [
            'Artista,Trabajo,Fecha Publicación, Ok\n',
            'Artista,Trabajo,Fecha Publicación,Extra separator,\n',
            'Artista,Trabajo,Fecha (Publicación,Parentheses issue\n',
            'Artista,Trabajo,Fecha (Publicación,Extra separator + Parentheses issue,\n'
        ]

        self.extra_separators_expected = [
            'Artista,Trabajo,Fecha Publicación,Extra separator,\n',
            'Artista,Trabajo,Fecha (Publicación,Extra separator + Parentheses issue,\n'
        ]

        self.parentheses_issues_expected = [
            'Artista,Trabajo,Fecha (Publicación,Parentheses issue\n',
            'Artista,Trabajo,Fecha (Publicación,Extra separator + Parentheses issue,\n'
        ]

    def test_get_issues(self):
        extra_separators, parentheses_issues = _get_issues(self.lines)
        self.assertEquals(self.extra_separators_expected, extra_separators)
        self.assertEquals(self.parentheses_issues_expected, parentheses_issues)
