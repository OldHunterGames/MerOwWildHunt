# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy


class WildHuntSession(object):

    def __init__(self, hero):
        self.hero = hero
        self.enemy = Person("Fey")
        self.captive = None
        self.wilderness = 0         # 0 - "sparse woods", 1 - "forest", 2 - "dense forest"
        self.wilderness_name = ["sparse woods", "forest", "dense forest"]
        self.encounters = {
            "sparse woods": (
                "Catgirl",
                "Beastman"
            ),
            "forest": (
                "Beegirl",
                "Rapetor"
            ),
            "dense forest": (
                "Black Widow",
                "Shoggoth"
            )
        }
        self.menus = {}
        self.menus["Choose action"] = self.choose_action()

    def random_encounter(self, environment):
        self.enemy = Person(choice(self.encounters[environment]))

    def random_craft(self):
        craft_list = ["exotic fruits salad", "flint", "sturdy branch", "heavy club"]
        random_crafts = []
        for item in self.hero.possessions:
            if item == "flint":
                craft_list.append("flint chopper")
        if "tough meat" in self.hero.possessions:
            craft_list.append("tough roast")
        if "tender meat" in self.hero.possessions:
            craft_list.append("girlmeat steak")
        if "sturdy branch" in self.hero.possessions and "flint chopper" in self.hero.possessions:
            craft_list.append("sturdy spear")
        if "sturdy branch" in self.hero.possessions and "silk" in self.hero.possessions:
            craft_list.append("hunting bow")
        if "furry rawhide" in self.hero.possessions:
            craft_list.append("rawhide armor")
        if "chitin" in self.hero.possessions:
            craft_list.append("chitin plates armor")
        if "scales" in self.hero.possessions:
            craft_list.append("scaled hide armor")
        if "silk" in self.hero.possessions:
            craft_list.append("silky rope")
        if "bones" in self.hero.possessions:
            craft_list.append("bone dagger")
        if "sting" in self.hero.possessions:
            craft_list.append("stinger sword")
        if "bone dagger" in self.hero.possessions and "sturdy branch" in self.hero.possessions:
            craft_list.append("bone spear")
        if "stinger sword" in self.hero.possessions and "sturdy branch" in self.hero.possessions:
            craft_list.append("stinger spear")
        for i in range(3):
            random_crafts.append(craft_list.pop(randint(0, len(craft_list)-1)))
        return random_crafts

    def choose_action(self):
        list_of_actions = []
        if self.captive:
            list_of_actions.append(("Slaughter", [renpy.store.Function(self.slaughter, self.captive), "return"]))
            list_of_actions.append(("Capture", [renpy.store.Function(self.capture, self.captive), "return"]))
        list_of_actions.append(("Gather fruits", [renpy.store.Function(self.gather, "fruits"), "return"]))

        return list

    def gather(self, thing):
        self.hero.possessions.append(thing)
        renpy.store.Jump("fruits")

    def slaughter(self, victim):
        pass

    def capture(self, victim):
        pass

    def fight(self):
        self.hero.power -= self.enemy.power


class Person(object):

    def __init__(self, name):
        self.name = name
        self.gender = "male"
        self.physique = 3
        self.agility = 3
        self.spirit = 3
        self.mind = 3
        self.equipment = {"weapon": None, "armor": None}
        self.possessions = []

        if name == "Catgirl":
            self.gender = "female"
            self.possessions = ["bones", "tender meat"]
            self.power_bonus = -1

        if name == "Beastman":
            self.possessions = ["bones", "tough meat", "furry rawhide"]
            self.power_bonus = 0

        if name == "Beegirl":
            self.gender = "female"
            self.possessions = ["sting", "tender meat", "chitin"]
            self.power_bonus = 1

        if name == "Rapetor":
            self.possessions = ["bones",  "tough meat", "scales"]
            self.power_bonus = 2

        if name == "Black Widow":
            self.gender = "female"
            self.possessions = ["silk", "chitin"]
            self.power_bonus = 3

        if name == "Shoggoth":
            self.possessions = ["stupefying ichor"]
            self.power_bonus = 4

        self.power = self.physique + self.agility


class Item(object):

    def __init__(self, name):
        self.name = name
        self.type = "misc"  # misc, weapon, armor, consumable
        self.bonus = 1
        self.components = ()
        self.craft_result = "Crafted {}".format(self.name)

    def craft(self, autor):
        autor.possessions.append(self)
        if self.components:
            for component in self.components:
                autor.possessions.remove(component)

        return self.craft_result




