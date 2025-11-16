import skill
class Character:
  def __init__(self, name, sprite, speed, hp, skills=[], supportSkills=[]):
    self.name = name
    self.sprite = sprite
    self.speed = speed
    self.hp = hp
    self.skills = skills
    self.supportSkills = supportSkills

  def add_skill(self, skill_name, level):
    new_skill = skill.Skill(skill_name, level)
    self.skills.append(new_skill)

  def calculate_speed(self):
    # speed var is a range, get a random value within that range
    return self.speed
    
  def get_skills(self):
    return [(s.name, s.level) for s in self.skills]