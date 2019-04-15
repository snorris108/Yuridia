
import math
import random


def mob_basic_atk(mob, target):
    strike = math.floor((mob.stats['melee_base_atk'] + mob.stats['melee_boost']) * random.uniform(0.7, 1.1))
    target.stats['hp_current'] = math.floor(max(target.stats['hp_current'] - strike, 0))
    print(f"You are hit for {strike} points.")


def use_ability(name, target, caster, context):
    # if requires mp, check and deduct
    if 'mp_cost' in ability_dict[name].keys():
        if caster.stats["mp_current"] >= ability_dict[name]['mp_cost']:
            caster.stats["mp_current"] -= ability_dict[name]['mp_cost']
        else:
            print(f"You need {ability_dict[name]['mp_cost']} mana to cast that.")
            return "ability failed"

    # process damages
    melee_damage, magic_damage = 0, 0
    if 'melee_power' in ability_dict[name].keys():
        melee_damage = math.floor((caster.stats["melee_base_atk"] + caster.stats["melee_boost"])
                                  * ability_dict[name]['melee_power'] * random.uniform(0.90, 1.10))
    if 'magic_power' in ability_dict[name].keys():
        magic_damage = math.floor((caster.stats["magic_base_atk"] + caster.stats["magic_boost"])
                                  * ability_dict[name]['magic_power'] * random.uniform(0.90, 1.10))
    damage = melee_damage + magic_damage
    target.stats["hp_current"] = math.floor(max(target.stats["hp_current"] - damage, 0))
    # print contextual messages
    if 'melee_power' in ability_dict[name].keys() or 'magic_power' in ability_dict[name].keys():
        player_msg = f"{ability_dict[name]['msg1']} {str(damage)} points!"
        mob_msg = f"{ability_dict[name]['msg2']} {str(damage)} health."
        print(player_msg) if context == "hero's turn" else print(mob_msg)
    if 'recoil' in ability_dict[name].keys():
        caster.stats["hp_current"] -= caster.stats["hp_base"] * ability_dict[name]['recoil']
        print("You took some recoil damage from the blast, yourself.") if context == "hero's turn"\
            else print("It sustained minor injuries in the process.")

    # apply any benefits
    if 'hp_gain' in ability_dict[name].keys():
        health_gained = math.floor(caster.stats["hp_base"] * ability_dict[name]['hp_gain']
                                   + caster.stats["hp_base"] * caster.stats["magic_base_atk"] / 500)
        caster.stats["hp_current"] += health_gained
        if caster.stats["hp_current"] > caster.stats["hp_base"]:
            print(f"You feel exceedingly healthy. (^{health_gained}^ hp.)") if context == "hero's turn"\
                else print(f"It feels exceedingly healthy. (^{health_gained}^ hp.)")
        else:
            print(f"You're bleeding a bit less now. (^{health_gained}^ hp.)") if context == "hero's turn" \
                else print(f"It's bleeding a bit less now. (^{health_gained}^ hp.)")

    # allow ability to be learned
    if context == "mob's turn":
        rngesus = random.uniform(0, 1)
        if name not in target.abilities and rngesus < ability_dict[name]['learning_rate']:
            target.learn_ability(name)


ability_dict = {'Strike':   {'melee_power': 1,
                             'msg1': f"You stike your foe for",
                             'msg2': f"You are struck hard for"},
                'Combust':  {'mp_cost': 8,
                             'magic_power': 1,
                             'recoil': 0.5,
                             'msg1': f"You launch a chaotic volley of energy and damage your foe for",
                             'msg2': f"You are struck hard for"},
                'Rush':     {'melee_power': 1,
                             'recoil': 0.1,
                             'learning_rate': 0.80,
                             'msg1': f"You charge at your foe, ruthlessly dealing ",
                             'msg2': f"Enraged, the enemy rushes you! You lose "},
                'Fire':     {'mp_cost': 6,
                             'magic_power': 1.15,
                             'learning_rate': 0.60,
                             'msg1': f"A flash of fire burns your foe for",
                             'msg2': f"You are struck by a wild flash of fire! You lose "},
                'Fira':     {'mp_cost': 12,
                             'magic_power': 1.65,
                             'learning_rate': 0.40,
                             'msg1': f"You conjure a volley of fire at your foe for",
                             'msg2': f"You are struck by a chaotic volley of fire! You lose "},
                'Firaga':   {'mp_cost': 18,
                             'magic_power': 2.25,
                             'learning_rate': 0.20,
                             'msg1': f"Roiling fire surrounds your foe for",
                             'msg2': f"You are surrounded by an eruption of fire! You lose "},
                'Heal':     {'mp_cost': 3,
                             'hp_gain': 0.1,
                             'msg1': f"With Audro's blessing, you heal",
                             'msg2': f" "}}

ability_order = ['Strike', 'Combust', 'Rush', 'Heal',
                 'Fire', 'Fira', 'Firaga']
ability_weights = {k: v for k, v in zip(ability_order, range(1, len(ability_order) + 1))}


def Heal(x, y, context):
    if context == "hero's turn":
        if y.stats["mp_current"] >= 3:
            y.stats["mp_current"] -= 3
            health_gained = math.floor(y.stats["hp_base"] * 0.30 + y.stats["hp_base"] * y.stats["magic_boost"] / 500)
            y.stats["hp_current"] += health_gained
            if y.stats["hp_current"] > y.stats["hp_base"]:
                print("You feel exceedingly healthy. (^", health_gained, "^ hp.)", sep='')
            else:
                print("You're bleeding a bit less now. (^", health_gained, "^ hp.)", sep='')
        else:
            print("You unfortunately have even less mana than blood left.")
            return "ability failed"
    elif context == "mob's turn":
        if x.stats["mp_current"] >= 3:
            x.stats["mp_current"] -= 3
            health_gained = math.floor(x.stats["hp_base"] * 0.30 + x.stats["hp_base"] * x.stats["magic_base_atk"] / 500)
            x.stats["hp_current"] += health_gained
            print("It's bleeding a bit less now. (^", health_gained, "^ hp.)", sep='')
