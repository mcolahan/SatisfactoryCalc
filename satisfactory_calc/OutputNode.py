from .AbstractNode import AbstractNode
from .utils import *

class OutputNode(AbstractNode):
    def __init__(self, factory, item, rate):
        super().__init__(factory)
        self.item = item
        self.rate = rate

    def get_shape(self):
        return 'plaintext'

    def get_label(self):
        return self.item + "\n" + get_display_of_number(self.rate)
    
    
    def calculate(self, caller):
        # assert caller is self.factory, "Output node should not be called by other nodes"
        
        if len(self.output_streams) == 0:
            self.factory.set_supplier(self, self.item, rate=self.rate)
            self.input_streams[self.item].locked = True
            self.input_streams[self.item].calculate(self)

        elif caller in self.input_streams.values():
            if caller.rate != self.rate:
                raise Exception("Output node rate should not be changed")
            
        else:
            raise NotImplemented
  