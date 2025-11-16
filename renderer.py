import pygame
# initialization
pygame.init()
screen = pygame.display.set_mode((1920, 1080)) # this has to be static as long as the camera system depends on it
# game init
with open("story/test.txt", "r", encoding="utf-8") as f: # load text
  dialog_lines = [line.strip() for line in f.readlines()]
font = pygame.font.Font(None, 32)   # None = default font, 32 = size



current_line_index = 0

# sprite loading
dragon_sprite = pygame.image.load('sprites/spacedragon.png').convert() # 64x64 so double of a normal human
dragon_sprite_big = pygame.transform.scale(dragon_sprite, (dragon_sprite.get_width()*2, dragon_sprite.get_height()*2))# 128x128

unknown_sprite = pygame.image.load('sprites/unknown.png').convert() # 32x32



# vars
dragoncenter_y = 540 - (dragon_sprite.get_height() // 2)
dragoncenter_x = 960 - (dragon_sprite.get_width() // 2)
center_x = 960
center_y = 540
clock = pygame.time.Clock() # frame rate controller





def spriteNovelify(sprite):
  novelSprite = pygame.transform.scale(sprite, (sprite.get_width()*35, sprite.get_height()*35))
  return novelSprite

def main():
  current_gamemode = "novel" # VN mode or combat mode
  running = True

  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    screen.fill((0, 0, 0))  # Clear screen with black
    if(current_gamemode == "novel"):
      # start drawing
      # find speaking character
      # load sprite in novel format
      novelSprite = spriteNovelify(dragon_sprite)
      screen.blit(novelSprite, (center_x - (novelSprite.get_width() // 2), center_y - (novelSprite.get_height() // 2)))
      # find right textlist
      # load text box
      novelText = pygame.Surface((1920,200), pygame.SRCALPHA)
      novelText.fill((0, 0, 0, 150))  # semi-transparent black
      
      dialogue = font.render(dialog_lines[0], True, (255, 255, 255))
      novelText.blit(dialogue, (20, 20))  # small padding from left and top
      
      screen.blit(novelText, (0, 880))  # position at bottom of
    
    
    if(current_gamemode == "combat"):
    # start drawing
    # positional hypothesis:
    # to put it in the middle in y axis: 540 - (sprite_height / 2)
    # to put it in the middle in x axis: 960 - (sprite_width / 2)
    # normal characters are 32x32, might get scaled
    
    # the position sprites are drawn are from top-left of the sprites. so x can be closer to 0 and y needs to be further down than usual
    
    # testing values
      screen.blit(dragon_sprite, (100, dragoncenter_y - 128)) 
      screen.blit(dragon_sprite, (300, dragoncenter_y - 128))  # upper middle
      screen.blit(dragon_sprite, (500, dragoncenter_y - 128))
      
      screen.blit(dragon_sprite, (100, dragoncenter_y + 128)) 
      screen.blit(dragon_sprite, (300, dragoncenter_y + 128))  # upper middle
      screen.blit(dragon_sprite, (500, dragoncenter_y + 128))
    pygame.display.flip()  # Update the display to show changes
    
    clock.tick(60)  # Limit to 60 frames per second
  pygame.quit()

  return

main()