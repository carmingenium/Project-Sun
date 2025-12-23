import random

#region Skill

class Skill:
  def __init__(self, name, coinamount, coinpower, damage, sprite, implementation, available_targets=[("enemy", "skills")]):
    self.name = name
    self.coinamount = coinamount
    self.coinpower = coinpower
    self.damage = damage
    self.implementation = implementation
    self.sprite = sprite
    
    self.available_targets = available_targets # [("friendly", "skills"), ("friendly, characters"), ("enemy", "characters"), ("enemy", "skills")] ("all") for both categories
    # animation (stop motion, so sprite list here for coins to select from maybe)

  def __repr__(self):
    return f"Skill(name={self.name}, coinamount={self.amount}, coinpower={self.coinpower}, damage={self.damage})"

  def use(self, user, target, effectslist):
    # chance = user.sp + 50
    # random coinflip with 'chance' for every coin
    return


#region Skill Functions

def engineer_wrench_skill(user, target):
  target.take_damage(15) #get dmg from skill object
  return


# list_of_funcs = [character.func1, character.func2, character.func3]
# for func in list_of_funcs:
#     func(param1, param2)

#endregion


#endregion



class Character:
  def __init__(self, name, sprite, speed, hp, base_skills=[], sig_skills=[], supportSkills=[]):
    self.name = name
    self.sprite = sprite
    self.speedRange = speed
    self.speed = self.calculate_speed() # calculated at turn start
    self.sanity = 0 # almost always starts as 0
    self.hp = hp
    self.base_skills = base_skills
    self.sig_skills = sig_skills
    self.supportSkills = supportSkills

    self.currentBaseSkills = [] # limit 2
    # initialization here as a test, later in different function to repeat per turn
    self.currentBaseSkills.append(self.base_skills[0])
    self.currentBaseSkills.append(self.base_skills[0])
    
    self.currentSigSkills = [] # depends on implementation, defense skill might always be here
    self.currentSigSkills.append(self.sig_skills[0])

  # def add_skill(self, skill_name, level):
  #   new_skill = Skill.Skill(skill_name, level)
  #   self.skills.append(new_skill)
  
  # def get_skills(self):
  #   return [(s.name, s.level) for s in self.skills]

  def calculate_speed(self):
    # speed var is a range, get a random value within that range
    currentSpeed = random.randint(self.speedRange[0], self.speedRange[1])
    self.speed = currentSpeed
    return currentSpeed

  def take_damage(self, damage):
    self.hp -= damage
    if self.hp < 0:
      self.hp = 0
      # death
    return self.hp
  
  def load_skills(self):
    # this is the format when there are more skills
    # self.currentBaseSkills = random.sample(self.base_skills, 2)
    
    # select 2 base skills randomly and load them to current base skills
    
    # load signature skills
    
    self.currentBaseSkills.append(self.base_skills[0])
    self.currentBaseSkills.append(self.base_skills[0])
    self.currentSigSkills.append(self.sig_skills[0])
    return


#region CHARACTER INITIALIZATION
def initialize_characters(renderer):
  character_list = []
  return character_list
#endregion