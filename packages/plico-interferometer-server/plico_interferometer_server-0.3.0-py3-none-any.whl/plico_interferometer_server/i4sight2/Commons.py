''' 
Set of commons info needed by Pyro Server and Client.

Used with 4sight 2.23 and 2.4
'''


class Constants:

    # Pyro controller object name: used by both server and client
    I4D_CONTROLLER_NAME = "I4D_Controller"

    # Timeout used for TCP connection between Client and Server, used by
    # InterferometerCtrl (actually by Python/Pyro library) and 4Sight
    # Python/Pyro Server.
    #
    # This is the upper bound for every communication, so don't set it too low!!!
    # NOTE: it doesn't seems to work in case of communication problems, i.e
    #		Server is down.
    #
    # TODO Evaluate better timeout problem
    I4D_CONNECTION_CLIENT_TIMEOUT_S = 60
    I4D_CONNECTION_SERVER_TIMEOUT_S = 30
