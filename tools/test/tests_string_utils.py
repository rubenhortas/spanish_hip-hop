import unittest

from tools.utils.string_utils import fix_volumes, fix_mismatched_parentheses, fix_mismatched_square_brackets


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

        self.mismatched_parentheses = [
            ('1,Bob,Album (instrumentals,,,,,,,,,,,,', '1,Bob,Album (instrumentals),,,,,,,,,,,,'),
            ('2,Bob,Album instrumentals),,,,,,,,,,,,', '2,Bob,Album (instrumentals),,,,,,,,,,,,'),
            ('3,Bob,Album (instrumentals),,,,,,,,,,,,', '3,Bob,Album (instrumentals),,,,,,,,,,,,'),
            ('4,Bob,Album (instrumentals,),,,,,,,,,,,', '4,Bob,Album (instrumentals,),,,,,,,,,,,')
        ]

        self.mismatched_square_brackets = [
            ('1,Bob,Album [instrumentals,,,,,,,,,,,,', '1,Bob,Album [instrumentals],,,,,,,,,,,,'),
            ('2,Bob,Album instrumentals],,,,,,,,,,,,', '2,Bob,Album [instrumentals],,,,,,,,,,,,'),
            ('3,Bob,Album [instrumentals],,,,,,,,,,,,', '3,Bob,Album [instrumentals],,,,,,,,,,,,'),
            ('4,Bob,Album [instrumentals,],,,,,,,,,,,', '4,Bob,Album [instrumentals,],,,,,,,,,,,')
        ]

    def test_fix_volumes(self):
        for string, expected_result in self.volumes:
            self.assertEqual(expected_result, fix_volumes(string))

    def test_fix_mismatched_parentheses(self):
        for string, expected_result in self.mismatched_parentheses:
            self.assertEqual(expected_result, fix_mismatched_parentheses(string))

    def test_fix_mismatched_square_brackets(self):
        for string, expected_result in self.mismatched_square_brackets:
            self.assertEqual(expected_result, fix_mismatched_square_brackets(string))
