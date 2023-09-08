from .AbstractNode import AbstractNode
from .utils import *


class SupplyNode(AbstractNode):
    def __init__(self, factory, item, rate):
        super().__init__(factory)
        self.item = item
        self.rate = rate

    def get_shape(self):
        return 'cds'

    def get_label(self):
        return self.item + "\n" + get_display_of_number(self.rate)
        
    def calculate(self, caller):
        # assert caller is self.factory, "Output node should not be called by other nodes"
        assert len(self.output_streams) == 1, "Supply node should have only one type of output"
        r = 0
        for stream in list(self.output_streams.values())[0]:
            r += stream.rate
        self.rate = r

    # def calculate(self, calling_stream):
    #     for stream in self.streams:
    #         if stream.item == calling_stream.item:
    #             self.building_count = 
        
    #     calling_stream.item

    #     self.building_count = self.production_rate / self.recipe['Output 1 Rate'] / self.overclock
        
    #     for i in range(4):
    #         input_item = self.recipe['Input ' + str(i+1)]
    #         if not pd.isna(input_item):
    #             input_rate = self.recipe['Input ' + str(i+1) + ' Rate']
    #             self.inputs[input_item] = input_rate * self.building_count * self.overclock
        
    #     self.notify_listeners()

    # def on_update(self):
    #     self.calculate()
    