import abc
import matplotlib
from observer import *

class AbstractFactoryObject(abc.ABC, Listener, Notifier):
    
    def __init__(self):
        self._calculated:bool=False
        self.factory = None
        
    @abc.abstractmethod
    def calculate(self) -> None:
        pass


    @property
    def calculated(self):
        return self._calculated


    @calculated.setter
    def calculated(self, value):
        if value != self._calculated:
            self._calculated = value
            self._notify_listeners_calc_update()

    def update_calc_without_notifying_listeners(self, calc: bool) -> None:
        self._calculated = calc


    @abc.abstractmethod   
    def plot(ax: matplotlib.axes.Axes):
        pass

    
    def _notify_listeners_calc_update(self):
        self.notify_listeners(OBSERVER_MSG_CALCULATED)

    def notify(self, sender:Notifier, msg:str="") -> None:
        if msg == OBSERVER_MSG_CALCULATED:
            self.on_upstream_calc_update(sender)
    
    def on_upstream_calc_update(self, sender:Notifier):
        if isinstance(sender, AbstractFactoryObject):
            if not sender.calculated:
                self.calculated = False
            else:
                if self.factory is not None:
                    self.factory.add_to_calclist(self)