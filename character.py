import random

#region Skill

class Skill:
  def __init__(self, name, damage, sprite, implementation, description = f"Deals X damage.", available_targets=[("enemy", "skills")]):
    self.name = name
    self.damage = damage
    self.currentdamage = damage
    self.implementation = implementation
    self.description = description
    self.sprite = sprite
    
    self.available_targets = available_targets # [("friendly", "skills"), ("friendly, characters"), ("enemy", "characters"), ("enemy", "skills")] ("all") for both categories, ("click") for no targets?
    self.user = None

  def __repr__(self):
    return f"Skill(name={self.name}, description={self.description}, damage={self.damage})"

  def use(self, user, target):
    if(self != user.sig_skills[1]): # if not a defense skill
      chance = user.sp + 50
      random_roll = random.randint(1, 100)
      if random_roll > chance:
        print(f"{user.name}'s skill {self.name} missed!") # maybe dialog over character?
        return
    self.implementation(self, target) 
    # after skill is used, restore to base format.
    self.currentdamage = self.damage 
    return

#region Skill Functions
#region Player Skills
#region Engineer DONE
def engineer_baseskill1(self, target):
  target.take_damage(self.currentdamage)
  return
def engineer_baseskill2(self, target):
  if(target.name == "Mediorg"):
    target.hp += self.currentdamage #healing effect
    if target.hp > target.max_hp:
      target.hp = target.max_hp
    return
  target.take_damage(self.currentdamage) 
  return

def engineer_sigskill1(self, target):
  target.take_damage(self.currentdamage)
  self.user.add_sanity(10)
  return
def engineer_sigskill2(self, target): # decrease damage of target skill by 16 for 1 turn
  target.currentdamage -= self.currentdamage
  if target.currentdamage < 0:
    target.currentdamage = 0
  target.take_damage(self.currentdamage)
  return
#endregion
#region Unknown
def unknown_baseskill1(self, target):
  target.take_damage(self.currentdamage) 
  return
def unknown_baseskill2(self, target):
  if(target.name == "Mediborg"):
    return
  if(target.name == "Head of Security"):
    target.hp += self.damage #healing effect
    if(target.hp > target.max_hp):
      target.hp = target.max_hp
    return
  if(target.name == "Security Officer"):
    target.hp += self.damage // 2 #healing effect
    if(target.hp > target.max_hp):
      target.hp = target.max_hp
    return

  # Determine if target is an enemy (not in player party)
  # For this context, treat 'enemy' as not one of the following names:
  other_player_names = ["Blacked Out Engineer", "Unknown", "Clown", "Mime", "Medic"]
  if target.name not in other_player_names:
    target.take_damage(self.damage)
    self.user.add_sanity(-10)
    return
  else:
    self.user.add_sanity(-5)
    return
def unknown_sigskill1(self, target):
  target.take_damage(self.currentdamage)
  target.currentSpeed -= 1
  if target.currentSpeed < 1:
    target.currentSpeed = 1
  return
def unknown_sigskill2(self, target):
  target.currentdamage -= self.currentdamage
  if target.currentdamage < 0:
    target.currentdamage = 0
  random_roll = random.randint(1, 100)
  if random_roll <= 30:
    return
  target.take_damage(self.currentdamage)
  return
#endregion
#region Head of Security
def hos_baseskill1(self, target):
  target.take_damage(self.damage)
  target.currentSpeed -= 1
  if target.currentSpeed < 1:
    target.currentSpeed = 1
  return
def hos_baseskill2(self, target):
  target.take_damage(self.damage)
  return
def hos_sigskill1(self, target):
  target.take_damage(self.damage)
  return
def hos_sigskill2(self, target):
  target.currentSpeed += self.damage 
  return
#endregion
#region Security Officer
def secoff_baseskill1(self, target):
  target.take_damage(self.damage) 
  target.currentSpeed -= 1
  if target.currentSpeed < 1:
    target.currentSpeed = 1
def secoff_baseskill2(self, target):
  target.take_damage(self.damage) 
  return
def secoff_sigskill1(self, target):
  target.take_damage(self.damage) 
  return
def secoff_sigskill2(self, target):
  target.currentdamage -= self.damage
  if target.currentdamage < 0:
    target.currentdamage = 0 
  return
#endregion
#region Clown
def clown_baseskill1(self, target):
  target.currentSpeed -= self.damage
  if target.currentSpeed < 1:
    target.currentSpeed = 1
  return
def clown_baseskill2(self, target):
  target.add_sanity(-self.damage)
  return
def clown_sigskill1(self, target):
  other_player_names = ["Blacked out Engineer", "Unknown", "Clown", "Mime", "Medic", "Head of Security", "Security Officer"]
  if target.name in other_player_names:
    target.add_sanity(self.damage)
  else:
    target.add_sanity(-self.damage)
  return
def clown_sigskill2(self, target): # CLICK SKILL, lastly used maybe?
  target.hp += self.damage
  if target.hp > target.max_hp:
    target.hp = target.max_hp
  return
#endregion
#region Mime
def mime_baseskill1(self, target):
  target.currentSpeed -= self.damage
  if target.currentSpeed < 1:
    target.currentSpeed = 1
  return
def mime_baseskill2(self, target):
  target.add_sanity(-self.damage)
  return
def mime_sigskill1(self, target):
  target.take_damage(self.damage)
  return
def mime_sigskill2(self, target):
  target.currentdamage -= self.damage
  if target.currentdamage < 0:
    target.currentdamage = 0
  return
#endregion
#region Borg
def borg_baseskill1(self, target):
  target.hp += self.damage
  if target.hp > target.max_hp:
    target.hp = target.max_hp
  return
def borg_baseskill2(self, target): # speed related
  target.currentSpeed += 1
  target.hp += self.damage
  if target.hp > target.max_hp:
    target.hp = target.max_hp
  return
def borg_sigskill1(self, target): #not implemented
  target.take_damage(self.damage) 
  return
def borg_sigskill2(self, target): #not implemented
  target.take_damage(self.damage) 
  return
#endregion
#region Medic
def medic_baseskill1(self, target):
  other_player_names = ["Blacked Out Engineer", "Unknown", "Clown", "Mime", "Head of Security", "Security Officer"]
  if target.name in other_player_names:
    target.hp += self.damage
    if target.hp > target.max_hp:
      target.hp = target.max_hp
  else:
    target.take_damage(self.damage)
  return
def medic_baseskill2(self, target):
  target.hp += self.damage
  if target.hp > target.max_hp:
    target.hp = target.max_hp 
  return
def medic_sigskill1(self, target):
  target.currentSpeed += self.damage
  return
def medic_sigskill2(self, target):
  target.take_damage(self.damage) 
  return
#endregion

#endregion

#region Encounter1
#region Carps
def carp_baseskill1(self, target):
  target.take_damage(self.damage)
  return
def carp_baseskill2(self, target):
  target.currentSpeed += self.damage
  return
def carp_sigskill1(self, target):
  target.take_damage(self.damage)
  return
def carp_sigskill2(self, target):
  target.currentdamage -= self.damage
  if target.currentdamage < 0:
    target.currentdamage = 0
  return
#endregion
#endregion

#region Encounter2
#region Changeling #hopefully form changing.
def changeling_baseskill1(self, target):
  target.take_damage(self.damage)  
  return
def changeling_baseskill2(self, target):
  target.take_damage(self.damage)
  target.add_sanity(-5)  
  return
def changeling_sigskill1(self, target):
  target.take_damage(self.damage)
  target.currentSpeed -= 1
  if target.currentSpeed < 1:
    target.currentSpeed = 1  
  return
def changeling_sigskill2(self, target):
  target.hp += self.damage
  if target.hp > target.max_hp:
    target.hp = target.max_hp 
  return
#endregion
#region Traitor
def traitor_baseskill1(self, target):
  target.take_damage(self.damage)  
  return
def traitor_baseskill2(self, target):
  target.add_sanity(-self.damage)  
  return
def traitor_sigskill1(self, target):
  target.take_damage(self.damage)  
  return
def traitor_sigskill2(self, target):
  target.hp += self.damage
  if target.hp > target.max_hp:
    target.hp = target.max_hp 
  return
#endregion
#endregion

#region Encounter3
#region Heretic
def heretic_baseskill1(self, target):
  target.take_damage(self.damage)
  target.add_sanity(-self.damage)  
  return
def heretic_baseskill2(self, target):
  target.hp += self.damage
  if target.hp > target.max_hp:
    target.hp = target.max_hp
  target.add_sanity(self.damage)
  return
def heretic_sigskill1(self, target):
  target.take_damage(self.damage)
  target.add_sanity(-self.damage) 
  return
def heretic_sigskill2(self, target):
  target.currentdamage -= self.damage
  self.user.add_sanity(self.damage) 
  return
#endregion
#endregion

#region Encounter4
#region Dragon
def dragon_baseskill1(self, target):
  target.take_damage(self.damage)  
  return
def dragon_baseskill2(self, target):
  target.take_damage(self.damage)  
  return
def dragon_sigskill1(self, target):
  target.take_damage(self.damage)  
  return
def dragon_sigskill2(self, target):
  target.take_damage(self.damage)  
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
    elif(self.sanity + amount >= 50):
      self.sanity = 50
    else:
      self.sanity += amount
    return self.sanity

#region CHARACTER INITIALIZATION
def initialize_characters(renderer):
  character_list = []
  return character_list
#endregion