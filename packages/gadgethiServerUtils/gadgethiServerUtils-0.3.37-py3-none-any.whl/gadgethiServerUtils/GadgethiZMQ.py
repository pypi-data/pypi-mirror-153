import zmq
import abc
import threading

class GadgethiZMQ(metaclass=abc.ABCMeta):
    """
    This is the basic ZMQ structure 
    for python application purposes.
    """
    handler = None
    
    def __init__(self, **kwargs):
        self.context = zmq.Context()
        self.setup(**kwargs)

    def start(self):
        """
        Initialize the zmq thread. 
        """
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        """
        Main zmq thread forever
        """
        while True:
            self.handler()

    @classmethod
    def set_handler(cls, func):
        """
        This is the function to set
        the handler for the zmq
        """
        cls.handler = func

    @abc.abstractmethod
    def setup(self, **configs):
        """
        This is the initial setup for the
        zmq class. setup socket topology
        """
        return NotImplemented
