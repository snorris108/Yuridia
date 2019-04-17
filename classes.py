
from abilities import *
from items import *


class Char:
    """
    This is our hero class. I still think I need to change how the program handles equipped gear as
    an inventory, rather than individual attributes. Granted, this 'gear inventory' won't ever get as large
    as the standard inventory so won't scale much, but aligning types feels cleaner, and may save lines.
    inventory - list
    abilities - dictionary
    ability bar - dictionary
    equipment - dictionary
    """

    def __init__(self, stats, inventory, abilities, ability_bar, equipment,
                 xpos=0, ypos=0, can_move=5, name=''):
        self.stats = stats
        self.inventory = inventory
        self.abilities = abilities
        self.ability_bar = ability_bar
        self.equipment = equipment
        self.xpos = xpos
        self.ypos = ypos
        self.dist = 0
        self.can_move = can_move
        self.dist = math.floor(math.sqrt(xpos ** 2 + ypos ** 2))  # determines mob difficulty
        self.name = name
        self.gold = 0


    def level_up(self):
        """
        This method processes attribute updates associated with leveling up.
        :return: The printed display showing new hero base stats[
        """
        levels_gained = 0
        while self.stats['xp'] > self.stats['next_level_at']:
            self.stats['prev_level_xp'] = self.stats['next_level_at']
            difference = (math.floor(self.stats['level'] - 1 + 300 * (2 ** ((self.stats['level'] - 1) / 7)))) / 4
            self.stats['next_level_at'] = self.stats['prev_level_xp'] + difference
            levels_gained += 1
            self.stats['level'] += 1

        self.stats['hp_current'] += self.stats['hp_base'] * 0.05 * levels_gained
        self.stats['hp_base'] += (42 * 1.05) * levels_gained
        self.stats['melee_base_atk'] += 4 * levels_gained
        self.stats['mp_base'] += 6 * levels_gained
        self.stats['magic_base_atk'] += 3 * levels_gained
        self.can_move += 1  # may need to adjust this number. Currently linear.

        # FORMAT: LEVEL-UP NOTIFICATION
        print('-' * 25,
              '\n', "Your strength increases.",
              '\n', f"You've gained {levels_gained} level{'s' if levels_gained > 1 else ''}.",
              '\n', '-' * 25,
              '\n', f"{'Level: ':8}{self.stats['level']}",
              '\n', f"{'Health: ':8}",
              f"{str(math.floor(self.stats['hp_current']))}/{str(math.floor(self.stats['hp_base']))}",
              '\n', f"{'Mana: ':8}",
              f"{str(math.floor(self.stats['mp_current']))}/{str(math.floor(self.stats['mp_base']))}",
              '\n', f"{'Attack: ':8}{self.stats['melee_base_atk']}",
              '\n', f"{'M. Attack: ':8}{self.stats['magic_base_atk']}", sep='')

    def display_inventory(self):
        # HEADER
        gold_padding = ' ' * (60 - 17 - len(str(self.gold)))
        print(f"{'Inventory: '}{gold_padding}{'Gold: '}{self.gold}",
              '\n', '----+' * 12, sep='')
        # ITEM LIST
        for item in self.inventory:
            if isinstance(item, Gear):
                print(f"{'':4}{'  '}{item.name:14}{item.value:>8}", sep='')
            else:
                print(f"{item.quantity:4}{'  '}{item.name:14}{item.value:>8}")
        if not self.inventory:
            print("Your backpack is empty.")
        print('----+' * 12)

    def display_character_sheet(self):
        xp_bar_fill = int((1 - ((self.stats['next_level_at'] - self.stats['xp']) /
                           (self.stats['next_level_at'] - self.stats['prev_level_xp']))) * 35)
        padding = ' ' * (60 - len(str(self.stats['race'] + ' (Level ' + str(self.stats['level']) + ')')) - 2 - 35)
        hp_regen_fmt = ''
        mp_regen_fmt = ''
        melee_boost_fmt = ''
        magic_boost_fmt = ''
        if self.stats['hp_regen'] != 0:
            hp_regen_fmt = f"{' (^'}{str(int(self.stats['hp_regen']))}{'^)'}"
        if self.stats['mp_regen'] != 0:
            mp_regen_fmt = f"{' (^'}{str(int(self.stats['mp_regen']))}{'^)'}"
        if self.stats['melee_boost'] != 0:
            melee_boost_fmt = f"{' (+'}{str(int(self.stats['melee_boost']))}{')'}"
        if self.stats['magic_boost'] != 0:
            magic_boost_fmt = f"{' (+'}{str(int(self.stats['magic_boost']))}{')'}"
        gold_padding = ' ' * (60 - 17 - 6 - len(self.name) - len(str(self.gold)))
        
        print(f"{'Character sheet: ':16}{self.name}{gold_padding}{'Gold: ':>}{self.gold:>}",
              '\n',
              '----+' * 12,
              '\n',
              f"{str(self.stats['race'])}{' (Level '}{str(self.stats['level'])}{')'}{padding}"
              f"{'['}{'='* xp_bar_fill:35}{']'}",
              '\n',
              f"{'Health: ':>15}{'   '}", "{:>14}{:<}".format(
                str(int(self.stats['hp_current'])) + '/' + str(int(self.stats['hp_base'])), hp_regen_fmt),
              '\n',
              f"{'Mana: ':>15}{'   '}", "{:>14}{:<}".format(
                str(self.stats['mp_current']) + '/' + str(self.stats['mp_base']), mp_regen_fmt),
              '\n',
              f"{'Attack: ':>15}{'   '}{self.stats['melee_base_atk']:>14}{melee_boost_fmt:<}",
              '\n',
              f"{'M. Attack: ':>15}{'   '}{self.stats['magic_base_atk']:>14}{magic_boost_fmt:<}", sep='')
        print('-' * 60)
        self.display_gear_equipped('while viewing character sheet')
        print('----+' * 12)
        self.display_ability_bar()
        print('\n')

    def display_gear_equipped(self, context):
        """
        Prints all gear slots to the screen
        :param context: determines presence of hotkeys for selection
        """
        hotkey = 1
        for k, v in self.equipment.items():
            hotkey_fmt = f'[{str(hotkey)}]' if context in ['during unequip', 'weaponsmith'] else ''
            ohAtkPenalty = 0.7 if k == 'Offhand' else 1
            if v:
                melatk = int(v.melee_boost * ohAtkPenalty)
                melee_atk_fmt = '' if melatk == 0 else f"(/{str(melatk)})"
                magatk = int(v.magic_boost * ohAtkPenalty)
                magic_atk_fmt = '' if magatk == 0 else f"(*{str(magatk)})"
                hp_regen = int(v.hp_regen)
                hp_regen_fmt = '' if hp_regen == 0 else f"(^{str(hp_regen)}^hp)"
                mp_regen = int(v.mp_regen)
                mp_regen_fmt = '' if mp_regen == 0 else f"(^{str(mp_regen)}^mp)"

                print(f"{hotkey_fmt:4}{k + ': ':>11}{v.name:14}{melee_atk_fmt}{magic_atk_fmt}{hp_regen_fmt}"
                      f"{mp_regen_fmt}")
            else:
                print(f"{'':4}{k:>9}{'-----':^15}")
            hotkey += 1

    def equip(self):
        # HEADER
        gear_list = self.get_list_of_all(Gear, 'from gear')
        if gear_list:
            print('-' * 60)
            self.display_gear_equipped('during equip')
            print('-' * 60)
            self.display_item_list(Gear, 'from gear', gear_list)
            print('-' * 60)
            choice = input('What would you like to equip? ([Enter]-cancel)\n')
            # ITEM LIST
            for index, gear_instance in enumerate(gear_list):
                if choice == str(index + 1):
                    if 'Offhand' in gear_instance.slot:
                        slot_options_dict = {'Mainhand': '1', 'Offhand': '2'}
                        slot_options_choice = input('[1] - Mainhand  |  [2] - Offhand\n')
                        for k, v in slot_options_dict.items():
                            if v == slot_options_choice:
                                if self.equipment[k]:
                                    self.unequipping(k, self.equipment[k])
                                self.equipping(gear_instance, slot_options_choice)
                                self.equipment[k] = gear_instance
                    else:
                        for k, v in self.equipment.items():
                            if k in gear_instance.slot:
                                if self.equipment[k]:
                                    self.unequipping(k, self.equipment[k])
                                self.equipping(gear_instance, gear_instance.slot)
                                self.equipment[k] = gear_instance
        else:
            print("You don't have any gear.")

    def unequip(self):
        print('-' * 60)
        self.display_gear_equipped('during unequip')
        print('-' * 60)
        print("Which slot would you like to unequip? ([Enter]-cancel)")
        value_choice = input()

        key_chose = ''
        pairs = {'Mainhand': '1', 'Offhand': '2', 'Head': '3', 'Body': '4',
                 'Legs': '5', 'Hands': '6', 'Feet': '7', 'Ring': '8'}
        for k, v in pairs.items():
            if v == value_choice:
                key_chose = k
        for k, v in self.equipment.items():
            if key_chose == k:
                if self.equipment[k]:
                    self.unequipping(k, v)
                else:
                    print("You have nothing equipped there.")

    def unequipping(self, equipping_str, unequipping_obj):
        self.inventory.append(unequipping_obj)
        ohAtkPenalty = 0.7 if equipping_str == 'Offhand' else 1
        self.stats['melee_boost'] -= unequipping_obj.melee_boost * ohAtkPenalty
        self.stats['magic_boost'] -= unequipping_obj.magic_boost * ohAtkPenalty
        self.stats['hp_regen'] -= unequipping_obj.hp_regen
        self.stats['mp_regen'] -= unequipping_obj.mp_regen
        self.equipment[equipping_str] = ''
        print(f"You unequip your {unequipping_obj.name}.")

    def equipping(self, equipping_obj, slot_option_choice):
        ohAtkPenalty = 0.7 if slot_option_choice == '2' else 1
        self.stats['melee_boost'] += equipping_obj.melee_boost * ohAtkPenalty
        self.stats['magic_boost'] += equipping_obj.magic_boost * ohAtkPenalty
        self.stats['hp_regen'] += equipping_obj.hp_regen
        self.stats['mp_regen'] += equipping_obj.mp_regen
        self.inventory.remove(equipping_obj)
        print(f"You equip your {equipping_obj.name}.")

    def ability_to_bar(self):
        enumerated_abilities = {k: v for k, v in zip(range(1, len(self.abilities) + 1), self.abilities)}
        print("Learned Abilities:")
        print('-' * 30,
              '\n', ' Hotkey',
              '\n', '-' * 8, sep='')
        for index, ability in enumerated_abilities.items():
            hotkey_fmt = f"[{index}]"
            print(f"  {hotkey_fmt:6}{ability}")
        print('-' * 30)
        choice = input("Enter the hotkey to select an ability to add. ([Enter]-cancel)\n")
        if choice.isdigit():
            choice = int(choice)
            if choice in enumerated_abilities.keys():
                print("Add to which slot?")
                self.display_ability_bar()
                slot_choice = input()
                self.ability_bar[slot_choice] = enumerated_abilities[choice]
                print('\n' * 80)
                print("You add ", enumerated_abilities[choice], " to your bar.", sep='')

    def learn_ability(self, ability):
        self.abilities.append(ability)
        self.abilities = sorted(self.abilities, key=lambda x: ability_weights[x])
        print(f"You've learned {ability}. Access your abilities with [A].")

    def display_ability_bar(self):
        joint = '}-{'
        count = 0

        print("    1         2         3         4         5         6\n{", end='')
        for k, v in self.ability_bar.items():
            count += 1
            print(f"{v:^7}", end='') if self.ability_bar[k] else print('       ', end='')
            if count < 6:
                print(joint, end='')
        print('}')

    def chug(self):
        consumables_list = []
        count = 1
        for i in self.inventory:
            if isinstance(i, Consumable):
                hotkeyid = count
                consumables_list.append([i, hotkeyid])
                count += 1
        print("Consumables: ",
              '\n', '-' * 30, sep='')

        if consumables_list:
            print(f"{'':6}{'Type':15}{'Quantity':>}")
            for i in consumables_list:
                hotkey = f"[{str(i[1])}]"
                cons_type = i[0].name
                quantity = f"({str(i[0].quantity)})"
                padding = ' ' * (30 - 6 - len(cons_type) - 8)
                print(f"{hotkey:6}{cons_type}{padding}{quantity:8}")
            print('-' * 30, sep='')
            choice = input("What would you like to consume?\n")

            for i in consumables_list:
                if choice[0] == str(i[1]):
                    for _ in choice:  # allows consuming multiple items at once
                        if i[0] in self.inventory:
                            print(f"You drink the {i[0].name}.")
                            self.stats['hp_current'] = self.stats['hp_current'] + i[0].hp_regen
                            self.mp_current = self.mp_current + i[0].mp_regen
                            if i[0].hp_regen:
                                print("You now have", math.floor(self.stats['hp_current']), "hp.")
                            if i[0].mp_regen:
                                print("You gain", i[0].mp_regen, "mp.")
                            i[0].quantity -= 1
                            if i[0].quantity == 0:
                                self.inventory.remove(i[0])
                        else:
                            print("You have 0 ", i[0].name, ".", sep='')
        else:
            print("You have nothing to consume.",
                  '\n', '-' * 30, sep='')

    def get_list_of_all(self, class_type, context):
        item_list = []
        if context == "unequipping":
            for gear in self.equipment.values():
                item_list.append(gear)
        elif context == "weaponsmith":
            for item in self.inventory:
                if isinstance(item, Gear):
                    if "Mainhand" in item.slot or "Offhand" in item.slot:
                        item_list.append(item)
        else:
            for item in self.inventory:
                if isinstance(item, class_type):
                    item_list.append(item)
        # SORTS the list by total damage, then by total regen.
        item_list.sort(key=lambda k: (k.melee_boost + k.magic_boost), reverse=True)
        return item_list

    def display_item_list(self, class_type, context, item_list):
        if item_list:
            if context in ["weaponsmith", "armorsmith", "apothecary"]:
                print("Selling:",
                      '\n', '----+' * 13, sep='')
                if class_type == Gear:
                    print(f"{'      ':6}{'Type':20}{'Damage':^16}{'Effect':^15}{'Value':^8}")
                else:
                    print(f"{'':6}{'Type':14}")
            else:
                print(f"{class_type.__name__}: ")
                if class_type == Gear:
                    print(f"{'':<6}{'Name':<20}{'Damage':^15}{'Effect':^15}{'Value':^8}")

            for index, item in enumerate(item_list):
                hotkey = f"[{index + 1}]"
                if class_type == Gear:
                    value = item.value if context in ['weaponsmith', 'armorsmith', 'apothecary'] else ''
                    atk_str = f"(/{str(item.melee_boost)}) " if item.melee_boost else ''
                    if item.magic_boost:
                        atk_str += f"(*{str(item.magic_boost)})"
                    regen_str = f"(^{str(item.hp_regen)}^hp)" if item.hp_regen else ''
                    if item.mp_regen:
                        regen_str += f"(^{str(item.mp_regen)}^mp)"
                    print(f"{hotkey:<6}{item.name:<20}{atk_str:^15}{regen_str:^15}{value:>8}")

    def regen(self, context):
        increment = 3 if context == "roaming" else 1
        if self.stats['mp_current'] < self.stats['mp_base']:
            self.stats['mp_current'] = \
                min(self.stats['mp_current'] + increment + self.stats['mp_regen'], self.stats['mp_base'])
        if self.stats['hp_current'] < self.stats['hp_base']:
            self.stats['hp_current'] = \
                min(self.stats['hp_current'] + self.stats['hp_regen'], self.stats['hp_base'])

    def view_location(self):
        return f"({str(self.xpos)}, {str(self.ypos)})"


class Mob:
    def __init__(self, stats, loot, abilities):
        self.stats = stats
        self.init_stats = stats.copy()
        self.loot = loot
        self.abilities = abilities
        self.inventory = []

    def equip(self):
        chance = {i: random.uniform(0, 1) for i in range(1, 9)}
        pack = {1: Gear(*random.choice([i for i in list_of_gear if 'Mainhand' in i[4]])),
                2: Gear(*random.choice([i for i in list_of_gear if 'Offhand' in i[4]])),
                3: Gear(*random.choice([i for i in list_of_gear if 'Head' in i[4]])),
                4: Gear(*random.choice([i for i in list_of_gear if 'Body' in i[4]])),
                5: Gear(*random.choice([i for i in list_of_gear if 'Legs' in i[4]])),
                6: Gear(*random.choice([i for i in list_of_gear if 'Hands' in i[4]])),
                7: Gear(*random.choice([i for i in list_of_gear if 'Feet' in i[4]])),
                8: Gear(*random.choice([i for i in list_of_gear if 'Ring' in i[4]]))}
        for index, odds in chance.items():
            if odds < 0.1:
                self.inventory.append(pack[index])
                self.equipping(pack[index])

    def equipping(self, equipping_obj):
        self.stats['melee_boost'] += equipping_obj.melee_boost
        self.stats['magic_boost'] += equipping_obj.magic_boost
        self.stats['hp_regen'] += equipping_obj.hp_regen
        self.stats['mp_regen'] += equipping_obj.mp_regen

    def regen(self):
        if self.stats['mp_current'] < self.stats['mp_base']:
            self.stats['mp_current'] = min(self.stats['mp_current'] + self.stats['mp_regen'], self.stats['mp_base'])
        if self.stats['hp_current'] < self.stats['hp_base']:
            self.stats['hp_current'] = min(self.stats['hp_current'] + self.stats['hp_regen'], self.stats['hp_base'])

    def plunder(self, hero):
        for gear in self.inventory:
            print(gear.name, "looted!")
            hero.inventory.append(gear)
        for _list in self.loot:
            for item in _list:
                chance = random.uniform(0, 1)
                if chance > 0.95:
                    if item not in hero.inventory:
                        hero.inventory.append(item)
                    quantity_looted = 1
                    if isinstance(item, Item):
                        quantity_looted = random.randint(8, 12)
                    item.quantity += quantity_looted
                    print(f"You have looted {quantity_looted} {item.name}.")

    def death(self, hero):
        hero.stats['xp'] += self.stats['xp_worth']
        print(f"You have slain the {self.stats['race']}!")
        self.plunder(hero)
        if hero.stats['xp'] > hero.stats['next_level_at']:
            hero.level_up()


def create_mob(race, hp_current, hp_base, hp_regen, mp_current, mp_base, mp_regen, melee_base_atk, melee_boost,
               melee_affinity, magic_base_atk, magic_boost, magic_affinity, level, xp_worth, loot, abilities):
    return Mob({'race': race,
                'hp_current': hp_current,
                'hp_base': hp_base,
                'hp_regen': hp_regen,
                'mp_current': mp_current,
                'mp_base': mp_base,
                'mp_regen': mp_regen,
                'melee_base_atk': melee_base_atk,
                'melee_boost': melee_boost,
                'melee_affinity': melee_affinity,
                'magic_base_atk': magic_base_atk,
                'magic_boost': magic_boost,
                'magic_affinity': magic_affinity,
                'level': level,
                'xp_worth': xp_worth},
               loot, abilities)


def player():
    return Char({'race': 'human',
                 'hp_current': 200,
                 'hp_base': 200,
                 'hp_regen': 0,
                 'mp_current': 10,
                 'mp_base': 10,
                 'mp_regen': 0,
                 'melee_base_atk': 14,
                 'melee_boost': 0,
                 'magic_base_atk': 25,
                 'magic_boost': 0,
                 'burden_current': 0,
                 'burden_limit': 20,
                 'level': 1,
                 'xp': 0,
                 'prev_level_xp': 0,
                 'next_level_at': 83},
                # INVENTORY     list
                [],
                # ABILITIES     set
                ['Strike', 'Heal', 'Combust'],
                # ABILITY BAR   dict
                {'1': 'Strike', '2': '', '3': '', '4': '', '5': '', '6': ''},
                # EQUIPMENT     dict
                {'Mainhand': '', 'Offhand': '', 'Head': '', 'Body': '', 'Legs': '', 'Hands': '', 'Feet': '',
                 'Ring': ''})


thief = \
    ['thief',               200, 200, 0, 10, 10, 0, 14, 0, 0.7, 8, 0, 0.2, 1, 12,
     [list_of_common_items, list_of_bait],
     {'Fire', 'Heal', 'Rush'}]
kaelas_boar = \
    ['Kaelas boar',         60, 60, 0, 4, 4, 0, 24, 0, 0.7, 4, 0, 0.2, 1, 8,
     [list_of_common_items],
     {'Heal', 'Rush'}]
wolves = \
    ['pack of wolves',      300, 300, 0, 10, 10, 0, 7, 0, 0.7, 0, 0, 0.2, 1, 14,
     [list_of_common_items],
     {'Strike'}]
cultist = \
    ['cultist',             200, 200, 10, 100, 100, 4, 8, 0, 0.7, 38, 0, 0.2, 1, 46,
     [list_of_common_items, list_of_bait],
     {'Fire', 'Fira', 'Firaga', 'Heal', 'Rush'}]
giant_kitty = \
    ['giant... kitty?',     3000, 3000, 0, 10, 10, 0, 75, 0, 0.7, 85, 0, 0.2, 1, 666,
     [list_of_common_items],
     {'Heal', 'Firaga'}]
kraken = ['Kraken',         5000, 5000, 0, 79, 79, 4, 72, 0, 0.35, 68, 0, 0.65, 1, 1247,
          [list_of_common_items],
          {'Fira', 'Firaga'}]

list_of_mobs = [thief, kaelas_boar, wolves, cultist]
list_of_bosses = [giant_kitty, kraken]
