from argparse import ArgumentError
import json
import abc

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

from satisfactorycalc.AbstractFactoryObject import AbstractFactoryObject
from Item import *
from NameList import SPLIT_OPTIONS

class StreamNode():
    
    rect_dim = 0.07

    def __init__(self, building, lowerleft_xy, io_type='input'):
        self.building = building
        self.pos = lowerleft_xy
        self.io_type = io_type
        self.stream = None

    def anchor_point(self):
        """gets the center point of the node"""
        if self.io_type == 'input':
            return np.array(self.pos) + np.array([0, self.rect_dim/2])
        else:
            return np.array(self.pos) + np.array([self.rect_dim, self.rect_dim/2])

    def plot(self, ax, node_color=None):
        zorder=0
        fc = 'C0'
        if self.io_type == 'output':
            fc = 'C1'
            zorder=0

        if node_color is not None:
            zorder = 20
            fc=node_color

        rect = patches.Rectangle((self.pos[0], self.pos[1]), self.rect_dim, self.rect_dim, fc=fc, zorder=zorder)
        ax.add_patch(rect)



class AbstractBuilding(AbstractFactoryObject, abc.ABC):

    class_2_name = {}

    def __init__(self, param_dict: dict, inputs=0, outputs=0, pos=(0,0), count:int=1, clock=100):
        super().__init__()
        
        self._pos = [pos[0], pos[1]]

        self.width = 1
        self.height = 1
    
        self.io = {}

        self.name = param_dict['name']
        self.class_name = param_dict['className']
        self.description = param_dict['description']

        if not self.class_name in AbstractBuilding.class_2_name:
            AbstractBuilding.class_2_name[self.class_name] = self.name

        
        self.input_count = inputs
        self.output_count = outputs

        if self.input_count > 0:
            gap = self.height / (self.input_count + 1)
            for i in range(self.input_count):
                center_height = self.y + self.height - (i + 1) * gap
                x_left = self.x
                y_lower = center_height - StreamNode.rect_dim/2

                self.io[f'Input {i}'] = StreamNode(self, (x_left, y_lower), io_type='input')
                
                # rect = patches.Rectangle((x_left, y_lower), rect_dim, rect_dim, fc='C0')
                # ax.add_patch(rect)


        if self.output_count > 0:
            gap = self.height / (self.output_count + 1)
            for i in range(self.output_count):
                center_height = self.y + self.height - (i + 1) * gap
                x_left = self.x + self.width - StreamNode.rect_dim
                y_lower = center_height - StreamNode.rect_dim/2
                self.io[f'Output {i}'] = StreamNode(self, (x_left, y_lower), io_type='output')

                # rect = patches.Rectangle((x_left, y_lower), rect_dim, rect_dim, fc='C3')
                # ax.add_patch(rect)

        self.image = None    
        self.count = count    
        self.clock = clock
        self.is_source = False

    def _plot_props(self, props):
        return props

    def plot(self, ax: matplotlib.axes.Axes):
        props = {
            'ec': 'k',
            'count text color': 'k'
        }
        self._plot_props(props)

        edge_color = props['ec']        
        if not self.calculated:
            edge_color = 'r'
            
        rect = patches.Rectangle(self._pos, self.width, self.height, fc='w', ec=edge_color, lw=2, zorder=20)
        ax.add_patch(rect)

        # count annotation
        count_loc_x = self.x + 0.02
        count_loc_y = self.y + self.height - 0.1
        count_str = f'Count: {self.count}'
        plt.annotate(count_str, (count_loc_x, count_loc_y), zorder=20, c=props['count text color'])

        # recipe annotation
        if 'recipe' in props.keys():
            recipe_loc_x = self.x + 0.02
            recipe_loc_y = self.y + 0.02
            recipe_str = f'Recipe: {props["recipe"].name}'
            plt.annotate(recipe_str, (recipe_loc_x, recipe_loc_y), zorder=20)
        
        for node in self.io.values():
            if 'bottlenecking item' in props.keys(): #= self.bottleneck_item
                if node.stream.item == props['bottlenecking item']:
                    node.plot(ax, 'c')
                    continue

            node.plot(ax)

        if self.image is not None:
            image_gap = 0.2
            offset_x = 0
            offset_y = 0
            bound_x = [self.x + image_gap, self.x + self.width - image_gap]
            bound_y = [self.y + image_gap + offset_y, self.y + self.height - image_gap + offset_y]
            bounds = bound_x + bound_y
            ax.imshow(self.image, extent=bounds, zorder=20)



    def _set_pos(self, pos):
        assert len(pos) == 2, "Input position must be length 2 for x and y coords."
        self._pos = list(pos)
    
    def _get_pos(self):
        return self._pos

    position = property(_get_pos, _set_pos, None, "Position of the lower-left corner of the node.")


    @property
    def x(self) -> float:
        return self._pos[0]
    
    @x.setter
    def _set_x_pos(self, new_x: float):
        self._pos[0] = new_x

    @property
    def y(self) -> float:
        return self._pos[1]
    
    @y.setter
    def _set_y_pos(self, new_y: float):
        self._pos[1] = new_y

    @property
    def bounding_box(self):
        return (self.x, self.y, self.width, self.height)
    
    @property
    def outputs(self):
        return [val for key, val in self.io.items() if "Output" in key]

    @property
    def inputs(self):
        return [val for key, val in self.io.items() if "Input" in key]

    def output(self, output_num):
        return self.io[f'Output {output_num}']
    
    def input(self, input_num):
        return self.io[f'Input {input_num}']

    def __repr__(self):
        return f"<Building: {self.name}>"


    def calculate(self):
        self.calculated = False

# json handling
with open('data.json', 'r') as f:
    json_str = f.read()

json_dict = json.loads(json_str)
building_entries = json_dict['buildings']
manfact_build_cats = ['SC_Manufacturers_C', 'SC_Smelters_C',
        'SC_OilProduction_C', 'SC_Miners_C', 'SC_ConveyorAttachments_C', 'SC_Special_C']

buildings_by_cat = {}
for key in building_entries.keys():
    cats = building_entries[key]['categories']
    for cat in cats:
        if cat not in buildings_by_cat.keys():
            buildings_by_cat[cat] = []
        buildings_by_cat[cat].append(building_entries[key])

building_json = {}
for cat in manfact_build_cats:
    cat_entries = buildings_by_cat[cat]
    for entry in cat_entries:
        building_json[entry['name']] = entry

miners_json = json_dict['miners']


class AbstractMiner(AbstractBuilding):
    def __init__(self, build_json, mine_json, pos, resource, count=1, purity='normal', clock=100):
        
        json = build_json
        for key, val in mine_json.items():
            if not key in json.keys():
                json[key] = val

        super().__init__(json, 0, 1, pos, count=count, clock=clock)
        self.prod_multipier = 0
        self.resource = resource
        self.is_source = True
        

        if purity == 'normal':
            self.purity_multiplier = 1
        elif purity == 'pure':
            self.purity_multiplier = 2
        elif purity == 'impure':
            self.purity_multiplier = 0.5
        else:
            raise ValueError("Purity can only be either 'impure', 'normal', or 'pure'.")

    @property
    def production_rate(self):
        return 60 * self.purity_multiplier * self.prod_multiplier * self.count * self.clock/100

    def calculate(self):
        self.io['Output 0'].stream.set_item_rate(self.resource, self.production_rate)
        self.calculated = True
        

class MinerMk1(AbstractMiner):
    def __init__(self, pos, resource, count=1, purity='normal', clock=100):
        super().__init__(building_json['Miner Mk.1'], miners_json['Build_MinerMk1_C'], 
                            pos, resource, count, purity, clock)
        self.image = Image.open('./images/miner-mk-1_256.png')
        self.prod_multiplier = 1


class MinerMk2(AbstractMiner):
    def __init__(self, pos, resource, count=1, purity='normal', clock=100):
        super().__init__(building_json['Miner Mk.2'], miners_json['Build_MinerMk2_C'], 
                            pos, resource, count, purity, clock)
        self.image = Image.open('./images/miner-mk-2_256.png')
        self.prod_multiplier = 2

class MinerMk3(AbstractMiner):
    def __init__(self, pos, resource, count=1, purity='normal', clock=100):
        super().__init__(building_json['Miner Mk.3'], miners_json['Build_MinerMk3_C'],
                        pos, resource, count, purity, clock)
        self.image = Image.open('./images/miner-mk-3_256.png')
        self.prod_multiplier = 4


class AbstractRecipeBuilding(AbstractBuilding):
    def __init__(self, param_dict: dict, inputs, outputs, pos, count, recipe, clock):
        super().__init__(param_dict, inputs, outputs, pos, count, clock)
        
        if not recipe.produced_in == self.class_name:
            raise ArgumentError(f"{recipe} cannot be used in {self}")
        self.recipe = recipe
        self.bottlenecked = False
        self.bottleneck_item = None
        self.bottlenecked_by_building = False

    def _set_outputs_to_zero(self):
        for key, val in self.io.items():
            if 'Output' in key:
                val.item = None

    def calculate(self):
        try:
            # check to see if all input streams are calculated
            input_rates = {}
            required_ingredients = list(self.recipe.ingredients.keys())

            for key, val in self.io.items():
                if "Input" in key:
                    if val.stream.calculated:
                        input_rates[val.stream.item.name] = val.stream.rate
                        if val.stream.item.class_name in required_ingredients:
                            required_ingredients.remove(val.stream.item.class_name)
                    else:
                        self.calculated = False
                        self._set_outputs_to_zero()
                        return False
            
            if len(required_ingredients) > 0:
                self.calculated = False
                self._set_outputs_to_zero()
                
            # determine the rate limiter : supply or building count
            max_consumption = {}
            for key, val in self.recipe.ingredients.items():
                max_consumption[Item.get_item_by_class_name(key).name] = val * self.count * self.clock / 100
            
            supply = {} # key item name, value: item input rate / item consumption rate set by building
            self.bottleneck_item = None
            min_bottleneck = 1
            for key, val in max_consumption.items():
                supply[key] = input_rates[key]/val
                if supply[key] < 1 and supply[key] < min_bottleneck:
                    min_bottleneck = supply[key]
                    self.bottleneck_item = Item.get_item_by_name(key)

            rate_mult = min(supply.values())
            self.bottlenecked_by_building = rate_mult > 1
            rate_mult = min([rate_mult, 1])

            self.bottlenecked = self.bottlenecked_by_building or self.bottleneck_item is not None

            # output rates
            # ToDo: fluid and multi output!
            output_list = []
            for key, val in self.recipe.products.items():
                out_rate = val * self.count * self.clock / 100 * rate_mult
                output_list.append((Item.get_item_by_class_name(key), out_rate))

            if len(output_list) > 1:
                raise NotImplemented
            else:
                self.io['Output 0'].stream.set_item_rate(output_list[0][0], output_list[0][1])
                self.calculated = True
        except:
            self.calculated = False

    def _plot_props(self, props):
        props['recipe'] = self.recipe
        if self.bottlenecked:
            props['ec'] = 'c'
        if self.bottlenecked_by_building:
            props['count text color'] = 'c'
        if self.bottleneck_item is not None:
            props['bottlenecking item'] = self.bottleneck_item
        return props

class AwesomeSink(AbstractBuilding):
    def __init__(self, pos):
        super().__init__(building_json['AWESOME Sink'], 1, 0, pos)
        self.image = Image.open('./images/awesome-sink_256.png')
    
    def calculate(self):
        self.calculated = True    

class Constructor(AbstractRecipeBuilding):
    def __init__(self, recipe, pos, count=1, clock=100):
        super().__init__(building_json['Constructor'], 1, 1, pos, count, recipe, clock)
        self.image = Image.open('./images/constructor_256.png')


class Assembler(AbstractRecipeBuilding):
    def __init__(self, recipe, pos, count=1):
        super().__init__(building_json['Assembler'], 2, 1, pos, count, recipe)
        self.image = Image.open('./images/assembler_256.png')

class Manufacturer(AbstractRecipeBuilding):
    def __init__(self, recipe, pos, count=1):
        super().__init__(building_json['Manufacturer'], 4, 1, pos, count, recipe)
        self.image = Image.open('./images/manufacturer_256.png')

class Refinery(AbstractRecipeBuilding):
    def __init__(self, recipe, pos, count=1):
        super().__init__(building_json['Refinery'], 2, 2, pos, count, recipe)
        self.image = Image.open('./images/refinery_256.png')

class Packager(AbstractRecipeBuilding):
    def __init__(self, recipe, pos, count=1):
        super().__init__(building_json['Packager'], 2, 2, pos, count, recipe)
        self.image = Image.open('./images/packager_256.png')

#smelter
class Smelter(AbstractRecipeBuilding): 

    def __init__(self, recipe, pos, count=1, clock=100):
        super().__init__(building_json['Smelter'], 1, 1, pos, count, recipe, clock=clock)
        self.image = Image.open('./images/smelter_256.png')

class Foundry(AbstractRecipeBuilding): 
    def __init__(self, recipe, pos, count=1, clock=100):
        super().__init__(building_json['Foundry'], 1, 1, pos, count, recipe, clock=clock)
        self.image = Image.open('./images/foundry_256.png')


class AbstractRoutingBuilding(AbstractBuilding):
    def __init__(self, json, pos, inputs, outputs, split_type='even', percentages=None, rates=None):
        super().__init__(json, inputs, outputs, pos)
        
        self.split_type = split_type
        if split_type.lower() == NameList.EVEN:
            pass
        elif split_type.lower() == NameList.PERCENTAGE:
            assert percentages is not None
            self.percentages = percentages
        elif split_type.lower() == NameList.RATE:
            assert rates is not None
            self.rates = rates
        else:
            raise ValueError(f"Split type {split_type} not understood. Options are {NameList.SPLIT_OPTIONS}.")


    def calculate(self):
        
        item = None
        rate = 0
        for input in self.inputs:
            if input.stream is not None:
                if input.stream.rate > 0:
                    if item is None: 
                        item = input.stream.item
                    elif input.stream.item.name != item.name:
                        print(f"Cannot have multiple item types going to the same {self.name}.")
                        self.calculated = False
                        return
                    
                    rate += input.stream.rate

        if self.split_type == NameList.EVEN:
            output_count = 0
            for output in self.outputs:
                if output.stream is not None:
                    output_count += 1
            if output_count > 0:
                per_stream = rate / output_count
                for output in self.outputs:
                    if output.stream is not None:
                        output.stream.set_item_rate(item, per_stream)
            
            self.calculated = True



class Splitter(AbstractRoutingBuilding):
    def __init__(self, pos):
        super().__init__(json=building_json['Conveyor Splitter'], pos=pos, inputs=1, outputs=3, split_type='even')
        self.image = Image.open('./images/conveyor-splitter_256.png')

# smart splitter
# programmable splitter

class Merger(AbstractRoutingBuilding):
    def __init__(self, pos):
        super().__init__(json=building_json['Conveyor Merger'], pos=pos, inputs=3, outputs=1)
        self.image = Image.open('./images/conveyor-merger_256.png')
        




