import random

#region Skill

class Skill:
  def __init__(self, name, coinlist, coinpower, damage):
    self.name = name
    self.coinlist = coinlist
    self.coinpower = coinpower
    self.damage = damage
    # animation (stop motion, so sprite list here for coins to select from maybe)
    
  def __repr__(self):
    return f"Skill(name={self.name}, coinlist={self.coinlist}, coinpower={self.coinpower}, damage={self.damage})"
  
  def use(self, user, target, effectslist):
    # chance = user.sp + 50 
    # random coinflip with 'chance' for every coin
    return 
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
  
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


class Character:
  def __init__(self, name, sprite, speed, hp, skills=[], supportSkills=[]):
    self.name = name
    self.sprite = sprite
    self.speed = speed
    self.hp = hp
    self.skills = skills
    self.supportSkills = supportSkills

  def add_skill(self, skill_name, level):
    new_skill = Skill.Skill(skill_name, level)
    self.skills.append(new_skill)

  def calculate_speed(self):
    # speed var is a range, get a random value within that range
    currentSpeed = random.randint(self.speed[0], self.speed[1])
    #debuffs might be applied here in the future
    return currentSpeed
    
  def get_skills(self):
    return [(s.name, s.level) for s in self.skills]
  
  
  
  
