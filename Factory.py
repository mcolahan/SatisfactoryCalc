from re import L
from building import *
from Item import Item
from Recipe import Recipe
import abc
import matplotlib.pyplot as plt
import matplotlib
import NameList
from color_palette import *
from typing import List
# load buildings


# load items
Item.load_items()

# load recipes
Recipe.load_recipes()



class FactoryStream(AbstractFactoryObject):

    def __init__(self, from_node: StreamNode, to_node: StreamNode):
        super().__init__()
        
        self.start = from_node
        self.finish = to_node
        self.mode = 'right angles'
        self._line_coords_x = []
        self._line_coords_y = []
        self._center = (0,0)
        self._calc_points()
        self._item = None
        self._rate = 0

        self.start.stream = self
        self.finish.stream = self

        from_node.building.add_listener(self)
        self.add_listener(to_node.building)



    def _calc_points(self):

        from_coord = self.start.anchor_point()
        to_coord = self.finish.anchor_point()

        self._line_coords_x = [from_coord[0]]
        self._line_coords_y = [from_coord[1]]
        
        if self.mode == 'direct':
            self._line_coords_x.append(to_coord[0])
            self._line_coords_y.append(to_coord[1])

            self._center = (from_coord[0] + (to_coord[0] - from_coord[0]) / 2, 
                            from_coord[1] + (to_coord[1] - from_coord[1]) / 2)


        elif self.mode == 'right angles':

            delta_x = to_coord[0] - from_coord[0]
            delta_y = to_coord[1] - from_coord[1]

            if delta_x > 0.3:
            
                self._line_coords_x.append(self._line_coords_x[-1] + delta_x / 2)
                self._line_coords_y.append(self._line_coords_y[-1])
                
                self._line_coords_x.append(self._line_coords_x[-1])
                self._line_coords_y.append(self._line_coords_y[-1] + delta_y)

                self._line_coords_x.append(to_coord[0])
                self._line_coords_y.append(to_coord[1])

            else:
                
                extra_x = 0.3
                points = [
                    (from_coord[0] + extra_x, from_coord[1]),
                    (from_coord[0] + extra_x, from_coord[1] + delta_y/2),
                    (from_coord[0] + delta_x - extra_x, from_coord[1] + delta_y/2),
                    (to_coord[0] - extra_x, to_coord[1]),
                    (to_coord[0], to_coord[1])
                ]

                for point in points:
                    self._line_coords_x.append(point[0])
                    self._line_coords_y.append(point[1])

            self._center = (from_coord[0] + (to_coord[0] - from_coord[0]) / 2, 
            from_coord[1] + (to_coord[1] - from_coord[1]) / 2)




    def plot(self, ax):
        
        plt.plot(self._line_coords_x, self._line_coords_y, 'k')

        to_coord = self.finish.anchor_point()
        tri_width=0.08
        tri_height=0.15
        triangle = patches.Polygon(np.array([
            [to_coord[0], to_coord[1]],
            [to_coord[0]-tri_height/2, to_coord[1]+tri_width/2],
            [to_coord[0]-tri_height/2, to_coord[1]-tri_width/2] 
        ]), fc='k', zorder=15)
        ax.add_patch(triangle)

        circle = patches.Ellipse(self._center, 0.5,0.5, fc='w', zorder=20)
        img_gap = 0.15
        bounds = [self._center[0]-img_gap, self._center[0] + img_gap,
                  self._center[1]-img_gap, self._center[1] + img_gap 
                ]

        if self.item is not None:
            if self.item.image is not None:
                ax.imshow(self.item.image, extent=bounds, zorder=21)
        ax.add_patch(circle)

        if self.rate >= 0:
            rate_loc_x = self._center[0]
            rate_loc_y = self._center[1] - 0.2
            rate_str = str(self.rate)
            plt.text(rate_loc_x, rate_loc_y, rate_str, zorder=20, ha='center')




    @property
    def bounding_box(self):
        from_coord = self.start.anchor_point()
        to_coord = self.finish.anchor_point()
        
        xlims = [from_coord[0], to_coord[0]]
        for val in self._line_coords_x:
            if val > xlims[1]:
                xlims[1] = val
            if val < xlims[0]:
                xlims[0] = val

        ylims = [from_coord[1], to_coord[1]]
        for val in self._line_coords_y:
            if val > ylims[1]:
                ylims[1] = val
            if val < ylims[0]:
                ylims[0] = val

        return (xlims[0], ylims[0], xlims[1] - xlims[0], ylims[1] - ylims[0])


    @property
    def item(self):
        return self._item     
    
    @item.setter
    def _set_item(self, item: Item):
        self._item = item
        if self._item is None:
            self._rate = 0

    @property
    def rate(self):
        return self._rate
    
    @rate.setter
    def _set_rate(self, rate):
        self._rate = rate

    def set_item_rate(self, item: Item, rate: float):
        self._item = item
        self._rate = rate
 

    def calculate(self):
        if self.item is not None and self.rate > 0:
            self.calculated = True
        else:
            self.calculated = False


class Factory(object):
    
    def __init__(self):
        self.buildings = []
        self.streams = []
        self._plot_objs = []
        self.sources = []
        self._calclist = []


    def add_building(self, building: AbstractBuilding):
        building.factory = self
        self.buildings.append(building)
        self._plot_objs.append(building)
        if building.is_source:
            self.sources.append(building)

    def add_buildings(self, buildings: List[AbstractBuilding]) -> None:
        for building in buildings:
            self.add_building(building)
    
    def add_stream(self, stream: FactoryStream):
        stream.factory = self
        self.streams.append(stream)
        self._plot_objs.append(stream)

    def add_streams(self, streamlist: List[FactoryStream]):
        for stream in streamlist:
            self.add_stream(stream)
        
    def add_to_calclist(self, to_calc: AbstractFactoryObject) -> None:
        if isinstance(to_calc, AbstractFactoryObject):
            self._calclist.append(to_calc)
    
    def calculate(self):
        for stream in self.streams:
            stream.update_calc_without_notifying_listeners(False)
        for building in self.buildings:
            building.update_calc_without_notifying_listeners(False)

        self._calclist = []
        for source in self.sources:
            source.calculate()
            while len(self._calclist) > 0:
                to_calc = self._calclist.pop(0)
                to_calc.calculate()



    def plot(self, image_name: str = None):

        fig = plt.figure()
        ax = plt.subplot(111, aspect='equal')
        ax.set_facecolor(BACKGROUND)
        ax.grid(color=GRID, linestyle='--')

        xlim = [0, 1]
        ylim = [0, 1]
        for obj in self._plot_objs:
            obj.plot(ax)

            bounds = obj.bounding_box
            if bounds[0] < xlim[0]:
                xlim[0] = bounds[0]

            if bounds[1] < ylim[0]:
                ylim[0] = bounds[1]
            
            if (bounds[0] + bounds[2]) > xlim[1]:
                xlim[1] = bounds[0] + bounds[2]
            
            if (bounds[1] + bounds[3]) > ylim[1]:
                ylim[1] = bounds[1] + bounds[3]


        x_margin = (xlim[1] - xlim[0]) * 0.05
        xlim[0] -= x_margin
        xlim[1] += x_margin

        y_margin = (ylim[1] - ylim[0]) * 0.05
        ylim[0] -= y_margin
        ylim[1] += y_margin

        fig_scale = 1.6
        fig_width = (xlim[1] - xlim[0]) * fig_scale
        fig_height = (ylim[1] - ylim[0]) * fig_scale
        fig.set_size_inches(fig_width, fig_height)

        plt.xlim(xlim)
        plt.ylim(ylim)                

        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    factory = Factory()

    iron_ore = Item.get_item_by_name(NameList.IRON_ORE)
    iron_ingot = Item.get_item_by_name(NameList.IRON_INGOT)
    iron_smelting = Recipe.get_base_recipe_for_item(iron_ingot)

    delta_y = 4
    for i in range(1):

        miner = MinerMk3((0,0 + i * delta_y), iron_ore, count=1, purity='pure')  
        splitter = Splitter((2,0 + i * delta_y))
        smelter1 = Smelter(iron_smelting, (4, 0 + i * delta_y), count=8)
        smelter2 = Smelter(iron_smelting, (4, 2 + i * delta_y), count=9)
        merger = Merger((6,0 + i * delta_y))

        sink = AwesomeSink((8,0 + i * delta_y))

        factory.add_buildings([miner, smelter1, smelter2, sink, splitter, merger])

        factory.add_streams([
            FactoryStream(miner.output(0), splitter.input(0)),
            FactoryStream(splitter.output(0), smelter2.input(0)),
            FactoryStream(splitter.output(1), smelter1.input(0)),
            FactoryStream(smelter2.output(0), merger.input(0)),
            FactoryStream(smelter1.output(0), merger.input(1)),
            FactoryStream(merger.output(0), sink.input(0))
        ])


    factory.calculate()
    factory.plot()
