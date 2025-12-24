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
encounters = []
encounterParty = []
encounterParty1 = []
encounterParty2 = []
encounterParty3 = []
encounterParty4 = []
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

def characterSetup(character, party):
  global skillslist, characterslist
  for base_skill in character.base_skills:
    skillslist.append(base_skill)
  for sig_skill in character.sig_skills:
    skillslist.append(sig_skill)
  characterslist.append(character)
  party.append(character)
  return
 
def initializeCharacters():
  global playerParty, encounterParty1, encounterParty2, encounterParty3, encounterParty4, characterslist, skillslist, encounters
  #region PLAYER AVAILABLE CHARACTERS
  player = character.Character(
    name="Blacked out Engineer",
    sprite='sprites/characters/player/engineer.png',
    speed=(3, 6),
    hp=100,
    base_skills=[character.Skill("Clink Clank", 2, 4, 10, 'sprites/skills/skill1.png', character.engineer_wrench_skill, ["enemy", "characters"]),
                  character.Skill("GET WELDED", 3, 3, 5, 'sprites/skills/skill2.png', None, ["all", "characters"])    ],
    sig_skills=[character.Skill("Ray Emitter", 4, 4, 8, 'sprites/skills/evade.png', None, ["enemy", "characters"]),
                character.Skill("We need to build a wall", 1, 0, 16, 'sprites/skills/def.png', None, ["enemy", "skills"])   ],
    supportSkills=[]
  )
  characterSetup(player, playerParty)
  
  unknown = character.Character(
    name="Unknown",
    sprite='sprites/characters/player/unknown.png',
    speed=(3, 7),
    hp=100,
    base_skills=[character.Skill("Toolbox", 2, 4, 10, 'sprites/skills/skill1.png', None, ["enemy", "characters"]),
                 character.Skill("Mysterious Syringe", 3, 3, 15, 'sprites/skills/skill2.png', None, ["all", "characters"])],
    sig_skills=[character.Skill("Suspicious Attack", 4, 4, 25, 'sprites/skills/evade.png', None, ["enemy", "characters"]),
                character.Skill("Stolen Shield", 3, 5, 20, 'sprites/skills/def.png', None, ["enemy", "skills"])],
    supportSkills=[]
  )
  characterSetup(unknown, playerParty)
  
  hos = character.Character(
    name="Head of Security",
    sprite='sprites/characters/player/hos.png',
    speed=(4, 7),
    hp=120,
    base_skills=[character.Skill("Taser Shot", 2, 4, 12, 'sprites/skills/skill1.png', None, ["enemy", "characters"]),
                 character.Skill("Shield Bash", 3, 3, 14, 'sprites/skills/skill2.png', None, ["enemy", "characters"])],
    sig_skills=[character.Skill("Shotgun Unload", 3, 6, 20, 'sprites/skills/evade.png', None, ["enemy", "characters"]),
                character.Skill("Fortify Position", 4, 4, 18, 'sprites/skills/def.png', None, ["player", "characters"])],
    supportSkills=[]
  )
  characterSetup(hos, playerParty)
  
  secoff = character.Character(
    name="Security Officer",
    sprite='sprites/characters/player/secoff.png',
    speed=(3, 6),
    hp=110,
    base_skills=[character.Skill("Baton Strike", 2, 4, 10, 'sprites/skills/skill1.png', None , ["enemy", "characters"]),
                 character.Skill("Pepper Spray", 3, 3, 12, 'sprites/skills/skill2.png', None, ["enemy", "characters"])],
    sig_skills=[character.Skill("Call Backup", 4, 4, 18, 'sprites/skills/evade.png', None, ["player", "characters"]),
                character.Skill("Expect Attack", 2, 5, 15, 'sprites/skills/def.png', None, ["enemy", "skills"])],
    supportSkills=[]
  )
  characterSetup(secoff, playerParty)
  
  clown = character.Character(
    name="Clown",
    sprite='sprites/characters/player/clown.png',
    speed=(4, 8),
    hp=90,
    base_skills=[character.Skill("Pie Throw", 2, 4, 14, 'sprites/skills/skill1.png', None, ["all", "characters"]),
                 character.Skill("Vicious Mockery", 3, 3, 16, 'sprites/skills/skill2.png', None, ["all", "characters"])],
    sig_skills=[character.Skill("Laughing Gas", 4, 4, 22, 'sprites/skills/evade.png', None, ["all", "characters"]),
                character.Skill("Lie Down", 2, 5, 19, 'sprites/skills/def.png', None, ["player", "skills"])], # does not need to be targetable, could add a 'click only' category
    supportSkills=[]
  )
  characterSetup(clown, playerParty)
  
  mime = character.Character(
    name="Mime",
    sprite='sprites/characters/player/mime.png',
    speed=(4, 7),
    hp=95,
    base_skills=[character.Skill("Banana Slip", 2, 4, 13, 'sprites/skills/skill1.png', None, ["enemy", "characters"]),
                 character.Skill("Silent Mockery", 3, 3, 17, 'sprites/skills/skill2.png', None, ["enemy", "characters"])],
    sig_skills=[character.Skill("Silent Strike", 4, 4, 21, 'sprites/skills/evade.png', None, ["enemy", "characters"]),
                character.Skill("Invisible Wall", 2, 4, 13, 'sprites/skills/skill1.png', None, ["all", "characters"])],
    supportSkills=[]
  )
  characterSetup(mime, playerParty) 
  
  # could initialize with together with the syndie counterpart
  borg = character.Character(
    name="Mediborg",
    sprite='sprites/characters/player/medicalborg_south.png',
    speed=(3, 5),
    hp=130,
    base_skills=[character.Skill("Medibeam", 2, 4, 15, 'sprites/skills/skill1.png', None, ["player", "characters"]),    
                 character.Skill("Hypospray", 3, 3, 18, 'sprites/skills/skill2.png', None, ["player", "characters"])],
    sig_skills=[character.Skill("Nanite Swarm", 4, 4, 23, 'sprites/skills/evade.png', None, ["player", "characters"])
                ,character.Skill("Reinforced Plating", 2, 5, 20, 'sprites/skills/def.png', None, ["enemy", "skills"])],
    supportSkills=[]
  )
  characterSetup(borg, playerParty)
  
  felinid = character.Character(
    name="Medic",
    sprite='sprites/characters/player/medic.png',
    speed=(4, 6),
    hp=100,
    base_skills=[character.Skill("Hypospray", 2, 4, 12, 'sprites/skills/skill1.png', None, ["player", "characters"]),
                 character.Skill("First Aid", 3, 3, 15, 'sprites/skills/skill2.png', None, ["player", "characters"])],    
    sig_skills=[character.Skill("Adrenaline Boost", 4, 4, 20, 'sprites/skills/evade.png', None, ["player", "characters"]),
                character.Skill("Electroshock", 2, 5, 18, 'sprites/skills/def.png', None, ["player", "skills"])],
    supportSkills=[]
  )
  characterSetup(felinid, playerParty)
  #endregion
  
  #region ENCOUNTER 1
  encounterParty1 = []
  carp1 = character.Character(
    name="Gray Space Carp",
    sprite='sprites/characters/encounter/encounter1/carp_gray_west.png',
    speed=(2, 5),
    hp=80,
    base_skills=[character.Skill("Splash Attack", 1, 3, 8, 'sprites/skills/skill1.png', None, ["player", "characters"]),
                 character.Skill("Prepare", 2, 2, 10, 'sprites/skills/skill2.png', None, ["enemy", "characters"])], # on-click category
    sig_skills=[character.Skill("Fin Swipe", 2, 4, 12, 'sprites/skills/evade.png', None, ["player", "characters"]),
                character.Skill("Evasive Teleport", 1, 5, 14, 'sprites/skills/def.png', None, ["player", "skills"])],
    supportSkills=[]
  )
  characterSetup(carp1, encounterParty1)
  carp2 = character.Character(
    name="Red Space Carp",
    sprite='sprites/characters/encounter/encounter1/carp_red_west.png',
    speed=(2, 5),
    hp=80,
    base_skills=[character.Skill("Splash Attack", 1, 3, 8, 'sprites/skills/skill1.png', None, ["player", "characters"]),
                 character.Skill("Prepare", 2, 2, 10, 'sprites/skills/skill2.png', None, ["enemy", "characters"])], # on-click category
    sig_skills=[character.Skill("Fin Swipe", 2, 4, 12, 'sprites/skills/evade.png', None, ["player", "characters"]),
                character.Skill("Evasive Teleport", 1, 5, 14, 'sprites/skills/def.png', None, ["player", "skills"])],
    supportSkills=[]
  )
  characterSetup(carp2, encounterParty1)
  carp3 = character.Character(
    name="Purple Space Carp",
    sprite='sprites/characters/encounter/encounter1/carp_purple_west.png',
    speed=(2, 5),
    hp=80,
    base_skills=[character.Skill("Splash Attack", 1, 3, 8, 'sprites/skills/skill1.png', None, ["player", "characters"]),
                 character.Skill("Prepare", 2, 2, 10, 'sprites/skills/skill2.png', None, ["enemy", "characters"])], # on-click category
    sig_skills=[character.Skill("Fin Swipe", 2, 4, 12, 'sprites/skills/evade.png', None, ["player", "characters"]),
                character.Skill("Evasive Teleport", 1, 5, 14, 'sprites/skills/def.png', None, ["player", "skills"])],
    supportSkills=[]
  )
  characterSetup(carp3, encounterParty1)
  carp4 = character.Character(
    name="Green Space Carp",
    sprite='sprites/characters/encounter/encounter1/carp_green_west.png',
    speed=(2, 5),
    hp=80,
    base_skills=[character.Skill("Splash Attack", 1, 3, 8, 'sprites/skills/skill1.png', None, ["player", "characters"]),
                 character.Skill("Prepare", 2, 2, 10, 'sprites/skills/skill2.png', None, ["enemy", "characters"])], # on-click category
    sig_skills=[character.Skill("Fin Swipe", 2, 4, 12, 'sprites/skills/evade.png', None, ["player", "characters"]),
                character.Skill("Evasive Teleport", 1, 5, 14, 'sprites/skills/def.png', None, ["player", "skills"])],
    supportSkills=[]
  )
  characterSetup(carp4, encounterParty1)
  encounter1 = renderer.Encounter(
    name="Encounter1",
    encounterPartyCharacters=encounterParty1,
    encounterPartyPositions=[(1400, 400), (1600, 400), (1400, 600), (1600, 600)],
    playerPartyCharacters=[playerParty[0], playerParty[1], playerParty[2], playerParty[3]], # later defined by character selection screen
    playerPartyPositions=[(200, 400), (400, 400), (200, 600), (400, 600)],
    combatBGimage='sprites/backgrounds/encounter_1.png'
  )
  #endregion
  
  #region ENCOUNTER 2
  #changeling - traitor
  encounterParty2 = []
  changeling = character.Character(
    name="Changeling",
    sprite='sprites/characters/encounter/encounter2/changeling_base.png', # has 4 sprites, handled later with skills or during novel to combat process
    speed=(4, 7),
    hp=110,
    base_skills=[character.Skill("Shapeshift Strike", 3, 4, 15, 'sprites/skills/skill1.png', None, ["player", "characters"]),
                 character.Skill("Mimicry", 2, 3, 12, 'sprites/skills/skill2.png', None, ["enemy", "characters"])],
    sig_skills=[character.Skill("Adaptive Defense", 4, 5, 20, 'sprites/skills/evade.png', None, ["enemy", "skills"]),
                character.Skill("Regeneration", 3, 4, 18, 'sprites/skills/def.png', None, ["enemy", "characters"])],
    supportSkills=[]
  )
  characterSetup(changeling, encounterParty2)
  traitor = character.Character(
    name="Traitor",
    sprite='sprites/characters/encounter/encounter2/traitor.png', #sprite not ready
    speed=(3, 6),
    hp=100,
    base_skills=[character.Skill("Backstab", 3, 4, 14, 'sprites/skills/skill1.png', None, ["player", "characters"]),
                 character.Skill("Sabotage", 2, 3, 16, 'sprites/skills/skill2.png', None, ["enemy", "skills"])],
    sig_skills=[character.Skill("Poisoned Blade", 4, 5, 22, 'sprites/skills/evade.png', None, ["player", "characters"]),
                character.Skill("Vanish", 3, 4, 19, 'sprites/skills/def.png', None, ["enemy", "skills"])],
    supportSkills=[]
  )
  characterSetup(traitor, encounterParty2) # NEED TO REMOVE UNKNOWN FROM PLAYER PARTY
  encounter2 = renderer.Encounter(
    name="Encounter2",
    encounterPartyCharacters=encounterParty2,
    encounterPartyPositions=[(1400, 400), (1600, 400)],
    playerPartyCharacters=[playerParty[0], playerParty[1], playerParty[2], playerParty[3]], # later defined by character selection screen
    playerPartyPositions=[(200, 400), (400, 400), (200, 600), (400, 600)],
    combatBGimage='sprites/backgrounds/encounter_2.png'
  )
  #endregion
  
  #region ENCOUNTER 3
  # MOON HERETIC
  encounterParty3 = []
  heretic = character.Character(
    name="Moon Heretic",
    sprite='sprites/characters/encounter/encounter3/heretic_battle.png',
    speed=(4, 7),
    hp=120,
    base_skills=[character.Skill("Lunar Strike", 3, 4, 18, 'sprites/skills/skill1.png', None, ["player", "characters"]),
                 character.Skill("Gravity Well", 2, 3, 15, 'sprites/skills/skill2.png', None, ["enemy", "characters"])],
    sig_skills=[character.Skill("Lunacy", 4, 5, 25, 'sprites/skills/evade.png', None, ["player", "characters"]),
                character.Skill("Eclipse Shield", 3, 4, 22, 'sprites/skills/def.png', None, ["enemy", "skills"])],
    supportSkills=[]
  )
  characterSetup(heretic, encounterParty3)
  encounter3 = renderer.Encounter(
    name="Encounter3",
    encounterPartyCharacters=encounterParty3,
    encounterPartyPositions=[(1400, 800)],
    playerPartyCharacters=[playerParty[0], playerParty[1], playerParty[2], playerParty[3]], # later defined by character selection screen
    playerPartyPositions=[(200, 400), (400, 400), (200, 600), (400, 600)],
    combatBGimage='sprites/backgrounds/encounter_3.png'
  )
  #endregion
  
  #region ENCOUNTER 4
  # dragon
  encounterParty4 = []
  spacedragon = character.Character(
    name="Space Dragon",
    sprite='sprites/characters/encounter/encounter4/spacedragon.png',
    speed=(4, 8),
    hp=150,
    base_skills=[character.Skill("Cosmic Breath", 4, 5, 20, 'sprites/skills/skill1.png', None, ["player", "characters"]),
                 character.Skill("Tail Swipe", 3, 4, 18, 'sprites/skills/skill2.png', None, ["player", "characters"])],
    sig_skills=[character.Skill("Starfall", 5, 6, 30, 'sprites/skills/evade.png', None, ["player", "characters"]),
                character.Skill("Galactic Roar", 4, 5, 25, 'sprites/skills/def.png', None, ["enemy", "skills"])],
    supportSkills=[]
  )
  characterSetup(spacedragon, encounterParty4)
  encounter4 = renderer.Encounter(
    name="Encounter4",
    encounterPartyCharacters=encounterParty4,
    encounterPartyPositions=[(1400, 800)],
    playerPartyCharacters=[playerParty[0], playerParty[1], playerParty[2], playerParty[3]], # later defined by character selection screen
    playerPartyPositions=[(200, 400), (400, 400), (200, 600), (400, 600)],
    combatBGimage='sprites/backgrounds/encounter_4.png'
  )
  # nukies
  
  #endregion

  encounters = [encounter1, encounter2, encounter3, encounter4]
  renderer.spriteListInitialize(characterslist, encounters)
  renderer.skillSpriteInitialize(skillslist)
  return
#endregion




def main():
  initializeGame()
  running = True
  # renderer.renderNovelScene(characterslist[0], "This is a test dialogue line.") # have to send index for now as there are 2 lists in two different files.
  # renderer.renderCombatScene(playerParty, encounterParty)
  renderer.initializePlayerCharacters(playerParty)
  encounterDefaultPlayerParty = [playerParty[0], playerParty[1], playerParty[2], playerParty[3]]
  
  encounterDefault = renderer.Encounter(
    name="Encounter1",
    encounterPartyCharacters=encounterParty1,
    encounterPartyPositions=[(1400, 400), (1600, 400), (1400, 800), (1600, 800)],
    playerPartyCharacters=encounterDefaultPlayerParty, 
    playerPartyPositions=[(200, 400), (400, 400), (200, 800), (400, 800)],
    combatBGimage='sprites/backgrounds/encounter_1.png'
  )
  
  
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEBUTTONUP:
        # on click, check for sprite collision
        partyPositions, skillPositions = renderer.CombatSpriteTransformCalculation(encounterDefault)
        renderer.ClickEvent("combat", partyPositions, skillPositions, playerParty, encounterParty)
        # renderer.GetMousePos()
        # renderer.ClickEvent("partyselect")
        continue
    renderer.CombatSceneRender(encounterDefault)
    # renderer.RenderPartySelecter(playerParty)
    clock.tick(FPS)  # Limit to 60 frames per second
  return
  
main()
