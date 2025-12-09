import os
import pygame
import character
import renderer

# constants
FPS = 60



#region Variables
skillslist = []
# list of all encounters & characters
characterslist = []
spriteslist = []

# party
playerParty = []
encounterParty = []
# dialogues
dialogueList = []

#endregion

def initializeGame():
  
  # loading all story files - reserved for later
  
  # story_dir = "story"
  # for filename in os.listdir(story_dir): 
  #   if filename.endswith(".txt"):
  #     with open(os.path.join(story_dir, filename), "r", encoding="utf-8") as f:
  #       dialog_lines = [line.strip() for line in f.readlines()]
  #       dialogueList.append((filename, dialog_lines))
  
  pygame.init()
  global clock
  clock = pygame.time.Clock()
  
  pygame.display.set_caption("Project Sun")
  
  with open("story/test.txt", "r", encoding="utf-8") as f:
    dialog_lines = [line.strip() for line in f.readlines()]
  
  # initialize characters
  initializeCharacters()
  playerParty.append(characterslist[0]) # main character
  encounterParty.append(characterslist[1]) # 'unknown' character
  
  
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
    sprite='sprites/characters/engineer.png',
    speed=(3, 6),
    hp=100,
    base_skills=[character.Skill("Engineer Wrench", [], [], 15, 'sprites/skills/skill1.png', character.engineer_wrench_skill)],
    sig_skills=[],
    supportSkills=[]
  )
  skillslist.append(player.base_skills[0])
  characterslist.append(player)
  
  unknown = character.Character(
    name="Unknown",
    sprite='sprites/characters/unknown.png',
    speed=(3, 7),
    hp=100,
    base_skills=[],
    sig_skills=[],
    supportSkills=[]
  )
  characterslist.append(unknown)

  spacedragon = character.Character(
    name="Space Dragon",
    sprite='sprites/characters/spacedragon.png',
    speed=(4, 8),
    hp=150,
    base_skills=[],
    sig_skills=[],
    supportSkills=[]
  )
  characterslist.append(spacedragon)



  renderer.spriteListInitialize(characterslist)
  renderer.skillSpriteInitialize(skillslist)
  return

def main():
  initializeGame()
  running = True
  # renderer.renderNovelScene(0, "This is a test dialogue line.") # have to send index for now as there are 2 lists in two different files.
  # renderer.renderCombatScene(playerParty, encounterParty)
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    renderer.renderCombatScene(playerParty, encounterParty)
    clock.tick(FPS)  # Limit to 60 frames per second
  return

main()
