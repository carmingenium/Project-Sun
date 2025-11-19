import pygame
# initialization
pygame.init()
screen = pygame.display.set_mode((1920, 1080)) # this has to be static as long as the camera system depends on it




# sprite loading
dragon_sprite = pygame.image.load('sprites/spacedragon.png').convert() # 64x64 so double of a normal human
dragon_sprite_big = pygame.transform.scale(dragon_sprite, (dragon_sprite.get_width()*2, dragon_sprite.get_height()*2))# 128x128
unknown_sprite = pygame.image.load('sprites/unknown.png').convert() # 32x32


sprites = []
characterList = []
def spriteListInitialize(characters):
  global characterList, sprites
  for char in characters:
    try:
      sprites.append(pygame.image.load(char.sprite).convert())
      print(f"Loaded sprite for {char.name} from path {char.sprite}")
    except: 
      print(f"Error loading sprite for {char.name} from path {char.sprite}") 
  characterList = characters


# vars
dragoncenter_y = 540 - (dragon_sprite.get_height() // 2)
dragoncenter_x = 960 - (dragon_sprite.get_width() // 2)
center_x = 960
center_y = 540
clock = pygame.time.Clock() # frame rate controller

# for dialogues
renderposRight = (1400, 200)
renderposLeft = (100, 200)





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
      return sprites[index]

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
  # testing render
  # screen.blit(dragon_sprite, (100, dragoncenter_y - 128)) 
  # screen.blit(dragon_sprite, (300, dragoncenter_y - 128))  # upper middle
  # screen.blit(dragon_sprite, (500, dragoncenter_y - 128))
  
  # screen.blit(dragon_sprite, (100, dragoncenter_y + 128)) 
  # screen.blit(dragon_sprite, (300, dragoncenter_y + 128))  # upper middle
  # screen.blit(dragon_sprite, (500, dragoncenter_y + 128))
  
  for char in playerParty or []:
    sprite = findCharacterSprite(char)
    screen.blit(sprite, (100 , center_y)) # instead of 100 need a math function to calculate positions based on party size
    
  for char in enemyParty or []:
    sprite = findCharacterSprite(char)
    screen.blit(sprite, (1600 , center_y)) # instead of 1600 need a math function to calculate positions based on party size
    
    
  pygame.display.flip()  # Update the display to show changes
#endregion

def main():
  return

main()