from plico.utils.decorator import override
from plico.utils.logger import Logger
from plico_interferometer_server.devices.abstract_interferometer import \
    AbstractInterferometer
from plico_interferometer.client.simulated_interferometer_client \
    import SimulatedInterferometerClient


class SimulatedInterferometer(AbstractInterferometer):
    SIZE_H = SimulatedInterferometerClient.SIZE_H
    SIZE_W = SimulatedInterferometerClient.SIZE_W

    def __init__(self, name='Simulated Interferometer'):
        self._name = name
        self._logger = Logger.of('SimulatedInterferometer')

    @override
    def name(self):
        return self._name

    @override
    def wavefront(self, how_many=1):
        sic = SimulatedInterferometerClient()
        return sic.wavefront(how_many)

    @override
    def deinitialize(self):
        pass

    @property
    def shape(self):
        return (self.SIZE_H, self.SIZE_W)
