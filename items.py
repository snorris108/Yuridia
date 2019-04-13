
import random


class Item:
    def __init__(self, name, value, quantity=0):
        self.name = name
        self.value = value
        self.quantity = quantity


class Gear(Item):
    def __init__(self, name, value, tier, stats, quantity=0):
        super().__init__(name, value, quantity)
        self.tier = tier
        self.stats = stats


class Consumable(Item):
    def __init__(self, name, stats, value, quantity=0):
        super().__init__(name, value, quantity)
        self.stats = stats
        # self.melee_atk = melee_atk
        # self.magic_atk = magic_atk
        # self.poison_atk = poison_atk
        # self.hp_regen = hp_regen
        # self.mp_regen = mp_regen


class Bait(Item):
    def __init__(self, name, value, quantity=0):
        super().__init__(name, value, quantity)


class Tool(Item):
    def __init__(self, name, stats, value, quantity=0):
        super().__init__(name, value, quantity)
        self.stats = stats
        # self.durability = durability


def create_item(name, value, tier, dmg_style, slot, melee_boost, magic_boost, poison_boost, hp_regen, mp_regen):
    return Gear(name, value, tier,
                {'dmg_style': dmg_style,
                 'slot': slot,
                 # can reforge scalars < 1 at a smith
                 'melee_boost_scalar': 1 * random.choice([0.5, 0.75, 1]),
                 'magic_boost_scalar': 1 * random.choice([0.5, 0.75, 1]),
                 'hp_regen_scalar': 1 * random.choice([0.5, 0.75, 1]),
                 'mp_regen_scalar': 1 * random.choice([0.5, 0.75, 1]),
                 'melee_boost': melee_boost,
                 'magic_boost': magic_boost,
                 'poison_boost': poison_boost,
                 'hp_regen': hp_regen,
                 'mp_regen': mp_regen,
                 'durability': 100 * random.choice([0.5, 0.75, 1]),
                 'default_name': name})


gear_dict = {'small_dagger':    create_item('small dagger', 10, 1, 'melee', ['Mainhand', 'Offhand'],   12, 0, 0, 0, 0),
             'scimitar':        create_item('scimitar', 16, 1, 'melee', ['Mainhand', 'Offhand'],       20, 0, 0, 0, 0),
             'kings_blade':     create_item('King\'s Blade', 1, 26, 'melee', ['Mainhand', 'Offhand'],  25, 0, 0, 0, 0),
             'ilan_branch':     create_item('ilan branch', 1, 10, 'magic', ['Mainhand', 'Offhand'],    0, 7, 0, 0, 1),
             'wand':            create_item('wand', 16, 1, 'magic', ['Mainhand', 'Offhand'],           0, 20, 0, 0, 2),
             'targe':           create_item('targe', 10, 1, 'melee, defense', ['Offhand'],             5, 0, 0, 0, 0),
             'glimmering_orb':  create_item('glimmering orb', 36, 1, 'magic', ['Offhand'],             0, 8, 0, 0, 6),
             'leather_cap':     create_item('leather cap', 8, 1, 'melee, defense', ['Head'],           0, 0, 0, 3, 0),
             'heavy_tunic':     create_item('heavy tunic', 8, 1, 'defense', ['Body'],                  5, 0, 0, 2, 0),
             'thick_chaps':     create_item('thick chaps', 16, 1, 'defense', ['Legs'],                 4, 0, 0, 2, 0),
             'iron_gloves':     create_item('iron gloves', 10, 1, 'defense', ['Hands'],                2, 0, 0, 0, 0),
             'cut_boots':       create_item('cut boots', 10, 1, 'defense', ['Feet'],                   2, 0, 0, 0, 0),
             'old_ring':        create_item('old ring', 28, 1, 'magic', ['Ring'],                      0, 14, 0, 0, 7),
             'clay_ring':       create_item('clay ring', 22, 1, 'melee', ['Ring'],                     14, 0, 0, 7, 0),
             'crooked_staff':   create_item('crooked staff', 24, 1, 'magic', ['Mainhand', 'Offhand'],  0, 15, 0, 0, 4)}

list_of_mainhand = [k for k, v in gear_dict.items() if 'Mainhand' in v.stats['slot']]
list_of_offhand = [k for k, v in gear_dict.items() if 'Offhand' in v.stats['slot']]
list_of_head = [k for k, v in gear_dict.items() if 'Head' in v.stats['slot']]
list_of_body = [k for k, v in gear_dict.items() if 'Body' in v.stats['slot']]
list_of_legs = [k for k, v in gear_dict.items() if 'Legs' in v.stats['slot']]
list_of_hands = [k for k, v in gear_dict.items() if 'Hands' in v.stats['slot']]
list_of_feet = [k for k, v in gear_dict.items() if 'Feet' in v.stats['slot']]
list_of_ring = [k for k, v in gear_dict.items() if 'Ring' in v.stats['slot']]
list_of_common_gear = [k for k, v in gear_dict.items() if v.tier == 1]

consumable_dict = {}
# # hotkey, name, value, melee_atk, magic_atk, poison_atk, hp_regen, mp_regen
# potion = Consumable('potion', 1, 14, hp_regen=25)
# ether = Consumable('ether', 1, 14, mp_regen=8)
# elixir = Consumable('elixir', 2, 58, mp_regen=48)

bait_dict = {}
# ilan_berries = Bait('ilan berries', 1, 2)
# thread_worms = Bait('thread worms', 1, 2)

list_of_common_items = []

list_of_bait = []

# herring = Item('herring', 1, 6)
# salmon = Item('salmon', 1, 6)
#
# logs = Item('logs', 1, 2)
# worn_hatchet = Tool('worn hatchet', 1, 4, 20)
