from .OutputNode import OutputNode
from .ProductionNode import ProductionNode
from .SupplyNode import SupplyNode
from .Stream import Stream
from .utils import *

import pandas as pd
import pathlib
import pydot

class Factory:


    recipes_df = None

    base_items = ['Iron Ore', 'Copper Ore','Caterium Ore', 'Coal','Limestone', 'Raw Quartz', 'Sulfur', 'Crude Oil', 'Water']

    def __init__(self, products, combine_production=True, alt_recipes=[]):
        self.products = products
        self.combine_production = combine_production
        self.alt_recipes = alt_recipes
        self.nodes = []       # a list of nodes    
        self.streams = []     # a list of streams
        self.producers = {}   # a dict of part name, Production node
           
        self.recipes_df = self._load_recipe_df()


    def calculate(self):
        self.nodes = []
        self.streams = []
        i = 0
        for product, rate in self.products.items():
            out_node = OutputNode(self, product, rate)
            self.nodes.append(out_node)
            out_node.calculate(self)
            # i += 1
            # if i > 3:
            #     break

    @staticmethod
    def _load_recipe_df():
        recipes_df = pd.read_csv(str(pathlib.Path(__file__).parent.resolve()) + '\\recipes.csv', delimiter="\t")
        for i in range(4):
            recipes_df['Input ' + str(i+1) + ' Rate (/min)'] = recipes_df['Input ' + str(i+1) + ' Ratio'] * 60 / recipes_df['Time (s)']
        for i in range(2):
            recipes_df['Output ' + str(i+1) + ' Rate (/min)'] = recipes_df['Output ' + str(i+1) + ' Ratio'] * 60 / recipes_df['Time (s)']
        return recipes_df
    
    def set_supplier(self, to_node, item, rate=0):
        node = None
        if item in self.producers.keys():
            node = self.producers[item]
        else:
            recipe = self._get_recipe(item)
            if recipe is not None:
                node = ProductionNode(self, recipe, 1)
            else:
                node = SupplyNode(self, item, rate)
                
            if self.combine_production:
                self.producers[item] = node

            self.nodes.append(node)
        
        assert node is not None, "No supplier found for " + item

        stream = Stream(self, node, to_node, item, rate)
        node.add_output(stream)
        to_node.add_input(stream)
        self.streams.append(stream)


    def _get_recipe(self, item):
        recipe = None
        recipe_df = self.recipes_df
        if item in self.base_items:
            return None

        recipes = recipe_df.loc[(recipe_df['Output 1'] == item) | 
                                (recipe_df['Output 2'] == item), :]
        
        for index, row in recipes.iterrows():
            if row['Recipe Name'] in self.alt_recipes:
                recipe = row
                break
        
        # use default recipe if no alt recipe found
        if recipe is None:
            rows = recipes.loc[recipes['Recipe Name'] == item, :]
            if rows.shape[0] > 0:
                recipe = rows.iloc[0, :]

        assert recipe is not None, "No recipe found for " + item
        return recipe
    
    def draw(self, img_path):
        self.graph = pydot.Dot(graph_type="digraph", strict=True, rankdir="LR")
        for node in self.nodes:           
            node.draw(self.graph)

        for stream in self.streams:
            stream.draw(self.graph)

        self.graph.write_png(img_path)

