import abc
from typing import List

OBSERVER_MSG_CALCULATED = "Just finished calculating"
OBSERVER_MSG_UPSTREAM_UPDATE = "Updated calculation status"


class Listener():
    @abc.abstractmethod
    def notify(self, sender, msg:str="") -> None:
        pass


class Notifier():
    
    def __init__(self):
        self._listeners: List[Listener] = []


    def add_listener(self, listener: Listener) -> None:
        if not hasattr(self, "_listeners"):
            self._listeners = []
        
        self._listeners.append(listener)


    def remove_listener(self, listener: Listener) -> None:
        if not hasattr(self, "_listeners"):
            self._listeners = []
        
        if listener in self._listeners:
            self._listeners.remove(listener)
        

    def notify_listeners(self, message=""):
        if not hasattr(self, "_listeners"):
            self._listeners = []

        for listener in self._listeners:
            listener.notify(self, message)

