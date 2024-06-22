import unittest

from tools.utils.string_utils import fix_volumes, fix_mismatched_parentheses, fix_mismatched_square_brackets, \
    has_mismatched_parentheses, has_mismatched_square_brackets, has_mismatched_quotes, fix_mismatched_quotes


class TestStringUtils(unittest.TestCase):
    def setUp(self):
        self.volumes = [
            ('vol?.?1', 'Vol. 1'),
            ('vol.01', 'Vol. 01'),
            ('vol.1', 'Vol. 1'),
            ('vol. 1', 'Vol. 1'),
            ('Vol .1', 'Vol. 1'),
            ('vol. 01', 'Vol. 01'),
            ('vol 1', 'Vol. 1'),
            ('volume 1', 'Volume 1'),
            ('volumen 1', 'Volumen 1'),
            ('volume 1.5', 'Volume 1.5'),
            ('vol i', 'Vol. I'),
            ('vol.ii', 'Vol. II'),
            ('vol.iii', 'Vol. III'),
            ('vol.iv', 'Vol. IV'),
            ('vol.v', 'Vol. V'),
            ('vol.ix', 'Vol. IX'),
            ('vol.xxi', 'Vol. XXI'),
            ('Voltage', 'Voltage'),
            ('Revolucionario', 'Revolucionario')
        ]

        self.matched_parentheses = [
            ('Album instrumentals', 'Album instrumentals'),
            ('Album (instrumentals)', 'Album (instrumentals)')
        ]

        self.mismatched_parentheses = [
            ('Album (instrumentals', 'Album (instrumentals)'),
            ('Album instrumentals)', 'Album (instrumentals)'),
            ('bob (01.01.2005', 'bob (01.01.2005)'),
            ('bob 01.01.2005)', 'bob (01.01.2005)'),
            ('bob 01/01/2005)', 'bob (01/01/2005)'),
            ('bob 01.01 2005)', 'bob 01.01 (2005)')
        ]

        self.matched_square_brackets = [
            ('1,Bob,Album instrumentals', '1,Bob,Album instrumentals'),
            ('1,Bob,Album [instrumentals]', '1,Bob,Album [instrumentals]')
        ]

        self.mismatched_square_brackets = [
            ('Album [instrumentals', 'Album [instrumentals]'),
            ('Album instrumentals]', 'Album [instrumentals]'),
            ('bob [01.01.2005', 'bob [01.01.2005]'),
            ('bob 01.01.2005]', 'bob [01.01.2005]'),
            ('bob 01/01/2005]', 'bob [01/01/2005]'),
            ('bob 01.01 2005]', 'bob 01.01 [2005]')
        ]

        self.matched_quotes = [
            ('Album instrumentals', 'Album instrumentals'),
            ('Album "instrumentals"', 'Album "instrumentals"'),
        ]

        self.mismatched_quotes = [
            ('Album "instrumentals', 'Album "instrumentals"'),
            ('Album instrumentals"', 'Album "instrumentals"'),
            ('bob "01.01.2005', 'bob "01.01.2005"'),
            ('bob 01.01.2005"', 'bob "01.01.2005"'),
            ('bob 01/01/2005"', 'bob "01/01/2005"'),
            ('bob 01.01 2005"', 'bob 01.01 "2005"')
        ]

    def test_fix_volumes(self):
        for string, expected_result in self.volumes:
            self.assertEqual(expected_result, fix_volumes(string))

    def test_has_mismatched_parentheses(self):
        for string, _ in self.matched_parentheses:
            self.assertFalse(has_mismatched_parentheses(string))

        for string, _ in self.mismatched_parentheses:
            self.assertTrue(has_mismatched_parentheses(string))

    def test_fix_mismatched_parentheses(self):
        for string, expected_result in self.matched_parentheses:
            self.assertEqual(expected_result, fix_mismatched_parentheses(string))

        for string, expected_result in self.mismatched_parentheses:
            self.assertEqual(expected_result, fix_mismatched_parentheses(string))

    def test_has_mismatched_square_brackets(self):
        for string, _ in self.matched_square_brackets:
            self.assertFalse(has_mismatched_square_brackets(string))

        for string, _ in self.mismatched_square_brackets:
            self.assertTrue(has_mismatched_square_brackets(string))

    def test_fix_mismatched_square_brackets(self):
        for string, expected_result in self.mismatched_square_brackets:
            self.assertEqual(expected_result, fix_mismatched_square_brackets(string))

    def test_has_mismatched_quotes(self):
        for string, _ in self.matched_quotes:
            self.assertFalse(has_mismatched_quotes(string))

        for string, _ in self.mismatched_quotes:
            self.assertTrue(has_mismatched_quotes(string))

    def test_fix_mismatched_quotes(self):
        for string, expected_result in self.mismatched_quotes:
            self.assertEqual(expected_result, fix_mismatched_quotes(string))
