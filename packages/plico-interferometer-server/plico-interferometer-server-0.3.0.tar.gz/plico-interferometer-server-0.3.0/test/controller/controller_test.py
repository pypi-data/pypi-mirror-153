#!/usr/bin/env python
import unittest
from plico_interferometer_server.controller.controller import \
    InterferometerController
from plico_interferometer_server.devices.simulated_interferometer import \
    SimulatedInterferometer


class MyReplySocket():
    pass


class MyPublisherSocket():
    pass


class MyRpcHandler():

    def __init__(self):
        self._publish = {}

    def handleRequest(self, obj, socket, multi):
        pass

    def publishPickable(self, socket, anObject):
        self._publish[socket] = anObject

    def getLastPublished(self, socket):
        return self._publish[socket]

    def sendCameraFrame(self, socket, frame):
        self.publishPickable(socket, frame)


class InterferometerControllerTest(unittest.TestCase):

    def setUp(self):
        self._interferometer = SimulatedInterferometer()
        self._rpcHandler = MyRpcHandler()
        self._replySocket = MyReplySocket()
        self._statusSocket = MyPublisherSocket()
        self._serverName = 'pippo'
        self._ports = 'foo'
        self._ctrl = InterferometerController(
            self._serverName,
            self._ports,
            self._interferometer,
            self._replySocket,
            self._statusSocket,
            self._rpcHandler)

    def tearDown(self):
        self._interferometer.deinitialize()

    def test_publishes_status(self):
        self._ctrl.step()
        status = self._rpcHandler.getLastPublished(
            self._statusSocket)
        self.assertEqual(self._interferometer.name(),
                         status.name)

    def test_new_status_is_published_at_every_step(self):
        self._ctrl.step()
        status1 = self._rpcHandler.getLastPublished(
            self._statusSocket)
        self._ctrl.step()
        status2 = self._rpcHandler.getLastPublished(
            self._statusSocket)
        self.assertNotEqual(status1, status2)

    def test_terminate(self):
        self._ctrl.terminate()
        self.assertTrue(self._ctrl.isTerminated())

    def test_wavefront(self):
        wf = self._ctrl.wavefront()
        self.assertEqual(wf.shape, self._interferometer.shape)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
