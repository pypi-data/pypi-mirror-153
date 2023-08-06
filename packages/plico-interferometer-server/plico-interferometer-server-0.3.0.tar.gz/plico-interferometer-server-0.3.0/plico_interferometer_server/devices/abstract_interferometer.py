import abc
from six import with_metaclass


class InterferometerException(Exception):
    pass


class AbstractInterferometer(with_metaclass(abc.ABCMeta, object)):

    # -------------
    # Queries

    @abc.abstractmethod
    def name(self):
        assert False

    @abc.abstractmethod
    def wavefront(self, how_many=1):
        '''
        Parameters
        -----------
        how_many: int (default=1)
            return the average of how_many measurements.

        Returns
        -------
        wavefront: ~numpy.masked.array
            wavefront map in meters

        '''
        assert False

    @abc.abstractmethod
    def deinitialize(self):
        assert False
