from abc import ABC, abstractmethod
import uuid
import pydot


class AbstractNode(ABC):

    def __init__(self, factory):
        self.factory = factory
        self.id = self._generate_id()
        self.listeners = []
        self.input_streams = {}
        self.output_streams = {}

    @abstractmethod
    def get_shape():
        pass
    
    def draw(self, graph):
        self.node = pydot.Node(
            name=self.id, 
            label=self.get_label(),
            shape=self.get_shape()    
        )
        graph.add_node(self.node)
    
    @abstractmethod
    def get_label(self):
        pass

    def add_input(self, stream):
        self.input_streams[stream.item] = stream
        stream.to_node = self

    def add_output(self, stream):
        if stream.item not in self.output_streams.keys():
            self.output_streams[stream.item] = []

        if not stream in self.output_streams[stream.item]:
            self.output_streams[stream.item].append(stream)
            stream.from_node = self
    
    @property
    def streams(self):
        stream_list = list(self.input_streams.values())
        for streams in self.output_streams.values():
            stream_list += streams
        return stream_list

    def update(self, caller):
        self.calculate()
        for stream in self.streams:
            if stream != caller:
                stream.update(self)

    def calculate(self, caller):
        pass 
   
    @staticmethod
    def _generate_id():
        return uuid.uuid4().hex
    
    def get_stream_by_item(self, item):
        for stream in self.streams:
            if stream.item == item:
                return stream
        return None
    
    def get_all_output_streams(self):
        streams = []
        for stream_list in self.output_streams.values():
            streams += stream_list
        return streams

    def get_total_outputs(self):
        totals = {}
        for item, streams in self.output_streams.items():
            if not item in totals.keys():
                totals[item] = 0
            for stream in streams:
                totals[item] += stream.rate
        return totals
