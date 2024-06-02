import unittest

from tools.libraries.string_utils import replace_volumes


class TestStringUtils(unittest.TestCase):
    def setUp(self):
        self.positives = [
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
            ('volúmen 1', 'Volúmen 1')
        ]

    def test_replace_volumes(self):
        for string, expected_result in self.positives:
            self.assertEqual(expected_result, replace_volumes(string))
