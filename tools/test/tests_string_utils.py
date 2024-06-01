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
        ]

        self.roman_numerals = [
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
            ('Vol.XXI', 'Vol. XXI'),
        ]

        self.exceptions = [
            '#1vs1',
            'Casi nuevo EP 1',
            'Mis temas favoritos del 2010',
            'Mis temas favoritos del 2011',
            'V.I.P. remixes 2.0',
            'Moët entre tus piernas- bvkXr 19710 X yosef the Soul',
            'El mundo cambia / las bases permanecen v 1.0',
            'Beatz to break with v.3 (dope breaks mixtape)',
            'Bravo 2010',
            'Bienvenido a buenos aires (parte 3)',
            'Shadow hours V.2',
            'Se te va a partir el cuello 2',
            'Underground world_ level 1',
            'Reggae dancehall sobrevive vl 2 mp3',
            'Despamix 10 - noviembre 2009',
            'El poeta y el coleccionista (live 18-10-2007)',
            'The real rap simulator v3',
            'The real rap simulator v1.1',
            '11 vezes 1',
            'Version 1.0',
            'Flaviolous 2.0 the k-funk sessions',
            'Jazz band live (bilbao 2007)',
            'Groove \'12',
            'Almika con el rision v0.5',
            'Penumbra (street tape advance 2007)',
            'Varios 1',
            'Varios 2',
            'Nvmb3r5 no l3tt3r5',
            'Everyday 2007/2010',
            'Vividores 2',
            'Revival 2007',
            'Love mugen 2: dream y existence',
            'Vamos a por tí planeta tierra(2004)',
            'Plan renove 2012: los remixes',
            'Las nuevas aventuras 1990',
            'Kuaderno de vitákora 2003',
            'Live rap 1 to 1',
            'Reserva del 84',
            'Secretos del vaticano (vatican classics 2003-2006)',
            'Reserva del 85',
            'Preview 05',
            'Nivel 3',
            'Survivalseries (calagad 13 rmxs)',
            'Exclusive tracks serie 2',
            'Madrid aprieta (single vinilo 7'')',
            'Supanova 10-44',
            'Vivero hills 666',
            'Introspeccion v.2.0',
            'Level hardest 2',
            'Salvados 2007 a 2011',
            'Versión 0.0',
            'Estudios blancos v.1.0',
            'Estudios blancos v.2.0',
            'Final de la batalla de mcs en sevilla fun club (02-04-04)',
            'Supakanja - supanova 10/44',
            'Eleven o\' clock - 11 veces 1',
            'Producto infinito version 0.4',
            'Elevacion 2009'
        ]

    def test_positives(self):
        for string, expected_result in self.positives:
            self.assertEqual(expected_result, replace_volumes(string))

    def test_exceptions(self):
        for string in self.exceptions:
            self.assertEqual(string, replace_volumes(string))

    def test_roman_numerals(self):
        for string, expected_result in self.roman_numerals:
            self.assertEqual(expected_result, replace_volumes(string))
