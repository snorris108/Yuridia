
import math
import random


def mob_basic_atk(mob, target):
    strike = math.floor((mob.stats['melee_base_atk'] + mob.stats['melee_boost']) * random.uniform(0.7, 1.1))
    target.stats['hp_current'] = math.floor(max(target.stats['hp_current'] - strike, 0))
    print("You are hit for ", strike, " points.", sep='')


def use_ability(name, target, caster, context, learning_rate=1):
    # if requires mp, check and deduct
    if 'mp_cost' in ability_dict[name].keys():
        if caster.stats["mp_current"] >= ability_dict[name]['mp_cost']:
            caster.stats["mp_current"] -= ability_dict[name]['mp_cost']
        else:
            print(f"You need {ability_dict[name]['mp_cost']} mana to cast that.")
            return "ability failed"

    # process damages
    if 'power' in ability_dict[name].keys():
        damage = math.floor((caster.stats["magic_base_atk"] + caster.stats["magic_boost"])
                            * ability_dict[name]['power'] * random.uniform(0.90, 1.10))
        target.stats["hp_current"] = math.floor(max(target.stats["hp_current"] - damage, 0))
        # print contextual messages
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
        rngesus = random.randint(1, 10)
        if name not in target.abilities and rngesus < learning_rate:
            target.learn_ability(name)


ability_dict = {'Strike':   {'power': 1,
                             'msg1': f"You stike your foe for ",
                             'msg2': f"You are struck hard for "},
                'Combust':  {'mp_cost': 8,
                             'power': 1,
                             'recoil': 0.5,
                             'msg1': f"You launch a chaotic volley of energy and damage your foe for ",
                             'msg2': f"You are struck hard for "},
                'Rush':     {'mp_cost': 0,
                             'power': 1,
                             'recoil': 0.1,
                             'msg1': f"You charge at your foe, ruthlessly dealing ",
                             'msg2': f"Enraged, the enemy rushes you! You lose "},
                'Fire':     {'mp_cost': 6,
                             'power': 1.15,
                             'msg1': f"A flash of fire burns your foe for ",
                             'msg2': f"You are struck by a wild flash of fire! You lose "},
                'Fira':     {'mp_cost': 12,
                             'power': 1.65,
                             'msg1': f"You conjure a volley of fire at your foe for ",
                             'msg2': f"You are struck by a chaotic volley of fire! You lose "},
                'Firaga':   {'mp_cost': 18,
                             'power': 2.25,
                             'msg1': f"Roiling fire surrounds your foe for ",
                             'msg2': f"You are surrounded by an eruption of fire! You lose "},
                'Heal':     {'mp_cost': 3,
                             'hp_gain': 0.1,
                             'msg1': f"You cast Heal on yourself",
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
