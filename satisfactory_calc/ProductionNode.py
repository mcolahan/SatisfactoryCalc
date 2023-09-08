from .AbstractNode import AbstractNode
from .utils import *
import pandas as pd
       
class ProductionNode(AbstractNode):
    def __init__(self, factory, recipe, overclock=1):
        super().__init__(factory)

        self.recipe = recipe
        self.overclock = overclock

        self.building_count = 0
    
    def get_shape(self):
        return 'box'

    def get_label(self):
        return (self.recipe['Recipe Name'] + "\n" + 
            f'Building Count: {get_display_of_number(self.building_count)}\n'
        )

    def get_recipe_ratios_permin(self):
        ratios = {}
        for i in range(4):
            input_item = self.recipe['Input ' + str(i+1)]
            if not pd.isna(input_item):
                input_rate = self.recipe['Input ' + str(i+1) + ' Rate (/min)']
                ratios[input_item] = -input_rate
        for i in range(2):
            output_item = self.recipe['Output ' + str(i+1)]
            if not pd.isna(output_item):
                output_rate = self.recipe['Output ' + str(i+1) + ' Rate (/min)']
                ratios[output_item] = output_rate

        return ratios

    def calculate(self, caller):
        outputs = self.get_all_output_streams()
        recipe_ratios = self.get_recipe_ratios_permin()
        if caller in outputs:
            max_builds = 0
            for item, rate in self.get_total_outputs().items():
                build_count = rate / recipe_ratios[item] / self.overclock
                if build_count > max_builds:
                    max_builds = build_count
            self.building_count = max_builds

            required_inputs = {}
            for item, rate in recipe_ratios.items():
                if rate < 0:
                    required_inputs[item] = -rate * self.building_count * self.overclock
            
            for item, rate in required_inputs.items():
                if not item in self.input_streams.keys():
                    self.factory.set_supplier(self, item, rate=rate)
                    self.input_streams[item].calculate(self)

        else:
            raise NotImplemented
