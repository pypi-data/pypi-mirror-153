import time
from plico.utils.hackerable import Hackerable
from plico.utils.snapshotable import Snapshotable
from plico.utils.stepable import Stepable
from plico.utils.serverinfoable import ServerInfoable
from plico.utils.logger import Logger
from plico.utils.decorator import override, logEnterAndExit
from plico.utils.timekeeper import TimeKeeper
from plico_interferometer.types.interferometer_status import \
    InterferometerStatus


class InterferometerController(Stepable,
                               Snapshotable,
                               Hackerable,
                               ServerInfoable):

    def __init__(self,
                 servername,
                 ports,
                 interferometer,
                 replySocket,
                 statusSocket,
                 rpcHandler,
                 timeMod=time):
        self._interferometer = interferometer
        self._replySocket = replySocket
        self._statusSocket = statusSocket
        self._rpcHandler = rpcHandler
        self._timeMod = timeMod
        self._logger = Logger.of('InterferometerController')
        Hackerable.__init__(self, self._logger)
        ServerInfoable.__init__(self, servername,
                                ports,
                                self._logger)
        self._isTerminated = False
        self._stepCounter = 0
        self._timekeep = TimeKeeper()

    @override
    def step(self):
        self._rpcHandler.handleRequest(self, self._replySocket, multi=True)
        self._publishStatus()
        if self._timekeep.inc():
            self._logger.notice(
                'Stepping at %5.2f Hz' % (self._timekeep.rate))
        self._stepCounter += 1

    def getStepCounter(self):
        return self._stepCounter

    def terminate(self):
        self._logger.notice("Got request to terminate")
        try:
            self._interferometer.deinitialize()
        except Exception as e:
            self._logger.warn(
                "Could not deinitialize interferometer: %s" % str(e))
        self._isTerminated = True

    @override
    def isTerminated(self):
        return self._isTerminated

    @logEnterAndExit('Getting wavefront', 'Getting wavefront executed')
    def wavefront(self, how_many=1):
        return self._interferometer.wavefront(how_many)

    def _getInterferometerStatus(self):
        self._logger.debug('get InterferometerStatus')
        interferometerStatus = InterferometerStatus(
            self._interferometer.name())
        return interferometerStatus

    def _publishStatus(self):
        self._rpcHandler.publishPickable(self._statusSocket,
                                         self._getInterferometerStatus())

    def getSnapshot(self, _):
        assert False, \
            'Should not be used, client.snapshot uses published status'

