import os
import pygame
import character
import renderer

# constants
FPS = 60



#region Variables


gamestate = "" # "partyselect", "novel" or "combat"
current_encounter = 0
current_novel = 0
current_dialogue_line = 0

# object lists
characterslist = []
spriteslist = []
skillslist = []

# party
currentParty = []
playerParty = []
encounters = []
encounterParty1 = []
encounterParty2 = []
encounterParty3 = []
encounterParty4 = []
# novel
novelList = [ # 4 encounters, 5 dialogues => pre 1, post 1, post 2, post 3, post 4
  [], [], [], [], []
]

#endregion

#region initialization

def initializeGame():
  
  # loading all story files - reserved for later
  
  # NOVEL INITIALIZATION:
  # set novel list with amount of story precalculated.
  global novelList
  # load all text and characters from txt file into proper lists
  story_dir = "story"
  
  for filename in os.listdir(story_dir): 
    dialogueList = []
    if filename.endswith(".txt"):
      index = int(filename.split("_")[0]) - 1  # assuming filenames are like '1_level.txt'
      with open(os.path.join(story_dir, filename), "r", encoding="utf-8") as f:
        dialog_lines = [line.strip() for line in f.readlines()]
        dialogueList.append((filename, dialog_lines))
    novelList[index] = dialogueList
  # load in game by index.

  
  pygame.init()
  global clock
  clock = pygame.time.Clock()
  
  pygame.display.set_caption("Project Sun")
  
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
    name="Blacked Out Engineer",
    sprite='sprites/characters/player/engineer.png',
    speed=(3, 6),
    hp=100,
    base_skills=[character.Skill("Clink Clank", 10, 'sprites/skills/skill1.png', character.engineer_baseskill1, "Hits an enemy with a wrench, deals 10 damage.", ["enemy", "characters"]),
                  character.Skill("Quick Weld", 8, 'sprites/skills/skill2.png', character.engineer_baseskill2,  "Welds a target for 8 damage. If target is mechanical, heals it instead.", ["all", "characters"])],
    sig_skills=[character.Skill("Ray Emitter", 6, 'sprites/skills/evade.png', character.engineer_sigskill1, "Burns an enemy with a ray emitter, deals 6 damage. If it hits, increases sanity by 10", ["enemy", "characters"]),
                character.Skill("Instant Wall", 10, 'sprites/skills/def.png', character.engineer_sigskill2, "Builds a wall with Rapid Construction Device, negating 10 damage from an enemy attack. ", ["enemy", "skills"])]
  )
  characterSetup(player, playerParty)
  
  unknown = character.Character(
    name="Unknown",
    sprite='sprites/characters/player/unknown.png',
    speed=(3, 7),
    hp=100,
    base_skills=[character.Skill("Toolbox", 10, 'sprites/skills/skill1.png', character.unknown_baseskill1, "Hits an enemy with a toolbox, deals 10 damage.", ["enemy", "characters"]),
                 character.Skill("Mysterious Syringe", 6, 'sprites/skills/skill2.png', character.unknown_baseskill2, "Uses a mysterious syringe, effect unknown.", ["all", "characters"])],
    sig_skills=[character.Skill("Suspicious Baton", 5, 'sprites/skills/evade.png', character.unknown_sigskill1, "Uses a stun baton to decrease targets speed by 1, deals 5 damage.", ["enemy", "characters"]),
                character.Skill("Stolen Shield", 5, 'sprites/skills/def.png', character.unknown_sigskill2, "Blocks incoming attacks, reducing damage by 5. Also has a chance to fully block damage.", ["enemy", "skills"])]
  )
  characterSetup(unknown, playerParty)
  
  hos = character.Character(
    name="Head of Security",
    sprite='sprites/characters/player/hos.png',
    speed=(4, 7),
    hp=120,
    base_skills=[character.Skill("Taser Shot", 4, 'sprites/skills/skill1.png', character.hos_baseskill1, "Tasers an enemy, deals 4 damage. Decreases speed by one from target.", ["enemy", "characters"]),
                 character.Skill("Shield Bash", 10, 'sprites/skills/skill2.png', character.hos_baseskill2, "Bashes an enemy with the shield.", ["enemy", "characters"])],
    sig_skills=[character.Skill("Shotgun Unload", 15, 'sprites/skills/evade.png', character.hos_sigskill1, "Shoots an enemy with a shotgun, deals 15 damage.", ["enemy", "characters"]),
                character.Skill("Fortify Position", 2, 'sprites/skills/def.png', character.hos_sigskill2, "Fortifies position, gaining speed for this turn.", ["player", "characters"])]
    
  )
  characterSetup(hos, playerParty)
  
  secoff = character.Character(
    name="Security Officer",
    sprite='sprites/characters/player/secoff.png',
    speed=(3, 6),
    hp=110,
    base_skills=[character.Skill("Baton Strike", 2, 'sprites/skills/skill1.png', character.secoff_baseskill1, "Deals 2 damage with a baton strike. Disorients the enemy by decreasing their speed by 1.", ["enemy", "characters"]),
                 character.Skill("Pepper Spray", 8, 'sprites/skills/skill2.png', character.secoff_baseskill2, "Sprays pepper spray, dealing 8 damage.", ["enemy", "characters"])],
    sig_skills=[character.Skill("Energy Gun", 12, 'sprites/skills/evade.png', character.secoff_sigskill1, "Deals 12 damage with an energy gun.", ["player", "characters"]),
                character.Skill("Expect Attack", 10, 'sprites/skills/def.png', character.secoff_sigskill2, "Prepares to expect an attack, decreasing incoming damage by 10.", ["enemy", "skills"])]
    
  )
  characterSetup(secoff, playerParty)
  
  clown = character.Character(
    name="Clown",
    sprite='sprites/characters/player/clown.png',
    speed=(4, 8),
    hp=90,
    base_skills=[character.Skill("Pie Throw", 3, 'sprites/skills/skill1.png', character.clown_baseskill1, "Throws a pie at the enemy, decreasing speed by 3.", ["all", "characters"]),
                 character.Skill("Vicious Mockery", 10, 'sprites/skills/skill2.png', character.clown_baseskill2, "Mocks the target, dealing 10 sanity damage.", ["all", "characters"])],
    sig_skills=[character.Skill("Laughing Gas", 5, 'sprites/skills/evade.png', character.clown_sigskill1, "Throws a gas bomb, causing various effects.", ["all", "characters"]),
                character.Skill("Lie Down", 20, 'sprites/skills/def.png', character.clown_sigskill2, "Lies down to rest.", ["click", "player"])]
    
  )
  characterSetup(clown, playerParty)
  
  mime = character.Character(
    name="Mime",
    sprite='sprites/characters/player/mime.png',
    speed=(4, 7),
    hp=95,
    base_skills=[character.Skill("Banana Slip", 3, 'sprites/skills/skill1.png', character.mime_baseskill1, "Throws a banana peel to make the enemy slip, decreasing their speed by 3.", ["all", "characters"]),
                 character.Skill("Silent Mockery", 10, 'sprites/skills/skill2.png', character.mime_baseskill2, "Silently mocks the target, dealing 10 sanity damage.", ["all", "characters"])],
    sig_skills=[character.Skill("Silent Strike", 5, 'sprites/skills/evade.png', character.mime_sigskill1, "Silently strikes the enemy, dealing 10 damage.", ["enemy", "characters"]),
                character.Skill("Invisible Wall", 10, 'sprites/skills/def.png', character.mime_sigskill2, "Creates an invisible wall to decrease 10 damage from incoming attack", ["enemy", "skill"])]
  )
  characterSetup(mime, playerParty) 
  
  borg = character.Character(
    name="Mediborg",
    sprite='sprites/characters/player/medicalborg_south.png',
    speed=(3, 5),
    hp=130,
    base_skills=[character.Skill("Medibeam", 8, 'sprites/skills/skill1.png', character.borg_baseskill1, "Heals target organism by 8", ["all", "characters"]),    
                 character.Skill("Hypospray", 5, 'sprites/skills/skill2.png', character.borg_baseskill2, "Uses built in hypospray to inject chemicals. Heals by 5 and increases speed by 1", ["all", "characters"])],
    sig_skills=[character.Skill("Nanite Swarm", 1, 'sprites/skills/evade.png', character.borg_sigskill1, "Swarms the target with nanite bots, disorienting them", ["all", "characters"]),
                character.Skill("Reinforced Plating", 15, 'sprites/skills/def.png', character.borg_sigskill2, "Gets in the way of one of the attacks, which target player was being targeted by.", ["player", "characters"])]
  )
  characterSetup(borg, playerParty)
  
  felinid = character.Character(
    name="Medic",
    sprite='sprites/characters/player/medic.png',
    speed=(4, 6),
    hp=100,
    base_skills=[character.Skill("Physical Hypospray", 8, 'sprites/skills/skill1.png', character.medic_baseskill1, "Uses a physical hypospray to inject chemicals.", ["player", "characters"]),
                 character.Skill("First Aid", 12, 'sprites/skills/skill2.png', character.medic_baseskill2, "Heals target by 12", ["player", "characters"])],    
    sig_skills=[character.Skill("Adrenaline Boost", 2, 'sprites/skills/evade.png', character.medic_sigskill1, "Gives an adrenaline boost, increasing speed by 2.", ["player", "characters"]),
                character.Skill("Electroshock", 10, 'sprites/skills/def.png', character.medic_sigskill2, "Electroshocks the target, dealing 10 damage.", ["player", "skills"])]
    
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
    base_skills=[character.Skill("Splash Attack", 6, 'sprites/skills/skill1.png', character.carp_baseskill1, "Attacks target for 6 damage.", ["player", "characters"]),
                 character.Skill("Prepare", 1, 'sprites/skills/skill2.png', character.carp_baseskill2, "Prepares for an attack, increasing speed by 1.", ["click", "characters"])],
    sig_skills=[character.Skill("Fin Swipe", 8, 'sprites/skills/evade.png', character.carp_sigskill1, "Attacks target for 8 damage.", ["player", "characters"]),
                character.Skill("Evasive Teleport", 8, 'sprites/skills/def.png', character.carp_sigskill2, "Decreases target skill's damage by 8.", ["player", "skills"])]
  )
  characterSetup(carp1, encounterParty1)
  carp2 = character.Character(
    name="Red Space Carp",
    sprite='sprites/characters/encounter/encounter1/carp_red_west.png',
    speed=(2, 5),
    hp=80,
    base_skills=[character.Skill("Splash Attack", 6, 'sprites/skills/skill1.png', character.carp_baseskill1, "Attacks target for 6 damage.", ["player", "characters"]),
                 character.Skill("Prepare", 1, 'sprites/skills/skill2.png', character.carp_baseskill2, "Prepares for an attack, increasing speed by 1.", ["click", "characters"])],
    sig_skills=[character.Skill("Fin Swipe", 8, 'sprites/skills/evade.png', character.carp_sigskill1, "Attacks target for 8 damage.", ["player", "characters"]),
                character.Skill("Evasive Teleport", 8, 'sprites/skills/def.png', character.carp_sigskill2, "Decreases target skill's damage by 8.", ["player", "skills"])]
  )
  characterSetup(carp2, encounterParty1)
  carp3 = character.Character(
    name="Purple Space Carp",
    sprite='sprites/characters/encounter/encounter1/carp_purple_west.png',
    speed=(2, 5),
    hp=80,
    base_skills=[character.Skill("Splash Attack", 6, 'sprites/skills/skill1.png', character.carp_baseskill1, "Attacks target for 6 damage.", ["player", "characters"]),
                 character.Skill("Prepare", 1, 'sprites/skills/skill2.png', character.carp_baseskill2, "Prepares for an attack, increasing speed by 1.", ["click", "characters"])],  
    sig_skills=[character.Skill("Fin Swipe", 8, 'sprites/skills/evade.png', character.carp_sigskill1, "Attacks target for 8 damage.", ["player", "characters"]),
                character.Skill("Evasive Teleport", 8, 'sprites/skills/def.png', character.carp_sigskill2, "Decreases target skill's damage by 8.", ["player", "skills"])]    
  )
  characterSetup(carp3, encounterParty1)
  carp4 = character.Character(
    name="Green Space Carp",
    sprite='sprites/characters/encounter/encounter1/carp_green_west.png',
    speed=(2, 5),
    hp=80,
    base_skills=[character.Skill("Splash Attack", 6, 'sprites/skills/skill1.png', character.carp_baseskill1, "Attacks target for 6 damage.", ["player", "characters"]),
                 character.Skill("Prepare", 1, 'sprites/skills/skill2.png', character.carp_baseskill2, "Prepares for an attack, increasing speed by 1.", ["click", "characters"])],  
    sig_skills=[character.Skill("Fin Swipe", 8, 'sprites/skills/evade.png', character.carp_sigskill1, "Attacks target for 8 damage.", ["player", "characters"]),
                character.Skill("Evasive Teleport", 8, 'sprites/skills/def.png', character.carp_sigskill2, "Decreases target skill's damage by 8.", ["player", "skills"])]    
  )
  characterSetup(carp4, encounterParty1)
  encounter1 = renderer.Encounter(
    name="Encounter1",
    encounterPartyCharacters=encounterParty1,
    encounterPartyPositions=[(1360, 350), (1560, 350), (1360, 600), (1560, 600)],
    playerPartyCharacters=[playerParty[0], playerParty[1], playerParty[2], playerParty[3]],
    playerPartyPositions=[(200, 350), (400, 350), (200, 600), (400, 600)],
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
    hp=200,
    base_skills=[character.Skill("Slice", 20, 'sprites/skills/skill1.png', character.changeling_baseskill1, "Deals 20 damage.", ["player", "characters"]),
                 character.Skill("Slash", 15, 'sprites/skills/skill2.png', character.changeling_baseskill2, "Deals 15 damage and 5 sanity damage.", ["player", "characters"])],
    sig_skills=[character.Skill("Bone Impact", 12, 'sprites/skills/evade.png', character.changeling_sigskill1, "Deals 12 damage, slows target down by 1.", ["player", "skills"]),
                character.Skill("Regeneration", 20, 'sprites/skills/def.png', character.changeling_sigskill2, "Heals by 20.", ["click", "characters"])] 
  )
  characterSetup(changeling, encounterParty2)
  
  
  changeling_human = character.Character(
    name="Cargo Technician",
    sprite='sprites/characters/encounter/encounter2/changeling_human.png',
    speed=(4, 7),
    hp=200,
    base_skills=[character.Skill("Slice", 20, 'sprites/skills/skill1.png', character.changeling_baseskill1, "Deals 20 damage.", ["player", "characters"]),
                 character.Skill("Slash", 15, 'sprites/skills/skill2.png', character.changeling_baseskill2, "Deals 15 damage and 5 sanity damage.", ["player", "characters"])],
    sig_skills=[character.Skill("Bone Impact", 12, 'sprites/skills/evade.png', character.changeling_sigskill1, "Deals 12 damage, slows target down by 1.", ["player", "skills"]),
                character.Skill("Regeneration", 20, 'sprites/skills/def.png', character.changeling_sigskill2, "Heals by 20.", ["click", "characters"])] 
  )
  characterslist.append(changeling_human) # only for novel purposes
  
  traitor = character.Character(
    name="Traitor",
    sprite='sprites/characters/encounter/encounter2/traitor.png', #sprite not ready
    speed=(3, 6),
    hp=150,
    base_skills=[character.Skill("Backstab", 20, 'sprites/skills/skill1.png', character.traitor_baseskill1, "Deals 20 damage.", ["player", "characters"]),
                 character.Skill("Injector", 15, 'sprites/skills/skill2.png', character.traitor_baseskill2, "Injects unknown chemicals, decreasing sanity by 15.", ["player", "characters"])],
    sig_skills=[character.Skill("Double Energy Sword Slash", 30, 'sprites/skills/evade.png', character.traitor_sigskill1, "Slashes an enemy, dealing 30 damage.", ["player", "characters"]),
                character.Skill("Vanish", 15, 'sprites/skills/def.png', character.traitor_sigskill2, "Vanishes to heal by 15.", ["click", "characters"])]
    
  )
  characterSetup(traitor, encounterParty2)
  encounter2 = renderer.Encounter(
    name="Encounter2",
    encounterPartyCharacters=encounterParty2,
    encounterPartyPositions=[(990, 450), (1305, 450)],
    playerPartyCharacters=[playerParty[0], playerParty[1], playerParty[2], playerParty[3]],
    playerPartyPositions=[(242, 350), (455, 350), (242, 600), (455, 600)],
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
    base_skills=[character.Skill("Lunar Strike", 15, 'sprites/skills/skill1.png', character.heretic_baseskill1, "Deals 15 physical and sanity damage", ["player", "characters"]),
                 character.Skill("Gravity Well", 20, 'sprites/skills/skill2.png', character.heretic_baseskill2, "Restores 20 sanity and health", ["enemy", "characters"])],
    sig_skills=[character.Skill("Lunacy", 25, 'sprites/skills/evade.png', character.heretic_sigskill1, "Deals 25 physical and sanity damage", ["player", "characters"]),
                character.Skill("Eclipse Shield", 15, 'sprites/skills/def.png', character.heretic_sigskill2, "Removes 15 damage from incoming attacks and heals 15 sanity.", ["player", "skills"])]
    
  )
  characterSetup(heretic, encounterParty3)
  encounter3 = renderer.Encounter(
    name="Encounter3",
    encounterPartyCharacters=encounterParty3,
    encounterPartyPositions=[(1075, 565)],
    playerPartyCharacters=[playerParty[0], playerParty[1], playerParty[2], playerParty[3]],
    playerPartyPositions=[(410, 410), (600, 410), (410, 660), (600, 660)],
    combatBGimage='sprites/backgrounds/encounter_3.png'
  )
  #endregion
  
  #region ENCOUNTER 4
  # dragon # SPRITE SIZE INCREASE
  encounterParty4 = []
  spacedragon = character.Character(
    name="Space Dragon",
    sprite='sprites/characters/encounter/encounter4/spacedragon.png',
    speed=(4, 8),
    hp=150,
    base_skills=[character.Skill("Cosmic Breath", 20, 'sprites/skills/skill1.png', character.dragon_baseskill1, "Deals 20  damage", ["player", "characters"]),
                 character.Skill("Tail Swipe", 25, 'sprites/skills/skill2.png', character.dragon_baseskill2, "Deals 25 damage", ["player", "characters"])],
    sig_skills=[character.Skill("Starfall", 30, 'sprites/skills/evade.png', character.dragon_sigskill1, "Deals 30 damage", ["player", "characters"]),
                character.Skill("Galactic Roar", 35, 'sprites/skills/def.png', character.dragon_sigskill2, "Deals 35 damage", ["player", "characters"])]
    
  )
  characterSetup(spacedragon, encounterParty4)
  encounter4 = renderer.Encounter(
    name="Encounter4",
    encounterPartyCharacters=encounterParty4,
    encounterPartyPositions=[(1000, 280)],
    playerPartyCharacters=[playerParty[0], playerParty[1], playerParty[2], playerParty[3]],
    playerPartyPositions=[(250, 300), (430, 300), (250, 550), (430, 550)],
    combatBGimage='sprites/backgrounds/encounter_4.png'
  )
  # nukies
  
  #endregion

  encounters = [encounter1, encounter2, encounter3, encounter4]
  renderer.spriteListInitialize(characterslist, encounters)
  renderer.skillSpriteInitialize(skillslist)
  return
#endregion

def advanceEncounter(): # needs to run at combat end!
  global current_encounter, playerParty
  if(current_encounter == 1):
    playerParty.remove(playerParty[1]) # remove unknown
    renderer.barCharacterPositions.remove(renderer.barCharacterPositions[7])
  current_encounter += 1
  return
def advanceDialogue():
  global current_dialogue_line
  if(current_dialogue_line < len(novelList[current_novel][0][1]) - 1):
    current_dialogue_line += 1 
  else:
    advanceNovel()
  return
def advanceNovel():
  global current_novel, current_dialogue_line
  advanceEncounter()
  renderer.AdvanceGameState("partyselect")
  current_novel += 1
  current_dialogue_line = 0
  if(current_novel >= len(novelList)):
    pygame.QUIT()
  return

def FindCharacterByName(name):
  global characterslist
  # first words until ':' are the name of the character speaking
  name = name.split(":", 1)[0]

  for char in characterslist:
    if char.name == name:
      return char



def main():
  initializeGame()
  running = True
  renderer.initializePlayerCharacters(playerParty)

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
          partyPositions, skillPositions = renderer.CombatSpriteTransformCalculation(encounters[current_encounter - 1])
          renderer.ClickEvent("combat", partyPositions, skillPositions, playerParty, encounters[current_encounter - 1].encounterPartyCharacters)
        if(gamestate == "novel"):
          renderer.ClickEvent("novel", [], [], playerParty, [])
          advanceDialogue()
        continue
    if gamestate == "combat":
      encounters[current_encounter - 1].playerPartyCharacters = currentParty
      renderer.RenderCombatScene(encounters[current_encounter - 1])
    elif gamestate == "partyselect":
      renderer.RenderPartySelecter(playerParty)
    elif gamestate == "novel":
      # get story file and render accordingly
      renderer.RenderNovelScene(FindCharacterByName(novelList[current_novel][0][1][current_dialogue_line]), novelList[current_novel][0][1][current_dialogue_line])
    clock.tick(FPS)  # Limit to 60 frames per second
  return
  
main()
