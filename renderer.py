import pygame
import character
import math

#region initialization
# constants
pygame.init()
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

combatBackGround = pygame.image.load('sprites/backgrounds/combat_test.png').convert()

turnEndButtonSprite = pygame.image.load('sprites/ui/winrate.png').convert_alpha()
turnEndButton = pygame.Rect(x - 200, y - 100, 180, 80) # position and size of the button
turnEndButtonSprite = pygame.transform.scale(turnEndButtonSprite, (turnEndButton.width, turnEndButton.height))

# variables
leftPartyPositions = []
rightPartyPositions = []

# temporary variables
selected_skill_pos = None
targeted_skill_pos = None
targeted_character_pos = None

targeted_skills_position_list = []
targeted_skills_list = []

rightPartyChars = []
leftPartyChars = []



character_sprites = []
characterList = []
def spriteListInitialize(characters):
  global characterList, character_sprites
  for char in characters:
    try:
      character_sprites.append(pygame.image.load(char.sprite).convert_alpha())
      print(f"Loaded sprite for {char.name} from path {char.sprite}")
    except: 
      print(f"Error loading sprite for {char.name} from path {char.sprite}") 
  characterList = characters

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
    
  targeted_object = FindSkillByPosition(target_pair[1]) or FindCharacterByPosition(target_pair[1])

  
  # target is character or skill
  if(isinstance(targeted_object, character.Skill)): # skill
    targeted_char = FindCharacterBySkill(targeted_object)
    targeted_object_type = "skill"
  elif(isinstance(targeted_object, character.Character)): # character
    targeted_char = targeted_object
    targeted_object_type = "character"
  
  targeting_party = FindPartyFromCharacter(targeting_char)
  targeted_party = FindPartyFromCharacter(targeted_char)
  
  # prevent targeting invalid target types
  if(not (targeting_skill.available_targets[0] == targeted_party and targeting_skill.available_targets[1] == targeted_object_type)): # target invalid
    return
  
  for pairs in targeted_skills_position_list:
    if(pairs[0] == selected_skill_pos):
      targeted_skills_position_list.remove(pairs) # remove previous targeting for same skill
  
  targeted_skills_list.append((targeting_skill, targeted_object)) # to be actualized at turn ends when they are implemented
  targeted_skills_position_list.append(target_pair)
  return

def FindSkillByPosition(pos):
  # find party depending on x coordinate
  
  if(pos[0] < center_x):
    party = leftPartyPositions
    charParty = leftPartyChars
  else:
    party = rightPartyPositions 
    charParty = rightPartyChars
  
  # find position in party depending on coordinates
  for charPos in party:
    if ((pos[0] == charPos[0]+(sprite_size//2)-(skill_size//2)) or (pos[0] == charPos[0]+(sprite_size//2)+(skill_size//2))):
      char = charParty[party.index(charPos)]
      # base skills
      baseSkill_1_Pos = (charPos[0]+(sprite_size//2)-(skill_size//2) , charPos[1]-(skill_size*2))
      baseSkill_2_Pos = (charPos[0]+(sprite_size//2)-(skill_size//2), charPos[1]-(skill_size*2)+skill_size)
      sigSkillPos = (charPos[0]+(sprite_size//2)+(skill_size//2), charPos[1]-(skill_size*2))
      
      if pos == baseSkill_1_Pos:
        return char.currentBaseSkills[0]
      elif pos == baseSkill_2_Pos:
        return char.currentBaseSkills[1]
      elif pos == sigSkillPos:
        return char.currentSignatureSkills[0]
  return None
def FindCharacterByPosition(pos):
  if(pos[0] < center_x):
    party = leftPartyPositions
    charParty = leftPartyChars
  else:
    party = rightPartyPositions 
    charParty = rightPartyChars
  
  # find position in party depending on coordinates
  for charPos in party:
    index = party.index(charPos)
    if charPos[0] == party[index][0]: # found character position
      char = charParty[index]
      return char
  return None
def FindCharacterBySkill(skill):
  for char in leftPartyChars + rightPartyChars:
    if(skill in char.currentBaseSkills or skill in char.currentSigSkills):
      return char
  return None
def FindPartyFromCharacter(character):
  if(character in leftPartyChars):
    return "player"
  elif(character in rightPartyChars):
    return "enemy"
  return None

#endregion

#region Rendering support functions

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
  for target_pair in targeted_skills_position_list: # when characters are added as targets, rewrite this part of the code
    start_pos = (target_pair[0][0]+(skill_size//2), target_pair[0][1]+(skill_size//2))
    end_pos = (target_pair[1][0]+(skill_size//2), target_pair[1][1]+(skill_size//2))
    DrawTargetingLine(start_pos, end_pos)

def CombatSpriteTransformCalculation(): # calculate all positions
  offset = (100, 50)
  # region return values
  CombatBGPos = (0, 0)
  global leftPartyPositions, rightPartyPositions
  
  leftPartyPositions = [(offset[0], center_y - sprite_size), (offset[0] + sprite_size, center_y - sprite_size), (offset[0] + sprite_size*2, center_y - sprite_size),
                       (offset[0]*3//2, center_y + sprite_size), (offset[0]*3//2 + sprite_size, center_y + sprite_size) , (offset[0]*3//2 + sprite_size*2, center_y + sprite_size)]
  rightPartyPositions = [(x - offset[0] - sprite_size, center_y - sprite_size), (x - offset[0] - sprite_size*2, center_y - sprite_size), (x - offset[0] - sprite_size*3, center_y - sprite_size),
                         (x - offset[0]*3//2 - sprite_size, center_y + sprite_size), (x - offset[0]*3//2 - sprite_size*2, center_y + sprite_size), (x - offset[0]*3//2 - sprite_size*3, center_y + sprite_size)]

  leftPartyBaseSkillPositions = []
  leftPartySignatureSkillPositions = []
  
  rightPartyBaseSkillPositions = []
  rightPartySignatureSkillPositions = []
  #endregion
  for pos in leftPartyPositions:
    baseSkillPos = (pos[0]+(sprite_size//2)-(skill_size//2) , pos[1]-(skill_size*2))
    baseSkill_2_Pos = (pos[0]+(sprite_size//2)-(skill_size//2), pos[1]-(skill_size*2)+skill_size)
    sigSkillPos = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2))
    
    leftPartyBaseSkillPositions.append(baseSkillPos)
    leftPartyBaseSkillPositions.append(baseSkill_2_Pos)
    leftPartySignatureSkillPositions.append(sigSkillPos)
  
  for pos in rightPartyPositions:
    baseSkillPos = (pos[0]+(sprite_size//2)-(skill_size//2) , pos[1]-(skill_size*2))
    baseSkill_2_Pos = (pos[0]+(sprite_size//2)-(skill_size//2), pos[1]-(skill_size*2)+skill_size)
    sigSkillPos = (pos[0]+(sprite_size//2)+(skill_size//2), pos[1]-(skill_size*2))
    
    rightPartyBaseSkillPositions.append(baseSkillPos)
    rightPartyBaseSkillPositions.append(baseSkill_2_Pos)
    rightPartySignatureSkillPositions.append(sigSkillPos)
    
  
  return CombatBGPos, leftPartyPositions, rightPartyPositions, leftPartyBaseSkillPositions, leftPartySignatureSkillPositions, rightPartyBaseSkillPositions, rightPartySignatureSkillPositions

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

def SupportSkillsRender():
  # render support skills - to be implemented
  supportSurface = pygame.Surface((200,1080), pygame.SRCALPHA)
  supportSurface.fill((0, 0, 30, 150))  # semi-transparent black

  # condition for glowy filter
  # render all support skills, filter depending on condition fulfilled

#endregion

#region Rendering
def RenderCharacterSurface(character, sprite, characterPos, collisionPos):
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

def CombatSceneRender(playerParty=None, enemyParty=None):
  # calculate all positions
  CombatBGPos, leftPartyPositions, rightPartyPositions, leftPartyBaseSkillPositions, leftPartySignatureSkillPositions, rightPartyBaseSkillPositions, rightPartySignatureSkillPositions = CombatSpriteTransformCalculation()
  # check & handle collisions
  collisionPos = DetectCombatCollision(leftPartyPositions, rightPartyPositions, leftPartyBaseSkillPositions, leftPartySignatureSkillPositions, rightPartyBaseSkillPositions, rightPartySignatureSkillPositions, playerParty, enemyParty)
  # set temporary parties
  global leftPartyChars, rightPartyChars
  leftPartyChars = playerParty
  rightPartyChars = enemyParty
  
  
  
  # render
  
  #Background
  combatBGRender = pygame.transform.scale(combatBackGround, (x, y))
  screen.blit(combatBGRender, CombatBGPos)  # Draw the background image
  # constant UI
  screen.blit(turnEndButtonSprite, (turnEndButton.x, turnEndButton.y)) 
  
  #PlayerParty
  for char in playerParty or []:
    sprite = findCharacterSprite(char)
    index = playerParty.index(char)
    
    # render positions
    CharacterPosition = leftPartyPositions[index]
    SkillsPosition = (leftPartyBaseSkillPositions[index*2]) # position of the top skill is used for the surface that contains both.
    SigSkillPosition = (leftPartySignatureSkillPositions[index])
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
    
    CharacterPosition = rightPartyPositions[index]
    SkillsPosition = (rightPartyBaseSkillPositions[index*2]) # position of the top skill is used for the surface that contains both.
    SigSkillPosition = (rightPartySignatureSkillPositions[index])
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
  
  pygame.display.flip()  # Update the display to show changes
#endregion

#region Collision Handling

def ClickEvent(leftPartyPositions=None, rightPartyPositions=None, leftPartyBaseSkillPositions=None, leftPartySignatureSkillPositions=None, rightPartyBaseSkillPositions=None, rightPartySignatureSkillPositions=None, playerParty=None, enemyParty=None):
  clickPos = DetectCombatCollision(leftPartyPositions, rightPartyPositions, leftPartyBaseSkillPositions, leftPartySignatureSkillPositions, rightPartyBaseSkillPositions, rightPartySignatureSkillPositions, playerParty, enemyParty, click=True)
    
  if(clickPos == None):
    ResetCurrentTargeting()
  return

def DetectCombatCollision(leftPartyPositions=None, rightPartyPositions=None, leftPartyBaseSkillPositions=None, leftPartySignatureSkillPositions=None, rightPartyBaseSkillPositions=None, rightPartySignatureSkillPositions=None, playerParty=None, enemyParty=None, click=False):
  # check for collisions on all characters & skills
  targeting = False
  mouse_pos = pygame.mouse.get_pos()
  if(selected_skill_pos != None):
    targeting = True
    
  # define rects for all characters & skills
  
  if(turnEndButton.collidepoint(mouse_pos) and click):
    return HandleTurnEndClick()
  
  # currently no character interaction - commented
  for pos in leftPartyPositions or []:
    rect = pygame.Rect(pos[0], pos[1], sprite_size, sprite_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleCharacterClick(pos, targeting)
      return (pos)
  for pos in rightPartyPositions or []:
    rect = pygame.Rect(pos[0], pos[1], sprite_size, sprite_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleCharacterClick(pos, targeting)
      return (pos)
  
  for pos in leftPartyBaseSkillPositions or []:
    rect = pygame.Rect(pos[0], pos[1], skill_size, skill_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleBaseSkillClick(pos, targeting)
      return (pos)
  for pos in leftPartySignatureSkillPositions or []:
    rect = pygame.Rect(pos[0], pos[1], skill_size, skill_size*2) # signature skill is taller
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleSignatureSkillClick(pos, targeting)
      return (pos)
  
  for pos in rightPartyBaseSkillPositions or []:
    rect = pygame.Rect(pos[0], pos[1], skill_size, skill_size)
    if rect.collidepoint(mouse_pos):
      if(click):
        return HandleBaseSkillClick(pos, targeting)
      return (pos)
  for pos in rightPartySignatureSkillPositions or []:
    rect = pygame.Rect(pos[0], pos[1], skill_size, skill_size*2) # signature skill is taller
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
  if(skill in skillList not in targeted_skills_list): # enemy skills need to be appointed in a guaranteed running function
    return False
  return True
def EndTurn():
  # execute all targeted skills

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