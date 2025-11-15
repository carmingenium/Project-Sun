import pygame
#initialization
pygame.init()
screen = pygame.display.set_mode((1920, 1080)) # this has to be static as long as the camera system depends on it
#sprite loading
dragon_sprite = pygame.image.load('sprites/spacedragon.png').convert()
print(dragon_sprite.get_size()) # 64x64 so double a normal human
dragon_sprite = pygame.transform.scale(dragon_sprite, (dragon_sprite.get_width()*2, dragon_sprite.get_height()*2))
print(dragon_sprite.get_size()) # 128x128

center_y = 540 - (dragon_sprite.get_height() // 2)
center_x = 960 - (dragon_sprite.get_width() // 2)



running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  screen.fill((0, 0, 0))  # Clear screen with black
  # start drawing
  # positional hypothesis:
  # to put it in the middle in y axis: 540 - (sprite_height / 2)
  # to put it in the middle in x axis: 960 - (sprite_width / 2)
  # normal characters are 32x32, might get scaled
  
  # the position sprites are drawn are from top-left of the sprites. so x can be closer to 0 and y needs to be further down than usual
  
  # testing values
  screen.blit(dragon_sprite, (100, center_y - 128)) 
  screen.blit(dragon_sprite, (300, center_y - 128))  # upper middle
  screen.blit(dragon_sprite, (500, center_y - 128))
  
  screen.blit(dragon_sprite, (100, center_y + 128)) 
  screen.blit(dragon_sprite, (300, center_y + 128))  # upper middle
  screen.blit(dragon_sprite, (500, center_y + 128))
  pygame.display.flip()  # Update the display to show changes

pygame.quit()