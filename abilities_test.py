import math
import random


def action_msg(context, player_msg, mob_msg):
    print(player_msg) if context == "hero's turn" else print(mob_msg)


def learn_ability(ability, learning_rate, target):
    rngesus = random.randint(1, 10)
    if ability.__name__ not in target.abilities and rngesus < learning_rate:
        target.learn_ability(ability.__name__, ability)


def Strike(target, caster, context):
    damage = math.floor((caster.stats["base_melee_atk"] + caster.stats["melee_boost"]) * random.uniform(0.90, 1.10))
    target.stats["current_hp"] = math.floor(max(target.stats["current_hp"] - damage, 0))
    player_msg = f"You stike your foe for {str(damage)} points!"
    mob_msg = f"You are struck hard for {str(damage)} points!"
    action_msg(context, player_msg, mob_msg)


def Rush(target, caster, context):
    damage = math.floor((caster.stats["base_melee_atk"] + caster.stats["melee_boost"]) * random.uniform(1.90, 2.10))
    target.stats["current_hp"] = math.floor(max(target.stats["current_hp"] - damage, 0))
    caster.stats["current_hp"] -= caster.stats["base_hp"] * 0.1
    player_msg = f"You charge at your foe, ruthlessly dealing {str(damage)} damage. You take a minor blow in your haste."
    mob_msg = f"Enraged, the enemy rushes you! You lose {str(damage)} health."
    action_msg(context, player_msg, mob_msg)

    if context == "mob's turn":
        learn_ability(Rush, 8, target)


def Fire(target, caster, context):
    if caster.stats["current_mp"] >= 6:
        caster.stats["current_mp"] -= 6
        damage = math.floor((caster.stats["base_magic_atk"] + caster.stats["magic_boost"]) * 1.15 * random.uniform(0.90, 1.10))
        target.stats["current_hp"] = math.floor(max(target.stats["current_hp"] - damage, 0))
        player_msg = f"You cast Fire on your foe for {str(damage)} points!"
        mob_msg = f"You are struck by a wild flash of fire! You lose {str(damage)} points."
    else:
        print("You need 6 mana to cast that.")
        return "ability failed"

    if context == "mob's turn":
        learn_ability(Fire, 8, target)


def Fira(x, y, context):
    if context == "hero's turn":
        if y.stats["current_mp"] >= 12:
            y.stats["current_mp"] -= 12
            damage = math.floor((y.stats["base_magic_atk"] + y.stats["magic_boost"]) * 1.65 * random.uniform(0.90, 1.10))
            x.stats["current_hp"] = math.floor(max(x.stats["current_hp"] - damage, 0))
            print("You cast Fira on your foe for ", damage, " points! ", sep='')
        else:
            print("You need 12 mana to cast that.")
            return "ability failed"
    elif context == "mob's turn":
        if x.stats["current_mp"] >= 12:
            x.stats["current_mp"] -= 12
            damage = math.floor((x.stats["base_magic_atk"] + x.stats["magic_boost"]) * 1.65 * random.uniform(0.90, 1.10))
            y.stats["current_hp"] = math.floor(max(y.stats["current_hp"] - damage, 0))
            print("You are struck by a chaotic burst of fire! You lose ", damage, " points.", sep='')
            rngesus = random.randint(1, 10)
            if "Fira" not in y.abilities and rngesus < 8:
                y.learn_ability("Fira", Fira)


def Firaga(x, y, context):
    if context == "hero's turn":
        if y.stats["current_mp"] >= 18:
            y.stats["current_mp"] -= 18
            damage = math.floor((y.stats["base_magic_atk"] + y.stats["magic_boost"]) * 2.25 * random.uniform(0.90, 1.10))
            x.stats["current_hp"] = math.floor(max(x.stats["current_hp"] - damage, 0))
            print("You cast Firaga on your foe for ", damage, " points! ", sep='')
        else:
            print("You need 18 mana to cast that.")
            return "ability failed"
    elif context == "mob's turn":
        if x.stats["current_mp"] >= 18:
            x.stats["current_mp"] -= 18
            damage = math.floor((x.stats["base_magic_atk"] + x.stats["magic_boost"]) * 2.25 * random.uniform(0.90, 1.10))
            y.stats["current_hp"] = math.floor(max(y.stats["current_hp"] - damage, 0))
            print("You are surrounded by an eruption of fire! You lose ", damage, " points.", sep='')
            rngesus = random.randint(1, 10)
            if "Firaga" not in y.abilities and rngesus < 8:
                y.learn_ability("Firaga", Firaga)


def Combust(x, y, context):
    if y.stats["current_mp"] >= 9:
        y.stats["current_mp"] -= 9
        y.stats["current_hp"] -= y.stats["base_hp"] * 0.2
        damage = math.floor((y.stats["base_magic_atk"] + y.stats["magic_boost"]) * random.uniform(2.90, 3.10))
        x.stats["current_hp"] = math.floor(max(x.stats["current_hp"] - damage, 0))
        print("You launch a chaotic volley of energy and damage your foe for ", damage, " points!",
              " You took some recoil damage from the blast, yourself.",
              sep='')
    else:
        print("You need 9 mana to cast that.")
        return "ability failed"


def Heal(x, y, context):
    if context == "hero's turn":
        if y.stats["current_mp"] >= 3:
            y.stats["current_mp"] -= 3
            health_gained = math.floor(y.stats["base_hp"] * 0.30 + y.stats["base_hp"] * y.stats["magic_boost"] / 500)
            y.stats["current_hp"] += health_gained
            if y.stats["current_hp"] > y.stats["base_hp"]:
                print("You feel exceedingly healthy. (^", health_gained, "^ hp.)", sep='')
            else:
                print("You're bleeding a bit less now. (^", health_gained, "^ hp.)", sep='')
        else:
            print("You unfortunately have even less mana than blood left.")
            return "ability failed"
    elif context == "mob's turn":
        if x.stats["current_mp"] >= 3:
            x.stats["current_mp"] -= 3
            health_gained = math.floor(x.stats["base_hp"] * 0.30 + x.stats["base_hp"] * x.stats["base_magic_atk"] / 500)
            x.stats["current_hp"] += health_gained
            print("It's bleeding a bit less now. (^", health_gained, "^ hp.)", sep='')
