#!/usr/bin/env python

# @File: Server.py
# Pyro Server for the 4D interferometer.
# This runs in a Windows PC directly connected to the interferometer, and
# remotely export the 4D python libraries (by means of the Controller object).
# @

from threading import Thread

# def path_to_py26():
#    # Add this to have the socket lib
#    sys.path.append('C:\python26\lib')
#    sys.path.append('C:\python26\DLLs')
#    # Add this to have Pyro
#    sys.path.append('C:\Python26\Lib\site-packages')

# path_to_py26()

import Pyro.core
import Pyro.naming
import Pyro.util
from Pyro.errors import PyroError, NamingError

from .Commons import Constants
from .Controller import Controller


# @Class: Controller
# Wrapper around the 4D python library to control the interferometer.
#
# NOTE: it works in the local interferometer host, but is exported by
# the server using the Pyro library.
# @
class RemoteController(Controller, Pyro.core.ObjBase):

    # This is only called on the server when the object is constructed.
    # Can't be used to really initialize the Controller: use initialize(...)
    def __init__(self):
        Controller.__init__(self)
        Pyro.core.ObjBase.__init__(self)

        self.server = None
        #self.userLog = Pyro.util.UserLogger()

    # Log using the Pyro logger
    # The log file is define in Pyro config file (Pyro_Server.conf)
    # def log(self, message):
    #    self.userLog.msg(self.logSource, message)

    # Initialize the object.
    # Use this Client side.
    def initialize(self, server):
        self.log("Initializing Controller...")
        self.server = server


# @Class: Server
# Thread running the Pyro Server
#
# Can be started calling Server.start()
#
# NOTE: to run the Server in the main thread, freezing the 4Sight GUI:
#           - Not inherit Server from Thread
#           - Remove Thread.__init__(self)
#           - Add Pyro.config.PYRO_MULTITHREADED = 0
#           - Directly call Server.run()
# @
class Server(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)

        # The Server is a thread (so it doesn't freeze the 4D GUI), but the request
        # handling can't support concurrent requests (because of the 4D
        # library)
        Pyro.config.PYRO_MULTITHREADED = 0

        print("------ 4D INTERFEROMETER PYRO SERVER ------")
        print("Pyro config file: %s" % Pyro.config.PYRO_CONFIG_FILE)
        print("Pyro storage:     %s" % Pyro.config.PYRO_STORAGE)
        print("Pyro logging:     %s" % Pyro.config.PYRO_USER_LOGFILE)

        # Init logging facility
        self.userLog = Pyro.util.UserLogger()
        self.logSource = "SERVER I4D"

        self.log("----------- 4D INTERFEROMETER PYRO-SERVER -------")

        # Init the Pyro server
        Pyro.core.initServer()

        # Init the daemon
        self.daemon = Pyro.core.Daemon()
        self.daemon.setTimeout(Constants.I4D_CONNECTION_SERVER_TIMEOUT_S)

        # Tell the daemon about the controller
        self.log("I4D Server instancing controller...")
        self.controller = RemoteController()
        self.log("I4D Server initializing controller...")
        self.controller.initialize(self)
        self.log("I4D Server connecting daemon...")
        self.daemon.connect(self.controller, Constants.I4D_CONTROLLER_NAME)
        self.log("I4D Server initialized")

    # Log using the Pyro logger
    def log(self, message):
        self.userLog.msg(self.logSource, message)

    # Called by thread.start()
    def run(self):
        self.log("I4D Server started")
        self.daemon.requestLoop()
