#!/usr/bin/env python
import unittest
import logging
from plico.utils.logger import Logger
from plico_interferometer_server.devices.simulated_interferometer import \
    SimulatedInterferometer


class SimulatedAuxiliaryCameraTest(unittest.TestCase):

    def setUp(self):
        self._setUpLogging()
        self._interferometer = SimulatedInterferometer()

    def tearDown(self):
        pass

    def _setUpLogging(self):
        FORMAT = '%(asctime)s %(levelname)s %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
        self._logger = Logger.of(self.__class__.__name__)

    def test_wavefront(self):
        wv = self._interferometer.wavefront(how_many=10)
        want_shape = (SimulatedInterferometer.SIZE_H,
                      SimulatedInterferometer.SIZE_W)
        self.assertEqual(want_shape, wv.shape)


if __name__ == "__main__":
    unittest.main()
