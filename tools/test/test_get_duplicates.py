import unittest

from tools.get_duplicates import _get_duplicates


class TestGetDuplicates(unittest.TestCase):
    def setUp(self):
        self.lines = [
            'Bob,Title vol.1',
            'Bob,Title vol.2',
            'Bob,Title',
            'Bob,Title@?!$',
            'Bob,Title (more words),',
            'Bob,T.i.t.u.l.@,',
            'Alice,Another title'
        ]

        self.expected_duplicates = ['Bob,Title  -> Bob,Title@?!$']
        self.expected_possible_duplicates = [
            'Bob,Title vol.1  -> Bob,Title vol.2',
            'Bob,Title  -> Bob,T.i.t.l.@,',
            'Bob,Title@?!$  -> Bob,T.i.t.l.@,']


    def test_get_duplicates(self):
        duplicates, possible_duplicates = _get_duplicates(self.lines)
        print()
        print(duplicates)
        print('*')
        print(possible_duplicates)
        print('*')
        # self.assertEquals(self.expected_duplicates, _get_duplicates(self.lines))
