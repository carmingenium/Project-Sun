import pygame
import character
import math
import random

#region Encounter Class
class Encounter:
  def __init__(self, name, encounterPartyCharacters, encounterPartyPositions, playerPartyPositions, playerPartyCharacters, combatBGimage):
    self.name = name
    self.encounterPartyCharacters = encounterPartyCharacters
    self.encounterPartyPositions = encounterPartyPositions
    self.playerPartyCharacters = playerPartyCharacters
    self.playerPartyPositions = playerPartyPositions
    self.combatBGimage = combatBGimage
#endregion

#region initialization
# constants
pygame.init()
CombatBGPos = (0, 0)
x = 1920
y = 1080
screen = pygame.display.set_mode((x, y)) # this has to be static as long as the camera system depends on it
center_x = x // 2
center_y = y // 2

sprite_size = 160 # 32*5 - defined so that positions can be calculated from this variable.
skill_size = 32 # per skill 

# dialogue positions # possibly moved to another initialization part?
renderposRight = (1400, 200)
renderposLeft = (100, 200)

barBG = pygame.image.load('sprites/backgrounds/characterselect.png').convert()
combatBackGround = pygame.image.load('sprites/backgrounds/combat_test.png').convert()

turnEndButtonSprite = pygame.image.load('sprites/ui/winrate.png').convert_alpha()
turnEndButton = pygame.Rect(x - 200, y - 100, 180, 80) # position and size of the button
turnEndButtonSprite = pygame.transform.scale(turnEndButtonSprite, (turnEndButton.width, turnEndButton.height))

# variables
playerPartyPositions = []
enemyPartyPositions = []

# temporary variables
selected_skill_pos = None
targeted_skill_pos = None
targeted_character_pos = None

targeted_skills_position_list = []
targeted_skills_list = []

enemyPartyChars = []
playerPartyChars = []

# party select variables
select_x_offset = 34
select_y_offset = 50
barCharacterPositions = [(408, 910), (408+sprite_size+select_x_offset, 910), (408+sprite_size*2+select_x_offset*2, 910), (408+sprite_size*3+select_x_offset*3, 910), (408+sprite_size*4+select_x_offset*4, 910),
                        (1190, 110), (1190, 110 + sprite_size+select_y_offset), (1190, 110 + (sprite_size + select_y_offset)*2 )]
allPlayerCharacters = []
selectedPartyCharacters = [None, None, None, None] # max 4 characters in active party
benchedPartyCharacters = [] # rest of the characters


character_sprites = []
characterList = []
encountersList = []
encounterBackgroundSprites = []
def spriteListInitialize(characters, encounters):
  # characters
  global characterList, character_sprites, encountersList, encounterBackgroundSprites
  for char in characters:
    try:
      character_sprites.append(pygame.image.load(char.sprite).convert_alpha())
      print(f"Loaded sprite for {char.name} from path {char.sprite}")
    except: 
      print(f"Error loading sprite for {char.name} from path {char.sprite}") 
  characterList = characters
  # backgrounds
  for encounter in encounters:
    try:
      encounter.combatBGimage = pygame.image.load(encounter.combatBGimage).convert()
      print(f"Loaded combat background for {encounter.name} from path {encounter.combatBGimage}")
      encountersList.append(encounter)
      encounterBackgroundSprites.append(encounter.combatBGimage)
    except:
      print(f"Error loading combat background for {encounter.name} from path {encounter.combatBGimage}")
  

skill_sprites = []
skillList = []
def skillSpriteInitialize(skills):
  global skillList, skill_sprites
  for skill in skills:
    try:
      skill_sprites.append(pygame.image.load(skill.sprite).convert_alpha())
      print(f"Loaded sprite for skill {skill.name} from path {skill.sprite}")
    except: 
      print(f"Error loading sprite for skill {skill.name} from path {skill.sprite}")
  skillList = skills

def initializePlayerCharacters(availableCharacters):
  global benchedPartyCharacters, allPlayerCharacters
  allPlayerCharacters = availableCharacters.copy()
  benchedPartyCharacters = availableCharacters.copy()
  return
  
#endregion 

#region Skill association
def ResetCurrentTargeting():
  global selected_skill_pos, targeted_skill_pos, targeted_character_pos
  selected_skill_pos = None
  targeted_skill_pos = None
  targeted_character_pos = None
  return
def SetSkillTargeting(target_pair): # target pair is two tuples of positions
  global targeted_skills_position_list, targeted_skills_list
  if(target_pair[0] == target_pair[1]): # prevent targeting self
    return  
  if(target_pair in targeted_skills_position_list): # targeted before, return
    return
  targeting_skill = FindSkillByPosition(target_pair[0])
  targeting_char = FindCharacterBySkill(targeting_skill)
  skill_type = targeting_skill in targeting_char.base_skills and "base" or targeting_skill in targeting_char.sig_skills and "sig" or None
    
  targeted_object = FindSkillByPosition(target_pair[1]) or FindCharacterByPosition(target_pair[1])

  
  # target is character or skill
  if(isinstance(targeted_object, character.Skill)): # skill
    targeted_char = FindCharacterBySkill(targeted_object)
    targeted_object_type = "skills"
  elif(isinstance(targeted_object, character.Character)): # character
    targeted_char = targeted_object
    targeted_object_type = "characters"
  
  targeting_party = FindPartyFromCharacter(targeting_char)
  targeted_party = FindPartyFromCharacter(targeted_char)
  
  # prevent targeting invalid target types
  if( not ((targeting_skill.available_targets[0] == targeted_party  or targeting_skill.available_targets[0] == "all") and (targeting_skill.available_targets[1] == targeted_object_type)) ): # target invalid
    return
  
  if(HasCharacterUsedSkillType(targeting_char, skill_type)): # already used skill of this type
    # find old targeting
    for new_pair in targeted_skills_position_list:
      if(new_pair[0][0] == target_pair[0][0]): # found old targeting 
        # remove
        targeted_skills_position_list.remove(new_pair)
        targeted_skills_list.remove((FindSkillByPosition(new_pair[0]), FindSkillByPosition(new_pair[1]) or FindCharacterByPosition(new_pair[1])))  
        break
      
  targeted_skills_list.append((targeting_skill, targeted_object)) # to be actualized at turn ends when they are implemented
  targeted_skills_position_list.append(target_pair)

  return
def EnemySkillTargeting(): 
  # random target selection:
  # for every enemy skill type (1 for base 1 for signature), select a target once
  
  for enemy in enemyPartyChars:
    # base skill
    skillSelection = random.randint(0, 1) # base skill index
    skill = enemy.base_skills[skillSelection]
    valid_targets = []
    if(skill.available_targets[1] == "characters"):
      if(skill.available_targets[0] == "player"):
        target_party = playerPartyChars
      elif(skill.available_targets[0] == "enemy"):
        target_party = enemyPartyChars
      elif(skill.available_targets[0] == "all"):
        target_party = playerPartyChars + enemyPartyChars
      valid_targets = target_party
    
    elif(skill.available_targets[1] == "skills"):
      if(skill.available_targets[0] == "player"):
        target_party = playerPartyChars
      elif(skill.available_targets[0] == "enemy"):
        target_party = enemyPartyChars
      elif(skill.available_targets[0] == "all"):
        target_party = playerPartyChars + enemyPartyChars
      elif(skill.available_targets[0] == "click"):
        target_party = [enemy] # self-targeting skills for now
        return # later added
      valid_targets = []
      for target_char in target_party:
        for target_skill in target_char.base_skills + target_char.sig_skills:
          valid_targets.append(target_skill)
    if(len(valid_targets) == 0):
      continue
    target = random.choice(valid_targets)
    targeted_skills_list.append((skill, target))
    targeted_skills_position_list.append( (FindPositionFromSkill(skill), FindPositionFromSkill(target) or FindPositionFromCharacter(target)) )
    
    
    
    # signature skill
    skillSelection = random.randint(0, 1) # sig skill index
    skill = enemy.sig_skills[skillSelection]
    valid_targets = []
    if(skill.available_targets[1] == "characters"):
      if(skill.available_targets[0] == "player"):
        target_party = playerPartyChars
      elif(skill.available_targets[0] == "enemy"):
        target_party = enemyPartyChars
      elif(skill.available_targets[0] == "all"):
        target_party = playerPartyChars + enemyPartyChars
      valid_targets = target_party
    
    elif(skill.available_targets[1] == "skills"):
      if(skill.available_targets[0] == "player"):
        target_party = playerPartyChars
      elif(skill.available_targets[0] == "enemy"):
        target_party = enemyPartyChars
      elif(skill.available_targets[0] == "all"):
        target_party = playerPartyChars + enemyPartyChars
      elif(skill.available_targets[0] == "click"):
        target_party = [enemy] # self-targeting skills for now
        return # later added
      valid_targets = []
      for target_char in target_party:
        for target_skill in target_char.base_skills + target_char.sig_skills:
          valid_targets.append(target_skill)
  
  return

def HasCharacterUsedSkillType(character, skill_type):
  for pair in targeted_skills_list:
    sk = pair[0]
    if skill_type == "base" and sk in character.base_skills:
      return True
    if skill_type == "sig" and sk in character.sig_skills:
      return True
  return False


def FindSkillByPosition(pos):
  # find party depending on x coordinate
  
  if(pos[0] < center_x):
    party = playerPartyPositions
    charParty = playerPartyChars
  else:
    party = enemyPartyPositions 
    charParty = enemyPartyChars
  
  # find position in party depending on coordinates
  for charPos in party:
    if ((pos[0] == charPos[0]+(sprite_size//2)-(skill_size//2)) or (pos[0] == charPos[0]+(sprite_size//2)+(skill_size//2))):
      char = charParty[party.index(charPos)]
      # base skills
      baseSkill_1_Pos = (charPos[0]+(sprite_size//2)-(skill_size//2) , charPos[1]-(skill_size*2))
      baseSkill_2_Pos = (charPos[0]+(sprite_size//2)-(skill_size//2), charPos[1]-(skill_size*2)+skill_size)
      sigSkillPos = (charPos[0]+(sprite_size//2)+(skill_size//2), charPos[1]-(skill_size*2))
      sigSkillPos_2 = (charPos[0]+(sprite_size//2)+(skill_size//2), charPos[1]-(skill_size*2)+skill_size)
      
      if pos == baseSkill_1_Pos:
        return char.base_skills[0]
      elif pos == baseSkill_2_Pos:
        return char.base_skills[1]
      elif pos == sigSkillPos:
        return char.sig_skills[0]
      elif pos == sigSkillPos_2:
        return char.sig_skills[1]
  return None
def FindCharacterByPosition(pos):
  if(pos[0] < center_x):
    party = playerPartyPositions
    charParty = playerPartyChars
  else:
    party = enemyPartyPositions 
    charParty = enemyPartyChars
  
  # find position in party depending on coordinates
  for charPos in party:
    index = party.index(charPos)
    if pos == charPos: # found character position
      char = charParty[index]
      return char
  return None
def FindCharacterBySkill(skill):
  for char in playerPartyChars + enemyPartyChars:
    if(skill in char.base_skills or skill in char.sig_skills):
      return char
  return None
def FindPartyFromCharacter(character):
  if(character in playerPartyChars):
    return "player"
  elif(character in enemyPartyChars):
    return "enemy"
  return None
def FindPositionFromCharacter(character):
  if(character in playerPartyChars):
    index = playerPartyChars.index(character)
    return playerPartyPositions[index]
  elif(character in enemyPartyChars):
    index = enemyPartyChars.index(character)
    return enemyPartyPositions[index]
  return None
def FindPositionFromSkill(skill):
  char = FindCharacterBySkill(skill)
  charPos = FindPositionFromCharacter(char)
  if skill in char.base_skills:
    skillIndex = char.base_skills.index(skill)
    skillPos = (charPos[0]+(sprite_size//2)-(skill_size//2), charPos[1]-(skill_size*2)+ (skill_size * skillIndex))
    return skillPos
  elif skill in char.sig_skills:
    skillIndex = char.sig_skills.index(skill)
    skillPos = (charPos[0]+(sprite_size//2)+(skill_size//2), charPos[1]-(skill_size*2)+ (skill_size * skillIndex))
    return skillPos
  return None
#endregion

#region Rendering support functions
def findBackgroundForEncounter(encounter):
  for enc in encountersList:
    if enc.name == encounter.name:
      index = encountersList.index(enc)
      return encounterBackgroundSprites[index]
  return None
def spriteNovelify(sprite):
  novelSprite = pygame.transform.scale(sprite, (sprite.get_width()*35, sprite.get_height()*35))
  return novelSprite

def findCharacterSprite(character):
  for char in characterList:
    if char.name == character.name:
      index = characterList.index(char)
      return character_sprites[index]
def findSkillSprite(skill):
  for sk in skillList:
    if sk.name == skill.name:
      index = skillList.index(sk)
      return skill_sprites[index]

def HighlightValidTargets(skill):
  # highlight valid targets for given skill in green, non-valid targets in red.
  targets = skill.available_targets[0] # "player", "enemy", "all", "click"
  if targets == "click":
    # highlight user
    return
  elif (targets == "player"):
    valid_party = playerPartyPositions
    invalid_party = enemyPartyPositions
  elif (targets == "enemy"):
    valid_party = enemyPartyPositions
    invalid_party = playerPartyPositions
  elif (targets == "all"):
    valid_party = playerPartyPositions + enemyPartyPositions
    invalid_party = []
  
  targets = skill.available_targets[1] # "characters", "skills"
  
  final_validation = []
  final_invalids = []
  if(targets == "characters"):
    for pos in valid_party: # character pos
      baseSkill_1_Pos = (pos[0]+(sprite_size//2)-(skill_size//2) , pos[1]-(skill_size*2))
      baseSkill_2_Pos = (pos[0]+(sprite_size//2)-(skill_size//2), pos[1]-(skill_size*2)+skill_size)
      sigSkillPos = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2))
      sigSkillPos_2 = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2)+skill_size)
      
      base1rect = pygame.rect.Rect(baseSkill_1_Pos[0], baseSkill_1_Pos[1], skill_size, skill_size)
      base2rect = pygame.rect.Rect(baseSkill_2_Pos[0], baseSkill_2_Pos[1], skill_size, skill_size)
      sig1rect = pygame.rect.Rect(sigSkillPos[0], sigSkillPos[1], skill_size, skill_size)
      sig2rect = pygame.rect.Rect(sigSkillPos_2[0], sigSkillPos_2[1], skill_size, skill_size)
      charRect = pygame.rect.Rect(pos[0], pos[1], sprite_size, sprite_size)
      
      final_invalids.append(base1rect)
      final_invalids.append(base2rect)
      final_invalids.append(sig1rect)
      final_invalids.append(sig2rect)
      final_validation.append(charRect)
    for pos in invalid_party:
      baseSkill_1_Pos = (pos[0]+(sprite_size//2)-(skill_size//2) , pos[1]-(skill_size*2))
      baseSkill_2_Pos = (pos[0]+(sprite_size//2)-(skill_size//2), pos[1]-(skill_size*2)+skill_size)
      sigSkillPos = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2))
      sigSkillPos_2 = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2)+skill_size)
      
      base1rect = pygame.rect.Rect(baseSkill_1_Pos[0], baseSkill_1_Pos[1], skill_size, skill_size)
      base2rect = pygame.rect.Rect(baseSkill_2_Pos[0], baseSkill_2_Pos[1], skill_size, skill_size)
      sig1rect = pygame.rect.Rect(sigSkillPos[0], sigSkillPos[1], skill_size, skill_size)
      sig2rect = pygame.rect.Rect(sigSkillPos_2[0], sigSkillPos_2[1], skill_size, skill_size)
      charRect = pygame.rect.Rect(pos[0], pos[1], sprite_size, sprite_size)
      
      final_invalids.append(base1rect)
      final_invalids.append(base2rect)
      final_invalids.append(sig1rect)
      final_invalids.append(sig2rect)
      final_invalids.append(charRect)
  elif(targets == "skills"):
    for pos in valid_party:
      baseSkill_1_Pos = (pos[0]+(sprite_size//2)-(skill_size//2) , pos[1]-(skill_size*2))
      baseSkill_2_Pos = (pos[0]+(sprite_size//2)-(skill_size//2), pos[1]-(skill_size*2)+skill_size)
      sigSkillPos = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2))
      sigSkillPos_2 = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2)+skill_size)
      
      base1rect = pygame.rect.Rect(baseSkill_1_Pos[0], baseSkill_1_Pos[1], skill_size, skill_size)
      base2rect = pygame.rect.Rect(baseSkill_2_Pos[0], baseSkill_2_Pos[1], skill_size, skill_size)
      sig1rect = pygame.rect.Rect(sigSkillPos[0], sigSkillPos[1], skill_size, skill_size)
      sig2rect = pygame.rect.Rect(sigSkillPos_2[0], sigSkillPos_2[1], skill_size, skill_size)
      charRect = pygame.rect.Rect(pos[0], pos[1], sprite_size, sprite_size)
      
      
      final_validation.append(base1rect)
      final_validation.append(base2rect)
      final_validation.append(sig1rect)
      final_validation.append(sig2rect)
      final_invalids.append(charRect)
    for pos in invalid_party:
      baseSkill_1_Pos = (pos[0]+(sprite_size//2)-(skill_size//2) , pos[1]-(skill_size*2))
      baseSkill_2_Pos = (pos[0]+(sprite_size//2)-(skill_size//2), pos[1]-(skill_size*2)+skill_size)
      sigSkillPos = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2))
      sigSkillPos_2 = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2)+skill_size)
      
      base1rect = pygame.rect.Rect(baseSkill_1_Pos[0], baseSkill_1_Pos[1], skill_size, skill_size)
      base2rect = pygame.rect.Rect(baseSkill_2_Pos[0], baseSkill_2_Pos[1], skill_size, skill_size)
      sig1rect = pygame.rect.Rect(sigSkillPos[0], sigSkillPos[1], skill_size, skill_size)
      sig2rect = pygame.rect.Rect(sigSkillPos_2[0], sigSkillPos_2[1], skill_size, skill_size)
      charRect = pygame.rect.Rect(pos[0], pos[1], sprite_size, sprite_size)
      
      final_invalids.append(charRect)
      final_invalids.append(base1rect)
      final_invalids.append(base2rect)
      final_invalids.append(sig1rect)
      final_invalids.append(sig2rect)
  
  # rendering
  for rect in final_invalids:
    highlight = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    highlight.fill((255, 0, 0, 100))  # Red
    screen.blit(highlight, (rect.x, rect.y))
  for rect in final_validation:
    highlight = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    highlight.fill((0, 255, 0, 100))  # Green
    screen.blit(highlight, (rect.x, rect.y))
  return
def DrawTargetingLine(start_pos, end_pos):
  # Calculate direction and distance
  dx = end_pos[0] - start_pos[0]
  dy = end_pos[1] - start_pos[1]
  distance = math.sqrt(dx*dx + dy*dy)
  
  if distance > 0:
    # Normalize direction
    dx /= distance
    dy /= distance
      
    # Parameters | will be adjusted for character and or party
    color = (255, 0, 0)
    dash_length = 10
    gap_length = 5
    segment_length = dash_length + gap_length
    
    # Draw dashed line
    current_distance = 0
    while current_distance < distance:
      # Start of dash
      dash_start_x = start_pos[0] + dx * current_distance
      dash_start_y = start_pos[1] + dy * current_distance
      
      # End of dash (don't exceed total distance)
      dash_end_distance = min(current_distance + dash_length, distance)
      dash_end_x = start_pos[0] + dx * dash_end_distance
      dash_end_y = start_pos[1] + dy * dash_end_distance
      
      # Draw the dash
      pygame.draw.line(screen, color, (dash_start_x, dash_start_y), (dash_end_x, dash_end_y), 5)
      
      # Move to next segment
      current_distance += segment_length
def DrawAllTargetedLines():
  for target_pair in targeted_skills_position_list:
    start_pos = (target_pair[0][0]+(skill_size//2), target_pair[0][1]+(skill_size//2))
    if(target_pair[1] in enemyPartyPositions or target_pair[1] in playerPartyPositions):
      end_pos = (target_pair[1][0]+(sprite_size//2), target_pair[1][1]+(sprite_size//2))
    else:
      end_pos = (target_pair[1][0]+(skill_size//2), target_pair[1][1]+(skill_size//2))
    DrawTargetingLine(start_pos, end_pos)

def CombatSpriteTransformCalculation(encounter): # calculate all positions
  offset = (100, 50)

  global playerPartyPositions, enemyPartyPositions
  
  playerPartyPositions = encounter.playerPartyPositions
  enemyPartyPositions = encounter.encounterPartyPositions
  # playerPartyPositions = [(offset[0], center_y - sprite_size), (offset[0] + sprite_size, center_y - sprite_size), (offset[0] + sprite_size*2, center_y - sprite_size),
  #                      (offset[0]*3//2, center_y + sprite_size), (offset[0]*3//2 + sprite_size, center_y + sprite_size) , (offset[0]*3//2 + sprite_size*2, center_y + sprite_size)]
  # enemyPartyPositions = [(x - offset[0] - sprite_size, center_y - sprite_size), (x - offset[0] - sprite_size*2, center_y - sprite_size), (x - offset[0] - sprite_size*3, center_y - sprite_size),
  #                        (x - offset[0]*3//2 - sprite_size, center_y + sprite_size), (x - offset[0]*3//2 - sprite_size*2, center_y + sprite_size), (x - offset[0]*3//2 - sprite_size*3, center_y + sprite_size)]

  partyPositions = [playerPartyPositions, enemyPartyPositions]
  
  leftPartyBaseSkillPositions = []
  leftPartySignatureSkillPositions = []
  
  rightPartyBaseSkillPositions = []
  rightPartySignatureSkillPositions = []
  
  skillPositions = [leftPartyBaseSkillPositions, leftPartySignatureSkillPositions, rightPartyBaseSkillPositions, rightPartySignatureSkillPositions]

  for pos in playerPartyPositions:
    baseSkillPos = (pos[0]+(sprite_size//2)-(skill_size//2) , pos[1]-(skill_size*2))
    baseSkill_2_Pos = (pos[0]+(sprite_size//2)-(skill_size//2), pos[1]-(skill_size*2)+skill_size)
    sigSkillPos = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2))
    sigSkill_2_Pos = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2)+skill_size)
    
    leftPartyBaseSkillPositions.append(baseSkillPos)
    leftPartyBaseSkillPositions.append(baseSkill_2_Pos)
    leftPartySignatureSkillPositions.append(sigSkillPos)
    leftPartySignatureSkillPositions.append(sigSkill_2_Pos)
  
  for pos in enemyPartyPositions:
    baseSkillPos = (pos[0]+(sprite_size//2)-(skill_size//2) , pos[1]-(skill_size*2))
    baseSkill_2_Pos = (pos[0]+(sprite_size//2)-(skill_size//2), pos[1]-(skill_size*2)+skill_size)
    sigSkillPos = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2))
    sigSkill_2_Pos = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2)+skill_size)
    
    rightPartyBaseSkillPositions.append(baseSkillPos)
    rightPartyBaseSkillPositions.append(baseSkill_2_Pos)
    rightPartySignatureSkillPositions.append(sigSkillPos)
    rightPartySignatureSkillPositions.append(sigSkill_2_Pos)
    
  
  return partyPositions, skillPositions

def CombatDescriptiveSurfaceRender():
  # render descriptive surfaces for combat - to be implemented
  descriptiveText = pygame.Surface((1920,400), pygame.SRCALPHA)
  descriptiveText.fill((0, 0, 30, 150))  # semi-transparent black

  font = pygame.font.Font(None, 32)   # None = default font, 32 = size
  # top left = skill image enlarged
  # on the right = coin amount and coin power
  # under and continuing to the right = skill description
  # maybe per coin explanation
  return
#endregion

#region Rendering
def RenderCharacterSurface(character, sprite, characterPos, collisionPos, selection=False):
  fontSize = 32
  renderSprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))
  charSurface = pygame.Surface((sprite_size, sprite_size+fontSize), pygame.SRCALPHA) 
  
  # collision hover
  charRect = pygame.Rect(characterPos[0], characterPos[1], sprite_size, sprite_size)
  if charRect.collidepoint(collisionPos or (0,0)):
    highlight = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    highlight.fill((255, 255, 255, 120)) # semi-transparent white
    charSurface.blit(highlight, (0,0))
  charSurface.blit(renderSprite, (0,0)) # character sprite render
  font = pygame.font.Font(None, fontSize)
  
  # text rendering does not feel well placed, centering does not feel perfect.
  if(selection):
    return charSurface
  # text for stats
  sanity_text = font.render(f"{character.sanity}", True, (137, 207, 240))
  hp_text = font.render(f"{character.hp}", True, (238, 75, 43))
  speed_text = font.render(f"{character.speed}", True, (255, 255, 255)) # calculation will be moved to game.py when turn system is implemented.
  # space for stats
  sanity_space = pygame.Rect((sprite_size)*6/8, sprite_size, sprite_size/8, fontSize)
  hp_space= pygame.Rect((sprite_size)*3/8, sprite_size, sprite_size*2/8, fontSize) 
  speed_space = pygame.Rect((sprite_size)*1/8, sprite_size, sprite_size/8, fontSize)
  # centered rect
  sanity_centered = sanity_text.get_rect(center=sanity_space.center)
  hp_centered = hp_text.get_rect(center=hp_space.center)
  speed_centered = speed_text.get_rect(center=speed_space.center)
  
  # sanity
  charSurface.blit(sanity_text, sanity_centered) # 120
  # hp
  charSurface.blit(hp_text, hp_centered) # 80
  # speed
  charSurface.blit(speed_text, speed_centered) # 60
  return charSurface

def BaseSkillSurface(character, globalPosition, collisionPos=None):
  # game.py needs to calculate skills that will be shown here later
  skillSurface = pygame.Surface((32, 64), pygame.SRCALPHA)
  
  # Skill Grouping
  rects = []
  rect1 = pygame.Rect(globalPosition[0], globalPosition[1], skill_size, skill_size)
  rects.append(rect1)
  rect2 = pygame.Rect(globalPosition[0], globalPosition[1]+skill_size, skill_size, skill_size)
  rects.append(rect2)
  
  skillSprite1 = findSkillSprite(character.base_skills[0]) 
  renderSkillSprite1 = pygame.transform.scale(skillSprite1, (skill_size, skill_size))
  skillSprite2 = findSkillSprite(character.base_skills[1])
  renderSkillSprite2 = pygame.transform.scale(skillSprite2, (skill_size, skill_size))
  
  for rect in rects:
    if(selected_skill_pos == (rect.x, rect.y)):
      highlight = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
      highlight.fill((255, 255, 255, 255)) # white background
      skillSurface.blit(highlight, (rect.x - globalPosition[0], rect.y - globalPosition[1]))
    elif rect.collidepoint(collisionPos or (0,0)):
      highlight = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
      highlight.fill((255, 255, 255, 120)) # semi-transparent white
      skillSurface.blit(highlight, (rect.x - globalPosition[0], rect.y - globalPosition[1]))
    if(rect.y == globalPosition[1]):
      skillSurface.blit(renderSkillSprite1, (rect.x - globalPosition[0], rect.y - globalPosition[1]))
    else: 
      skillSurface.blit(renderSkillSprite2, (rect.x - globalPosition[0], rect.y - globalPosition[1]))  
  return skillSurface

def SignatureSkillSurface(character, globalPosition, collisionPos=None):
  # game.py needs to calculate skills that will be shown here later
  skillSurface = pygame.Surface((32, 64), pygame.SRCALPHA)
  
  # Skill Grouping
  rects = []
  rect1 = pygame.Rect(globalPosition[0], globalPosition[1], skill_size, skill_size)
  rects.append(rect1)
  rect2 = pygame.Rect(globalPosition[0], globalPosition[1]+skill_size, skill_size, skill_size)
  rects.append(rect2)
  
  skillSprite1 = findSkillSprite(character.sig_skills[0]) 
  renderSkillSprite1 = pygame.transform.scale(skillSprite1, (skill_size, skill_size))
  skillSprite2 = findSkillSprite(character.sig_skills[1])
  renderSkillSprite2 = pygame.transform.scale(skillSprite2, (skill_size, skill_size))
  
  for rect in rects:
    if(selected_skill_pos == (rect.x, rect.y)):
      highlight = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
      highlight.fill((255, 255, 255, 255)) # white background
      skillSurface.blit(highlight, (rect.x - globalPosition[0], rect.y - globalPosition[1]))
    elif rect.collidepoint(collisionPos or (0,0)):
      highlight = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
      highlight.fill((255, 255, 255, 120)) # semi-transparent white
      skillSurface.blit(highlight, (rect.x - globalPosition[0], rect.y - globalPosition[1]))
    if(rect.y == globalPosition[1]):
      skillSurface.blit(renderSkillSprite1, (rect.x - globalPosition[0], rect.y - globalPosition[1]))
    else: 
      skillSurface.blit(renderSkillSprite2, (rect.x - globalPosition[0], rect.y - globalPosition[1]))  
  return skillSurface

def renderNovelScene(character, dialogue_line):
  # start drawing
  # find speaking character
  # load sprite in novel format
  
  # possibly putting main character on left and others on right
  # if(character.name == "Blacked out Engineer"): renderpos = left
  # else: renderpos = right
  
  sprite = findCharacterSprite(character)
  novelSprite = spriteNovelify(sprite)
  screen.blit(novelSprite, (center_x - (novelSprite.get_width() // 2), center_y - (novelSprite.get_height() // 2)))
  # find right textlist
  # load text box
  novelText = pygame.Surface((1920,200), pygame.SRCALPHA)
  novelText.fill((0, 0, 30, 150))  # semi-transparent black
  
  font = pygame.font.Font(None, 32)   # None = default font, 32 = size
  dialogue = font.render(dialogue_line, True, (255, 255, 255))  # white text
  novelText.blit(dialogue, (20, 20))  # small padding from left and top
  
  screen.blit(novelText, (0, 880))  # position at bottom of screen
  
  
  pygame.display.flip()  # Update the display to show changes

def CombatSceneRender(encounter=type(Encounter)):
  enemyParty = encounter.encounterPartyCharacters
  playerParty = encounter.playerPartyCharacters
  # calculate all positions
  partyPositions, skillPositions = CombatSpriteTransformCalculation(encounter)
  # check & handle collisions
  collisionPos = DetectCombatCollision(partyPositions, skillPositions, playerParty, enemyParty)
  # set temporary parties
  global playerPartyChars, enemyPartyChars
  playerPartyChars = playerParty
  enemyPartyChars = enemyParty
  
  
  
  # render
  
  #Background
  combatBGRender = findBackgroundForEncounter(encounter)
  combatBGRender = pygame.transform.scale(combatBGRender, (x, y))
  screen.blit(combatBGRender, (0, 0))  # Draw the background image
  # constant UI
  screen.blit(turnEndButtonSprite, (turnEndButton.x, turnEndButton.y)) 
  
  #PlayerParty
  for char in playerParty or []:
    sprite = findCharacterSprite(char)
    index = playerParty.index(char)
    
    # render positions
    # CharacterPosition = encounter.encounterPartyPositions[index] 
    CharacterPosition = partyPositions[0][index] # NOT A HEALTHY SOLUTION FOR THE SKILLS!!!
    SkillsPosition = (skillPositions[0][index*2]) # position of the top skill is used for the surface that contains both.
    SigSkillPosition = (skillPositions[1][index*2]) # position of the top skill is used for the surface that contains both.
    # surface prep & collision
    characterSurface = RenderCharacterSurface(char, sprite, CharacterPosition, collisionPos)
    skillSurface = BaseSkillSurface(char, SkillsPosition, collisionPos)
    sigSkillSurface = SignatureSkillSurface(char, SigSkillPosition, collisionPos)
    
    # character render
    screen.blit(characterSurface, CharacterPosition)
    # skill render
    screen.blit(skillSurface, SkillsPosition)
    screen.blit(sigSkillSurface, SigSkillPosition) # signature skill next to base skill
      
  #EnemyParty
  for char in enemyParty or []:
    sprite = findCharacterSprite(char)
    index = enemyParty.index(char)
    
    CharacterPosition = partyPositions[1][index]
    SkillsPosition = (skillPositions[2][index*2]) # position of the top skill is used for the surface that contains both.
    SigSkillPosition = (skillPositions[3][index*2]) # position of the top skill is used for the surface that contains both.
    # surface prep & collision
    characterSurface = RenderCharacterSurface(char, sprite, CharacterPosition, collisionPos)
    skillSurface = BaseSkillSurface(char, SkillsPosition, collisionPos)
    sigSkillSurface = SignatureSkillSurface(char, SigSkillPosition, collisionPos)
    
    # character render
    screen.blit(characterSurface, CharacterPosition)
    # skill render
    screen.blit(skillSurface, SkillsPosition)
    screen.blit(sigSkillSurface, SigSkillPosition) # signature skill next to base skill

  # targeting line render
  if(selected_skill_pos != None):
    if(targeted_skill_pos != None):
      centered_targeted_pos = (targeted_skill_pos[0]+(skill_size//2), targeted_skill_pos[1]+(skill_size//2))
      end_pos = centered_targeted_pos
    else:
      end_pos = pygame.mouse.get_pos()
    start_pos = (selected_skill_pos[0]+(skill_size//2), selected_skill_pos[1]+(skill_size//2))
    DrawTargetingLine(start_pos, end_pos)
    DrawAllTargetedLines()
    HighlightValidTargets(FindSkillByPosition(selected_skill_pos))
  
  pygame.display.flip()  # Update the display to show changes

def RenderPartySelecter(availableCharacters):
  # draw bg
  characterSelectBG = pygame.transform.scale(barBG, (x, y))
  screen.blit(characterSelectBG, (0, 0))  # Draw the background image
  # character amount = 8 to 7
  characterPositions = barCharacterPositions.copy()
  # collider
  collisionPos = DetectCollision(characterPositions)
  
  
  # draw characters
  for char in availableCharacters or []:
    sprite = findCharacterSprite(char)
    index = availableCharacters.index(char)
    
    # render positions
    charPos = characterPositions[index]
    
    # surface prep & collision
    characterSurface = RenderCharacterSurface(char, sprite, charPos, collisionPos, selection=True)
    if(char in selectedPartyCharacters):
      # highlight selected characters
      highlight = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
      highlight.fill((0, 255, 0, 160)) # semi-transparent green
      characterSurface.blit(highlight, (0,0))
    
    # character render
    screen.blit(characterSurface, charPos)
  # draw finalize party button
  
  # Update the display to show what was drawn
  pygame.display.flip()
  
  return
#endregion

#region Collision Handling

def ClickEvent(state, partyPositions=None, skillPositions=None, playerParty=None, enemyParty=None):
  if(state == "combat"):
    clickPos = DetectCombatCollision(partyPositions, skillPositions, playerParty, enemyParty, click=True)
  elif(state == "partyselect"):
    clickPos = DetectCollision(barCharacterPositions, click=True)
  elif(state == "novel"):
    return 
  else:
    return "error: invalid state"
  
  
  if(clickPos == None):
    ResetCurrentTargeting()
  return

def DetectCombatCollision(partyPositions=None, skillPositions=None, playerParty=None, enemyParty=None, click=False):
  # check for collisions on all characters & skills
  targeting = False
  mouse_pos = pygame.mouse.get_pos()
  if(selected_skill_pos != None):
    targeting = True
  
  # define rects for all characters & skills
  
  if(turnEndButton.collidepoint(mouse_pos) and click):
    return HandleTurnEndClick()
  
  # currently no character interaction - commented
  for pos in partyPositions[0] or []:
    rect = pygame.Rect(pos[0], pos[1], sprite_size, sprite_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleCharacterClick(pos, targeting)
      return (pos)
  for pos in partyPositions[1] or []:
    rect = pygame.Rect(pos[0], pos[1], sprite_size, sprite_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleCharacterClick(pos, targeting)
      return (pos)
  
  for pos in skillPositions[0] or []:
    rect = pygame.Rect(pos[0], pos[1], skill_size, skill_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleBaseSkillClick(pos, targeting)
      return (pos)
  for pos in skillPositions[1] or []:
    rect = pygame.Rect(pos[0], pos[1], skill_size, skill_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleSignatureSkillClick(pos, targeting)
      return (pos)
  
  for pos in skillPositions[2] or []:
    rect = pygame.Rect(pos[0], pos[1], skill_size, skill_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleBaseSkillClick(pos, targeting)
      return (pos)
  for pos in skillPositions[3] or []:
    rect = pygame.Rect(pos[0], pos[1], skill_size, skill_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleSignatureSkillClick(pos, targeting)
      return (pos)

  if(targeting and click):
    for target_pair in targeted_skills_position_list: # if skill is already targeted, remove target
      if(target_pair[0] == selected_skill_pos):
        targeted_skills_position_list.remove(target_pair)
    # clicked on empty space while targeting - reset selection
    ResetCurrentTargeting()
  return None

def DetectCollision(posList, click = False):
  mouse_pos = pygame.mouse.get_pos()
  for pos in posList:
    rect = pygame.Rect(pos[0], pos[1], sprite_size, sprite_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        HandleCharacterSelect(mouse_pos)
      return pos
  return None

def HandleCharacterSelect(clickPos):
  global selectedPartyCharacters, benchedPartyCharacters, barCharacterPositions
  # find character by position
  for char in allPlayerCharacters:
    charPos = barCharacterPositions[allPlayerCharacters.index(char)]
    charRect = pygame.Rect(charPos[0], charPos[1], sprite_size, sprite_size)
    if(charRect.collidepoint(clickPos)):
      if(char in selectedPartyCharacters):
        for i in range(len(selectedPartyCharacters)):
          if(selectedPartyCharacters[i] == char):
            selectedPartyCharacters[i] = None
            benchedPartyCharacters.append(char)
            return
      elif(char in benchedPartyCharacters):
        for i in range(len(selectedPartyCharacters)):
          if(selectedPartyCharacters[i] is None):
            selectedPartyCharacters[i] = char
            benchedPartyCharacters.remove(char)
            return
  return
def HandleCharacterClick(clickPos, targeting):
  # logic to handle character collision
  global selected_skill_pos, targeted_character_pos
  
  if(not targeting):
    # later added
    return
  else:
    targeted_character_pos = clickPos
    SetSkillTargeting((selected_skill_pos,targeted_character_pos))
    ResetCurrentTargeting()
    return targeted_character_pos
  return
def HandleBaseSkillClick(clickPos, targeting):
  # logic to handle base skill collision
  global selected_skill_pos, targeted_skill_pos
  
  # selecting first skill   
  if(not targeting):
    selected_skill_pos = clickPos
    targeted_skill_pos = None
    return selected_skill_pos
  else: # targeting with selected skill
    targeted_skill_pos = clickPos
    SetSkillTargeting((selected_skill_pos,targeted_skill_pos))
    ResetCurrentTargeting()
    return targeted_skill_pos
  return selected_skill_pos # failsafe
def HandleSignatureSkillClick(clickPos, targeting):
  # logic to handle signature skill collision
  global selected_skill_pos, targeted_skill_pos
  # selecting first skill   
  if(not targeting):
    selected_skill_pos = clickPos
    targeted_skill_pos = None
    return selected_skill_pos
  else: # targeting with selected skill
    targeted_skill_pos = clickPos
    SetSkillTargeting((selected_skill_pos,targeted_skill_pos))
    ResetCurrentTargeting()
    return targeted_skill_pos
  return selected_skill_pos # failsafe
def HandleTurnEndClick():
  if(CalculateTurnEndPrerequisites()):
    EndTurn()
  else:
    WarnPlayer()
  return
#endregion

#region turn system
def CalculateTurnEndPrerequisites():
  skill = None
  for skill in skillList: # enemy skills need to be appointed in a guaranteed running function
    if(skill not in targeted_skills_list):
      # check if character used another skill in the same type
      user = FindCharacterBySkill(skill)
      skill_type = skill in user.base_skills and "base" or skill in user.sig_skills and "sig" or None
      if(HasCharacterUsedSkillType(user, skill_type)):
        continue
      return False
  return True
def EndTurn():
  # execute all targeted skills
  for target_pair in targeted_skills_list:
    skill = target_pair[0]
    target = target_pair[1]
    skill.ExecuteSkill(target)
  # reset for next turn
  targeted_skills_list.clear()
  targeted_skills_position_list.clear()
  return
#endregion

#region UI
def WarnPlayer(errorReason="null"):
  # render a message on screen about given param
  return errorReason
#endregion

def GetMousePos():
  mousePos = pygame.mouse.get_pos()
  print(mousePos)
  return mousePos