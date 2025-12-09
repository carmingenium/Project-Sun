import pygame
import character


# initialization
pygame.init()
x = 1920
y = 1080
screen = pygame.display.set_mode((x, y)) # this has to be static as long as the camera system depends on it
center_x = x // 2
center_y = y // 2

sprite_size = 160 # 32*5 - defined so that positions can be calculated from this variable.
skill_size = 32 # per skill 

# for dialogues 
renderposRight = (1400, 200)
renderposLeft = (100, 200)

combatBackGround = pygame.image.load('sprites/backgrounds/combat_test.png').convert()

#endregion 



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




#region rendering functions

#region NOTES
# positional hypothesis:
# to put it in the middle in y axis: 540 - (sprite_height / 2)
# to put it in the middle in x axis: 960 - (sprite_width / 2)
# normal characters are 32x32, might get scaled
# the position sprites are drawn are from top-left of the sprites. so x can be closer to 0 and y needs to be further down than usual
# testing values
#endregion

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


#region old char surface
#   renderSprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))
#   offset = (100,50)
#   statSurface = pygame.Surface((sprite_size+offset[0], sprite_size+offset[1]), pygame.SRCALPHA) 
#   statSurface.blit(renderSprite, (offset[0]//2, offset[1]//2))
#   font = pygame.font.Font(None, 24)
#   # sanity
#   statSurface.blit(font.render(f"{character.sanity}", True, (137, 207, 240)), ((offset[0] + sprite_size)*4/6, sprite_size + offset[1]//2)) # 120
#   # hp
#   statSurface.blit(font.render(f"{character.hp}", True, (238, 75, 43)), ((offset[0] + sprite_size)*2/6, sprite_size + offset[1]//2)) # 80
#   # speed
#   statSurface.blit(font.render(f"{character.calculate_speed()}", True, (255, 255, 255)), ((offset[0] + sprite_size)*1/6, sprite_size + offset[1]//2)) # 60
#   return statSurface, offset
#endregion
def RenderCharacterSurface(character, sprite):
  fontSize = 32
  renderSprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))
  charSurface = pygame.Surface((sprite_size, sprite_size+fontSize), pygame.SRCALPHA) 
  charSurface.blit(renderSprite, (0,0)) # character sprite render
  font = pygame.font.Font(None, fontSize)
  
  # text rendering does not feel well placed, centering does not feel perfect.

  # text for stats
  sanity_text = font.render(f"{character.sanity}", True, (137, 207, 240))
  hp_text = font.render(f"{character.hp}", True, (238, 75, 43))
  speed_text = font.render(f"{character.calculate_speed()}", True, (255, 255, 255)) # calculation will be moved to game.py when turn system is implemented.
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

def BaseSkillSurface(character, globalPosition): # alignment problems because of magic numbers, tomorrows problem
  # game.py needs to calculate skills that will be shown here later
  skillSurface = pygame.Surface((32, 64), pygame.SRCALPHA)
  
  # collision detection
  rects = []
  
  rect1 = pygame.Rect(globalPosition[0], globalPosition[1], 32, 32)
  rects.append(rect1)
  rect2 = pygame.Rect(globalPosition[0], globalPosition[1]+32, 32, 32)
  rects.append(rect2)
  
  skillSprite = findSkillSprite(character.base_skills[0]) 
  renderSkillSprite = pygame.transform.scale(skillSprite, (32, 32))
  
  for rect in rects:
    if rect.collidepoint(pygame.mouse.get_pos()):
      highlight = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
      highlight.fill((0, 250, 0, 120))  # semi-transparent green
      skillSurface.blit(highlight, (rect.x - globalPosition[0], rect.y - globalPosition[1]))
    skillSurface.blit(renderSkillSprite, (rect.x - globalPosition[0], rect.y - globalPosition[1]))  
        
  # skillSurface.blit(renderSkillSprite, (0,0))
  # skillSurface.blit(renderSkillSprite, (0,32))
  
  
  
  #region future notes
  # for skill in character.base_skills:
  #   skillSprite = findSkillSprite(skill)
  #   renderSprite = pygame.transform.scale(skillSprite, (skillSprite.get_width(), skillSprite.get_height()))
  #   skillSurface.blit(renderSprite, (0,0))
  #endregion
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

def renderCombatScene(playerParty=None, enemyParty=None):
  combatBGRender = pygame.transform.scale(combatBackGround, (x, y))
  screen.blit(combatBGRender, (0, 0))  # Draw the background image
  
  offset = (100, 50)
  leftPartyPositions = [(offset[0], center_y - sprite_size*3//4), (offset[0] + sprite_size, center_y - sprite_size*3//4), (offset[0] + sprite_size*2, center_y - sprite_size*3//4),
                       (offset[0]*3//2, center_y + sprite_size*3//4), (offset[0]*3//2 + sprite_size, center_y + sprite_size*3//4) , (offset[0]*3//2 + sprite_size*2, center_y + sprite_size*3//4)]
  rightPartyPositions = [(x - offset[0] - sprite_size, center_y - sprite_size*3//4), (x - offset[0] - sprite_size*2, center_y - sprite_size*3//4), (x - offset[0] - sprite_size*3, center_y - sprite_size*3//4),
                         (x - offset[0]*3//2 - sprite_size, center_y + sprite_size*3//4), (x - offset[0]*3//2 - sprite_size*2, center_y + sprite_size*3//4), (x - offset[0]*3//2 - sprite_size*3, center_y + sprite_size*3//4)]

  # keeping rep for later tests
  # render as surfaces to show hp, speed etc.
  rep = 0
  for char in playerParty or []:
    sprite = findCharacterSprite(char)
    for i in range(6): 
      # render positions
      CharacterPosition = leftPartyPositions[rep]
      SkillsPosition = (leftPartyPositions[rep][0]+(sprite_size//2)-(skill_size//2), leftPartyPositions[rep][1]-(skill_size*2))
      
      # surface prep & collision
      characterSurface = RenderCharacterSurface(char, sprite)
      skillSurface = BaseSkillSurface(char, SkillsPosition)
      
      

      # character render
      screen.blit(characterSurface, CharacterPosition)
      # skill render
      screen.blit(skillSurface, SkillsPosition)
      rep += 1
  rep = 0
  for char in enemyParty or []:
    sprite = findCharacterSprite(char)
    for i in range(6):
      renderSprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))
      screen.blit(renderSprite, rightPartyPositions[rep]) 
      rep += 1
    
  pygame.display.flip()  # Update the display to show changes
#endregion
