
import random


class Gear:
    def __init__(self, name, value, tier, dmg_style, slot, melee_boost, magic_boost, poison_boost, hp_regen, mp_regen):
        self.name = name
        self.value = value
        self.tier = tier
        self.dmg_style = dmg_style
        self.slot = slot
        # can reforge scalars < 1 at a smith
        self.melee_boost_scalar = 1 * random.choice([0.5, 0.75, 1])
        self.magic_boost_scalar = 1 * random.choice([0.5, 0.75, 1])
        self.hp_regen_scalar = 1 * random.choice([0.5, 0.75, 1])
        self.mp_regen_scalar = 1 * random.choice([0.5, 0.75, 1])
        self.melee_boost = int(melee_boost * self.melee_boost_scalar)
        self.magic_boost = int(magic_boost * self.magic_boost_scalar)
        self.poison_boost = poison_boost
        self.hp_regen = int(hp_regen * self.hp_regen_scalar)
        self.mp_regen = int(mp_regen * self.mp_regen_scalar)
        self.durability = 100 * random.choice([0.5, 0.75, 1])
        self.default_name = name


class Item:
    def __init__(self, name, value, _type=None, quantity=0):
        self.name = name
        self.value = value
        self._type = _type
        self.quantity = quantity


class Consumable(Item):
    def __init__(self, name, value, hp_gain, mp_gain, melee_boost, magic_boost, xp_worth, _type=None, quantity=0):
        super().__init__(name, value, _type, quantity)
        self.hp_gain = hp_gain
        self.mp_gain = mp_gain
        self.melee_boost = melee_boost
        self.magic_boost = magic_boost
        self.xp_worth = xp_worth


class Tool(Item):
    def __init__(self, name, stats, value, quantity=0):
        super().__init__(name, value, quantity)
        self.stats = stats
        # self.durability = durability


small_dagger = ['small dagger', 10, 1, 'melee', ['Mainhand', 'Offhand'],    12, 0, 0, 0, 0]
scimitar = ['scimitar', 16, 1, 'melee', ['Mainhand', 'Offhand'],            20, 0, 0, 0, 0]
kings_blade = ["King's Blade", 26, 3, 'melee', ['Mainhand', 'Offhand'],     25, 0, 0, 0, 0]
ilan_branch = ['ilan branch', 1, 1, 'magic', ['Mainhand', 'Offhand'],       0, 7, 0, 0, 1]
wand = ['wand', 16, 1, 'magic', ['Mainhand', 'Offhand'],                    0, 20, 0, 0, 2]
targe = ['targe', 10, 1, 'melee, defense', ['Offhand'],                     5, 0, 0, 0, 0]
glimmering_orb = ['glimmering orb', 36, 1, 'magic', ['Offhand'],            0, 8, 0, 0, 6]
leather_cap = ['leather cap', 8, 1, 'melee, defense', ['Head'],             0, 0, 0, 3, 0]
heavy_tunic = ['heavy tunic', 8, 1, 'defense', ['Body'],                    5, 0, 0, 2, 0]
thick_chaps = ['thick chaps', 16, 1, 'defense', ['Legs'],                   4, 0, 0, 2, 0]
iron_gloves = ['iron gloves', 10, 1, 'defense', ['Hands'],                  2, 0, 0, 0, 0]
cut_boots = ['cut boots', 10, 1, 'defense', ['Feet'],                       2, 0, 0, 0, 0]
old_ring = ['old ring', 28, 3, 'magic', ['Ring'],                           0, 14, 0, 0, 7]
clay_ring = ['clay ring', 22, 1, 'melee', ['Ring'],                         14, 0, 0, 7, 0]
crooked_staff = ['crooked staff', 24, 1, 'magic', ['Mainhand', 'Offhand'],  0, 15, 0, 0, 4]

list_of_gear = [small_dagger, scimitar, kings_blade, ilan_branch, wand, targe, glimmering_orb, leather_cap, heavy_tunic,
                thick_chaps, iron_gloves, cut_boots, old_ring, clay_ring, crooked_staff]

# I think it's safe to call these objects at the top of execution, since they are static (only quantity changes)
potion = Consumable('potion', 14, 100, 0, 0, 0, 0)
ether = Consumable('ether', 21, 0, 18, 0, 0, 0)
elixir = Consumable('elixir', 58, 0, 48, 0, 0, 0)
beer = Consumable('beer', 12, 45, 18, 0, 0, 100)

ilan_berries = Item('ilan berries', 4, 'bait')
thread_worms = Item('thread worms', 4, 'bait')

# herring = Item('herring', 1, 6)
# salmon = Item('salmon', 1, 6)
#
# logs = Item('logs', 1, 2)
# worn_hatchet = Tool('worn hatchet', 1, 4, 20)


list_of_consumables = [potion, ether, elixir, beer]
list_of_bait = [ilan_berries, thread_worms]
list_of_common_items = []
list_of_common_items.extend(list_of_consumables)
list_of_common_items.extend(list_of_bait)
