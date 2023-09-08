from dataclasses import dataclass, field
from . import NameList
import json
from PIL import Image
import os

item_images = {
    NameList.ZIPLINE: 'zipline_256.png',
    NameList.BEACON: 'beacon_256.png',
    NameList.GAS_MASK: 'gas-mask_256.png',
    NameList.HAZMAT_SUIT: 'hazmat-suit_256.png',
    NameList.HOVER_PACK: 'hover-pack_256.png',
    NameList.JETPACK: 'jetpack_256.png',
    NameList.BLADE_RUNNERS: 'blade-runners_256.png',
    NameList.NOBELISK_DETONATOR: 'nobelisk-detonator_256.png',
    NameList.OBJECT_SCANNER: 'object-scanner_256.png',
    NameList.RIFLE: 'rifle_256.png',
    NameList.XENO_ZAPPER: 'xeno-zapper_256.png',
    NameList.XENO_BASHER: 'xeno-basher_256.png',
    NameList.PORTABLE_MINER: 'portable-miner_256.png',
    NameList.ALUMINA_SOLUTION: 'alumina-solution_256.png',
    NameList.ALUMINUM_CASING: 'aluminum-casing_256.png',
    NameList.ALUMINUM_INGOT: 'aluminum-ingot_256.png',
    NameList.HEAT_SINK: 'heat-sink_256.png',
    NameList.ALCLAD_ALUMINUM_SHEET: 'alclad-aluminum-sheet_256.png',
    NameList.ALUMINUM_SCRAP: 'aluminum-scrap_256.png',
    NameList.BATTERY: 'battery_256.png',
    NameList.PALEBERRY: 'paleberry_256.png',
    NameList.SOLID_BIOFUEL: 'solid-biofuel_256.png',
    NameList.CABLE: 'cable_256.png',
    NameList.RIFLE_CARTRIDGE: 'rifle-cartridge_256.png',
    NameList.CONCRETE: 'concrete_256.png',
    NameList.CHAINSAW: 'chainsaw_256.png',
    NameList.AI_LIMITER: 'ai-limiter_256.png',
    NameList.CIRCUIT_BOARD: 'circuit-board_256.png',
    NameList.COAL: 'coal_256.png',
    NameList.COLOR_CARTRIDGE: 'color-cartridge_256.png',
    NameList.COMPACTED_COAL: 'compacted-coal_256.png',
    NameList.SUPERCOMPUTER: 'supercomputer_256.png',
    NameList.COMPUTER: 'computer_256.png',
    NameList.COOLING_SYSTEM: 'cooling-system_256.png',
    NameList.COPPER_POWDER: 'copper-powder_256.png',
    NameList.COPPER_INGOT: 'copper-ingot_256.png',
    NameList.COPPER_SHEET: 'copper-sheet_256.png',
    NameList.CRYSTAL_OSCILLATOR: 'crystal-oscillator_256.png',
    NameList.POWER_SHARD: 'power-shard_256.png',
    NameList.BLUE_POWER_SLUG: 'blue-power-slug_256.png',
    NameList.YELLOW_POWER_SLUG: 'yellow-power-slug_256.png',
    NameList.PURPLE_POWER_SLUG: 'purple-power-slug_256.png',
    NameList.ELECTROMAGNETIC_CONTROL_ROD: 'electromagnetic-control-rod_256.png',
    NameList.FABRIC: 'fabric_256.png',
    NameList.GAS_FILTER: 'gas-filter_256.png',
    NameList.FLOWER_PETALS: 'flower-petals_256.png',
    NameList.EMPTY_CANISTER: 'empty-canister_256.png',
    NameList.PACKAGED_FUEL: 'packaged-fuel_256.png',
    NameList.EMPTY_FLUID_TANK: 'empty-fluid-tank_256.png',
    NameList.BIOMASS: 'biomass_256.png',
    NameList.CATERIUM_INGOT: 'caterium-ingot_256.png',
    NameList.BLACK_POWDER: 'black-powder_256.png',
    NameList.HUB_PARTS: 'hub-parts_256.png',
    NameList.IODINE_INFUSED_FILTER: 'iodine-infused-filter_256.png',
    NameList.HEAVY_OIL_RESIDUE: 'heavy-oil-residue_256.png',
    NameList.HIGH_SPEED_CONNECTOR: 'high-speed-connector_256.png',
    NameList.QUICKWIRE: 'quickwire_256.png',
    NameList.ALIEN_CARAPACE: 'alien-carapace_256.png',
    NameList.IRON_INGOT: 'iron-ingot_256.png',
    NameList.REINFORCED_IRON_PLATE: 'reinforced-iron-plate_256.png',
    NameList.IRON_PLATE: 'iron-plate_256.png',
    NameList.IRON_ROD: 'iron-rod_256.png',
    NameList.SCREW: 'screw_256.png',
    NameList.LEAVES: 'leaves_256.png',
    NameList.LIQUID_BIOFUEL: 'liquid-biofuel_256.png',
    NameList.FUEL: 'fuel_256.png',
    NameList.CRUDE_OIL: 'crude-oil_256.png',
    NameList.TURBOFUEL: 'turbofuel_256.png',
    NameList.MEDICINAL_INHALER: 'medicinal-inhaler_256.png',
    NameList.FUSED_MODULAR_FRAME: 'fused-modular-frame_256.png',
    NameList.HEAVY_MODULAR_FRAME: 'heavy-modular-frame_256.png',
    NameList.RADIO_CONTROL_UNIT: 'radio-control-unit_256.png',
    NameList.MODULAR_FRAME: 'modular-frame_256.png',
    NameList.TURBO_MOTOR: 'turbo-motor_256.png',
    NameList.MOTOR: 'motor_256.png',
    NameList.MYCELIA: 'mycelia_256.png',
    NameList.NITRIC_ACID: 'nitric-acid_256.png',
    NameList.NITROGEN_GAS: 'nitrogen-gas_256.png',
    NameList.NOBELISK: 'nobelisk_256.png',
    NameList.NON_FISSILE_URANIUM: 'non-fissile-uranium_256.png',
    NameList.URANIUM_FUEL_ROD: 'uranium-fuel-rod_256.png',
    NameList.URANIUM_WASTE: 'uranium-waste_256.png',
    NameList.BERYL_NUT: 'beryl-nut_256.png',
    NameList.BAUXITE: 'bauxite_256.png',
    NameList.COPPER_ORE: 'copper-ore_256.png',
    NameList.CATERIUM_ORE: 'caterium-ore_256.png',
    NameList.IRON_ORE: 'iron-ore_256.png',
    NameList.URANIUM: 'uranium_256.png',
    NameList.PACKAGED_ALUMINA_SOLUTION: 'packaged-alumina-solution_256.png',
    NameList.PACKAGED_LIQUID_BIOFUEL: 'packaged-liquid-biofuel_256.png',
    NameList.PACKAGED_NITRIC_ACID: 'packaged-nitric-acid_256.png',
    NameList.PACKAGED_NITROGEN_GAS: 'packaged-nitrogen-gas_256.png',
    NameList.PACKAGED_HEAVY_OIL_RESIDUE: 'packaged-heavy-oil-residue_256.png',
    NameList.PACKAGED_OIL: 'packaged-oil_256.png',
    NameList.PACKAGED_SULFURIC_ACID: 'packaged-sulfuric-acid_256.png',
    NameList.PACKAGED_WATER: 'packaged-water_256.png',
    NameList.PARACHUTE: 'parachute_256.png',
    NameList.PETROLEUM_COKE: 'petroleum-coke_256.png',
    NameList.PLASTIC: 'plastic_256.png',
    NameList.ENCASED_PLUTONIUM_CELL: 'encased-plutonium-cell_256.png',
    NameList.PLUTONIUM_FUEL_ROD: 'plutonium-fuel-rod_256.png',
    NameList.PLUTONIUM_PELLET: 'plutonium-pellet_256.png',
    NameList.PLUTONIUM_WASTE: 'plutonium-waste_256.png',
    NameList.POLYMER_RESIN: 'polymer-resin_256.png',
    NameList.PRESSURE_CONVERSION_CUBE: 'pressure-conversion-cube_256.png',
    NameList.QUARTZ_CRYSTAL: 'quartz-crystal_256.png',
    NameList.RAW_QUARTZ: 'raw-quartz_256.png',
    NameList.REBAR_GUN: 'rebar-gun_256.png',
    NameList.FICSIT_COUPON: 'ficsit-coupon_256.png',
    NameList.ROTOR: 'rotor_256.png',
    NameList.RUBBER: 'rubber_256.png',
    NameList.BACON_AGARIC: 'bacon-agaric_256.png',
    NameList.SILICA: 'silica_256.png',
    NameList.SMART_PLATING: 'smart-plating_256.png',
    NameList.VERSATILE_FRAMEWORK: 'versatile-framework_256.png',
    NameList.AUTOMATED_WIRING: 'automated-wiring_256.png',
    NameList.MODULAR_ENGINE: 'modular-engine_256.png',
    NameList.ADAPTIVE_CONTROL_UNIT: 'adaptive-control-unit_256.png',
    NameList.MAGNETIC_FIELD_GENERATOR: 'magnetic-field-generator_256.png',
    NameList.ASSEMBLY_DIRECTOR_SYSTEM: 'assembly-director-system_256.png',
    NameList.THERMAL_PROPULSION_ROCKET: 'thermal-propulsion-rocket_256.png',
    NameList.NUCLEAR_PASTA: 'nuclear-pasta_256.png',
    NameList.SPIKED_REBAR: 'spiked-rebar_256.png',
    NameList.ALIEN_ORGANS: 'alien-organs_256.png',
    NameList.STATOR: 'stator_256.png',
    NameList.STEEL_INGOT: 'steel-ingot_256.png',
    NameList.STEEL_PIPE: 'steel-pipe_256.png',
    NameList.ENCASED_INDUSTRIAL_BEAM: 'encased-industrial-beam_256.png',
    NameList.STEEL_BEAM: 'steel-beam_256.png',
    NameList.LIMESTONE: 'limestone_256.png',
    NameList.SULFUR: 'sulfur_256.png',
    NameList.SULFURIC_ACID: 'sulfuric-acid_256.png',
    NameList.PACKAGED_TURBOFUEL: 'packaged-turbofuel_256.png',
    NameList.ENCASED_URANIUM_CELL: 'encased-uranium-cell_256.png',
    NameList.WATER: 'water_256.png',
    NameList.WIRE: 'wire_256.png',
    NameList.WOOD: 'wood_256.png',
}

item_name_conversions = {}

@dataclass
class Item():
    name: str = ""
    class_name: str = ""
    stack_size: int = -1
    sink_points: float = 0.0
    is_liquid: bool = False
    description: str = ""
    production_recipes: list = field(default_factory=list)
    consumption_recipes: list = field(default_factory=list)
    is_radioactive: bool = False
    radioactive_decay: float = 0.0
    energy_value: float = 0.0
    image_loc: str = None
    _image: Image = None

    def load_from_json(self, json_dict):
        self.name: str = json_dict['name']
        self.class_name: str = json_dict['className']
        self.stack_size: int = json_dict['stackSize']
        self.sink_points: float = json_dict['sinkPoints']
        self.is_liquid: bool = json_dict['liquid']
        self.description: str = json_dict['description']
        self.energy_value: float = json_dict['energyValue']

        self.radioactive_decay = json_dict['radioactiveDecay']
        if self.radioactive_decay > 0:
            self.is_radioactive = True
        
        try:
            self.image_loc = item_images[self.name] 
 
        except:
            pass

    
    def __repr__(self):
        return f'<Item: {self.name}>'


    @property
    def image(self):
        if self._image is not None:
            return self._image
        else:
            try:
                if self.image_loc is not None:
                    self._image = Image.open(os.path.dirname(__file__) + '\\' + f'images/{self.image_loc}') 
            except:
                pass
            finally:
                return self._image
    
    @image.setter
    def _set_image(self):
        raise NotImplemented

    @classmethod
    def load_items(cls):
        json_str = None
        with open(os.path.dirname(__file__) + '\\' + 'data.json', 'r') as f:
            json_str = f.read()

        json_dict = json.loads(json_str)

        items_dict = json_dict['items']

        items = []
        for key in items_dict.keys():
            item_dict = items_dict[key]

            sat_item = Item()
            sat_item.load_from_json(item_dict)

            items.append(sat_item)

        cls.items = items

       

    @classmethod
    def get_item_by_class_name(cls, class_name: str):
        '''
        Get a Satisfactory item based on its class_name attribute. 
        Returns None if not found
        '''
        try:
            if len(cls.items) == 0:
                cls.load_items()
        except:
            cls.load_items()

        for it in cls.items:
            if it.class_name == class_name:
                return it

        return None
        

        

    @classmethod
    def get_item_by_name(cls, name: str):
        '''
        Get a Satisfactory item based on its name attribute. 
        Returns None if not found
        '''
        try:
            if len(cls.items) == 0:
                cls.load_items()
        except:
            cls.load_items()

        for it in cls.items:
            if it.name == name:
                return it

        return None

    @classmethod
    def search_for_item(cls, search_str: str):
        search_items = []
        for item in cls.items:
            if search_str.lower() in item.name.lower():
                search_items.append(item)
        return search_items
        



if __name__ == "__main__":
    Item.load_items()
    items = Item.items

    heavy_oil = Item.get_item_by_class_name('Desc_HeavyOilResidue_C')
    assert heavy_oil.name == "Heavy Oil Residue"

    iron_ore = Item.get_item_by_name("Iron Ore")
    assert iron_ore != None

    random_item = Item.get_item_by_name("random")
    assert random_item is None

    

   
