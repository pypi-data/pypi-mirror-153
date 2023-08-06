
import numpy as np
from .Commons import Constants
from Scripting.Measurements import Measure

import Pyro.util


# @Class: Controller
# Wrapper around the 4D python library to control the interferometer
#
#
# NOTE: it works in the local interferometer host
# @


class Controller:
    '''
    Interface to interact with 4sight to control the interferometer
    
    Tested on 4Sight 2.23 and 2.4
 
    '''

    def __init__(self):
        self.logSource = "CONTROLLER I4D"
        self.userLog = Pyro.util.UserLogger()
        self._ping_counter = 0

    def ping(self):
        self.log("Pinged from remote client")
        self._ping_counter += 1
        return self._ping_counter

    def wavefront(self):
        '''
        Measure a single wavefront

        Returns
        -------
        wavefront: np.ma.array
            wavefront map in nm
        '''
        self.log("Getting wavefront")
        ret = Measure().GetDataset().GetArray()
        # TODO convert lambda to nm
        return {'data': ret.data, 'mask': ret.mask}

    def matrix(self, size):
        '''
        Useless, just to check pyro transport
        '''
        self.log("getting matrix")
        ret = np.identity(size) * self._ping_counter
        return ret

    # Log using the Pyro logger
    # The log file is define in Pyro config file (Pyro_Server.conf)
    def log(self, message):
        self.userLog.msg(self.logSource, message)
