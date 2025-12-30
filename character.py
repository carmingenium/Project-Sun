import random

#region Skill

class Skill:
  def __init__(self, name, damage, sprite, implementation, description = f"Deals X damage.", available_targets=[("enemy", "skills")]):
    self.name = name
    self.damage = damage
    self.implementation = implementation
    self.description = description
    self.sprite = sprite
    
    self.available_targets = available_targets # [("friendly", "skills"), ("friendly, characters"), ("enemy", "characters"), ("enemy", "skills")] ("all") for both categories, ("click") for no targets?
    # animation (stop motion, so sprite list here for coins to select from maybe)

  def __repr__(self):
    return f"Skill(name={self.name}, description={self.description}, damage={self.damage})"

  def use(self, user, target):
    chance = user.sp + 50
    random_roll = random.randint(1, 100)
    if random_roll > chance:
      print(f"{user.name}'s skill {self.name} missed!") # maybe dialog over character?
      return
    self.implementation(self, target) 
    return

#region Skill Functions
#region Player Skills
#region Engineer
def engineer_baseskill1(self, target):
  target.take_damage(self.damage) #get dmg from skill object
  return
def engineer_baseskill2(self, target):
  target.take_damage(self.damage) #get dmg from skill object
  return

def engineer_sigskill1(self, target):
  target.take_damage(self.damage) #get dmg from skill object
  return
def engineer_sigskill2(self, target):
  target.take_damage(self.damage) #get dmg from skill object
  return
#endregion
#region Unknown
def unknown_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def unknown_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def unknown_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def unknown_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#region Head of Security
def hos_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def hos_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def hos_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def hos_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#region Security Officer
def secoff_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def secoff_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def secoff_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def secoff_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#region Clown
def clown_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def clown_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def clown_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def clown_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#region Mime
def mime_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def mime_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def mime_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def mime_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#region Borg
def borg_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def borg_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def borg_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def borg_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#region Medic
def medic_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def medic_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def medic_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def medic_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion

#endregion

#region Encounter1
#region Carps
def carp_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def carp_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def carp_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def carp_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#endregion

#region Encounter2
#region Changeling #hopefully form changing.
def changeling_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def changeling_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def changeling_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def changeling_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#region Traitor
def traitor_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def traitor_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def traitor_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def traitor_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#endregion

#region Encounter3
#region Heretic
def heretic_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def heretic_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def heretic_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def heretic_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#endregion

#region Encounter4
#region Dragon
def dragon_baseskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def dragon_baseskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def dragon_sigskill1(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
def dragon_sigskill2(user, target):
  target.take_damage(user.damage) #get dmg from skill object
  return
#endregion
#endregion

#endregion



class Character:
  def __init__(self, name, sprite, speed, hp, base_skills=[], sig_skills=[]):
    self.name = name
    self.sprite = sprite
    self.speedRange = speed
    self.speed = self.calculate_speed() # calculated at turn start
    self.sanity = 0 # almost always starts as 0
    self.max_hp = hp
    self.hp = self.max_hp
    self.base_skills = base_skills
    self.sig_skills = sig_skills
    self.alive = True

  def calculate_speed(self):
    # speed var is a range, get a random value within that range
    currentSpeed = random.randint(self.speedRange[0], self.speedRange[1])
    self.speed = currentSpeed
    return currentSpeed

  def take_damage(self, damage):
    self.hp -= damage
    if self.hp <= 0:
      self.hp = 0
      self.die()
    return self.hp
  
  def die(self):
    # dead state which disables characters from using skills
    self.alive = False
    # sprite change
    self.sprite = 'sprites/dead.png'
    return
  
  def add_sanity(self, amount):
    if(self.sanity + amount <= -50):
      self.sanity = 0
      self.insanity()
    elif(self.sanity + amount >= 50):
      self.sanity = 50
    self.sanity += amount
    
    return self.sanity
  def insanity(self):
    # handle insanity effects here
    return

#region CHARACTER INITIALIZATION
def initialize_characters(renderer):
  character_list = []
  return character_list
#endregion