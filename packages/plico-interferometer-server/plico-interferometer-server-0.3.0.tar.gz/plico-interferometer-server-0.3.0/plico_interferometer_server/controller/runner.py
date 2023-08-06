import os
import time
from plico.utils.base_runner import BaseRunner
from plico_interferometer_server.devices.simulated_interferometer import \
    SimulatedInterferometer
from plico.utils.logger import Logger
from plico.utils.control_loop import FaultTolerantControlLoop
from plico.utils.decorator import override
from plico_interferometer_server.controller.controller import \
    InterferometerController
from plico.rpc.zmq_ports import ZmqPorts


class Runner(BaseRunner):

    RUNNING_MESSAGE = "Interferometer controller is running."

    def __init__(self):
        BaseRunner.__init__(self)

    def _createInterferometerDevice(self):
        interferometerDeviceSection = self.configuration.getValue(
            self.getConfigurationSection(), 'interferometer')
        interferometerModel = self.configuration.deviceModel(
            interferometerDeviceSection)
        if interferometerModel == 'simulated_interferometer':
            self._createSimulatedInterferometer(interferometerDeviceSection)
        elif interferometerModel == 'phase_cam_4030':
            self._createPhaseCam4030(interferometerDeviceSection)
        elif interferometerModel == 'wyko_4100_4sight_223':
            self._createWyko4100(interferometerDeviceSection)
        elif interferometerModel == 'phase_cam_4020_4sight':
            self._createPhaseCam4020(interferometerDeviceSection)
        else:
            raise KeyError('Unsupported interferometer model %s' %
                           interferometerModel)

    def _createSimulatedInterferometer(self, interferometerDeviceSection):
        interferometerName = self.configuration.deviceName(
            interferometerDeviceSection)
        self._interferometer = SimulatedInterferometer(interferometerName)

    def _createPhaseCam4020(self, interferometerDeviceSection):
        from plico_interferometer_server.devices.phase_cam_4020 import \
            PhaseCam4020_4Sight
        name = self.configuration.deviceName(interferometerDeviceSection)
        self._interferometer = PhaseCam4020_4Sight(name=name)

    def _createWyko4100(self, interferometerDeviceSection):
        from plico_interferometer_server.devices.wyko4100 import \
            Wyko4100_4Sight223
        name = self.configuration.deviceName(interferometerDeviceSection)
        self._interferometer = Wyko4100_4Sight223(name=name)

    def _createPhaseCam4030(self, interferometerDeviceSection):
        from plico_interferometer_server.devices.phase_cam_4030 import \
            PhaseCam4030
        name = self.configuration.deviceName(interferometerDeviceSection)
        ipaddr = self.configuration.getValue(
            interferometerDeviceSection, 'ip_address')
        timeout = self.configuration.getValue(
            interferometerDeviceSection, 'comm_timeout', getfloat=True)
        kwargs = {'timeout': timeout, 'name': name}
        try:
            port = self.configuration.basePort(interferometerDeviceSection)
            kwargs['port'] = port
        except KeyError:
            pass
        self._interferometer = PhaseCam4030(ipaddr, **kwargs)

    def _replyPort(self):
        return self.configuration.replyPort(self.getConfigurationSection())

    def _publisherPort(self):
        return self.configuration.publisherPort(self.getConfigurationSection())

    def _statusPort(self):
        return self.configuration.statusPort(self.getConfigurationSection())

    def _setUp(self):
        self._logger = Logger.of("Interferometer Controller runner")

        self._zmqPorts = ZmqPorts.fromConfiguration(
            self.configuration, self.getConfigurationSection())
        self._replySocket = self.rpc().replySocket(
            self._zmqPorts.SERVER_REPLY_PORT)
        self._publishSocket = self.rpc().publisherSocket(
            self._zmqPorts.SERVER_PUBLISHER_PORT, hwm=100)
        self._statusSocket = self.rpc().publisherSocket(
            self._zmqPorts.SERVER_STATUS_PORT, hwm=1)

        self._createInterferometerDevice()

        self._controller = InterferometerController(
            self.name,
            self._zmqPorts,
            self._interferometer,
            self._replySocket,
            self._statusSocket,
            self.rpc())

    def _runLoop(self):
        self._logRunning()

        FaultTolerantControlLoop(
            self._controller,
            Logger.of("Interferometer Controller control loop"),
            time,
            0.02).start()
        self._logger.notice("Terminated")

    @override
    def run(self):
        self._setUp()
        self._runLoop()
        return os.EX_OK

    @override
    def terminate(self, signal, frame):
        self._controller.terminate()
