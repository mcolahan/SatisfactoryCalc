from dataclasses import dataclass, field
from building import *
import json
from Item import Item
from typing import TypeVar, Iterable, Tuple, List
import NameList

@dataclass
class Recipe():
    name: str = ""
    class_name: str = ""
    time: float = -1.0
    is_alternate: bool = False
    produced_in: str = None


    def load_from_json(self, json_dict):

        self.name = json_dict['name']
        self.class_name = json_dict['className']
        self.time = json_dict['time']
        self.is_alternate = json_dict['alternate']
        if len(json_dict['producedIn']) > 0:
            self.produced_in = json_dict['producedIn'][0]
        else:
            self.produced_in = None

        self.ingredients = {}
        for ing in json_dict['ingredients']:
            
            self.ingredients[ing['item']] = ing['amount'] * 60 / self.time
        
        self.products = {}
        for prod in json_dict['products']:
            self.products[prod['item']] = prod['amount'] * 60 / self.time


    def __repr__(self):
        return f'<Recipe: {self.name}>'

    @property
    def detailed_info(self):
        ret_str = f"Name: {self.name}\nClass Name: {self.class_name}\n"
        ret_str += f"Is Alternate: {self.is_alternate}\n"
        ret_str += f'Ingredients (/min): \n'
        for key, val in self.ingredients.items():
            item = Item.get_item_by_class_name(key)
            ret_str += f'   {item.name}: {val}\n'

        ret_str += f'Products (/min): \n'
        for key, val in self.products.items():
            item = Item.get_item_by_class_name(key)
            ret_str += f'    {item.name}: {val}\n'

        return ret_str

    @classmethod
    def load_recipes(cls):
        cls.recipes = []

        with open('data.json', 'r') as f:
            json_str = f.read()
        
        json_dict = json.loads(json_str)
        recipes_dict = json_dict['recipes']
        
        for key, val in recipes_dict.items():
            recip = Recipe()
            recip.load_from_json(val)

            cls.recipes.append(recip)

    @classmethod
    def get_recipes_to_produce_item(cls, item: Item) -> List['__class__']:
        try:
            if len(cls.recipes) == 0:
                cls.load_recipes()
        except:
            cls.load_items()
        
        producing_recipes = []
        
        for r in cls.recipes:
            if item.class_name in r.products.keys():
                producing_recipes.append(r)

        return producing_recipes
    
    @classmethod
    def get_base_recipe_for_item(cls, item: Item):
        prod_recipes = cls.get_recipes_to_produce_item(item)
        if len(prod_recipes) == 0:
            return None

        prod_recipes = [r for r in prod_recipes if not r.is_alternate] 
        
        assert len(prod_recipes) == 1
        return prod_recipes[0]

    @classmethod
    def get_alt_recipes_for_items(cls, item: Item):
        prod_recipes = cls.get_recipes_to_produce_item(item)
        if len(prod_recipes) == 0:
            return None

        prod_recipes = [r for r in prod_recipes if r.is_alternate] 
        return prod_recipes

    @classmethod
    def get_recipe_by_name(cls, recipe_name):
        try:
            if len(cls.recipes) == 0:
                cls.load_recipes()
        except:
            cls.load_items()
        
        for r in cls.recipes:
            if r.name == recipe_name:
                return r
        
        return None


if __name__ == "__main__":
    
    Recipe.load_recipes()
    iron_ingot = Item.get_item_by_name(NameList.IRON_INGOT)
    recipe = Recipe.get_base_recipe_for_item(iron_ingot)
    print(recipe.detailed_info)