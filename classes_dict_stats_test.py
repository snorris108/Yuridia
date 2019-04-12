from abilities_test import *

import math
import random


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
        self.message = ''  # what was this for?
        self.xpos = xpos
        self.ypos = ypos
        self.dist = 0
        self.can_move = can_move
        self.dist = math.floor(math.sqrt(xpos ** 2 + ypos ** 2))  # determines mob difficulty
        self.name = name


    def level_up(self):
        """
        This method processes attribute updates associated with leveling up.
        :return: The printed display showing new hero base stats[
        """
        levels_gained = 0
        difference = 0
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
              '\n', "You've gained ", levels_gained, " level", ("s" if levels_gained > 1 else ""), ".",
              '\n', '-' * 25,
              '\n', f"{'Level: ':8}{self.stats['level']}",
              '\n', f"{'Health: ':8}",
              f"{str(math.floor(self.stats['hp_current']))}/{str(math.floor(self.stats['hp_base']))}",
              '\n', f"{'Mana: ':8}",
              f"{str(math.floor(self.stats['mp_current']))}/{str(math.floor(self.stats['mp_base']))}",
              '\n', f"{'Attack: ':8}{self.stats['melee_base_atk']}",
              '\n', f"{'M. Attack: ':8}{self.stats['magic_base_atk']}", sep='')

    def view_inventory(self):
        gold_padding = ' ' * (60 - 10 - 7 - len(self.name) - len(str(gold.quantity)))
        print(f"{'Inventory: '}{gold_padding}{'Gold: ':>}{gold.quantity:>}",
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
        gold_padding = ' ' * (60 - 16 - 10 - len(str(gold.quantity)))
        
        print(f"{'Character sheet: ':16}{self.name}{gold_padding}{'Gold: ':>}{gold.quantity:>}",
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
        self.load_ability_bar_display('while viewing character sheet')
        print('\n')

    def menu_gear_equipped(self, context):
        """
        This function formats the display of each occupied equipment slot, and adjusts for offhand damage penalty
        :param context: 'from character sheet' or 'during equip or unequip', to determine if it will display a hotkey
        :return:
        """
        padding = '    '
        hotkey = 1
        for k, v in self.equipment.items():  # k - string, v - object
            if v:
                ohAtkPenalty = 1
                hotkey_fmt = ''
                if context == 'while viewing character sheet':
                    hotkey_fmt = ''
                if context == "during equip or unequip":
                    hotkey_fmt = '[' + str(hotkey) + ']'
                if k == 'Offhand':
                    ohAtkPenalty = 0.70
                melatk = math.floor(v.melee_atk * ohAtkPenalty)
                melee_atk_fmt = '(/ ' + str(melatk) + ')'
                if melatk == 0:
                    melee_atk_fmt = ''
                magatk = math.floor(v.magic_atk * ohAtkPenalty)
                magic_atk_fmt = '(* ' + str(magatk) + ')'
                if magatk == 0:
                    magic_atk_fmt = ''
                hp_regen = int(v.hp_regen)
                hp_regen_fmt = '(^' + str(hp_regen) + '^ hp)'
                if hp_regen == 0:
                    hp_regen_fmt = ''
                mp_regen = int(v.mp_regen)
                mp_regen_fmt = '(^' + str(mp_regen) + '^ mp)'
                if mp_regen == 0:
                    mp_regen_fmt = ''
                if context == "weaponsmith":
                    k = ''
                print(f"{hotkey_fmt:4}{k + ': ':>11}{v.name:14}{melee_atk_fmt}{magic_atk_fmt}{hp_regen_fmt}"
                      f"{mp_regen_fmt}")
            else:
                print(f"{padding:4}{k:>9}{'-----':^15}")
            hotkey += 1
        print('----+' * 12,
              sep='')

    def equip(self):
        list = self.item_selection(Gear, "from gear")
        if list:
            choice = input("What would you like to equip?\n")
            for i in list:
                if choice == str(i[1]):
                    if 'Offhand' in i[0].slot:
                        slot_options_dict = {"Mainhand": '1', "Offhand": '2'}
                        slot_options_choice = input("[1] - Mainhand  |  [2] - Offhand\n")
                        for k, v in slot_options_dict.items():  # k-str slot  v-str hotkey
                            if v == slot_options_choice:
                                if self.equipment[k]:
                                    self.unequip(k, self.equipment[k])
                                self.equipping(i[0], slot_options_choice)
                                self.equipment[k] = i[0]
                    else:  # we get here if we're equipping something that's not mainhand/offhand.
                        for k, v in self.equipment.items():  # k-str ('Body')   v-obj (tunic)
                            if k == i[0].slot:
                                if self.equipment[k]:
                                    self.unequip(k, self.equipment[k])
                                self.equipping(i[0], i[0].slot)
                                self.equipment[k] = i[0]
        else:
            print("You don't have any gear.")

    def unequip_direct(self):
        print("Which slot would you like to unequip?",
              '\n', '-' * 60,
              sep='')
        self.menu_gear_equipped('during equip or unequip')
        slot_choice = input('')
        slot_chose = ''
        pairs = {'Mainhand': '1', 'Offhand': '2', 'Head': '3', 'Body': '4',
                 'Legs': '5', 'Hands': '6', 'Feet': '7', 'Ring': '8'}
        for a, b in pairs.items():  # a-str         b-str_choice
            if b == slot_choice:
                slot_chose = a
        for k, v in self.equipment.items():  # k-str_choice  v-obj
            if slot_chose == k:
                if self.equipment[k]:
                    self.unequip(k, v)
                else:
                    print("You have nothing equipped there.")
        # else:
        #     print("You have nothing equipped.")

    def unequip(self, equipping_str, unequipping_obj):
        if unequipping_obj not in self.inventory:
            self.inventory.append(unequipping_obj)
        ohAtkPenalty = (0.7 if equipping_str == 'Offhand' else 1)
        self.stats['melee_boost'] -= unequipping_obj.melee_atk * ohAtkPenalty
        self.stats['magic_boost'] -= unequipping_obj.magic_atk * ohAtkPenalty
        self.stats['hp_regen'] -= unequipping_obj.hp_regen
        self.stats['mp_regen'] -= unequipping_obj.mp_regen
        self.equipment[equipping_str] = ''
        print("You unequip your ", unequipping_obj.name, '.', sep='')
        unequipping_obj.quantity += 1

    def equipping(self, equipping_obj, slot_option_choice):
        if slot_option_choice == '2':
            ohAtkPenalty = 0.70
        else:
            ohAtkPenalty = 1
        self.stats['melee_boost'] += equipping_obj.melee_atk * ohAtkPenalty
        self.stats['magic_boost'] += equipping_obj.magic_atk * ohAtkPenalty
        self.stats['hp_regen'] += equipping_obj.hp_regen
        self.stats['mp_regen'] += equipping_obj.mp_regen
        equipping_obj.quantity -= 1  # decrement or remove item from pack.
        if equipping_obj.quantity == 0:
            self.inventory.remove(equipping_obj)
        print("You equip your ", equipping_obj.name, ".",
              sep='')

    def view_abilities(self):
        """
        Either adds to or lists learned abilities.
        :return: None
        """
        print("Learned Abilities:")
        print('-' * 30,
              '\n', ' Hotkey',
              '\n', '-' * 8,
              sep='')
        for k, v in self.abilities.items():  # k-str (hotkey)  v-function name
            hotkey_fmt = '[' + k + ']'
            print(f"{hotkey_fmt:10}{v.__name__}")
        print('-' * 30,
              '\n', "Enter the hotkey to select an ability to add.",
              sep='')
        choice = input()
        choice = choice.capitalize()
        if choice in self.abilities:
            print("Add to which slot?")
            self.load_ability_bar_display('while viewing character sheet')
            slot_choice = input()
            for k, v in self.abilities.items():  # k-str (hotkey)  v-function name
                if choice == k:
                    self.ability_bar[slot_choice] = v
                    print("You add ", v.__name__, " to your bar.", sep='')

    def learn_ability(self, ability_key, ability_value):
        self.abilities.setdefault(ability_key, ability_value)
        # self.message = self.message + str("\nYou've learned " + ability_key + ". Access your abilities with [A].")
        print(f"You've learned {ability_key}. Access your abilities with [A].")

    def load_ability_bar_display(self, context):
        if context == "while viewing character sheet":
            option1 = ''
            option2 = ''
        else:
            option1 = '   Option'
            option2 = '[O]'
        cell = '}-{'
        abil_bar_disp = {'1': '     ', '2': '     ', '3': '     ', '4': '     ', '5': '     ', '6': '     '}
        for k, v in self.ability_bar.items():  # k-str ('1')           v-function ( Strike() )
            for a, b in self.abilities.items():  # a-str ( short_name )  b-function ( Strike() )
                if self.abilities[a] == v:
                    abil_bar_disp[k] = a
        print("    1        2        3        4        5        6", option1,
              '\n',
              f"{'{'}{abil_bar_disp['1']:^6}{cell}"
              f"{abil_bar_disp['2']:^6}{cell}"
              f"{abil_bar_disp['3']:^6}{cell}"
              f"{abil_bar_disp['4']:^6}{cell}"
              f"{abil_bar_disp['5']:^6}{cell}"
              f"{abil_bar_disp['6']:^6}{'}'}{option2:>6}")

    def consumables(self):
        consumables_list = []
        count = 1
        for i in self.inventory:
            if isinstance(i, Consumable):
                hotkeyid = count
                consumables_list.append([i, hotkeyid])
                count += 1
        print("Consumables: ",  # FORMAT: CONSUMABLES INTERFACE
              '\n', '-' * 30, sep='')
        # consumables_list.sort(key=lambda x: x[0])
        if consumables_list:
            print(f"{'':6}{'Type':15}{'Quantity':>}")
            for i in consumables_list:
                hotkey = '[' + str(i[1]) + ']'
                cons_type = i[0].name
                quantity = '(' + str(i[0].quantity) + ')'
                padding = ' ' * (30 - 6 - len(cons_type) - 8)
                print(f"{hotkey:6}{cons_type}{padding}{quantity:8}")
            print('-' * 30, sep='')
            choice = input("What would you like to consume?\n")

            for i in consumables_list:  # i-list [0-obj, 1-hotkey id]
                if choice[0] == str(i[1]):
                    for _ in choice:
                        if i[0] in self.inventory:
                            print("You drink the ", i[0].name, ".", sep='')
                            self.stats['hp_current'] = self.stats['hp_current'] + i[0].hp_regen
                            self.stats['mp_current'] = self.stats['mp_current'] + i[0].mp_regen
                            # self.stats[ = self.stats[
                            # self.stats[ = self.stats[
                            # self.stats[ = self.stats[
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
            print("You have no consumables.",
                  '\n', '-' * 30, sep='')

    def item_selection(self, class_type, context):
        item_list = []
        count = 1
        if context == "unequipping":
            for k, v in self.equipment.items():  # k-str  v-obj
                hotkeyid = count
                if v:
                    item_list.append([v, hotkeyid])  # [obj, str], [...
                    count += 1
        elif context == "weaponsmith":
            for i in self.inventory:
                if isinstance(i, class_type):
                    if "Mainhand" in i.slot or "Offhand" in i.slot:
                        hotkeyid = count
                        item_list.append([i, hotkeyid])
                        count += 1
        else:
            for i in self.inventory:
                if isinstance(i, class_type):
                    hotkeyid = count
                    item_list.append([i, hotkeyid])
                    count += 1
        if item_list:
            # FORMAT THE INTERFACE
            if context == "weaponsmith" or context == "armorsmith" or context == "apothecary":
                print("Selling:",
                      '\n', '----+' * 13, sep='')
                if class_type == Gear:
                    print(f"{'      ':6}{'Type':20}{'Damage':^16}{'Effect':^15}{'Value':^8}")
                elif class_type == Consumable or class_type == Bait:
                    print("{'':6}{'Type':15}{'Quantity':>}")
                else:
                    print(f"{'':6}{'Type':14}")
            else:
                print(class_type.__name__, ': ',
                      '\n',
                      '----+' * 13, sep='')
                if class_type == Gear:
                    print(f"{'':<6}{'Type':<20}{'Damage':^10}{'Effect':^20}{'Value':^8}")
                elif class_type == Consumable or class_type == Bait:
                    print(f"{'':6}{'Type':15}{'Quantity':>}")
                else:
                    print(f"{'':6}{'Type':14}")

            for i in item_list:
                if i[0]:  # checks for existence. Had trouble here while unequipping w/o this check.
                    hotkey = '[' + str(i[1]) + ']'  # [ hotkeyid ]
                    name = i[0].name
                    if class_type == Gear:
                        value = ''
                        if context in ['weaponsmith', 'armorsmith', 'apothecary']:
                            value = i[0].value
                        atk_str = ''
                        if i[0].melee_atk:
                            atk_str = atk_str + '(' + str(i[0].melee_atk) + ')'
                        elif i[0].magic_atk:
                            atk_str = atk_str + '(' + str(i[0].magic_atk) + ')'
                        regen_str = ''
                        if i[0].hp_regen:
                            regen_str = regen_str + "+" + str(i[0].hp_regen) + "hp/turn"
                        if i[0].mp_regen:
                            regen_str = regen_str + "+" + str(i[0].mp_regen) + "mp/turn"
                        print(f"{hotkey:<6}{name:<20}{atk_str:^10}{regen_str:^20}{value:>8}")
                    elif class_type == Consumable or class_type == Bait:
                        print(f"{hotkey:6}{name:14}{i[0].quantity:^8}")
            print('----+' * 13, sep='')
        return item_list

    def regen(self, context):
        increment = 0
        if context == 'roaming':
            increment = 3
        elif context == 'combat':
            increment = 1
        if self.stats['mp_current'] < self.stats['mp_base']:
            self.stats['mp_current'] = \
                min(self.stats['mp_current'] + increment + self.stats['mp_regen'], self.stats['mp_base'])
        if self.stats['hp_current'] < self.stats['hp_base']:
            self.stats['hp_current'] = \
                min(self.stats['hp_current'] + self.stats['hp_regen'], self.stats['hp_base'])

    def view_location(self):

        loc = '(' + str(self.xpos) + ", " + str(self.ypos) + ')'
        return loc

    def death(self):
        print("You've been put to rest.")
        print("Final stats:")
        self.character_sheet()
        self.equipment = {'Mainhand': '', 'Offhand': '', 'Head': '', 'Body': '', 'Legs': '', 'Hands': '',
                          'Feet': '', 'Ring': ''}
        self.inventory = []
        self.stats['level'] = 1
        self.stats['xp'] = 0
        self.stats['hp_current'] = 200
        self.stats['hp_base'] = 200
        self.stats['hp_regen'] = 0
        self.stats['mp_current'] = 10
        self.stats['mp_base'] = 10
        self.stats['melee_base_atk'] = 14
        self.stats['magic_base_atk'] = 25
        self.stats['mp_regen'] = 0
        self.stats['melee_boost'] = 0
        self.stats['magic_boost'] = 0
        self.abilities = {"Str": Strike, "Heal": Heal, "Cbust": Combust}
        self.ability_bar = {'1': Strike, '2': '', '3': '', '4': '', '5': '', '6': ''}


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
                self.equipping(pack[index])
            else:
                continue

    def equipping(self, equipping_obj):
        self.stats['melee_boost'] += equipping_obj.melee_atk
        self.stats['magic_boost'] += equipping_obj.magic_atk
        self.stats['hp_regen'] += equipping_obj.hp_regen
        self.stats['mp_regen'] += equipping_obj.mp_regen

    # def reset(self):
    #     # self.stats['melee_boost'] = self.init_melee_boost
    #     # self.stats['magic_boost'] = self.init_magic_boost
    #     # self.stats['hp_regen'] = self.init_hp_regen
    #     # self.stats['mp_regen'] = self.init_mp_regen
    #
    #     self.stats = self.init_stats

    def regen(self):
        if self.stats['mp_current'] < self.stats['mp_base']:
            self.stats['mp_current'] = min(self.stats['mp_current'] + self.stats['mp_regen'], self.stats['mp_base'])

        if self.stats['hp_current'] < self.stats['hp_base']:
            self.stats['hp_current'] = min(self.stats['hp_current'] + self.stats['hp_regen'], self.stats['hp_base'])


    def plunder(self, hero):
        for i in self.inventory:
            print(i.name, "looted!")
            if i not in hero.inventory:
                hero.inventory.append(i)
            i.quantity += 1
        for i in self.loot[0]:  # Items
            chance = random.randrange(1, 100)
            if chance > 95:
                if i not in hero.inventory:
                    hero.inventory.append(i)
                quantity_looted = 1
                if isinstance(i, Bait):
                    quantity_looted = random.randint(8, 12)
                i.quantity += quantity_looted
                print("You have looted ", quantity_looted, ' ', i.name, '.', sep='')

    def death(self, hero):
        hero.stats['xp'] += self.stats['xp_worth']
        # print("xp: ", hero.stats['xp'], "gained: ", self.xp_worth)
        print("You have slain the ", self.stats['race'], "!", sep='')
        if hero.message:
            print(hero.message)
        hero.message = ''
        # resets mob's hp at end of combat.
        self.plunder(hero)
        if hero.stats['xp'] > hero.stats['next_level_at']:
            hero.level_up()
        self.stats = self.init_stats


class Item:
    def __init__(self, name, tier, value, quantity=0):
        self.name = name
        self.tier = tier
        self.value = value
        self.quantity = quantity


class Gear(Item):
    def __init__(self, name, tier, value, dmg_style, slot, quantity=0,
                 melee_atk=0, magic_atk=0, poison_atk=0, hp_regen=0, mp_regen=0,
                 durability=100):
        super().__init__(name, tier, value, quantity)
        self.dmg_style = dmg_style  # melee, magic, etc.
        self.slot = slot  # gear slot it can go in (mainhand, head, etc.)

        self.melee_atk = melee_atk
        self.magic_atk = magic_atk
        self.poison_atk = poison_atk
        self.hp_regen = hp_regen
        self.mp_regen = mp_regen
        self.durability = durability


class Consumable(Item):
    def __init__(self, name, tier, value, melee_atk=0, magic_atk=0, poison_atk=0,
                 hp_regen=0, mp_regen=0, quantity=0):
        super().__init__(name, tier, value, quantity)
        self.melee_atk = melee_atk
        self.magic_atk = magic_atk
        self.poison_atk = poison_atk
        self.hp_regen = hp_regen
        self.mp_regen = mp_regen


class Bait(Item):
    def __init__(self, name, tier, value, quantity=0):
        super().__init__(name, tier, value, quantity)


class Tool(Item):
    def __init__(self, name, tier, value, durability=100, quantity=0):
        super().__init__(name, tier, value, quantity)
        self.durability = durability


# name, tier, value, dmg_style, slot, quantity=0,
# melee_atk=0, magic_atk=0, poison_atk=0, hp_regen=0, mp_regen=0, durability=100
small_dagger = Gear("small dagger", 1, 10, "melee", ['Mainhand', 'Offhand'],
                    melee_atk=12)
scimitar = Gear("scimitar", 1, 16, "melee", ['Mainhand', 'Offhand'],
                melee_atk=20)
kings_blade = Gear("King's blade", 2, 26, "melee", ['Mainhand', 'Offhand'],
                   melee_atk=25)

ilan_branch = Gear("ilam branch", 1, 10, "magic", ['Mainhand', 'Offhand'],
                   magic_atk=7, mp_regen=1)
wand = Gear("azalea wand", 1, 16, "magic", ['Mainhand', 'Offhand'],
            magic_atk=20, mp_regen=2)
crooked_staff = Gear("crooked staff", 1, 24, "magic", ['Mainhand', 'Offhand'],
                     magic_atk=15, mp_regen=4)

list_of_mainhand = [small_dagger, scimitar, kings_blade,
                    ilan_branch, wand, crooked_staff]

targe = Gear("targe", 1, 10, "melee, defense", ['Offhand'],
             melee_atk=5)
glimmering_orb = Gear("glimmering orb", 2, 36, "magic", ['Offhand'],
                      magic_atk=8, mp_regen=6)

list_of_offhand = [targe, glimmering_orb]

leather_cap = Gear("leather cap", 1, 8, "melee defense", "Head",
                   hp_regen=3)

list_of_head = [leather_cap]

heavy_tunic = Gear("heavy tunic", 1, 8, "defense", "Body",
                   melee_atk=5, hp_regen=5)

list_of_body = [heavy_tunic]

thick_chaps = Gear("thick chaps", 1, 16, "defense", "Legs",
                   melee_atk=4, hp_regen=2)

list_of_legs = [thick_chaps]

iron_gloves = Gear("iron gloves", 1, 10, "defense", "Hands",
                   melee_atk=2, magic_atk=2)

list_of_hands = [iron_gloves]

cut_boots = Gear("cut boots", 1, 10, "defense", "Feet",
                 melee_atk=2)

list_of_feet = [cut_boots]

old_ring = Gear("old ring", 2, 28, "magic", "Ring",
                magic_atk=14, mp_regen=7)
clay_ring = Gear("clay ring", 1, 22, "magic", "Ring",
                 melee_atk=14, hp_regen=7)

list_of_ring = [old_ring, clay_ring]

list_of_common_gear = [scimitar, kings_blade, targe, wand, crooked_staff, leather_cap, heavy_tunic, thick_chaps,
                       iron_gloves, cut_boots, old_ring, clay_ring]

gold = Item("Gold", 1, 1)

# hotkey, name, tier, value, melee_atk, magic_atk, poison_atk, hp_regen, mp_regen
potion = Consumable("potion", 1, 14, hp_regen=25)
ether = Consumable("ether", 1, 14, mp_regen=8)
elixir = Consumable("elixir", 2, 58, mp_regen=48)

ilan_berries = Bait("ilan berries", 1, 2)
thread_worms = Bait("thread worms", 1, 2)

list_of_common_items = [potion, ether, elixir,
                        ilan_berries, thread_worms]

list_of_bait = [ilan_berries, thread_worms]

herring = Item("herring", 1, 6)
salmon = Item("salmon", 1, 6)

logs = Item("logs", 1, 2)
worn_hatchet = Tool("worn hatchet", 1, 4, 20)


def player():
    return Char({"race": "human",
                          "hp_current": 200,
                          "hp_base": 200,
                          "hp_regen": 0,
                          "mp_current": 10,
                          "mp_base": 10,
                          "mp_regen": 0,
                          "melee_base_atk": 14,
                          "melee_boost": 0,
                          "magic_base_atk": 25,
                          "magic_boost": 0,
                          "level": 1,
                          "xp": 0,
                          "prev_level_xp": 0,
                          "next_level_at": 83},
                # INVENTORY,
                [],
                # ABILITIES
                {"Str": Strike, "Heal": Heal, "Cbust": Combust},
                # ABILITY BAR
                {'1': Strike, '2': '', '3': '', '4': '', '5': '', '6': ''},
                # EQUIPMENT
                {'Mainhand': '', 'Offhand': '', 'Head': '', 'Body': '', 'Legs': '', 'Hands': '', 'Feet': '',
                 'Ring': ''})


def thief():
    return Mob({"race": "thief",
                "hp_current": 200,
                "hp_base": 200,
                "hp_regen": 0,
                "mp_current": 10,
                "mp_base": 10,
                "mp_regen": 0,
                "melee_base_atk": 14,
                "melee_boost": 0,
                "melee_affinity": 0.7,
                "magic_base_atk": 8,
                "magic_boost": 0,
                "magic_affinity": 0.2,
                "level": 1,
                "xp_worth": 12},
               [[list_of_common_items], [list_of_bait]],
               {"Fire": Fire, "Heal": Heal, "Rush": Rush})


def kaelas_boar():
    return Mob({"race": "Kaelas boar",
                "hp_current": 60,
                "hp_base": 60,
                "hp_regen": 0,
                "mp_current": 4,
                "mp_base": 4,
                "mp_regen": 0,
                "melee_base_atk": 24,
                "melee_boost": 0,
                "melee_affinity": 0.7,
                "magic_base_atk": 4,
                "magic_boost": 0,
                "magic_affinity": 0.2,
                "level": 1,
                "xp_worth": 8},
               [list_of_common_items],
               {"Heal": Heal, "Rush": Rush})


def wolves():
    return Mob({"race": "pack of wolves",
                "hp_current": 300,
                "hp_base": 300,
                "hp_regen": 0,
                "mp_current": 10,
                "mp_base": 10,
                "mp_regen": 0,
                "melee_base_atk": 7,
                "melee_boost": 0,
                "melee_affinity": 0.7,
                "magic_base_atk": 0,
                "magic_boost": 0,
                "magic_affinity": 0.2,
                "level": 1,
                "xp_worth": 14},
               [list_of_common_items],
               {"Strike": Strike})


def cultist():
    return Mob({"race": "cultist",
                "hp_current": 200,
                "hp_base": 200,
                "hp_regen": 10,
                "mp_current": 100,
                "mp_base": 100,
                "mp_regen": 4,
                "melee_base_atk": 8,
                "melee_boost": 0,
                "melee_affinity": 0.7,
                "magic_base_atk": 38,
                "magic_boost": 0,
                "magic_affinity": 0.2,
                "level": 1,
                "xp_worth": 46},
               [[list_of_common_items], [list_of_bait]],
               {"Fire": Fire, "Fira": Fira, "Firaga": Firaga, "Heal": Heal, "Rush": Rush})


list_of_mobs = [thief, kaelas_boar, wolves, cultist]


def giant_kitty():
    return Mob({"race": "giant....kitty?",
                "hp_current": 3000,
                "hp_base": 3000,
                "hp_regen": 0,
                "mp_current": 10,
                "mp_base": 10,
                "mp_regen": 0,
                "melee_base_atk": 75,
                "melee_boost": 0,
                "melee_affinity": 0.7,
                "magic_base_atk": 85,
                "magic_boost": 0,
                "magic_affinity": 0.2,
                "level": 1,
                "xp_worth": 666},
               [list_of_common_items],
               {"Heal": Heal, "Firaga": Firaga})


def kraken():
    return Mob({"race": "Kraken",
                "hp_current": 5000,
                "hp_base": 5000,
                "hp_regen": 0,
                "mp_current": 10,
                "mp_base": 10,
                "mp_regen": 0,
                "melee_base_atk": 72,
                "melee_boost": 0,
                "melee_affinity": 0.7,
                "magic_base_atk": 68,
                "magic_boost": 0,
                "magic_affinity": 0.2,
                "level": 1,
                "xp_worth": 1247},
               [list_of_common_items],
               {"Fira": Fira, "Firaga": Firaga})


list_of_bosses = [giant_kitty, kraken]
