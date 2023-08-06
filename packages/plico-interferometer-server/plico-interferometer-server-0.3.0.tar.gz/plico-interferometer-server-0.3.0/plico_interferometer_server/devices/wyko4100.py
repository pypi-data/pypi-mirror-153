import numpy as np
from plico.utils.logger import Logger
from plico.utils.decorator import override
from plico_interferometer_server.devices.abstract_interferometer import \
    AbstractInterferometer
from plico_interferometer_server.i4sight2.Commons import Constants
import Pyro.core


class Wyko4100_4Sight223(AbstractInterferometer):
    '''
    Wyko 4100 retrofitted by 4D Technology
    '''
    WKYO_LAMBDA_IN_M = 632.8e-9

    def __init__(self,
                 name='wyko4100 on 4sight2.23',
                 **_):
        self._name = name
        self.ipaddr = 'localhost'
        self.logger = Logger.of('Wyko4100')
        # Init the Pyro client
        Pyro.core.initClient()
        self._remoteCtrlUri = \
            'PYROLOC://' + self.ipaddr + ':' + \
            str(Pyro.config.PYRO_PORT) + '/' + Constants.I4D_CONTROLLER_NAME
        self.logger.notice("RemoteCtrlUri: %s" % self._remoteCtrlUri)

        # Try to use the proxy to be sure the 4D Python/Pyro server is running
        try:
            remoteCtrl = self._retrieveProxy()
            remoteCtrl._setTimeout(2)
            remoteCtrl.ping()
        except Exception as e:
            raise Exception(
                "Couldn't connect to pyro server. "
                "Did you run StartupServer script on 4D? (%s)" % str(e))

    @override
    def name(self):
        return self._name

    @override
    def deinitialize(self):
        pass

    def _retrieveProxy(self):
        # Retrieve proxy at runtime to allow each different threads
        # to call these methods!
        # self.log('Getting proxy for %s' % self._remoteCtrlUri)
        remoteCtrl = Pyro.core.getProxyForURI(self._remoteCtrlUri)
        remoteCtrl._setTimeout(Constants.I4D_CONNECTION_CLIENT_TIMEOUT_S)
        return remoteCtrl

    def ping(self):
        self.logger.notice("Pinging remote controller...")
        remoteCtrl = self._retrieveProxy()
        remoteCtrl._setTimeout(2)
        return remoteCtrl.ping()

    @override
    def wavefront(self, how_many=1):
        self.logger.notice("Getting wavefront")
        remoteCtrl = self._retrieveProxy()
        remoteCtrl._setTimeout(int(4 * how_many))
        v = remoteCtrl.wavefront()
        return np.ma.array(data=v['data'] * self.WKYO_LAMBDA_IN_M, mask=v['mask'])

    def raise_exception(self):
        self.logger.notice("calling some unexisting method...")
        remoteCtrl = self._retrieveProxy()
        remoteCtrl._setTimeout(2)
        return remoteCtrl.pincopallino()

    def matrix(self, size):
        return self._retrieveProxy().matrix(size)
