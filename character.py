import random

#region Skill

class Skill:
  def __init__(self, name, coinlist, coinpower, damage, sprite, implementation):
    self.name = name
    self.coinlist = coinlist
    self.coinpower = coinpower
    self.damage = damage
    self.implementation = implementation
    self.sprite = sprite
    # animation (stop motion, so sprite list here for coins to select from maybe)
    
  def __repr__(self):
    return f"Skill(name={self.name}, coinlist={self.coinlist}, coinpower={self.coinpower}, damage={self.damage})"
  
  def use(self, user, target, effectslist):
    # chance = user.sp + 50 
    # random coinflip with 'chance' for every coin
    return 
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #

#region Coin
class Coin:
  def __init__(self, heads, tails, onhit, unbreakable=False):
    # heads, tails: list of effect dictionaries
    # onhit: list of effect dictionaries that trigger regardless of coin result
    self.heads = heads or []
    self.tails = tails or []
    self.onhit = onhit or []
    self.unbreakable = unbreakable
    # animations

  def __repr__(self):
    return f"Coin(unbreakable={self.unbreakable}, heads={self.heads}, tails={self.tails}, onhit={self.onhit})"

# coin is not really compatible in this state, later will be reworked %99

# Example usage:
# coin = Coin(
#   heads=[
#     {"type": "damage_modifier", "value": 0.5, "operation": "multiply"},  # +50% damage
#     {"type": "status", "effect": "bleed", "duration": 3} # Apply bleed for 3 turns
#   ],
#   tails=[
#     {"type": "sanity", "value": 10, "operation": "add"}  # +10 sanity
#   ],  
#   onhit=[
#     {"type": "healing", "value": 5, "target": "self"}
#   ],
#   unbreakable=True
# )
# possible additions:
  # flip coin function
  # 'type', 'value', 'effect', 'operation', 'duration', 'target' definitions 'support'
#endregion
#endregion

#region Skill Functions

def test_skill():
  print("Skill used!")
  

# list_of_funcs = [character.func1, character.func2, character.func3]
# for func in list_of_funcs:
#     func(param1, param2)

#endregion
class Character:
  def __init__(self, name, sprite, speed, hp, base_skills=[], sig_skills=[], supportSkills=[]):
    self.name = name
    self.sprite = sprite
    self.speedRange = speed
    self.speed = 0 # calculated at turn start
    self.sanity = 0 # almost always starts as 0
    self.hp = hp
    self.base_skills = base_skills
    self.sig_skills = sig_skills
    self.supportSkills = supportSkills

  def add_skill(self, skill_name, level):
    new_skill = Skill.Skill(skill_name, level)
    self.skills.append(new_skill)

  def calculate_speed(self):
    # speed var is a range, get a random value within that range
    currentSpeed = random.randint(self.speedRange[0], self.speedRange[1])
    self.speed = currentSpeed
    #debuffs might be applied here in the future
    return currentSpeed
    
  def get_skills(self):
    return [(s.name, s.level) for s in self.skills]
  
  
  
  
