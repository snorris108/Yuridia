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
    print('\n' * 80)


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
#     list = hero.item_selection(Bait, '')
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


def options(context):
    if context == 'check surroundings':
        padding = ' ' * (60 - 8 - len(hero.view_location()))
        print(f"\n{'Options:'}{padding}{hero.view_location()}",
              '\n', '-' * 60,
              '\n', f"{'[Enter]':^20}{'':^20}{'[=]':^20}",
              '\n', f"{'Check surroundings':^20}{'':^20}{'Save progress':^20}",
              '\n', f"{'[S]':^20}{'[I]':^20}{'[E]':^20}",
              '\n', f"{'Character Sheet':^20}{'Inventory':^20}{'Equipment':^20}",
              '\n', f"{'[A]':^20}{'[C]':^20}{'[H]':^20}",
              '\n', f"{'Abilities':^20}{'Consumables':^20}{'Heal':^20}",
              '\n', '-' * 60, sep='')
    elif context == 'combat':
        print('\nOptions: ',
              '\n', '-' * 60,
              '\n', f"{'[C]':^20}{'[I]':^20}{'[W]':^20}{'[R]':^20}",
              '\n', f"{'Consumables':^20}{'Inventory':^20}{'Wait':^20}{'Run Away':^20}",
              '\n', '-' * 60, sep='')
    elif context == 'village':
        print('\nOptions: ',
              '\n', '-' * 60,
              '\n', f"{'[W]':^20}{'[A]':^20}{'[P]':^20}",
              '\n', f"{'Weaponsmith':^20}{'Armorsmith':^20}{'Apothecary':^20}",
              '\n', f"{'[T]':^20}{'[I]':^20}{'[L]':^20}",
              '\n', f"{'Tavern':^20}{'Inn':^20}{'Leave':^20}",
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
            shop('weaponsmith')
        # elif playing == 'a':
        #     armorsmith()
        # elif playing == 'p':
        #     apothecary()
        # elif playing == 't':
        #     tavern()
        # elif playing == 'r':
        #     inn()
        elif playing == 's':
            hero.character_sheet()
        elif playing == 'i':
            hero.view_inventory()
        elif playing == 'e':
            hero.equip()
        elif playing == 'u':
            hero.unequip_direct()
        elif playing == 'a':
            hero.view_abilities()
        elif playing == 'c':
            hero.consumables()
        elif playing == 'o':
            options("village")
        options('village')
        playing = input().lower()
    # check_surroundings()


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


def shop(context):
    print("[B] Buy  |  [S] Sell  |  [L] Leave")
    choice = input().lower()
    clear_console()
    # if choice == 'b':
        # buying(context)
    if choice == 's':
        selling(context)
    elif choice == 'i':
        hero.view_inventory()
    if choice == 'l':
        print("You turn and step back into the main thoroughfare.")
        # in_village()


def selling(context):
    list = hero.item_selection(Gear, "weaponsmith")  # [ obj, (list item 1, 2, 3, etc...) ]
    if list:
        choice = input("What would you like to sell?  [B] Back\n")
        choice = choice.lower()
        for i in list:
            if choice == str(i[1]):
                number = 1
                if i[0].quantity > 1:
                    number = input("How many? You have " + str(i[0].quantity) + '.\n')
                    if number.isdigit():
                        number = int(number)
                    else:
                        print("Invalid entry.")
                for n in range(number):
                    i[0].quantity -= 1
                    if i[0].quantity == 0:
                        hero.inventory.remove(i[0])
                sold_for = i[0].value * number
                hero.gold += sold_for
                print("You sell ", number, ' ', i[0].name, " for ", sold_for, " gold.",
                      '\n', "You now have ", hero.gold, " gold.",
                      sep='')
                if list:
                    selling(context)
            elif choice == 'b':
                shop(context)
            elif choice == 'i':
                hero.view_inventory()
                shop(context)

    else:
        print("You have nothing to sell here.")
        shop(context)


def event_roll():
    hero.regen('roaming')
    rngesus = random.randint(1, 100)

    if rngesus > 75 and hero.dist > 100:
        encounter(random.choice(list_of_bosses), hero)
    elif rngesus > 30:
        encounter(mob_dict[random.choice(list_of_mobs)], hero)
    elif rngesus > 10:
        print("You walk through a field.\nNothing interesting happens.")
    else:
        chest()


def encounter(mob, hero):
    # Initiates first turn of combat and the encounter's loop.
    print(f"You encounter a {mob.stats['race']}!")
    mob.equip()
    combat_template(mob, hero)
    turn_start(mob, hero)


def turn_start(mob, hero):
    while mob.stats['hp_current'] > 0 and hero.stats['hp_current'] > 0:
        hero.display_ability_bar()
        turn_choice = input().lower()
        clear_console()
        if turn_choice in ['1', '2', '3', '4', '5', '6']:
            if hero_turn(mob, hero, turn_choice) == 'dead':
                print('You step carefully over the corpse.')
                break
        if turn_choice == 't':
            print('You punish your foe.')
            # Runs mob death and checks for hero level up.
            mob.death(hero)
            check_surroundings()
            break
        elif turn_choice == 'o':
            options('combat')
        elif turn_choice == 'c':
            hero.consumables()
        elif turn_choice == 'i':
            hero.view_inventory()
        elif turn_choice == 'a':
            hero.view_abilities()
            combat_template(mob, hero)
        elif turn_choice == 'w':
            mob_turn(mob, hero)
        elif turn_choice == 'r':
            roll = random.randint(1, 100)
            if roll > 50:
                print("You successfully evade combat.")
                break
            else:
                print("You fail to escape.")
                mob_turn(mob, hero)
        elif turn_choice == 'xp':
            print("xp worth: ", mob.stats['xp_worth'])
    if hero.stats['hp_current'] <= 0:
        print("You've been put to rest.")
        print("Final stats:")
        hero.character_sheet()
        intro()
    # mob.inventory = []
    hero.stats['mp_current'] += 1


def hero_turn(mob, hero, turn_choice):
    context = "hero's turn"
    if hero.ability_bar[turn_choice]:
        state = use_ability(hero.ability_bar[turn_choice], mob, hero, context)
        if state == "ability failed":
            turn_start(mob, hero)
    else:
        print("Ability slot is currently unassigned.")
        turn_start(mob, hero)
    return mob_turn(mob, hero)


def mob_turn(mob, hero):
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
                and "Heal" in mob.abilities:
            desire_to_heal = 1 - (mob.stats['hp_current'] / mob.stats['hp_base'])
            odds_to_heal = random.uniform(desire_to_heal, 1)
            if odds_to_heal >= rngesus:
                mob.abilities['Heal'](mob, hero, context)

        elif rngesus < mob.stats['melee_affinity']:
            if "Rush" in mob.abilities and mob.stats['melee_affinity'] > random.uniform(0, 1):
                # mob.abilities['Rush'](hero, mob, context)
                use_ability('Rush', hero, mob)
            elif "Strike" in mob.abilities:
                mob.abilities['Strike'](hero, mob, context)
            else:
                mob_basic_atk(mob, hero)
        elif rngesus < mob.stats['melee_affinity'] + mob.stats['magic_affinity']:
            if mob.stats['mp_current'] >= 18 and "Firaga" in mob.abilities:
                mob.abilities['Firaga'](hero, mob, context)
            elif mob.stats['mp_current'] >= 12 and "Fira" in mob.abilities:
                mob.abilities['Fira'](hero, mob, context)
            elif mob.stats['mp_current'] >= 6 and "Fire" in mob.abilities:
                mob.abilities['Fire'](hero, mob, context)
            else:
                mob_basic_atk(mob, hero)
        else:
            mob_basic_atk(mob, hero)
        combat_template(mob, hero)
    else:
        combat_template(mob, hero)
        mob.death(hero)
        return 'dead'


def combat_template(mob, hero):
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
          f"\n{mob.stats['race']:^22}{'':16}{hero.stats['race']:^22}",
          f"\n{'['}{'+' * mob_hp_bar:20}{']'}{'Health':^16}{'['}{'+' * hero_hp_bar:20}{']'}",
          f"\n{mp_regen_fmt:>10}{mob.stats['mp_current']:>11}{'Mana':^16}{hero.stats['mp_current']:<20}",
          f"\n{melee_boost_fmt:>10}{mob.stats['melee_base_atk']:>11}{'Attack':^16}"
          f"{(hero.stats['melee_base_atk'] + hero.stats['melee_boost']):<20}",
          f"\n{magic_boost_fmt:>10}{mob.stats['magic_base_atk']:>11}{'M. Attack':^16}"
          f"{(hero.stats['magic_base_atk'] + hero.stats['magic_boost']):<20}",
          '\n', '-' * 60,
          sep='')


def mob_basic_atk(mob, target):
    strike = math.floor((mob.stats['melee_base_atk'] + mob.stats['melee_boost']) * random.uniform(0.7, 1.1))
    target.stats['hp_current'] = math.floor(max(target.stats['hp_current'] - strike, 0))
    print("You are hit for ", strike, " points.", sep='')


def chest():
    """
    Creates chest encounter with option to loot. Evaluates odds of looting items and gear separately.
    :return: None
    """
    choice = input("You find a small treasure!\nDo you wish to loot it? (Y or N)\n").lower()
    looted_item = False
    looted_gear = False
    count = 0

    if choice == 'y':
        for i in list_of_common_items:
            rngesus = random.randint(1, 100)
            if rngesus < 20 and count < 5:
                chest_looting(items_dict[i])
                looted_item = True
                count += 1
        for i in list_of_common_gear:
            rngesus = random.randint(1, 100)
            if rngesus < 10 and count < 5:
                chest_looting(gear_dict[i])
                looted_gear = True
                count += 1

        if not looted_item and not looted_gear:
            print("You find nothing of value.")
    else:
        print("You leave it.")


def chest_looting(item):
    """
    Generates a random number used to evaluate odds of getting item/gear from chest. See below for handling items
    individually.
    :param item: function that returns instance of item/gear
    """
    if item not in hero.inventory:
        hero.inventory.append(item)

    num_rolled = random.randrange(1, 4)
    item.quantity += num_rolled

    if num_rolled == 1:
        plural = 'it'
    else:
        plural = 'them'
    print("You find ", num_rolled, ' ', item.name, ", and add ", plural, " to your pack.",
          sep='')


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
            hero.character_sheet()
        # elif playing == 'list':
        # print("xp: ", hero.stats.xp, "level: ", hero.stats.level)
        elif playing == 'i':
            hero.view_inventory()
        elif playing == 'e':
            hero.equip()
        elif playing == 'u':
            hero.unequip_direct()
        elif playing == 'a':
            hero.view_abilities()
        elif playing == 'c':
            hero.consumables()
        elif playing == 'm':
            move()
            event_roll()
        elif playing == 'v' and village:
            enter_village('from outside')
        # elif playing == 'f' and lake:
        #     fishing()
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
            encounter(kraken(), hero)
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