
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

    def view_inventory(self):
        gold_padding = ' ' * (60 - 10 - 7 - len(self.name) - len(str(self.gold)))
        print(f"{'Inventory: '}{gold_padding}{'Gold: ':>}{self.gold:>}",
              '\n', '----+' * 12, sep='')
        for i in self.inventory:
            print(f"{i.quantity:4}{'  '}{i.name:14}{i.value:>8}", sep='')
            print('-' * 60, sep='')
        if not self.inventory:
            print("Your backpack is empty.")
        print('----+' * 12)

    def character_sheet(self):
        # FORMAT: CHARACTER SHEET
        xp_bar_fill = int((1 - ((self.stats['next_level_at'] - self.stats['xp']) /
                           (self.stats['next_level_at'] - self.stats['prev_level_xp']))) * 35)
        # print(f"var xp_bar_fill: {xp_bar_fill}")
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
            melee_boost_fmt = f"{' ( +'}{str(int(self.stats['melee_boost']))}{')'}"
        if self.stats['magic_boost'] != 0:
            magic_boost_fmt = f"{' ( +'}{str(int(self.stats['magic_boost']))}{')'}"
        gold_padding = ' ' * (60 - 16 - 10 - len(str(self.gold)))
        
        print(f"{'Character sheet: ':16}{self.name}{gold_padding}{'Gold: ':>}{self.gold:>}",
              '\n',
              '----+' * 12,
              '\n',
              f"{str(self.stats['race'])}{' (Level '}{str(self.stats['level'])}{')'}{padding}{'['}{'='* xp_bar_fill:35}"
              f"{']'}",
              '\n',
              f"{'Health: ':>15}{'   '}", "{:>14}{:<}".format(
                str(int(self.stats['hp_current'])) + '/' + str(int(self.stats['hp_base'])), hp_regen_fmt),
              '\n',
              f"{'Mana: ':>15}{'   '}", "{:>14}{:<}".format(
                str(self.stats['mp_current']) + '/' + str(self.stats['mp_base']), mp_regen_fmt),
              '\n',
              f"{'Attack: ':>15}{'   '}{self.stats['melee_base_atk']:>14}{melee_boost_fmt:<}",
              '\n',
              f"{'M. Attack: ':>15}{'   '}{self.stats['magic_base_atk']:>14}{magic_boost_fmt:<}",
              '\n',
              '-' * 60, sep='')
        self.menu_gear_equipped('while viewing character sheet')
        self.display_ability_bar()
        print('\n')

    def menu_gear_equipped(self, context):
        """
        This function formats the display of each occupied equipment slot, and adjusts for offhand damage penalty
        :param context: 'from character sheet' or 'during equip or unequip', to determine if it will display a hotkey
        :return:
        """

        hotkey = 1
        for k, v in self.equipment.items():
            hotkey_fmt = ''
            if context == 'while viewing character sheet':
                hotkey_fmt = ''
            elif context == 'during equip or unequip':
                hotkey_fmt = f'[{str(hotkey)}]'

            ohAtkPenalty = (0.7 if k == 'Offhand' else 1)
            if v:
                melatk = math.floor(v.stats['melee_boost'] * ohAtkPenalty)
                melee_atk_fmt = f'(/{str(melatk)})'
                if melatk == 0:
                    melee_atk_fmt = ''
                magatk = math.floor(v.stats['magic_boost'] * ohAtkPenalty)
                magic_atk_fmt = f'(*{str(magatk)})'
                if magatk == 0:
                    magic_atk_fmt = ''
                hp_regen = int(v.stats['hp_regen'])
                hp_regen_fmt = f'(^{str(hp_regen)}^ hp)'
                if hp_regen == 0:
                    hp_regen_fmt = ''
                mp_regen = int(v.stats['mp_regen'])
                mp_regen_fmt = f'(^{str(mp_regen)}^ mp)'
                if mp_regen == 0:
                    mp_regen_fmt = ''
                if context == 'weaponsmith':
                    k = ''
                print(f"{hotkey_fmt:4}{k + ': ':>11}{v.name:14}{melee_atk_fmt}{magic_atk_fmt}{hp_regen_fmt}"
                      f"{mp_regen_fmt}")
            else:
                print(f"{'':4}{k:>9}{'-----':^15}")
            hotkey += 1
        print('----+' * 12, sep='')

    def equip(self):
        gear_list = self.item_selection(Gear, "from gear")
        if gear_list:
            choice = input("What would you like to equip? ([Enter]-cancel)\n")
            for index, gear_item in enumerate(gear_list):
                if choice == str(index + 1):
                    if 'Offhand' in gear_item.stats['slot']:
                        slot_options_dict = {"Mainhand": '1', "Offhand": '2'}
                        slot_options_choice = input("[1] - Mainhand  |  [2] - Offhand\n")
                        for k, v in slot_options_dict.items():
                            if v == slot_options_choice:
                                if self.equipment[k]:
                                    self.unequip(k, self.equipment[k])
                                self.equipping(gear_item, slot_options_choice)
                                self.equipment[k] = gear_item
                    else:
                        for k, v in self.equipment.items():
                            if k in gear_item.stats['slot']:
                                if self.equipment[k]:
                                    self.unequip(k, self.equipment[k])
                                self.equipping(gear_item, gear_item.stats['slot'])
                                self.equipment[k] = gear_item
        else:
            print("You don't have any gear.")

    def unequip_direct(self):
        print("Which slot would you like to unequip? ([Enter]-cancel)",
              '\n', '-' * 60, sep='')
        self.menu_gear_equipped('during equip or unequip')
        slot_choice = input()
        slot_chose = ''
        pairs = {'Mainhand': '1', 'Offhand': '2', 'Head': '3', 'Body': '4',
                 'Legs': '5', 'Hands': '6', 'Feet': '7', 'Ring': '8'}
        for k, v in pairs.items():
            if v == slot_choice:
                slot_chose = k
        for k, v in self.equipment.items():
            if slot_chose == k:
                if self.equipment[k]:
                    self.unequip(k, v)
                else:
                    print("You have nothing equipped there.")

    def unequip(self, equipping_str, unequipping_obj):
        if unequipping_obj not in self.inventory:
            self.inventory.append(unequipping_obj)
        ohAtkPenalty = (0.7 if equipping_str == 'Offhand' else 1)
        self.stats['melee_boost'] -= unequipping_obj.stats['melee_boost'] * ohAtkPenalty
        self.stats['magic_boost'] -= unequipping_obj.stats['magic_boost'] * ohAtkPenalty
        self.stats['hp_regen'] -= unequipping_obj.stats['hp_regen']
        self.stats['mp_regen'] -= unequipping_obj.stats['mp_regen']
        self.equipment[equipping_str] = ''
        print(f"You unequip your {unequipping_obj.name}.")
        unequipping_obj.quantity += 1

    def equipping(self, equipping_obj, slot_option_choice):
        ohAtkPenalty = (0.7 if slot_option_choice == '2' else 1)
        self.stats['melee_boost'] += equipping_obj.stats['melee_boost'] * ohAtkPenalty
        self.stats['magic_boost'] += equipping_obj.stats['magic_boost'] * ohAtkPenalty
        self.stats['hp_regen'] += equipping_obj.stats['hp_regen']
        self.stats['mp_regen'] += equipping_obj.stats['mp_regen']
        equipping_obj.quantity -= 1
        if equipping_obj.quantity == 0:
            self.inventory.remove(equipping_obj)
        print(f"You equip your {equipping_obj.name}.")

    def view_abilities(self):
        enumerated_abilities = {k: v for k, v in zip(range(1, len(self.abilities) + 1), self.abilities)}
        print("Learned Abilities:")
        print('-' * 30,
              '\n', ' Hotkey',
              '\n', '-' * 8, sep='')
        for index, ability in enumerated_abilities.items():
            hotkey_fmt = f"[{index}]"
            print(f"  {hotkey_fmt:6}{ability}")
        print('-' * 30)
        choice = int(input("Enter the hotkey to select an ability to add. ([Enter]-cancel)\n"))
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

        #     if ability in self.abilities:
        #         abil_bar_disp[k] = ability
        #     for a, b in self.abilities.items():
        #         if self.abilities[a] == v:
        #             update
        #             abil_bar_disp[k] = a
        #
        # display updated
        # print("    1        2        3        4        5        6",
        #       '\n',
        #       f"{'{'}{abil_bar_disp['1']:^6}{joint}"
        #       f"{abil_bar_disp['2']:^6}{joint}"
        #       f"{abil_bar_disp['3']:^6}{joint}"
        #       f"{abil_bar_disp['4']:^6}{joint}"
        #       f"{abil_bar_disp['5']:^6}{joint}"
        #       f"{abil_bar_disp['6']:^6}{'}'}")

    def consumables(self):
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
                            self.stats['hp_current'] = self.stats['hp_current'] + i[0].stats['hp_regen']
                            self.stats['mp_current'] = self.stats['mp_current'] + i[0].stats['mp_regen']
                            if i[0].stats['hp_regen']:
                                print("You now have", math.floor(self.stats['hp_current']), "hp.")
                            if i[0].stats['mp_regen']:
                                print("You gain", i[0].stats['mp_regen'], "mp.")
                            i[0].quantity -= 1
                            if i[0].quantity == 0:
                                self.inventory.remove(i[0])
                        else:
                            print("You have 0 ", i[0].name, ".", sep='')
        else:
            print("You have no consumables.",
                  '\n', '-' * 30, sep='')

    def item_selection(self, class_type, context):
        item_list = []
        count = 1
        if context == "unequipping":
            for k, v in self.equipment.items():
                hotkeyid = count
                if v:
                    item_list.append(v)
                    count += 1
        elif context == "weaponsmith":
            for i in self.inventory:
                if isinstance(i, class_type):
                    if "Mainhand" in i.slot or "Offhand" in i.slot:
                        hotkeyid = count
                        item_list.append(i)
                        count += 1
        else:
            for i in self.inventory:
                if isinstance(i, class_type):
                    hotkeyid = count
                    item_list.append(i)
                    count += 1
        if item_list:
            # FORMAT THE INTERFACE
            if context in ["weaponsmith", "armorsmith", "apothecary"]:
                print("Selling:",
                      '\n', '----+' * 13, sep='')
                if class_type == Gear:
                    print(f"{'      ':6}{'Type':20}{'Damage':^16}{'Effect':^15}{'Value':^8}")
                elif class_type in [Consumable, Bait]:
                    print("{'':6}{'Type':15}{'Quantity':>}")
                else:
                    print(f"{'':6}{'Type':14}")
            else:
                print(class_type.__name__, ': ',
                      '\n',
                      '----+' * 13, sep='')
                if class_type == Gear:
                    print(f"{'':<6}{'Type':<20}{'Damage':^10}{'Effect':^20}{'Value':^8}")
                elif class_type in [Consumable, Bait]:
                    print(f"{'':6}{'Type':15}{'Quantity':>}")
                else:
                    print(f"{'':6}{'Type':14}")

            for index, i in enumerate(item_list):
                # if i[0]:  # checks for existence. Had trouble here while unequipping w/o this check.
                hotkey = f"[{index + 1}]"
                # name = i[0].name
                if class_type == Gear:
                    value = ''
                    if context in ['weaponsmith', 'armorsmith', 'apothecary']:
                        value = i.value
                    atk_str = ''
                    if i.stats['melee_boost']:
                        atk_str = f"({str(i.stats['melee_boost'])})"
                    elif i.stats['magic_boost']:
                        atk_str = f"({str(i.stats['magic_boost'])})"
                    regen_str = ''
                    if i.stats['hp_regen']:
                        regen_str = f"+ {str(i.stats['hp_regen'])} hp/turn"
                    if i.stats['mp_regen']:
                        regen_str = f"+ {str(i.stats['mp_regen'])} mp/turn"
                    print(f"{hotkey:<6}{i.name:<20}{atk_str:^10}{regen_str:^20}{value:>8}")
                elif class_type in [Consumable, Bait]:
                    print(f"{hotkey:6}{i.name:14}{i.quantity:^8}")
            print('----+' * 13, sep='')
        return item_list

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
        chance = {i: random.randint(1, 10) for i in range(1, 9)}
        pack = {1: random.choice(list_of_mainhand),
                2: random.choice(list_of_offhand),
                3: random.choice(list_of_head),
                4: random.choice(list_of_body),
                5: random.choice(list_of_legs),
                6: random.choice(list_of_feet),
                7: random.choice(list_of_hands),
                8: random.choice(list_of_ring)}
        for index, odds in chance.items():
            if odds < 2:
                self.inventory.append(pack[index])
                self.equipping(gear_dict[pack[index]])

    def equipping(self, equipping_obj):
        self.stats['melee_boost'] += equipping_obj.stats['melee_boost']
        self.stats['magic_boost'] += equipping_obj.stats['magic_boost']
        self.stats['hp_regen'] += equipping_obj.stats['hp_regen']
        self.stats['mp_regen'] += equipping_obj.stats['mp_regen']

    def regen(self):
        if self.stats['mp_current'] < self.stats['mp_base']:
            self.stats['mp_current'] = min(self.stats['mp_current'] + self.stats['mp_regen'], self.stats['mp_base'])

        if self.stats['hp_current'] < self.stats['hp_base']:
            self.stats['hp_current'] = min(self.stats['hp_current'] + self.stats['hp_regen'], self.stats['hp_base'])

    def plunder(self, hero):
        for i in self.inventory:
            print(gear_dict[i].name, "looted!")
            if gear_dict[i] not in hero.inventory:
                hero.inventory.append(gear_dict[i])
            gear_dict[i].quantity += 1
        for i in self.loot[0]:
            chance = random.randrange(1, 100)
            if chance > 95:
                if gear_dict[i] not in hero.inventory:
                    hero.inventory.append(gear_dict[i])
                quantity_looted = 1
                if isinstance(gear_dict[i], Bait):
                    quantity_looted = random.randint(8, 12)
                i.quantity += quantity_looted
                print("You have looted ", quantity_looted, ' ', i.name, '.', sep='')

    def death(self, hero):
        hero.stats['xp'] += self.stats['xp_worth']
        print(f"You have slain the {self.stats['race']}!")
        self.plunder(hero)
        if hero.stats['xp'] > hero.stats['next_level_at']:
            hero.level_up()
        del self


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


mob_dict = {'thief':        create_mob('thief', 200, 200, 0, 10, 10, 0, 14, 0, 0.7, 8, 0, 0.2, 1, 12,
                                       [list_of_common_items, list_of_bait],
                                       {'Fire', 'Heal', 'Rush'}),
            'kaelas_boar':  create_mob('Kaelas boar', 60, 60, 0, 4, 4, 0, 24, 0, 0.7, 4, 0, 0.2, 1, 8,
                                       list_of_common_items,
                                       {'Heal', 'Rush'}),
            'wolves':       create_mob('pack of wolves', 300, 300, 0, 10, 10, 0, 7, 0, 0.7, 0, 0, 0.2, 1, 14,
                                       list_of_common_items,
                                       {'Strike'}),
            'cultist':      create_mob('cultist', 200, 200, 10, 100, 100, 4, 8, 0, 0.7, 38, 0, 0.2, 1, 46,
                                       [list_of_common_items, list_of_bait],
                                       {'Fire', 'Fira', 'Firaga', 'Heal', 'Rush'}),
            }


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


list_of_mobs = [k for k, v in mob_dict.items()]


def giant_kitty():
    return Mob({'race': 'giant....kitty?',
                'hp_current': 3000,
                'hp_base': 3000,
                'hp_regen': 0,
                'mp_current': 10,
                'mp_base': 10,
                'mp_regen': 0,
                'melee_base_atk': 75,
                'melee_boost': 0,
                'melee_affinity': 0.7,
                'magic_base_atk': 85,
                'magic_boost': 0,
                'magic_affinity': 0.2,
                'level': 1,
                'xp_worth': 666},
               [list_of_common_items],
               {'Heal', 'Firaga'})


def kraken():
    return Mob({'race': 'Kraken',
                'hp_current': 5000,
                'hp_base': 5000,
                'hp_regen': 0,
                'mp_current': 79,
                'mp_base': 79,
                'mp_regen': 4,
                'melee_base_atk': 72,
                'melee_boost': 0,
                'melee_affinity': 0.35,
                'magic_base_atk': 68,
                'magic_boost': 0,
                'magic_affinity': 0.65,
                'level': 1,
                'xp_worth': 1247},
               [list_of_common_items],
               {'Fira', 'Firaga'})


list_of_bosses = [giant_kitty, kraken]
