import abc


class GallerySqlConnector:

    @abc.abstractmethod
    def connect(self):
        pass
