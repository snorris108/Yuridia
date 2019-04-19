from classes import *

import time
import pickle
import os

# DONE add Consumables interface, the potions equivalent of Equipment.
# add new spells that unlock a certain levels.
# new weapons, armor, accessories
# DONE add offhand functionality for weapons (70% style d
# amage applied to base)
# limit player's gear inventory, forcing the player to destroy a gear piece of their choice before getting more loot.
# you learn abilities by having them used on you in combat, and maybe taught in towns.
# incorporate durability on weapons and armor, figure out how to handle items with diff durability states
#     possibly only 3 tiers of degradation, to minimize amount of gear versions needed


def intro():
    clear_console()
    print('-' * 60,
          '\n', "You awaken suddenly, a distant cry of pain from an unsettling dream still echoing in your mind. "
                "Around you, the cave is still and damp. A sharp edge of light cuts across the floor, and as your"
                " eyes adjust you hear the cry again, closer. A deer, possibly, finding its mortality. You gather "
                "your gear and leave your dwelling.", sep='')


def create_hero():
    option = input("What do they call you?\n")
    if option == '-':
        hero = load_game()
    else:
        hero = player()
        hero.name = option
        clear_console()
    return hero


def load_game():
    filename = input("What did they call you?\n")
    filename = str(filename) + ".pkl"
    if os.path.exists(filename):
        with open(filename, 'rb') as infile:
            print("Previous progress loaded.")
            return pickle.load(infile)
    else:
        print("You have no saved progress.")
        return create_hero()


def save_game():
    filename = str(hero.name) + ".pkl"
    with open(filename, 'wb') as outfile:
        pickle.dump(hero, outfile)
        print("Progress saved.")


def clear_console():
    print('\n' * 40)


def check_surroundings():
    print()
    village = compass(4, 12, 100,
                      "You think you see smoke rising over the treetops to the ",
                      "Your path forks off toward a village.")
    lake = compass(6, 18, 120,
                   "A gentle river is flowing away toward the ",
                   "You stand at the shoreline of a small lake.")
    grove = compass(6, 14, 60,
                    "An old grove of redwood stands tall to the ",
                    "The wood from these trees would make a strong fire.")
    # caves = compass(2, 4, 137, "")

    options('check surroundings')
    if village:
        print("[V] Enter the village")
    if lake:
        print("[F] Fish at the lake")
    if grove:
        print("[C] Chop firewood")
    # if caves and lantern in hero.inventory:
    #     print("[N] Navigate the cave system")
    return village, lake, grove


# def fishing():
#     list = hero.get_list_of_all(Bait, '')
#     if list:
#         bait = ''
#         fish = ''
#         choice = input("What bait would you like to use?\n")
#         for i in list:  # [obj, str], [...
#             if choice == str(i[1]):
#                 bait = i[0]
#         fish_types = {herring: ilan_berries, salmon: thread_worms}
#         for k, v in fish_types.items():  # k-obj fish  v-obj bait
#             if bait == v:
#                 fish = k
#         print("You attempt to catch a fish.")
#         time.sleep(random.randint(1, 10) * 0.5)
#         print("You get a bite!")
#         start = round(time.clock(), 4)
#         # stop = 0
#         Time = 10
#         catch = input()
#         if catch == '':
#             stop = round(time.clock(), 4)
#             Time = round((stop - start), 4)
#             # print(start, stop, (stop - start))
#         if Time < 0.6:
#             print("You caught a ", fish.name, ".  ", Time, sep='')
#             if fish not in hero.inventory:
#                 hero.inventory.append(fish)
#             bait.quantity -= 1
#             if bait.quantity == 0:
#                 hero.inventory.remove(bait)
#             fish.quantity += 1
#             print("You have ", bait.quantity, ' ', bait.name, " left.", sep='')
#         else:
#             print("It slips away with your bait.  ", Time)
#             bait.quantity -= 1
#             if bait.quantity == 0:
#                 hero.inventory.remove(bait)
#             print(bait.quantity, ' ', bait.name)
#     else:
#         print("You have no bait.")


def compass(visible_near, visible_far, freq_on_map, far_message, near_message):
    """
    Outputs messages detailing what locations of interest (LoI) the player can see from their position on the map.
    :param visible_near: radius within which we are near and can interact with LoI
    :param visible_far: radius within which we can see LoI
    :param freq_on_map: how many steps between centers of LoI's
    :param far_message:
    :param near_message:
    :return:
    """
    within_range = False
    direction = ''
    xabs = abs(hero.xpos)  # within x steps of nearest LoI
    yabs = abs(hero.ypos)
    # considers either side of an axis to be the same... (10, -3 == 10, 3)
    xcount = 0
    ycount = 0
    while xabs > freq_on_map:
        xabs -= freq_on_map
        xcount += 1
    while yabs > freq_on_map:
        yabs -= freq_on_map
        ycount += 1
    xnearest_event = xcount * freq_on_map  # abs of LoI xpos
    ynearest_event = ycount * freq_on_map

    if xabs > freq_on_map / 2:
        xnearest_event += freq_on_map
    if hero.xpos < 0:
        xnearest_event = -xnearest_event
    if yabs > freq_on_map / 2:
        ynearest_event += freq_on_map
    if hero.ypos < 0:
        ynearest_event = -ynearest_event
    xrem = xabs % freq_on_map
    yrem = yabs % freq_on_map

    if freq_on_map / 2 < xabs < freq_on_map:
        xrem = freq_on_map - (xabs % freq_on_map)
    if freq_on_map / 2 < yabs < freq_on_map:
        yrem = freq_on_map - (yabs % freq_on_map)
    ratio = 0
    distance = math.sqrt(xrem ** 2 + yrem ** 2)  # absolute distance from LoI

    if xrem != 0:
        ratio = abs(yrem / xrem)

    if visible_near < distance <= visible_far:  # if LoI is visible;
        if xrem == 0 or ratio > 2.414:
            if hero.ypos > ynearest_event:
                direction = 'south.'
            elif hero.ypos < ynearest_event:
                direction = 'north.'
        elif yrem == 0 or ratio < 0.414:
            if hero.xpos > xnearest_event:
                direction = 'west.'
            elif hero.xpos < xnearest_event:
                direction = 'east.'
        elif 0.414 < ratio < 2.414:  # if diagonal from LoI;
            if hero.xpos > xnearest_event and hero.ypos > ynearest_event:
                direction = 'south-west.'
            elif hero.xpos > xnearest_event and hero.ypos < ynearest_event:
                direction = 'north-west.'
            elif hero.xpos < xnearest_event and hero.ypos > ynearest_event:
                direction = 'south-east.'
            elif hero.xpos < xnearest_event and hero.ypos < ynearest_event:
                direction = 'north-east.'
        print(far_message, direction, sep='')
    elif distance <= visible_near:
        print(near_message, sep='')
        within_range = True
    return within_range


def options(context):
    if context == 'check surroundings':
        padding = ' ' * (60 - 8 - len(hero.view_location()))
        print(f"\n{'Options:'}{padding}{hero.view_location()}",
              '\n', '-' * 60,
              '\n', f"{'[Enter]':^20}{'[R]':^20}{'[=]':^20}",
              '\n', f"{'Check surroundings':^20}{'[Rename Gear]':^20}{'Save progress':^20}",
              '\n', f"{'[S]':^20}{'[I]':^20}{'[E]':^20}",
              '\n', f"{'Character Sheet':^20}{'Inventory':^20}{'Equipment':^20}",
              '\n', f"{'[A]':^20}{'[C]':^20}{'[H]':^20}",
              '\n', f"{'Abilities':^20}{'Consumables':^20}{'Cast Heal':^20}",
              '\n', '-' * 60, sep='')
    elif context == 'renaming':
        print(f"\n{'Options:'}",
              '\n', '-' * 60,
              '\n', f"{'[1]':^30}{'[2]':^30}",
              '\n', f"{'New Name':^30}{'[Revert Name]':^30}",
              '\n', '-' * 60, sep='')
    elif context == 'combat':
        print(f"\n{'[C]':^15}{'[I]':^15}{'[W]':^15}{'[R]':^15}",
              '\n', f"{'Consumables':^15}{'Inventory':^15}{'Wait':^15}{'Run Away':^15}",
              '\n', '-' * 60,sep='')
    elif context == 'village':
        print('\nOptions: ',
              '\n', '-' * 60,
              '\n', f"{'[W]':^20}{'[A]':^20}{'[]':^20}",
              '\n', f"{'Weaponsmith':^20}{'Armorsmith':^20}{'Apothecary':^20}",
              '\n', f"{'[]':^20}{'[]':^20}{'[L]':^20}",
              '\n', f"{'Tavern':^20}{'Inn':^20}{'Leave':^20}",
              '\n', '-' * 60, sep='')
    elif context == 'w':  # weaponsmith
        print(f"\n{'Options:'}",
              '\n', '-' * 60,
              '\n', f"{'[]':^20}{'[S]':^20}{'[L]':^20}",
              '\n', f"{'Buy':^20}{'Sell':^20}{'Leave':^20}",
              '\n', f"{'[]':^20}{'[E]':^20}",
              '\n', f"{'Repair':^20}{'Enhance':^20}",
              '\n', '-' * 60, sep='')
    elif context == 'a':  # armorsmith
        print(f"\n{'Options:'}",
              '\n', '-' * 60,
              '\n', f"{'[]':^20}{'[S]':^20}{'[L]':^20}",
              '\n', f"{'Buy':^20}{'Sell':^20}{'Leave':^20}",
              '\n', f"{'[]':^20}{'[E]':^20}",
              '\n', f"{'Repair':^20}{'Enhance':^20}",
              '\n', '-' * 60, sep='')


def enter_village(context):
    print("As the afternoon sun touches the tops of the trees, you enter the gates of a small village. "
          "The street is still busy with life as people walk among the shops to trade. "
          "You can hear music playing from the tavern, and your stomach tightens at the smell "
          "of hot stew and fresh bread. You feel anxious to finish your business here, "
          "but staying a night or two couldn't hurt.")
    options('village')
    playing = input().lower()
    while playing != 'l':
        clear_console()
        if playing == 'w':
            print("Following the rythmic beating of hammer to metal, you find the local weaponsmith. "
                  "With a glance up from her work and a small nod, she acknowledges you and offers her inventory.")
            shop(playing)
        elif playing == 'a':
            print("You spot the armorsmith near the village entrance. Various shields and a few half-decent riding"
                  " tunics on display endure what might well be their thousanth tortured day in the full sun.")
            shop(playing)
        # elif playing == 'p':
        #     apothecary()
        # elif playing == 't':
        #     tavern()
        # elif playing == 'r':
        #     inn()
        elif playing == 's':
            hero.display_character_sheet()
        elif playing == 'i':
            hero.display_inventory()
        elif playing == 'e':
            hero.equip()
        elif playing == 'u':
            hero.unequip()
        elif playing == 'a':
            hero.ability_to_bar()
        elif playing == 'c':
            hero.chug()
        options('village')
        playing = input().lower()
    clear_console()


def shop(shop_choice):
    service_option = ''
    while service_option != 'l':
        options(shop_choice)
        service_option = input().lower()
        clear_console()
        if shop_choice in ['w', 'a']:
            # if service_option == 'b':
                # buying(shop_choice)
            if service_option == 's':
                selling(Gear, shop_choice, service_option)
            elif service_option == 'r':
                repair(shop_choice, service_option)
            elif service_option == 'e':
                enhance(shop_choice, service_option)
            elif service_option == 'i':
                hero.display_inventory()
    print("You turn and step back onto the village road.")


def enhance(shop_choice, service_option):
    # DISPLAY
    gear_list = hero.get_list_of_all(Gear, shop_choice, service_option)
    if gear_list:
        print(f"Gold:{hero.gold:>55}")
        print('-' * 60)
        if hero.display_item_list(Gear, shop_choice, service_option, gear_list):
            print('-' * 60)
            choice = input("What would you like enhanced?  (O indicates enhancement available)\n")
            # SELECTION
            for index, item in enumerate(gear_list):
                if choice == str(index + 1):
                    print("Sure, hon. I can enhance the following on that;")
                    hotkey, d = 1, {}
                    cost = max(int(item.value/10), 1)
                    if item.melee_boost_scalar < 1:
                        print(f"[{hotkey}] {'melee power':14}{'Cost: '}{cost} gold")
                        d[hotkey] = 'melee'
                        hotkey += 1
                    if item.magic_boost_scalar < 1:
                        print(f"[{hotkey}] {'magic power':14}{'Cost: '}{cost} gold")
                        d[hotkey] = 'magic'
                        hotkey += 1
                    if item.hp_regen_scalar < 1:
                        print(f"[{hotkey}] {'health regen':14}{'Cost: '}{cost} gold")
                        d[hotkey] = 'hp_regen'
                        hotkey += 1
                    if item.mp_regen_scalar < 1:
                        print(f"[{hotkey}] {'mana regen':14}{'Cost: '}{cost} gold")
                        d[hotkey] = 'mp_regen'
                    choice = input()
                    if hero.gold >= cost:
                        for k, v in d.items():
                            if choice == str(k):
                                if v == 'melee':
                                    item.melee_boost_scalar += 0.25
                                    item.melee_boost = item.init_melee * item.melee_boost_scalar
                                    item.value = max(int(item.value + item.value/12), 1)
                                    hero.gold -= cost
                                elif v == 'magic':
                                    item.magic_boost_scalar += 0.25
                                    item.magic_boost = item.init_magic * item.magic_boost_scalar
                                    item.value = max(int(item.value + item.value/12), 1)
                                    hero.gold -= cost
                                elif v == 'hp_regen':
                                    item.hp_regen_scalar += 0.25
                                    item.hp_regen = item.init_hp_regen * item.hp_regen_scalar
                                    item.value = max(int(item.value + item.value/12), 1)
                                    hero.gold -= cost
                                elif v == 'mp_regen':
                                    item.mp_regen_scalar += 0.25
                                    item.mp_regen = item.init_mp_regen * item.mp_regen_scalar
                                    item.value = max(int(item.value + item.value/12), 1)
                                    hero.gold -= cost
                                if item.melee_boost_scalar + item.magic_boost_scalar\
                                        + item.hp_regen_scalar + item.mp_regen_scalar == 4:
                                    item.value = int(item.init_value * 1.6)
                                    item.fully_enhanced = True
                                    item.name = '*' + item.name
                                    item.default_name = item.name
                                    print("Looks like that's all I can do with this one.")
                                    print(f"Your {item.name} seems to glow as she hands it back.")
                                else:
                                    print("You're all set.")
                    else:
                        print("Seems you can't cover the cost.")
    else:
        print("You've got nothing that needs my touch.")


def repair(shop_choice, service_option):
    pass


def selling(class_type, shop_choice, service_option):
    # DISPLAY
    item_list = hero.get_list_of_all(class_type, shop_choice, service_option)
    if item_list:
        print(f"Gold:{hero.gold:>55}")
        print('-' * 60)
        hero.display_item_list(Gear, shop_choice, service_option, item_list)
        print('-' * 60)
        choice = input("What would you like to sell?\n").lower()
        # SELECTION
        for index, item in enumerate(item_list):
            if choice == str(index + 1):
                if shop_choice in ['w', 'a']:  # bc some shops deal in stackables, while 'w' and 'a' don't
                    clear_console()
                    hero.gold += item.value
                    hero.inventory.remove(item)
                    response = get_NPC_response(shop_choice, item.tier)
                    print(response)
                # number = 1
                # if item[0].quantity > 1:
                #     number = input("How many? You have " + str(item[0].quantity) + '.\n')
                #     if number.isdigit():
                #         number = int(number)
                #     else:
                #         print("Invalid entry.")
                # for n in range(number):
                #     item[0].quantity -= 1
                #     if item[0].quantity == 0:
                #         hero.inventory.remove(item[0])
                # sold_for = item[0].value * number
                # hero.gold += sold_for
                # print("You sell ", number, ' ', item[0].name, " for ", sold_for, " gold.",
                #       '\n', "You now have ", hero.gold, " gold.",
                #       sep='')
    else:
        print("You have nothing to sell here.")


def reset_name():
    options('renaming')
    choice = input()
    if choice == '1':
        hero.rename_gear()
        clear_console()
    elif choice == '2':
        hero.reset_gear_name()
        clear_console()


def get_NPC_response(context, tier=None):
    if context in ['w', 'a']:
        responses = ['You found this where, exactly?',
                     'Oh my...',
                     'Thank you for this.',
                     'You might have rinsed it off first.',
                     'I might be able to sell this.',
                     'Won\'t have much use for that.',
                     'What minstrel\'s child crafted this?',
                     'Well, I can see why its previous owner didn\'t survive.']
        return random.choice(responses)


def event_roll():
    hero.regen('roaming')
    rngesus = random.randint(1, 100)

    if rngesus > 75 and hero.dist > 100:
        encounter(create_mob(*random.choice(list_of_bosses)))
    elif rngesus > 30:
        encounter(create_mob(*random.choice(list_of_mobs)))
    elif rngesus > 10:
        print("You walk through a field.\nNothing interesting happens.")
    else:
        chest()


def encounter(mob):
    # Initiates first turn of combat and the encounter's loop.
    print(f"You encounter a {mob.stats['race']}!")
    mob.equip()
    combat_template(mob)
    turn_start(mob)


def turn_start(mob):
    while mob.stats['hp_current'] > 0 and hero.stats['hp_current'] > 0:
        hero.display_ability_bar()
        options('combat')
        turn_choice = input().lower()
        clear_console()
        if turn_choice in ['1', '2', '3', '4', '5', '6']:
            hero_turn(mob, turn_choice)
            if mob_turn(mob) == 'dead':
                print('You step carefully over the corpse.')
                break
        elif turn_choice == 't':
            print('You punish your foe.')
            mob.death(hero)
            del mob
            break
        elif turn_choice == 'o':
            options('combat')
        elif turn_choice == 'c':
            hero.chug()
        elif turn_choice == 'i':
            hero.display_inventory()
        elif turn_choice == 'a':
            hero.ability_to_bar()
            combat_template(mob)
        elif turn_choice == 'w':
            mob_turn(mob)
        elif turn_choice == 'r':
            roll = random.randint(1, 100)
            if roll > 50:
                print("You successfully evade combat.")
                break
            else:
                print("You fail to escape.")
                mob_turn(mob)
        elif turn_choice == 'xp':
            print("xp worth: ", mob.stats['xp_worth'])
    if hero.stats['hp_current'] <= 0:
        print("You've been put to rest.")
        print("Final stats:")
        hero.display_character_sheet()
        main()
    hero.stats['mp_current'] += 1


def hero_turn(mob, turn_choice):
    context = "hero's turn"
    if hero.ability_bar[turn_choice]:
        state = use_ability(hero.ability_bar[turn_choice], mob, hero, context)
        if state == "ability failed":
            turn_start(mob)
    else:
        print("Ability slot is currently unassigned.")
        turn_start(mob)


def mob_turn(mob):
    """
    Handles the mob's turn of combat, assuming the mob still has hp remaining from your attack.
    :return: 'dead' flag if mob has been killed to signal end of combat.
    """
    context = "mob's turn"

    if mob.stats['hp_current'] > 0:
        time.sleep(0.3)
        hero.regen('combat')
        mob.regen()

        # decide if should heal
        rngesus = random.uniform(0, 1)
        if mob.stats['mp_current'] >= 3 and (mob.stats['hp_current'] / mob.stats['hp_base']) < 0.2 \
                and 'Heal' in mob.abilities:
            desire_to_heal = 1 - (mob.stats['hp_current'] / mob.stats['hp_base'])
            odds_to_heal = random.uniform(desire_to_heal, 1)
            if odds_to_heal >= rngesus:
                use_ability('Heal', hero, mob, context)

        elif rngesus < mob.stats['melee_affinity']:
            if 'Rush' in mob.abilities and mob.stats['melee_affinity'] > random.uniform(0, 1):
                use_ability('Rush', hero, mob, context)
                if mob.stats['hp_current'] <= 0:
                    mob.death(hero)
                    del mob
                    return 'dead'

            elif 'Strike' in mob.abilities:
                use_ability('Strike', hero, mob, context)
            else:
                mob_basic_atk(mob, hero)
        elif rngesus < mob.stats['melee_affinity'] + mob.stats['magic_affinity']:
            if mob.stats['mp_current'] >= 18 and 'Firaga' in mob.abilities:
                use_ability('Firaga', hero, mob, context)
            elif mob.stats['mp_current'] >= 12 and 'Fira' in mob.abilities:
                use_ability('Fira', hero, mob, context)
            elif mob.stats['mp_current'] >= 6 and 'Fire' in mob.abilities:
                use_ability('Fire', hero, mob, context)
            else:
                mob_basic_atk(mob, hero)
        else:
            mob_basic_atk(mob, hero)
        combat_template(mob)
    else:
        combat_template(mob)
        mob.death(hero)
        del mob
        return 'dead'


def combat_template(mob):
    """Draws the combat 'window' """
    bar_len = 20
    mob_hp_bar = int((1 - ((mob.stats['hp_base'] - mob.stats['hp_current']) / mob.stats['hp_base'])) * bar_len)
    hero_hp_bar = min(int((1 - ((hero.stats['hp_base'] - hero.stats['hp_current']) / hero.stats['hp_base'])) * bar_len),
                      bar_len)
    # FORMAT: COMBAT INTERFACE
    mp_regen_fmt = ''
    melee_boost_fmt = ''
    magic_boost_fmt = ''

    if mob.stats['mp_regen'] != 0:
        mp_regen_fmt = f"(^{str(int(mob.stats['mp_regen']))}^)"
    if mob.stats['melee_boost'] != 0:
        melee_boost_fmt = f"( +{str(int(mob.stats['melee_boost']))})"
    if mob.stats['magic_boost'] != 0:
        magic_boost_fmt = f"( +{str(int(mob.stats['magic_boost']))})"
    print('-' * 60,
          f"\n{mob.stats['race']:^22}{'':16}{hero.name:^22}",
          f"\n{'['}{'+' * mob_hp_bar:20}{']'}{'Health':^16}{'['}{'+' * hero_hp_bar:20}{']'}",
          f"\n{mp_regen_fmt:>10}{mob.stats['mp_current']:>11}{'Mana':^16}{hero.stats['mp_current']:<20}",
          f"\n{melee_boost_fmt:>10}{mob.stats['melee_base_atk']:>11}{'Attack':^16}"
          f"{(hero.stats['melee_base_atk'] + hero.stats['melee_boost']):<20}",
          f"\n{magic_boost_fmt:>10}{mob.stats['magic_base_atk']:>11}{'M. Attack':^16}"
          f"{(hero.stats['magic_base_atk'] + hero.stats['magic_boost']):<20}",
          '\n', '-' * 60,
          sep='')


def chest():
    """
    Creates chest encounter with option to loot. Evaluates odds of looting items and gear separately.
    :return: None
    """
    choice = input("You find a small treasure!\nDo you wish to loot it? (Y or N)\n").lower()
    looted_item = False
    count = 0

    if choice == 'y':
        for item in list_of_common_items:
            rngesus = random.uniform(0, 1)
            if rngesus < 10.15 and count < 5:
                chest_looting(item)
                looted_item = True
                count += 1
# It'd be interesting to find gear tiered in a range around your level, so tier 1 items eventually don't drop
        if hero.stats['burden_current'] < hero.stats['burden_limit']:
            rngesus = random.uniform(0, 1)
            if rngesus < 1 and count < 5:
                chest_looting(Gear(*random.choice(list_of_gear)))
                looted_item = True
                count += 1

        if not looted_item:
            print("You find nothing of value.")
    else:
        print("You leave it.")


def chest_looting(item):
    """
    Generates a random number used to evaluate odds of getting item/gear from chest. See below for handling items
    individually.
    :param item: function that returns instance of item/gear
    """
    if isinstance(item, Gear):
        if hero.stats['burden_current'] < hero.stats['burden_limit']:
            hero.inventory.append(item)
            hero.stats['burden_current'] += item.burden
            print(f"You find a {item.name} and add it to your pack.")
    else:
        num_rolled = random.randrange(1, 4)
        if item not in hero.inventory:
            hero.inventory.append(item)
        item.quantity += num_rolled
        plural = 'it' if num_rolled == 1 else 'them'
        print(f"You find {num_rolled} {item.name} and add {plural} to your pack.")


def move():  # should this be a class method?
    print("Which direction will you head?")
    print("Enter direction or [C] to enter coordinates)")
    choice = input().lower()
    if choice == 'c':
        new_x = input("X:\n")
        new_y = input("Y:\n")
        if new_x.isdigit() and new_y.isdigit():
            x_diff = int(new_x) - int(hero.xpos)
            y_diff = int(new_y) - int(hero.ypos)
            new_dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
            if new_dist <= hero.can_move:
                hero.xpos = int(new_x)
                hero.ypos = int(new_y)
                hero.dist = math.sqrt(hero.xpos ** 2 + hero.ypos ** 2)
            else:
                print("You can't travel that quickly yet.")
        else:
            print("Invalid coordinates.")
            check_surroundings()
    elif choice in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
        side_of_tri = math.floor(math.sqrt((hero.can_move ** 2) / 2))
        choice = choice.lower()
        if choice == 'n':
            hero.ypos += hero.can_move
        elif choice == 'ne':
            hero.xpos += side_of_tri
            hero.ypos += side_of_tri
        elif choice == 'e':
            hero.xpos += hero.can_move
        elif choice == 'se':
            hero.xpos += side_of_tri
            hero.ypos -= side_of_tri
        elif choice == 's':
            hero.ypos -= hero.can_move
        elif choice == 'sw':
            hero.xpos -= side_of_tri
            hero.ypos -= side_of_tri
        elif choice == 'w':
            hero.xpos -= hero.can_move
        elif choice == 'nw':
            hero.xpos -= side_of_tri
            hero.ypos += side_of_tri
        else:
            print("Invalid direction.")
            check_surroundings()
        test = math.sqrt(hero.xpos ** 2 + hero.ypos ** 2)
        print(test)
        hero.dist = test


def main():
    global hero
    intro()
    hero = create_hero()

    alive = True
    while alive:
        village, lake, grove = check_surroundings()
        playing = input().lower()
        clear_console()
        if playing == 's':
            hero.display_character_sheet()
        # elif playing == 'list':
        # print("xp: ", hero.stats.xp, "level: ", hero.stats.level)
        elif playing == 'i':
            hero.display_inventory()
        elif playing == 'e':
            hero.equip()
        elif playing == 'u':
            hero.unequip()
        elif playing == 'a':
            hero.ability_to_bar()
        elif playing == 'c':
            hero.chug()
        elif playing == 'm':
            move()
            event_roll()
        elif playing == 'v' and village:
            enter_village('from outside')
        # elif playing == 'f' and lake:
        #     fishing()
        elif playing == 'r':
            reset_name()
        elif playing == '':
            event_roll()
        elif playing == '=':
            save_game()
        elif playing == '-':
            load_game()
        elif playing[0] == 'h':
            for _ in playing:
                x = ''
                if hero.stats['mp_current'] >= 3:
                    Heal(x, hero, "hero's turn")
        elif playing == 't':
            encounter(create_mob(*kraken))
        elif playing == 'x':
            chest()
        elif playing == 'stats':
            for k, v in hero.stats.items():
                print(f"{k:16}{': '}{int(v):>6}")
        elif playing == 'dist':
            print(hero.dist)
        # else:
        #     check_surroundings()
        # check_surroundings()


main()
