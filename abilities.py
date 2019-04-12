import math
import random


def action_msg(context, player_msg, mob_msg):
    print(player_msg) if context == "hero's turn" else print(mob_msg)


def learn_ability(ability, learning_rate, target):
    rngesus = random.randint(1, 10)
    if ability.__name__ not in target.abilities and rngesus < learning_rate:
        target.learn_ability(ability.__name__, ability)


def Strike(target, caster, context):
    damage = math.floor((caster.stats["melee_base_atk"] + caster.stats["melee_boost"]) * random.uniform(0.90, 1.10))
    target.stats["hp_current"] = math.floor(max(target.stats["hp_current"] - damage, 0))
    player_msg = f"You stike your foe for {str(damage)} points!"
    mob_msg = f"You are struck hard for {str(damage)} points!"
    action_msg(context, player_msg, mob_msg)


def Rush(target, caster, context):
    damage = math.floor((caster.stats["melee_base_atk"] + caster.stats["melee_boost"]) * random.uniform(1.90, 2.10))
    target.stats["hp_current"] = math.floor(max(target.stats["hp_current"] - damage, 0))
    caster.stats["hp_current"] -= caster.stats["hp_base"] * 0.1
    player_msg = f"You charge at your foe, ruthlessly dealing {str(damage)} damage. " \
        f"\nYou take a minor blow in your haste."
    mob_msg = f"Enraged, the enemy rushes you! You lose {str(damage)} health."
    action_msg(context, player_msg, mob_msg)

    if context == "mob's turn":
        learn_ability(Rush, 8, target)


def Fire(target, caster, context):
    if caster.stats["mp_current"] >= 6:
        caster.stats["mp_current"] -= 6
        damage = math.floor((caster.stats["magic_base_atk"] + caster.stats["magic_boost"]) * 1.15 * random.uniform(0.90, 1.10))
        target.stats["hp_current"] = math.floor(max(target.stats["hp_current"] - damage, 0))
        player_msg = f"You cast Fire on your foe for {str(damage)} points!"
        mob_msg = f"You are struck by a wild flash of fire! You lose {str(damage)} points."
    else:
        print("You need 6 mana to cast that.")
        return "ability failed"

    if context == "mob's turn":
        learn_ability(Fire, 8, target)


def Fira(x, y, context):
    if context == "hero's turn":
        if y.stats["mp_current"] >= 12:
            y.stats["mp_current"] -= 12
            damage = math.floor((y.stats["magic_base_atk"] + y.stats["magic_boost"]) * 1.65 * random.uniform(0.90, 1.10))
            x.stats["hp_current"] = math.floor(max(x.stats["hp_current"] - damage, 0))
            print("You cast Fira on your foe for ", damage, " points! ", sep='')
        else:
            print("You need 12 mana to cast that.")
            return "ability failed"
    elif context == "mob's turn":
        if x.stats["mp_current"] >= 12:
            x.stats["mp_current"] -= 12
            damage = math.floor((x.stats["magic_base_atk"] + x.stats["magic_boost"]) * 1.65 * random.uniform(0.90, 1.10))
            y.stats["hp_current"] = math.floor(max(y.stats["hp_current"] - damage, 0))
            print("You are struck by a chaotic burst of fire! You lose ", damage, " points.", sep='')
            rngesus = random.randint(1, 10)
            if "Fira" not in y.abilities and rngesus < 8:
                y.learn_ability("Fira", Fira)


def Firaga(x, y, context):
    if context == "hero's turn":
        if y.stats["mp_current"] >= 18:
            y.stats["mp_current"] -= 18
            damage = math.floor((y.stats["magic_base_atk"] + y.stats["magic_boost"]) * 2.25 * random.uniform(0.90, 1.10))
            x.stats["hp_current"] = math.floor(max(x.stats["hp_current"] - damage, 0))
            print("You cast Firaga on your foe for ", damage, " points! ", sep='')
        else:
            print("You need 18 mana to cast that.")
            return "ability failed"
    elif context == "mob's turn":
        if x.stats["mp_current"] >= 18:
            x.stats["mp_current"] -= 18
            damage = math.floor((x.stats["magic_base_atk"] + x.stats["magic_boost"]) * 2.25 * random.uniform(0.90, 1.10))
            y.stats["hp_current"] = math.floor(max(y.stats["hp_current"] - damage, 0))
            print("You are surrounded by an eruption of fire! You lose ", damage, " points.", sep='')
            rngesus = random.randint(1, 10)
            if "Firaga" not in y.abilities and rngesus < 8:
                y.learn_ability("Firaga", Firaga)


def Combust(x, y, context):
    if y.stats["mp_current"] >= 9:
        y.stats["mp_current"] -= 9
        y.stats["hp_current"] -= y.stats["hp_base"] * 0.2
        damage = math.floor((y.stats["magic_base_atk"] + y.stats["magic_boost"]) * random.uniform(2.90, 3.10))
        x.stats["hp_current"] = math.floor(max(x.stats["hp_current"] - damage, 0))
        print("You launch a chaotic volley of energy and damage your foe for ", damage, " points!",
              " You took some recoil damage from the blast, yourself.",
              sep='')
    else:
        print("You need 9 mana to cast that.")
        return "ability failed"


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
