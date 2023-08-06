import logging.config
import unittest

from sstools.ssconv import ssconv

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)-30s %(levelname)-8s %(message)s',
            '()': 'multiline_formatter.formatter.MultilineMessagesFormatter',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        # '' root logger
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
})

logger = logging.getLogger()
#                                                      Freestyle                                  Backstroke                 Breaststroke                       Butterfly                     Medley
#                       50       100      200         400         800         1500        50       100      200         50       100         200         50       100      200         100       200         400
m_lcm_fina_1000_2022 = ['20.91', '46.91', '01:42.00', '03:40.07', '07:32.12', '14:31.02',  '23.8', '51.85', '01:51.92', '25.95', '56.88',    '02:06.12', '22.27', '49.45',  '01:50.73',           '01:54.0',  '04:03.84']
f_lcm_fina_1000_2022 = ['23.67', '51.71', '01:52.98', '03:56.46', '08:04.79', '15:20.48', '26.98', '57.45', '02:03.35', '29.30', '01:04.13', '02:18.95', '24.43', '55.48', '02:01.81',           '02:06.12', '04:26.36']

m_lcm_fina_1000_2021 = ['20.91', '46.91', '01:42.00', '03:40.07', '07:32.12', '14:31.02',  '24.0', '51.85', '01:51.92', '25.95', '56.88',    '02:06.12', '22.27', '49.5',  '01:50.73',           '01:54.0',  '04:03.84']
m_scm_fina_1000_2021 = ['20.16', '44.94', '01:39.37', '03:32.25', '07:23.42', '14:08.06', '22.22', '48.33', '01:45.63', '25.25', '55.34',    '02:00.16', '21.75', '47.78', '01:48.24', '49.28',  '01:49.63', '03:54.81']
f_lcm_fina_1000_2021 = ['23.67', '51.71', '01:52.98', '03:56.46', '08:04.79', '15:20.48', '26.98', '57.57', '02:03.35', '29.40', '01:04.13', '02:19.11', '24.43', '55.48', '02:01.81',           '02:06.12', '04:26.36']
f_scm_fina_1000_2021 = ['22.93', '50.25', '01:50.43', '03:53.92', '07:59.34', '15:18.01', '25.60', '54.89', '01:58.94', '28.56', '01:02.36', '02:14.57', '24.38', '54.61', '01:59.61', '56.51',  '02:01.86', '04:18.94']

m_lcm_fina_1000_2020 = ['20.91', '46.91',  '01:42.0', '03:40.07', '07:32.12', '14:31.02',  '24.0', '51.85', '01:51.92', '25.95', '56.88',    '02:06.12', '22.27', '49.5',  '01:50.73',           '01:54.0',  '04:03.84']
m_scm_fina_1000_2020 = ['20.24', '44.94', '01:39.37', '03:32.25', '07:23.42', '14:08.06', '22.22', '48.88', '01:45.63', '25.25', '55.61',    '02:00.16', '21.75', '48.08', '01:48.24', '50.26',  '01:49.63', '03:54.81']
f_lcm_fina_1000_2020 = ['23.67', '51.71', '01:52.98', '03:56.46', '08:04.79', '15:20.48', '26.98', '57.57', '02:03.35', '29.40', '01:04.13', '02:19.11', '24.43', '55.48', '02:01.81',           '02:06.12', '04:26.36']
f_scm_fina_1000_2020 = ['22.93', '50.25', '01:50.43', '03:53.92', '07:59.34', '15:18.01', '25.67', '54.89', '01:59.23', '28.56', '01:02.36', '02:14.57', '24.38', '54.61', '01:59.61', '56.51',  '02:01.86', '04:18.94']

m_lcm_fina = ssconv.get_seconds_from_swimtime(m_lcm_fina_1000_2022)
f_lcm_fina = ssconv.get_seconds_from_swimtime(f_lcm_fina_1000_2022)

m_scm_fina = ssconv.get_seconds_from_swimtime(m_scm_fina_1000_2021)
f_scm_fina = ssconv.get_seconds_from_swimtime(f_scm_fina_1000_2021)


class ConverterTest(unittest.TestCase):
    # Conversion is verified with the FINA Points Calculator 6.47605
    @classmethod
    def setUpClass(cls):
        pass

    # preparing to test
    def setUp(self):
        """ Setting up for the test """

    def tearDown(self):
        """Cleaning up after the test"""

    def test_get_finapts_from_seconds(self):
        # Male
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '50m Freestyle', [m_lcm_fina[0]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '50m Freestyle', [m_scm_fina[0]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '100m Freestyle', [m_lcm_fina[1]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '100m Freestyle', [m_scm_fina[1]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '200m Freestyle', [m_lcm_fina[2]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '200m Freestyle', [m_scm_fina[2]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '400m Freestyle', [m_lcm_fina[3]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '400m Freestyle', [m_scm_fina[3]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '800m Freestyle', [m_lcm_fina[4]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '800m Freestyle', [m_scm_fina[4]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '1500m Freestyle', [m_lcm_fina[5]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '1500m Freestyle', [m_scm_fina[5]]), [1000])

        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '50m Backstroke', [m_lcm_fina[6]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '50m Backstroke', [m_scm_fina[6]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '100m Backstroke', [m_lcm_fina[7]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '100m Backstroke', [m_scm_fina[7]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '200m Backstroke', [m_lcm_fina[8]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '200m Backstroke', [m_scm_fina[8]]), [1000])

        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '50m Breaststroke', [m_lcm_fina[9]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '50m Breaststroke', [m_scm_fina[9]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '100m Breaststroke', [m_lcm_fina[10]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '100m Breaststroke', [m_scm_fina[10]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '200m Breaststroke', [m_lcm_fina[11]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '200m Breaststroke', [m_scm_fina[11]]), [1000])

        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '50m Butterfly', [m_lcm_fina[12]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '50m Butterfly', [m_scm_fina[12]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '100m Butterfly', [m_lcm_fina[13]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '100m Butterfly', [m_scm_fina[13]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '200m Butterfly', [m_lcm_fina[14]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '200m Butterfly', [m_scm_fina[14]]), [1000])

        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '100m Medley', [m_scm_fina[15]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '200m Medley', [m_lcm_fina[15]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '200m Medley', [m_scm_fina[16]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'M', '400m Medley', [m_lcm_fina[16]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'M', '400m Medley', [m_scm_fina[17]]), [1000])

        # Female
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '50m Freestyle', [f_lcm_fina[0]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '50m Freestyle', [f_scm_fina[0]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '100m Freestyle', [f_lcm_fina[1]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '100m Freestyle', [f_scm_fina[1]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '200m Freestyle', [f_lcm_fina[2]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '200m Freestyle', [f_scm_fina[2]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '400m Freestyle', [f_lcm_fina[3]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '400m Freestyle', [f_scm_fina[3]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '800m Freestyle', [f_lcm_fina[4]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '800m Freestyle', [f_scm_fina[4]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '1500m Freestyle', [f_lcm_fina[5]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '1500m Freestyle', [f_scm_fina[5]]), [1000])

        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '50m Backstroke', [f_lcm_fina[6]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '50m Backstroke', [f_scm_fina[6]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '100m Backstroke', [f_lcm_fina[7]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '100m Backstroke', [f_scm_fina[7]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '200m Backstroke', [f_lcm_fina[8]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '200m Backstroke', [f_scm_fina[8]]), [1000])

        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '50m Breaststroke', [f_lcm_fina[9]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '50m Breaststroke', [f_scm_fina[9]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '100m Breaststroke', [f_lcm_fina[10]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '100m Breaststroke', [f_scm_fina[10]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '200m Breaststroke', [f_lcm_fina[11]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '200m Breaststroke', [f_scm_fina[11]]), [1000])

        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '50m Butterfly', [f_lcm_fina[12]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '50m Butterfly', [f_scm_fina[12]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '100m Butterfly', [f_lcm_fina[13]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '100m Butterfly', [f_scm_fina[13]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '200m Butterfly', [f_lcm_fina[14]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '200m Butterfly', [f_scm_fina[14]]), [1000])

        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '100m Medley', [f_scm_fina[15]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '200m Medley', [f_lcm_fina[15]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '200m Medley', [f_scm_fina[16]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('LCM', 'F', '400m Medley', [f_lcm_fina[16]]), [1000])
        self.assertEqual(ssconv.get_finapts_from_seconds('SCM', 'F', '400m Medley', [f_scm_fina[17]]), [1000])

    @unittest.skip
    def test_get_seconds_from_finapts(self):
        self.assertAlmostEqual(ssconv.get_seconds_from_finapts('LCM', 'M', '100m Freestyle', 477), 60.03796637595453, 7)
        self.assertAlmostEqual(ssconv.get_seconds_from_finapts('SCM', 'M', '100m Freestyle', 477), 57.516653356115896, 7)
        self.assertAlmostEqual(ssconv.get_seconds_from_finapts('LCM', 'F', '100m Freestyle', 477), 66.18126713495224, 7)
        self.assertAlmostEqual(ssconv.get_seconds_from_finapts('SCM', 'F', '100m Freestyle', 477), 64.3126798207571, 7)

        self.assertAlmostEqual(ssconv.get_seconds_from_finapts('LCM', 'M', '100m Butterfly', 477), 63.76234246109689, 7)
        self.assertAlmostEqual(ssconv.get_seconds_from_finapts('SCM', 'M', '100m Butterfly', 477), 61.535395935960224, 7)
        self.assertAlmostEqual(ssconv.get_seconds_from_finapts('LCM', 'F', '100m Butterfly', 477), 71.006317939415, 7)
        self.assertAlmostEqual(ssconv.get_seconds_from_finapts('SCM', 'F', '100m Butterfly', 477), 69.89284467684666, 7)

    #@unittest.skip
    def test_get_rudolphpts_from_seconds(self):
        print(ssconv.get_rudolphpts_from_seconds('F', '100m Breaststroke', 20, 122.83))
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 9, 20), 20)

        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 9, [76.07, 75, 74]), [14.9, 15.9, 16.8])

        # https://www.swimrankings.net/index.php?page=athleteDetail&athleteId=4605725&pbest=2013
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 8, 106.65), 0)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 9, 76.07), 14.9)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 10, 66.99), 18.9)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 11, 61.2), 19.4)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 12, 57.16), 19.4)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 13, 55.56), 17.9)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 14, 52.8), 18.9)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 15, 50.9), 19.4)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('M', '100m Freestyle', 16, 50.68), 18.8)

        # https://www.swimrankings.net/index.php?page=athleteDetail&athleteId=4043784&pbest=2009
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('F', '200m Freestyle', 17, 131.62), 11.2)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('F', '200m Freestyle', 18, 126.16), 14.2)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('F', '200m Freestyle', 19, 125.46), 13.3)
        self.assertEqual(ssconv.get_rudolphpts_from_seconds('F', '200m Freestyle', 20, 122.83), 14.8)

    @unittest.skip
    def test_get_seconds_from_rudolphpts(self):
        self.assertEqual(ssconv.get_seconds_from_rudolphpts('M', '100m Freestyle', 9, [15.3, 16.2, 17.2]), [75.633, 74.652, 73.562])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ConverterTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
