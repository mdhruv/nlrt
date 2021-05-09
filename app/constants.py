Classes = ["Warrior", "Druid", "Rogue", "Hunter", "Mage", "Warlock", "Paladin", "Priest", "Shaman"]
Roles = ["Tank", "Melee DPS", "Ranged DPS", "Healer",]
Professions = ["None", "Tailoring", "Leathworking", "Blacksmithing", "Enchanting", "Alchemy", "Herbalist", "Mining", "Skinning", "Engineering", "Jewelcrafting"]
ParseMap = dict(list(map(lambda x: (x.lower(), x), Roles)) \
    + list(map(lambda x: (x.lower(), x), Classes)) \
    + list(map(lambda x: (x.lower(), x), Professions)) \
    + [("cooking", "Cooking"), \
    ("firstaid", "First Aid"), \
    ("fishing", "Fishing"), \
    ("raidleader", "Raid Leader"), \
    ("melee", "Melee DPS"), \
    ("ranged", "Ranged DPS")])