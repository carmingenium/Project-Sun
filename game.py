import os
import pygame
import character
import renderer

# constants
FPS = 60



#region Variables


gamestate = "" # "partyselect", "novel" or "combat"

# object lists
characterslist = []
spriteslist = []
skillslist = []

# party
currentParty = []
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
    base_skill.user = character
  for sig_skill in character.sig_skills:
    skillslist.append(sig_skill)
    sig_skill.user = character
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
    base_skills=[character.Skill("Clink Clank", 10, 'sprites/skills/skill1.png', character.engineer_baseskill1, "Hits an enemy with a wrench, deals 10 damage.", ["enemy", "characters"]),
                  character.Skill("GET WELDED", 8, 'sprites/skills/skill2.png', character.engineer_baseskill2,  "Welds a target for 8 damage. If target is mechanical, heals it instead.", ["all", "characters"])],
    sig_skills=[character.Skill("Ray Emitter", 6, 'sprites/skills/evade.png', character.engineer_sigskill1, "Burns an enemy with a ray emitter, deals 6 damage. If it hits, increases sanity by 10", ["enemy", "characters"]),
                character.Skill("We need to build a wall", 10, 'sprites/skills/def.png', character.engineer_sigskill2, "Builds a wall with Rapid Construction Device, negating 10 damage from an enemy attack. ", ["enemy", "skills"])]
  )
  characterSetup(player, playerParty)
  
  unknown = character.Character(
    name="Unknown",
    sprite='sprites/characters/player/unknown.png',
    speed=(3, 7),
    hp=100,
    base_skills=[character.Skill("Toolbox", 10, 'sprites/skills/skill1.png', character.unknown_baseskill1, "Baseskill1", ["enemy", "characters"]),
                 character.Skill("Mysterious Syringe", 10, 'sprites/skills/skill2.png', character.unknown_baseskill2, "Baseskill2", ["all", "characters"])],
    sig_skills=[character.Skill("Suspicious Attack", 10, 'sprites/skills/evade.png', character.unknown_sigskill1, "Sigskill1", ["enemy", "characters"]),
                character.Skill("Stolen Shield", 10, 'sprites/skills/def.png', character.unknown_sigskill2, "Sigskill2", ["enemy", "skills"])]
  )
  characterSetup(unknown, playerParty)
  
  hos = character.Character(
    name="Head of Security",
    sprite='sprites/characters/player/hos.png',
    speed=(4, 7),
    hp=120,
    base_skills=[character.Skill("Taser Shot", 10, 'sprites/skills/skill1.png', character.hos_baseskill1, "Baseskill1", ["enemy", "characters"]),
                 character.Skill("Shield Bash", 10, 'sprites/skills/skill2.png', character.hos_baseskill2, "Baseskill2", ["enemy", "characters"])],
    sig_skills=[character.Skill("Shotgun Unload", 10, 'sprites/skills/evade.png', character.hos_sigskill1, "Sigskill1", ["enemy", "characters"]),
                character.Skill("Fortify Position", 10, 'sprites/skills/def.png', character.hos_sigskill2, "Sigskill2", ["player", "characters"])]
    
  )
  characterSetup(hos, playerParty)
  
  secoff = character.Character(
    name="Security Officer",
    sprite='sprites/characters/player/secoff.png',
    speed=(3, 6),
    hp=110,
    base_skills=[character.Skill("Baton Strike", 10, 'sprites/skills/skill1.png', character.secoff_baseskill1, "Baseskill1", ["enemy", "characters"]),
                 character.Skill("Pepper Spray", 10, 'sprites/skills/skill2.png', character.secoff_baseskill2, "Baseskill2", ["enemy", "characters"])],
    sig_skills=[character.Skill("Call Backup", 10, 'sprites/skills/evade.png', character.secoff_sigskill1, "Sigskill1", ["player", "characters"]),
                character.Skill("Expect Attack", 10, 'sprites/skills/def.png', character.secoff_sigskill2, "Sigskill2", ["enemy", "skills"])]
    
  )
  characterSetup(secoff, playerParty)
  
  clown = character.Character(
    name="Clown",
    sprite='sprites/characters/player/clown.png',
    speed=(4, 8),
    hp=90,
    base_skills=[character.Skill("Pie Throw", 10, 'sprites/skills/skill1.png', character.clown_baseskill1, "Baseskill1", ["all", "characters"]),
                 character.Skill("Vicious Mockery", 10, 'sprites/skills/skill2.png', character.clown_baseskill2, "Baseskill2", ["all", "characters"])],
    sig_skills=[character.Skill("Laughing Gas", 10, 'sprites/skills/evade.png', character.clown_sigskill1, "Sigskill1", ["all", "characters"]),
                character.Skill("Lie Down", 10, 'sprites/skills/def.png', character.clown_sigskill2, "Sigskill2", ["player", "skills"])] # does not need to be targetable, could add a 'click only' category
    
  )
  characterSetup(clown, playerParty)
  
  mime = character.Character(
    name="Mime",
    sprite='sprites/characters/player/mime.png',
    speed=(4, 7),
    hp=95,
    base_skills=[character.Skill("Banana Slip", 13, 'sprites/skills/skill1.png', character.mime_baseskill1, "Baseskill1", ["enemy", "characters"]),
                 character.Skill("Silent Mockery", 13, 'sprites/skills/skill2.png', character.mime_baseskill2, "Baseskill2", ["enemy", "characters"])],
    sig_skills=[character.Skill("Silent Strike", 13, 'sprites/skills/evade.png', character.mime_sigskill1, "Sigskill1", ["enemy", "characters"]),
                character.Skill("Invisible Wall", 13, 'sprites/skills/skill1.png', character.mime_sigskill2, "Sigskill2", ["all", "characters"])]
  )
  characterSetup(mime, playerParty) 
  
  # could initialize with together with the syndie counterpart
  borg = character.Character(
    name="Mediborg",
    sprite='sprites/characters/player/medicalborg_south.png',
    speed=(3, 5),
    hp=130,
    base_skills=[character.Skill("Medibeam", 15, 'sprites/skills/skill1.png', character.borg_baseskill1, "Baseskill1", ["player", "characters"]),    
                 character.Skill("Hypospray", 15, 'sprites/skills/skill2.png', character.borg_baseskill2, "Baseskill2", ["player", "characters"])],
    sig_skills=[character.Skill("Nanite Swarm", 15, 'sprites/skills/evade.png', character.borg_sigskill1, "Sigskill1", ["player", "characters"])
                ,character.Skill("Reinforced Plating", 15, 'sprites/skills/def.png', character.borg_sigskill2, "Sigskill2", ["enemy", "skills"])]
  )
  characterSetup(borg, playerParty)
  
  felinid = character.Character(
    name="Medic",
    sprite='sprites/characters/player/medic.png',
    speed=(4, 6),
    hp=100,
    base_skills=[character.Skill("Physical Hypospray", 15, 'sprites/skills/skill1.png', character.medic_baseskill1, "Baseskill1", ["player", "characters"]),
                 character.Skill("First Aid", 15, 'sprites/skills/skill2.png', character.medic_baseskill2, "Baseskill2", ["player", "characters"])],    
    sig_skills=[character.Skill("Adrenaline Boost", 15, 'sprites/skills/evade.png', character.medic_sigskill1, "Sigskill1", ["player", "characters"]),
                character.Skill("Electroshock", 15, 'sprites/skills/def.png', character.medic_sigskill2, "Sigskill2", ["player", "skills"])]
    
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
    base_skills=[character.Skill("Splash Attack", 15, 'sprites/skills/skill1.png', character.carp_baseskill1, "Baseskill1", ["player", "characters"]),
                 character.Skill("Prepare", 15, 'sprites/skills/skill2.png', character.carp_baseskill2, "Baseskill2", ["enemy", "characters"])], # on-click category
    sig_skills=[character.Skill("Fin Swipe", 15, 'sprites/skills/evade.png', character.carp_sigskill1, "Sigskill1", ["player", "characters"]),
                character.Skill("Evasive Teleport", 15, 'sprites/skills/def.png', character.carp_sigskill2, "Sigskill2", ["player", "skills"])]
  )
  characterSetup(carp1, encounterParty1)
  carp2 = character.Character(
    name="Red Space Carp",
    sprite='sprites/characters/encounter/encounter1/carp_red_west.png',
    speed=(2, 5),
    hp=80,
    base_skills=[character.Skill("Splash Attack", 15, 'sprites/skills/skill1.png', character.carp_baseskill1, "Baseskill1", ["player", "characters"]),
                 character.Skill("Prepare", 15, 'sprites/skills/skill2.png', character.carp_baseskill2, "Baseskill2", ["enemy", "characters"])], # on-click category
    sig_skills=[character.Skill("Fin Swipe", 15, 'sprites/skills/evade.png', character.carp_sigskill1, "Sigskill1", ["player", "characters"]),
                character.Skill("Evasive Teleport", 15, 'sprites/skills/def.png', character.carp_sigskill2, "Sigskill2", ["player", "skills"])]
  )
  characterSetup(carp2, encounterParty1)
  carp3 = character.Character(
    name="Purple Space Carp",
    sprite='sprites/characters/encounter/encounter1/carp_purple_west.png',
    speed=(2, 5),
    hp=80,
    base_skills=[character.Skill("Splash Attack", 15, 'sprites/skills/skill1.png', character.carp_baseskill1, "Baseskill1", ["player", "characters"]),
                 character.Skill("Prepare", 15, 'sprites/skills/skill2.png', character.carp_baseskill2, "Baseskill2", ["enemy", "characters"])], # on-click category
    sig_skills=[character.Skill("Fin Swipe", 15, 'sprites/skills/evade.png', character.carp_sigskill1, "Sigskill1", ["player", "characters"]),
                character.Skill("Evasive Teleport", 15, 'sprites/skills/def.png', character.carp_sigskill2, "Sigskill2", ["player", "skills"])]
    
  )
  characterSetup(carp3, encounterParty1)
  carp4 = character.Character(
    name="Green Space Carp",
    sprite='sprites/characters/encounter/encounter1/carp_green_west.png',
    speed=(2, 5),
    hp=80,
    base_skills=[character.Skill("Splash Attack", 15, 'sprites/skills/skill1.png', character.carp_baseskill1, "Baseskill1", ["player", "characters"]),
                 character.Skill("Prepare", 15, 'sprites/skills/skill2.png', character.carp_baseskill2, "Baseskill2", ["enemy", "characters"])], # on-click category
    sig_skills=[character.Skill("Fin Swipe", 15, 'sprites/skills/evade.png', character.carp_sigskill1, "Sigskill1", ["player", "characters"]),
                character.Skill("Evasive Teleport", 15, 'sprites/skills/def.png', character.carp_sigskill2, "Sigskill2", ["player", "skills"])]
    
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
    base_skills=[character.Skill("Shapeshift Strike", 15, 'sprites/skills/skill1.png', character.changeling_baseskill1, "Baseskill1", ["player", "characters"]),
                 character.Skill("Mimicry", 15, 'sprites/skills/skill2.png', character.changeling_baseskill2, "Baseskill2", ["enemy", "characters"])],
    sig_skills=[character.Skill("Adaptive Defense", 15, 'sprites/skills/evade.png', character.changeling_sigskill1, "Sigskill1", ["enemy", "skills"]),
                character.Skill("Regeneration", 15, 'sprites/skills/def.png', character.changeling_sigskill2, "Sigskill2", ["enemy", "characters"])]
    
  )
  characterSetup(changeling, encounterParty2)
  traitor = character.Character(
    name="Traitor",
    sprite='sprites/characters/encounter/encounter2/traitor.png', #sprite not ready
    speed=(3, 6),
    hp=100,
    base_skills=[character.Skill("Backstab", 15, 'sprites/skills/skill1.png', character.traitor_baseskill1, "Baseskill1", ["player", "characters"]),
                 character.Skill("Sabotage", 15, 'sprites/skills/skill2.png', character.traitor_baseskill2, "Baseskill2", ["enemy", "skills"])],
    sig_skills=[character.Skill("Poisoned Blade", 15, 'sprites/skills/evade.png', character.traitor_sigskill1, "Sigskill1", ["player", "characters"]),
                character.Skill("Vanish", 15, 'sprites/skills/def.png', character.traitor_sigskill2, "Sigskill2", ["enemy", "skills"])]
    
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
    base_skills=[character.Skill("Lunar Strike", 15, 'sprites/skills/skill1.png', character.heretic_baseskill1, "Baseskill1", ["player", "characters"]),
                 character.Skill("Gravity Well", 15, 'sprites/skills/skill2.png', character.heretic_baseskill2, "Baseskill2", ["enemy", "characters"])],
    sig_skills=[character.Skill("Lunacy", 15, 'sprites/skills/evade.png', character.heretic_sigskill1, "Sigskill1", ["player", "characters"]),
                character.Skill("Eclipse Shield", 15, 'sprites/skills/def.png', character.heretic_sigskill2, "Sigskill2", ["enemy", "skills"])]
    
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
    base_skills=[character.Skill("Cosmic Breath", 20, 'sprites/skills/skill1.png', character.dragon_baseskill1, "Baseskill1", ["player", "characters"]),
                 character.Skill("Tail Swipe", 15, 'sprites/skills/skill2.png', character.dragon_baseskill2, "Baseskill2", ["player", "characters"])],
    sig_skills=[character.Skill("Starfall", 15, 'sprites/skills/evade.png', character.dragon_sigskill1, "Sigskill1", ["player", "characters"]),
                character.Skill("Galactic Roar", 15, 'sprites/skills/def.png', character.dragon_sigskill2, "Sigskill2", ["enemy", "skills"])]
    
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
    gamestate = renderer.game_state
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEBUTTONUP:
        # on click, check for sprite collision
        if(gamestate == "partyselect"):
          selectedCharacters = renderer.ClickEvent("partyselect", [], [], playerParty, [])
          if(selectedCharacters != None):
            currentParty = selectedCharacters
        if(gamestate == "combat"):
          partyPositions, skillPositions = renderer.CombatSpriteTransformCalculation(encounterDefault)
          renderer.ClickEvent("combat", partyPositions, skillPositions, playerParty, encounterParty)
        # renderer.GetMousePos()
        # renderer.ClickEvent("partyselect")
        continue
    if gamestate == "combat":
      encounterDefault.playerPartyCharacters = currentParty
      renderer.RenderCombatScene(encounterDefault)
    elif gamestate == "partyselect":
      renderer.RenderPartySelecter(playerParty)
    elif gamestate == "novel":
      # get story file and render accordingly
      renderer.RenderNovelScene(playerParty[0], "this is a test.")
    clock.tick(FPS)  # Limit to 60 frames per second
  return
  
main()
