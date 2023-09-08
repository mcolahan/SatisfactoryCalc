from .OutputNode import OutputNode
from .utils import *
import pydot

class Stream:
    def __init__(self, factory, from_node, to_node, item, rate, locked=False):
        self.factory = factory
        self.from_node = from_node
        self.to_node = to_node
        self.item = item
        self.rate = rate
        self.is_output = type(to_node) is OutputNode
        self.locked = locked

    def draw(self, graph):
        label = self.item + "\n" + str(self.rate)
        color = "black"
        if self.is_output:
            label = ""
            color = "purple"

        self.edge = pydot.Edge(
            src=self.from_node.id, 
            dst=self.to_node.id,
            label=label,
            color=color
        )
        graph.add_edge(self.edge)

    def calculate(self, caller):
        if caller is self.to_node:
            self.from_node.calculate(self)
           
        if caller is self.from_node:
            self.to_node.calculate(self)

