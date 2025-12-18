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
  
def initializeCharacters():
  #region charlist

  # player: drunk engineer sprite done
  # head of sec sprite done
  # sec off sprite done 
  # clown sprite done 
  # mime sprite done 
  # Borg (default ~ can transform (tranform delayed)) sprite ready not imported
  # unknown sprite done


  # encounter 1 - hallway - sprite not ready
  # X amount space carps | sprite ready not imported


  # encounter 2 - hallway
  # X amount zombies | sprite not found, might get removed


  # encounter 3 - behind fire alarms & in front of engineering department - sprite not ready
  # Changeling | 2 sprites needed - ready not imported
  # Traitor | sprite done


  # encounter 4  - inside engineering department - sprite not ready
  # Moon Heretic (alternative ending) - sprite ready not imported

  # encounter 5 (boss fight) - supermatter engine room - sprite not ready
  # 3 way fight (3 endings)

  # Party 1
  # Space Dragon - sprite ready (might add new sprite for new forms etc.)

  # Party 2 
  # Nukie Gunner (dps, cc) - sprite not ready
  # Nukie Engineer (summoner, heals borg) - sprite not ready 
  # Nukie Chemist (dps, healer, debuff) - sprite not ready 
  # Nukie Borg  (tank dps) sprite ready not imported
  #endregion
  # for testing purposes
  for i in range(6):
    player = character.Character(
      name="Blacked out Engineer",
      sprite='sprites/characters/engineer.png',
      speed=(3, 6),
      hp=100,
      base_skills=[character.Skill("Engineer Wrench", [], [], 15, 'sprites/skills/skill1.png', character.engineer_wrench_skill)],
      sig_skills=[character.Skill("Overclocked Repair", [], [], 25, 'sprites/skills/evade.png', None)],
      supportSkills=[]
    )
    skillslist.append(player.base_skills[0])
    skillslist.append(player.sig_skills[0])
    characterslist.append(player)
    playerParty.append(player)
  
  for i in range(6):
    unknown = character.Character(
      name="Unknown",
      sprite='sprites/characters/unknown.png',
      speed=(3, 7),
      hp=100,
      base_skills=[character.Skill("Unknown Wrench", [], [], 15, 'sprites/skills/skill1.png', None)],
      sig_skills=[character.Skill("Overclocked Repair", [], [], 25, 'sprites/skills/evade.png', None)],
      supportSkills=[]
    )
    characterslist.append(unknown)
    skillslist.append(unknown.base_skills[0])
    skillslist.append(unknown.sig_skills[0])
    encounterParty.append(unknown)

  # spacedragon = character.Character(
  #   name="Space Dragon",
  #   sprite='sprites/characters/spacedragon.png',
  #   speed=(4, 8),
  #   hp=150,
  #   base_skills=[],
  #   sig_skills=[],
  #   supportSkills=[]
  # )
  # characterslist.append(spacedragon)



  renderer.spriteListInitialize(characterslist)
  renderer.skillSpriteInitialize(skillslist)
  return

def main():
  initializeGame()
  running = True
  # renderer.renderNovelScene(characterslist[0], "This is a test dialogue line.") # have to send index for now as there are 2 lists in two different files.
  # renderer.renderCombatScene(playerParty, encounterParty)
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEBUTTONUP:
        # on click, check for sprite collision
        CombatBGPos, leftPartyPositions, rightPartyPositions, leftPartyBaseSkillPositions, leftPartySignatureSkillPositions, rightPartyBaseSkillPositions, rightPartySignatureSkillPositions = renderer.CombatSpriteTransformCalculation()
        renderer.ClickEvent(leftPartyPositions, rightPartyPositions, leftPartyBaseSkillPositions, leftPartySignatureSkillPositions, rightPartyBaseSkillPositions, rightPartySignatureSkillPositions, playerParty, encounterParty)
        continue
    renderer.CombatSceneRender(playerParty, encounterParty)
    clock.tick(FPS)  # Limit to 60 frames per second
  return
  
main()
