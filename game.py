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

#region initialization
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
  # Borg sprite ready
  # unknown sprite done


  # encounter 1 - bg ready
  # X amount space carps | sprite ready


  # encounter 2 - bg ready
  # Changeling | ready
  # Traitor | sprite ready


  # encounter 3  - bg ready
  # Moon Heretic (alternative ending) - ready

  # encounter 4 (boss fight) - bg ready
  # 3 way fight (3 endings)

  # Party 1
  # Space Dragon - sprite ready (might add new sprite for new forms etc.)

  # Party 2 
  # Nukie Gunner (dps, cc) - sprite not ready
  # Nukie Engineer (summoner, heals borg) - sprite not ready 
  # Nukie Chemist (dps, healer, debuff) - sprite not ready 
  # Nukie Borg  (tank dps) sprite ready
  #endregion
  
  # for testing purposes
  for i in range(6):
    player = character.Character(
      name="Blacked out Engineer",
      sprite='sprites/characters/player/engineer.png',
      speed=(3, 6),
      hp=100,
      base_skills=[character.Skill("Clink Clank", 2, 4, 10, 'sprites/skills/skill1.png', character.engineer_wrench_skill, ["enemy", "characters"]),
                   character.Skill("GET WELDED", 3, 3, 5, 'sprites/skills/skill2.png', None, ["all", "characters"])    ],
      sig_skills=[character.Skill("Ray Emitter", 4, 4, 8, 'sprites/skills/evade.png', None, ["enemy", "characters"]),
                  character.Skill("We need to build a wall", 1, 0, 16, 'sprites/skills/def.png', None, ["enemy", "characters"])   ],
      supportSkills=[]
    )
    skillslist.append(player.base_skills[0])
    skillslist.append(player.sig_skills[0])
    characterslist.append(player)
    playerParty.append(player)
  
  for i in range(6):
    unknown = character.Character(
      name="Unknown",
      sprite='sprites/characters/player/unknown.png',
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



  # final encounter
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
#endregion


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
