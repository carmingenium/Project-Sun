import pygame
import character
import renderer

print("Imported:", renderer)
print("Path:", renderer.__file__)
print("Members:", dir(renderer))



#region Variables
# list of all encounters & characters
characterslist = []
spriteslist = []

# party
playerParty = []
encounterParty = []
#endregion

def initializeGame():
  # initialize story text
  with open("story/test.txt", "r", encoding="utf-8") as f: # load text
    dialog_lines = [line.strip() for line in f.readlines()]
  # font = pygame.font.Font(None, 32)   # None = default font, 32 = size
  # initialize characters
  initializeCharacters()
  playerParty.append(characterslist[0]) # main character
  encounterParty.append(characterslist[1]) # unknown
  
  
def initializeCharacters():
  #region charlist

  # player: drunk engineer
  # head of sec
  # sec off
  # assistant
  # clown
  # mime
  # Borg (default ~ can transform)
  # unknown


  # encounter 1
  # X amount space carps


  # encounter 2
  # X amount zombies


  # encounter 3
  # Changeling
  # Traitor


  # encounter 4
  # Moon Heretic (alternative ending)

  # encounter 5 (boss fight)
  # 3 way fight (3 endings)

  # Party 1
  # Space Dragon

  # Party 2
  # Nukie Gunner (dps, cc)
  # Nukie Engineer (summoner, heals borg)
  # Nukie Chemist (dps, healer, debuff)
  # Nukie Borg  (tank dps)
  #endregion
  player = character.Character(
    name="Blacked out Engineer",
    sprite='sprites/engineer.png',
    speed=(3, 6),
    hp=100,
    skills=[],
    supportSkills=[]
  )
  characterslist.append(player)
  unknown = character.Character(
    name="Unknown",
    sprite='sprites/unknown.png',
    speed=(3, 7),
    hp=100,
    skills=[],
    supportSkills=[]
  )
  characterslist.append(unknown)

  spacedragon = character.Character(
    name="Space Dragon",
    sprite='sprites/spacedragon.png',
    speed=(4, 8),
    hp=150,
    skills=[],
    supportSkills=[]
  )
  characterslist.append(spacedragon)



  renderer.spriteListInitialize(characterslist)
  return
def getCharacterList():
  return characterslist


def main():
  initializeGame()
  running = True
  # renderer.renderNovelScene(0, "This is a test dialogue line.") # have to send index for now as there are 2 lists in two different files.
  renderer.renderCombatScene(playerParty, encounterParty)
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

  # clock.tick(60)  # Limit to 60 frames per second
  return

main()
