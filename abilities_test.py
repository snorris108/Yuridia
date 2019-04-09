# from Yuridia_OneDrive_project.Yuridia_OneDrive import *
import math
import random

def Strike(x, y, context):
    if context == "hero's turn":
        strike = math.floor((y.stats["base_melee_atk"] + y.stats["melee_boost"]) * random.uniform(0.90, 1.10))
        x.stats["current_hp"] = math.floor(max(x.stats["current_hp"] - strike, 0))
        print("You stike your foe for ", strike, " points! ", sep='')
    elif context == "mob's turn":
        strike = math.floor((x.stats["base_melee_atk"] + x.stats["melee_boost"]) * random.uniform(0.90, 1.10))
        y.stats["current_hp"] = math.floor(max(y.stats["current_hp"] - strike, 0))
        print("You are struck hard for ", strike, " points! ", sep='')


def Rush(x, y, context):
    if context == "hero's turn":
        y.stats["current_hp"] -= y.stats["base_hp"] * 0.1
        strike = math.floor((y.stats["base_melee_atk"] + y.stats["melee_boost"]) * random.uniform(2.90, 3.10))
        x.stats["current_hp"] = math.floor(max(x.stats["current_hp"] - strike, 0))
        print("You charge at your foe, ruthlessly dealing ", strike, "damage. You take a minor blow in your haste.")
    elif context == "mob's turn":
        x.stats["current_hp"] -= x.stats["base_hp"] * 0.1
        strike = math.floor((x.stats["base_melee_atk"] + x.stats["melee_boost"]) * random.uniform(2.90, 3.10))
        y.stats["current_hp"] = math.floor(max(y.stats["current_hp"] - strike, 0))
        print("Enraged, the enemy rushes you! You lose ", strike, " health.", sep='')
        chance = random.randint(1, 10)
        if "Rush" not in y.abilities and chance < 8:
            return y.learn_ability("Rush", Rush)


def Fire(x, y, context):
    if context == "hero's turn":
        if y.stats["current_mp"] >= 6:
            y.stats["current_mp"] -= 6
            strike = math.floor((y.stats["base_magic_atk"] + y.stats["magic_boost"]) * 1.15 * random.uniform(0.90, 1.10))
            x.stats["current_hp"] = math.floor(max(x.stats["current_hp"] - strike, 0))
            print("You cast Fire on your foe for ", strike, " points! ", sep='')
        else:
            print("You need 6 mana to cast that.")
            return "ability failed"
    elif context == "mob's turn":
        if x.stats["current_mp"] >= 6:
            x.stats["current_mp"] -= 6
            strike = math.floor((x.stats["base_magic_atk"] + x.stats["magic_boost"]) * 1.15 * random.uniform(0.90, 1.10))
            y.stats["current_hp"] = math.floor(max(y.stats["current_hp"] - strike, 0))
            print("You are struck by a wild flash of fire! You lose ", strike, " points.", sep='')
            chance = random.randint(1, 10)
            if "Fire" not in y.abilities and chance < 8:
                y.learn_ability("Fire", Fire)


def Fira(x, y, context):
    if context == "hero's turn":
        if y.stats["current_mp"] >= 12:
            y.stats["current_mp"] -= 12
            strike = math.floor((y.stats["base_magic_atk"] + y.stats["magic_boost"]) * 1.65 * random.uniform(0.90, 1.10))
            x.stats["current_hp"] = math.floor(max(x.stats["current_hp"] - strike, 0))
            print("You cast Fira on your foe for ", strike, " points! ", sep='')
        else:
            print("You need 12 mana to cast that.")
            return "ability failed"
    elif context == "mob's turn":
        if x.stats["current_mp"] >= 12:
            x.stats["current_mp"] -= 12
            strike = math.floor((x.stats["base_magic_atk"] + x.stats["magic_boost"]) * 1.65 * random.uniform(0.90, 1.10))
            y.stats["current_hp"] = math.floor(max(y.stats["current_hp"] - strike, 0))
            print("You are struck by a chaotic burst of fire! You lose ", strike, " points.", sep='')
            chance = random.randint(1, 10)
            if "Fira" not in y.abilities and chance < 8:
                y.learn_ability("Fira", Fira)


def Firaga(x, y, context):
    if context == "hero's turn":
        if y.stats["current_mp"] >= 18:
            y.stats["current_mp"] -= 18
            strike = math.floor((y.stats["base_magic_atk"] + y.stats["magic_boost"]) * 2.25 * random.uniform(0.90, 1.10))
            x.stats["current_hp"] = math.floor(max(x.stats["current_hp"] - strike, 0))
            print("You cast Firaga on your foe for ", strike, " points! ", sep='')
        else:
            print("You need 18 mana to cast that.")
            return "ability failed"
    elif context == "mob's turn":
        if x.stats["current_mp"] >= 18:
            x.stats["current_mp"] -= 18
            strike = math.floor((x.stats["base_magic_atk"] + x.stats["magic_boost"]) * 2.25 * random.uniform(0.90, 1.10))
            y.stats["current_hp"] = math.floor(max(y.stats["current_hp"] - strike, 0))
            print("You are surrounded by an eruption of fire! You lose ", strike, " points.", sep='')
            chance = random.randint(1, 10)
            if "Firaga" not in y.abilities and chance < 8:
                y.learn_ability("Firaga", Firaga)


def Combust(x, y, context):
    if y.stats["current_mp"] >= 9:
        y.stats["current_mp"] -= 9
        y.stats["current_hp"] -= y.stats["base_hp"] * 0.2
        strike = math.floor((y.stats["base_magic_atk"] + y.stats["magic_boost"]) * random.uniform(2.90, 3.10))
        x.stats["current_hp"] = math.floor(max(x.stats["current_hp"] - strike, 0))
        print("You launch a chaotic volley of energy and damage your foe for ", strike, " points!",
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
