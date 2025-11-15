import pygame
#initialization
pygame.init()
screen = pygame.display.set_mode((640, 640))
#sprite loading
dragon_sprite = pygame.image.load('sprites/spacedragon.png').convert()
dragon_sprite = pygame.transform.scale(dragon_sprite, (dragon_sprite.get_width()*2, dragon_sprite.get_height()*2))

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  screen.fill((0, 0, 0))  # Clear screen with black
  # start drawing
  screen.blit(dragon_sprite, (320,320))
  pygame.display.flip()  # Update the display to show changes

pygame.quit()