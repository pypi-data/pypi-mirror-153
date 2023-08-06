import os
import sys
import subprocess
import shutil
import unittest
import logging
import numpy as np
from test.test_helper import TestHelper, Poller, MessageInFileProbe, \
    ExecutionProbe
from plico.utils.configuration import Configuration
from plico.rpc.zmq_remote_procedure_call import ZmqRemoteProcedureCall
from plico.utils.logger import Logger
from plico.rpc.sockets import Sockets
from plico.rpc.zmq_ports import ZmqPorts
from plico_interferometer_server.utils.constants import Constants
from plico_interferometer_server.utils.starter_script_creator import \
    StarterScriptCreator
from plico_interferometer_server.utils.process_startup_helper import \
    ProcessStartUpHelper
from plico_interferometer_server.process_monitor.runner import Runner as \
    ProcessMonitorRunner
from plico_interferometer.client.interferometer_client import \
    InterferometerClient
from plico_interferometer.client.snapshot_entry import SnapshotEntry
from plico_interferometer_server.controller.runner import Runner


@unittest.skipIf(sys.platform == "win32",
                 "Integration test doesn't run on Windows. Fix it!")
class IntegrationTest(unittest.TestCase):

    TEST_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            "./tmp/")
    LOG_DIR = os.path.join(TEST_DIR, "log")
    CONF_FILE = 'test/integration/conffiles/plico_interferometer_server.conf'
    CALIB_FOLDER = 'test/integration/calib'
    CONF_SECTION = Constants.PROCESS_MONITOR_CONFIG_SECTION
    SERVER_LOG_PATH = os.path.join(LOG_DIR, "%s.log" % CONF_SECTION)
    BIN_DIR = os.path.join(TEST_DIR, "apps", "bin")
    SOURCE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              "../..")

    def setUp(self):
        self._setUpBasicLogging()
        self.server = None
        self._wasSuccessful = False

        self._removeTestFolderIfItExists()
        self._makeTestDir()
        self.configuration = Configuration()
        self.configuration.load(self.CONF_FILE)
        self.rpc = ZmqRemoteProcedureCall()

        calibrationRootDir = self.configuration.calibrationRootDir()
        self._setUpCalibrationTempFolder(calibrationRootDir)

    def _setUpBasicLogging(self):
        logging.basicConfig(level=logging.DEBUG)
        self._logger = Logger.of('Integration Test')

    def _makeTestDir(self):
        os.makedirs(self.TEST_DIR)
        os.makedirs(self.LOG_DIR)
        os.makedirs(self.BIN_DIR)

    def _setUpCalibrationTempFolder(self, calibTempFolder):
        shutil.copytree(self.CALIB_FOLDER,
                        calibTempFolder)

    def _removeTestFolderIfItExists(self):
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)

    def tearDown(self):
        TestHelper.dumpFileToStdout(self.SERVER_LOG_PATH)

        try:
            server1_log_path = os.path.join(
                self.LOG_DIR, "%s.log" % Constants.SERVER_1_CONFIG_SECTION)
            TestHelper.dumpFileToStdout(server1_log_path)
        except Exception:
            pass
        try:
            server2_log_path = os.path.join(
                self.LOG_DIR, "%s.log" % Constants.SERVER_1_CONFIG_SECTION)
            TestHelper.dumpFileToStdout(server2_log_path)
        except Exception:
            pass

        if self.server is not None:
            TestHelper.terminateSubprocess(self.server)

        if self._wasSuccessful:
            self._removeTestFolderIfItExists()

    def _createStarterScripts(self):
        ssc = StarterScriptCreator()
        ssc.setInstallationBinDir(self.BIN_DIR)
        ssc.setPythonPath(self.SOURCE_DIR)
        ssc.setConfigFileDestination(self.CONF_FILE)
        ssc.installExecutables()

    def _startProcesses(self):
        psh = ProcessStartUpHelper()
        serverLog = open(os.path.join(self.LOG_DIR, "server.out"), "wb")
        self.server = subprocess.Popen(
            [psh.processProcessMonitorStartUpScriptPath(),
             self.CONF_FILE,
             self.CONF_SECTION],
            stdout=serverLog, stderr=serverLog)
        Poller(5).check(MessageInFileProbe(
            ProcessMonitorRunner.RUNNING_MESSAGE, self.SERVER_LOG_PATH))

    def _testProcessesActuallyStarted(self):
        controllerLogFile = os.path.join(
            self.LOG_DIR,
            '%s.log' % Constants.SERVER_1_CONFIG_SECTION)
        Poller(5).check(MessageInFileProbe(
            Runner.RUNNING_MESSAGE, controllerLogFile))
        controller2LogFile = os.path.join(
            self.LOG_DIR,
            '%s.log' % Constants.SERVER_2_CONFIG_SECTION)
        Poller(5).check(MessageInFileProbe(
            Runner.RUNNING_MESSAGE, controller2LogFile))

    def _buildClients(self):
        ports1 = ZmqPorts.fromConfiguration(
            self.configuration,
            Constants.SERVER_1_CONFIG_SECTION)
        self.client1 = InterferometerClient(
            self.rpc, Sockets(ports1, self.rpc))
        ports2 = ZmqPorts.fromConfiguration(
            self.configuration,
            Constants.SERVER_2_CONFIG_SECTION)
        self.client2 = InterferometerClient(
            self.rpc, Sockets(ports2, self.rpc))

    def _check_backdoor(self):
        self.client1.execute(
            "import numpy as np; "
            "self._myarray= np.array([1, 2])")
        self.assertEqual(
            repr(np.array([1, 2])),
            self.client1.eval("self._myarray"))
        self.client1.execute("self._foobar= 42")
        self.assertEqual(
            "42",
            self.client1.eval("self._foobar"))

    def _test_get_snapshot(self):
        snapshot = self.client2.snapshot('aa')
        snKey = 'aa.%s' % SnapshotEntry.INTERFEROMETER_NAME
        self.assertEqual('My Simulated interferometer no 2', snapshot[snKey])

    def _test_server_info(self):
        serverInfo = self.client1.serverInfo()
        self.assertEqual('interferometer 1 server',
                         serverInfo.name)
        self.assertEqual('localhost', serverInfo.hostname)

    def _test_wavefront(self):
        wf1 = self.client1.wavefront()
        wf2 = self.client2.wavefront()
        Poller(3).check(ExecutionProbe(
            lambda: self.assertEqual((480, 512),
                                     wf1.shape)))
        Poller(3).check(ExecutionProbe(
            lambda: self.assertEqual((480, 512),
                                     wf2.shape)))

    def test_main(self):
        self._buildClients()
        self._createStarterScripts()
        self._startProcesses()
        self._testProcessesActuallyStarted()
        self._test_wavefront()
        self._test_get_snapshot()
        self._test_server_info()
        self._check_backdoor()
        self._wasSuccessful = True


if __name__ == "__main__":
    unittest.main()
