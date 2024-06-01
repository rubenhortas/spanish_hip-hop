import unittest

from tools.libraries.string_utils import replace_volumes


class TestStringUtils(unittest.TestCase):
    def setUp(self):
        self.positives = [
            ('vol?.?1', 'Vol. 1'),
            ('Vol?.?1', 'Vol. 1'),
            ('vol.01', 'Vol. 1'),
            ('Vol.01', 'Vol. 1'),
            ('vol.1', 'Vol. 1'),
            ('Vol.1', 'Vol. 1'),
            ('vol. 1', 'Vol. 1'),
            ('Vol .1', 'Vol. 1'),
            ('vol. 01', 'Vol. 1'),
            ('Vol. 01', 'Vol. 1'),
            ('vol 1', 'Vol. 1'),
            ('Vol 1', 'Vol. 1'),
            ('volume 1', 'Vol. 1'),
            ('Volume 1', 'Vol. 1'),
            ('volumen 1', 'Vol. 1'),
            ('Volumen 1', 'Vol. 1'),
            ('volume 1.5', 'Vol. 1.5'),
            ('Volume 1.5', 'Vol. 1.5'),
            ('vol i', 'Vol. I'),
            ('Vol I', 'Vol. I'),
            ('vol.ii', 'Vol. II'),
            ('Vol.II', 'Vol. II'),
            ('vol.iii', 'Vol. III'),
            ('Vol.III', 'Vol. III'),
            ('vol.iv', 'Vol. IV'),
            ('Vol.IV', 'Vol. IV'),
            ('vol.v', 'Vol. V'),
            ('Vol.V', 'Vol. V'),
            ('vol.ix', 'Vol. IX'),
            ('Vol.IX', 'Vol. IX'),
            ('vol.xxi', 'Vol. XXI'),
            ('Vol.XXI', 'Vol. XXI')
        ]

    def test_positives(self):
        for string, expected_result in self.positives:
            self.assertEqual(expected_result, replace_volumes(string))
