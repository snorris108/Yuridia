
import random


class Gear:
    def __init__(self, name, value, tier, burden, dmg_style, slot,
                 melee_boost, magic_boost, poison_boost, hp_regen, mp_regen):
        self.name = name
        self.value = value
        self.init_value = value  # possibly not needed, value *= 1.083 for each enhance
        self.tier = tier
        self.burden = burden
        self.dmg_style = dmg_style
        self.slot = slot
        # can enhance scalars < 1 at a smith
        self.melee_boost_scalar = random.choice([0.5, 0.75, 1])
        self.magic_boost_scalar = random.choice([0.5, 0.75, 1])
        self.hp_regen_scalar = random.choice([0.5, 0.75, 1])
        self.mp_regen_scalar = random.choice([0.5, 0.75, 1])
        # base stats for reference when applying modification
        self.init_melee = melee_boost
        self.init_magic = magic_boost
        self.init_hp_regen = hp_regen
        self.init_mp_regen = mp_regen
        # stats with boosts applied
        self.melee_boost = int(self.init_melee * self.melee_boost_scalar)
        self.magic_boost = int(self.init_magic * self.magic_boost_scalar)
        self.hp_regen = int(self.init_hp_regen * self.hp_regen_scalar)
        self.mp_regen = int(self.init_mp_regen * self.mp_regen_scalar)
        self.poison_boost = poison_boost
        self.durability = 100 * random.choice([0.5, 0.75, 1])
        self.fully_enhanced = False
        if self.melee_boost_scalar + self.magic_boost_scalar \
                + self.hp_regen_scalar + self.mp_regen_scalar == 4:
            self.fully_enhanced = True
            self.name = '*' + name
            self.value = int(value * 1.6)
        self.default_name = name



class Item:
    def __init__(self, name, value, _type=None, quantity=0):
        self.name = name
        self.value = value
        self._type = _type
        self.quantity = quantity


class Consumable(Item):
    def __init__(self, name, value, hp_gain, mp_gain,
                 melee_boost, magic_boost, xp_worth, _type=None, quantity=0):
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


# name, value, tier, burden, dmg_style, slot,       melee_boost, magic_boost, poison_boost, hp_regen, mp_regen
small_dagger = ['small dagger',     4, 1, 1, 'melee', ['Mainhand', 'Offhand'],          8, 0, 0, 0, 0]
ilorian_dagger = ['Ilorian dagger', 6, 1, 1, 'melee', ['Mainhand', 'Offhand'],          12, 0, 0, 0, 0]
ilorian_shortsword = ['Ilorian shortsword', 10, 1, 1, 'melee', ['Mainhand', 'Offhand'], 14, 0, 0, 0, 0]
ilorian_longsword = ['Ilorian longsword', 16, 1, 2, 'melee', ['Mainhand', 'Offhand'],   24, 0, 0, 0, 0]
ilorian_claymore = ['Ilorian claymore', 24, 1, 4, 'melee', ['Mainhand', 'Offhand'],     32, 0, 0, 0, 0]
flanged_mace = ['flanged mace',     14, 1, 2, 'melee', ['Mainhand', 'Offhand'],         14, 0, 0, 0, 0]
spiked_mace = ['spiked mace',       14, 1, 2, 'melee', ['Mainhand', 'Offhand'],         16, 0, 0, 0, 0]
blessed_mace = ['blessed mace',     18, 1, 2, 'melee', ['Mainhand', 'Offhand'],         4, 12, 0, 0, 0]
scimitar = ['scimitar',             16, 1, 2, 'melee', ['Mainhand', 'Offhand'],         20, 0, 0, 0, 0]
rapier = ['rapier',                 18, 1, 1, 'melee', ['Mainhand', 'Offhand'],         18, 0, 0, 0, 0]
gladius = ['gladius',               28, 1, 2, 'melee', ['Mainhand', 'Offhand'],         24, 0, 0, 0, 0]
kings_blade = ["King's Blade",      26, 3, 6, 'melee', ['Mainhand', 'Offhand'],         26, 0, 0, 8, 0]
ilan_branch = ['ilan branch',       1, 1, 1, 'magic', ['Mainhand', 'Offhand'],          0, 7, 0, 0, 1]
wand = ['wand',                     16, 1, 1, 'magic', ['Mainhand', 'Offhand'],         0, 16, 0, 0, 1]
targe = ['targe',                   10, 1, 2, 'melee, defense', ['Offhand'],            5, 0, 0, 0, 0]
glimmering_orb = ['glimmering orb', 36, 1, 1, 'magic', ['Offhand'],                     0, 8, 0, 0, 6]
leather_cap = ['leather cap',       8, 1, 1, 'melee, defense', ['Head'],                0, 0, 0, 3, 0]
heavy_tunic = ['heavy tunic',       8, 1, 8, 'defense', ['Body'],                       5, 0, 0, 2, 0]
thick_chaps = ['thick chaps',       16, 1, 6, 'defense', ['Legs'],                      4, 0, 0, 2, 0]
iron_gloves = ['iron gloves',       10, 1, 2, 'defense', ['Hands'],                     2, 0, 0, 0, 0]
cut_boots = ['cut boots',           10, 1, 2, 'defense', ['Feet'],                      2, 0, 0, 0, 0]
old_ring = ['old ring',             28, 3, 1, 'magic', ['Ring'],                        0, 6, 0, 0, 1]
clay_ring = ['clay ring',           22, 1, 1, 'melee', ['Ring'],                        6, 0, 0, 7, 0]
crooked_staff = ['crooked staff',   24, 1, 2, 'magic', ['Mainhand', 'Offhand'],         0, 15, 0, 0, 2]

list_of_gear = [small_dagger, scimitar, kings_blade, ilan_branch, wand, targe, glimmering_orb, leather_cap, heavy_tunic,
                thick_chaps, iron_gloves, cut_boots, old_ring, clay_ring, crooked_staff]

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
