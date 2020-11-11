import os
import random
from Content import activateContent

print("Welcome to Urgovaan")
print("Alpha Patch 0.2.5.5: Skills and banking! (and bugfixes!) (and more custom content support!)")
print("Type 'help' to see commands")
wanderLevel = 0
inTown = True
inShop = False
surroundings = []
surroundingsStats = []
loot = []

#NPC
npcTable = ["Rat", "Boar", "Orc", "Large Boar"]
npcBase = [[17, 10, 5], [32, 30, 8], [50, 20, 10], [50, 35, 12]]
npcDropTable = [[2, 1, 3], [2, 2, 50], [3, 12, 30], [1, 12, 15]]

#Items
itemTable = [["Nothing", 0, 0, 0, 0, 0,], ["Wooden Club", 2, 10, 3, 0, 0,], ["Orc Tusk", 0, 5, 0, 0, 0,], ["Spiked Wooden Club", 2, 50, 5, 0, 0,], ["Rough Leather Vest", 4, 30, 0, 0, 3,], ["Minor Healing Potion", 1, 15, 30, 0, 0,], ["Wool Cap", 3, 15, 0, 0, 1,], ["Torn Leather Pants", 5, 20, 0, 0, 2,], ["Leather Boots", 6, 15, 0, 0, 1,], ["Pickaxe", 0, 30, 0, 0, 0,], ["Copper Ore", 0, 20, 0, 0, 0], ["Iron Ore", 0, 40, 0, 0, 0], ["Boar Hide", 0, 5, 0, 0, 0], ["Copper Bar", 0, 60, 0, 0, 0], ["Iron Bar", 0, 120, 0, 0, 0], ["Leather", 0, 10, 0, 0, 0], ["Copper Shortsword", 2, 40, 7, 0, 0,], ["Copper Longsword", 2, 60, 9, 0, 0,]]
shopTable = [1, 3, 4, 5, 6, 7, 8, 9]
shopStock = [3, 1, 6, 5, 5, 1, 3, 4, 3, 9]
bankStored = []

#Skill stuff
ores = []
oreTable = [["Copper Ore", 0, 7, 9], ["Iron Ore", 2, 18, 9]]
barTable = [["Copper Bar", 14], ["Iron Bar", 36]]
craftingTable = [["Copper Shortsword", 0, 20, 13, 13, 13, 15], ["Copper Longsword", 3, 20, 13, 13, 13, 13, 13, 15]] #Item, levelreq, xp
tanAbles = [["Boar Hide", 3]] #Items which you can tan into leather & required amount
#return(npcTable, npcBase, npcDropTable, itemTable, shopTable, oreTable, barTable, craftingTable, tanAbles)
modValues = activateContent()
if modValues != False:
 i = 0
 npcTable = modValues[i]; i += 1
 npcBase = modValues[i]; i += 1
 npcDropTable = modValues[i]; i += 1
 itemTable = modValues[i]; i += 1
 shopTable = modValues[i]; i += 1
 shopStock = modValues[i]; i += 1
 oreTable = modValues[i]; i += 1
 barTable = modValues[i]; i += 1
 craftingTable = modValues[i]; i += 1
 tanAbles = modValues[i]
 
#Name, type, value, str, agi, stam
#Types:
#0 = Vendor
#1 = Consumable
#2 = Weapon
#3 = Head
#4 = Chest
#5 = Legs
#6 = Feet

#Player Stats
pGear = [0, 0, 0, 0, 0]
pHealth = 0
pMaxHealth = 0
pDamage = 0
pMoney = 0
pLevel = [1, 0, 30]
pAttributes = [5, 5, 5] #Strength, Agility, Stamina
pGearAttributes = [0, 0, 0]
pBag = [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pSkills = [[1, 0, 30], [1, 0, 30], [1, 0, 30]] #Magic, Crafting, Mining

def selectAorAn(letter):
 an = "eaoiu"
 for x in an:
  if letter.lower() == x: return "an"
 return "a"

def getStatsFromItem(item):
 global itemTable
 return (itemTable[item][3], itemTable[item][4], itemTable[item][5])

def initStats():
 global pHealth, pMaxHealth, pDamage, pAttributes, pGear, pGearAttributes
 pGearAttributes = [0, 0, 0]
 pMaxHealth = 50
 pMaxHealth += pAttributes[2] * 10
 pDamage = pAttributes[0] * 3
 for i in pGear: result = getStatsFromItem(i); pGearAttributes[0] += result[0]; pGearAttributes[1] += result[1]; pGearAttributes[2] += result[2]   
 pMaxHealth += pGearAttributes[2] * 10
 pDamage += pGearAttributes[0] * 3

def wander():
 global wanderLevel, surroundings, surroundingsStats, inTown, loot, npcTable, ores
 loot = []
 ores = []
 if inTown: print("You wander into the forest"); inTown = False
 else:
  if len(surroundings) > 0: print("You can't wander further while surrounded by enemies"); return
  print("You wander further into the forest")
  print("You feel the danger increase")
 if random.randint(0, 7) == 1:
  print("While wandering the wilderness, you stumble upon a mine. Enter/Pass")
  mineStumble()
  return
 surroundings = []
 surroundingsStats = []

 rng = random.randint(1, 3)
 
 for i in range(0, rng):
  i = i
  rng2 = random.randint(wanderLevel, wanderLevel + 2)
  surroundings.append(rng2)
  surroundingsStats.append(npcBase[rng2][0])

 if ((wanderLevel + 1) < len(npcTable) - 2): wanderLevel += 1

def translateSurroundings():
 global surroundings, npcTable, surroundingsStats
 if len(surroundings) == 0: return "No hostile creatures"
 returnString = ""
 for i in range(0, len(surroundings)):
  returnString += selectAorAn(npcTable[surroundings[i]][0]) + " "
  returnString += (npcTable[surroundings[i]] + "(" + str(surroundingsStats[i]) + "), ")
 return returnString
 
def translateTarget(target):
 global npcTable
 for i in range(0, len(npcTable)):
  if npcTable[i].lower() == target.lower(): return(i)
  
def look():
 global surroundings, loot, ores
 print("You look around and see:")
 print(translateSurroundings())
 if len(ores) > 0:
  result = ""
  for i in ores: result += i + ", "
  print(result)
 if len(loot) > 0:
  print("On the ground you see:")
  result = ""
  for i in loot: result += i + ", "
  print(result)
 
def checkTarget(target):
 global surroundings
 found = False
 for i in surroundings:
  if i == target: found = True
 return found
 
def playerKilled():
 print("Oh dear! You are dead!")

def addAttribute():
 global pAttributes
 print("Choose an attribute to add 1 point to")
 print("Strength | Agility | Stamina")
 cmd = input()
 if cmd.lower() == "strength": pAttributes[0] += 1; print("1 point added to " + cmd.lower()); initStats(); return
 if cmd.lower() == "agility": pAttributes[1] += 1; print("1 point added to " + cmd.lower()); initStats(); return
 if cmd.lower() == "stamina": pAttributes[2] += 1; print("1 point added to " + cmd.lower()); initStats(); return
 print(str(cmd) + " is not a valid input"); addAttribute()

def playerLeveled():
  global pLevel, pHealth, pMaxHealth, pDamage
  pLevel[0] += 1
  pLevel[1] = 0
  pLevel[2] *= 1.4
  pLevel[2] = int(pLevel[2])
  pHealth = pMaxHealth
  print("You have leveled up!")
  print("You are now level " + str(pLevel[0]))
  generateShopStock()
  addAttribute()

def targetKilled(target, id, pos):
 global pHealth, pDamage, surroundingsStats, npcBase, surroundings, pLevel, pMoney
 print("You kill the " + target)
 pLevel[1] += npcBase[id][2]
 goldreward = npcBase[id][2] / 2
 pMoney += int(goldreward)
 print("You receive " + str(npcBase[id][2]) + "xp and " + str(int(goldreward)) + " gold")
 npcDropItem(id)
 if pLevel[1] >= pLevel[2]: playerLeveled()
 surroundingsStats.pop(pos)
 surroundings.pop(pos)

def attack(target):
 global pHealth, pDamage, surroundingsStats, npcBase, surroundings, pAttributes, pGearAttributes
 id = translateTarget(target)
 pos = 0
 damage = pDamage
 agi = pAttributes[1]
 agi += pGearAttributes[1]
 if random.randint(0, 100) < agi: damage *= 1.5; damage = int(damage); print ("Critical hit!")
 for i in range(0, len(surroundings)):
   if surroundings[i] == id: pos = i; break
 if (checkTarget(id)):
  surroundingsStats[i] -= damage
  print("You attack the " + target.lower() + " for " + str(damage) + " health")
  if surroundingsStats[i] <= 0: targetKilled(target, id, pos); return
  if random.randint(0, 100) < agi: print("You dodge the " + target.lower() + "'s attack")
  else: pHealth -= npcBase[id][1]; print("The " + target.lower() + " hits you for " + str(npcBase[id][1]) + " health")
  if pHealth <= 0: playerKilled()
 else: print("There are no " + target.lower() + "s around")
 
def stats():
  global pHealth, pDamage, pMaxHealth, pLevel, pAttributes, pGearAttributes, pSkills
  print("Level: " + str(pLevel[0]))
  print("XP: " + str(pLevel[1]) + "/" + str(pLevel[2]))
  print("Health: " + str(pHealth) + "/" + str(pMaxHealth))
  print("Damage: " + str(pDamage))
  print("---Attributes---")
  print("Strength: " + str(pAttributes[0]) + " (+" + str(pGearAttributes[0]) + ")")
  print("Agility: " + str(pAttributes[1]) + " (+" + str(pGearAttributes[1]) + ")")
  print("Stamina: " + str(pAttributes[2]) + " (+" + str(pGearAttributes[2]) + ")")
  print("---Skills---")
  print("Magic: " + str(pSkills[0][0]) + " (" + str(pSkills[0][1]) + "/" + str(pSkills[0][2]) + ")")
  print("Crafting: " + str(pSkills[1][0]) + " (" + str(pSkills[1][1]) + "/" + str(pSkills[1][2]) + ")")
  print("Mining: " + str(pSkills[2][0]) + " (" + str(pSkills[2][1]) + "/" + str(pSkills[2][2]) + ")")

def goTown():
 global wanderLevel, surroundings, surroundingsStats, inTown, loot, ores
 loot = []
 surroundings = []
 surroundingsStats = []
 ores = []
 wanderLevel = 0

 inTown = True
 print("You wander to the town")
 print("Here you can 'rest', wander to the 'shop', 'smelt' your ores into bars, 'tan' your hides into leather, or store your items at the 'bank'")

def rest():
 global inTown, pHealth, pMaxHealth
 if inTown: print("You rest until you feel healthy again"); pHealth = pMaxHealth
 else: print("You can only rest in town")

def getBag():
 global pBag, itemTable
 result = ""
 for i in pBag:
  if (i > 0): result += itemTable[i][0] + ", "
 if result == "": result = "Your bag is empty"
 return(result)

def getItem(item): #Gets itemTable index from string
 global pBag, itemTable
 for i in range(0, len(itemTable)): 
   if item.lower() == itemTable[i][0].lower(): return(itemTable[i], i)
 return("None")

def buyItem(item):
  global pBag, itemTable, shopStock, pMoney
  item = getItem(item)
  if item == "None": return("You do not have this item")
  price = item[0][2] * 3
  #Check if item in stock, check if you can afford, check if bag is full, if not buy
  for i in range(0, len(shopStock)):
    if shopStock[i] == item[1]:
     if pMoney >= price:
       for x in range(0, len(pBag)):
         if pBag[x] == 0: pBag[x] = item[1]; pMoney -= price; shopStock.pop(i); return("Bought " + item[0][0] + " for " + str(price) + " gold")
       return("Your bag is full")
     else: return("You can't afford this")
  return("The shop does not have any " + str(item[0][0]) + " in stock")

def sellItem(item):
  global pBag, itemTable, shopStock, pMoney
  item = getItem(item)
  if item == "None": return("You do not have this item")
  for i in range(0, len(pBag)):
   if pBag[i] == item[1]: pBag[i] = 0; pMoney += item[0][2]; shopStock.append(item[1]); return("Sold " + item[0][0] + " for " + str(item[0][2]) + " gold")
  return("You do not have " + selectAorAn(item[0][0][0]) + " " + item[0][0])

def lootItem(item):
  global pBag, itemTable, loot
  if item == "": return("You can't loot nothing")
  for i in range(0, len(loot)):
   if loot[i].lower() == item.lower():
    for x in range(0, len(pBag)):
      if pBag[x] == 0:
       for y in range(0, len(itemTable)):
         if itemTable[y][0].lower() == item.lower(): pBag[x] = y; loot.pop(i); return("Looted " + itemTable[y][0])
    return("Your bag is full")
  return("There are no " + item.lower() + "s around")

def examineItemShop(item):
 global pBag, shopStock
 if item == "": return("You can't examine nothing")
 item = str(item)
 types = ["Commodity", "Consumeable", "Weapon", "Head", "Chest", "Legs", "Feet"]
 result = (getItem(item))
 for i in shopStock:
  if i == result[1]:
   print("Name: " + result[0][0])
   print("Type: " + types[result[0][1]])
   print("Price: " + str(result[0][2] * 3))
   if result[0][1] > 1:
    print("Strength: " + str(result[0][3]))
    print("Agility: " + str(result[0][4]))
    print("Stamina: " + str(result[0][5])) 
   return
 print("The shop doesn't have " + selectAorAn(item[0]) + " " + item) 

def examineItemBank(item):
 global pBag, shopStock, bankStored
 if item == "": return("You can't examine nothing")
 item = str(item) 
 types = ["Commodity", "Consumeable", "Weapon", "Head", "Chest", "Legs", "Feet"]
 result = (getItem(item))
 for i in pBag:
  if i == result[1]:
   print("Name: " + result[0][0])
   print("Type: " + types[result[0][1]])
   print("Value: " + str(result[0][2]))
   if result[0][1] > 1:
    print("Strength: " + str(result[0][3]))
    print("Agility: " + str(result[0][4]))
    print("Stamina: " + str(result[0][5])) 
   return
 for i in bankStored:
  if i == result[0][0]:
   print("Name: " + result[0][0])
   print("Type: " + types[result[0][1]])
   print("Value: " + str(result[0][2]))
   if result[0][1] > 1:
    print("Strength: " + str(result[0][3]))
    print("Agility: " + str(result[0][4]))
    print("Stamina: " + str(result[0][5])) 
   return   
 print("You do not have " + selectAorAn(item[0]) + " " + item) 
def examineItem(item):
 global pBag
 types = ["Commodity", "Consumeable", "Weapon", "Head", "Chest", "Legs", "Feet"]
 result = (getItem(item))
 for i in pBag:
  if i == result[1]:
   print("Name: " + result[0][0])
   print("Type: " + types[result[0][1]])
   print("Value: " + str(result[0][2]))
   if result[0][1] > 1:
    print("Strength: " + str(result[0][3]))
    print("Agility: " + str(result[0][4]))
    print("Stamina: " + str(result[0][5])) 
   return
 print("You don't have " + selectAorAn(item[0]) + " " + item) 

def equipItem(item):
 global pBag, pGear
 result = (getItem(item))
 for i in range(0, len(pBag)):
  if pBag[i] == result[1]:
   temp = 0
   if result[0][1] < 1: print("You can't equip this"); return
   else: temp = pGear[(result[0][1] - 2)]; pGear[(result[0][1] - 2)] = result[1]; pBag[i] = temp
   print("Equipped " + result[0][0])
   initStats()
   return
 print("You don't have " + selectAorAn(item[0]) + " " + item)

def npcDropItem(id):
 global npcDropTable, pBag, itemTable, loot
 #npcDropTable = [[0, 1, 3], [0, 2, 50]]
 for i in npcDropTable:
  if i[0] == id:
    if (random.randint(0, 100) <= i[2]): print("Dropped " + itemTable[i[1]][0]); loot.append(itemTable[i[1]][0])

def printGear():
 global pGear, itemTable
 slot = ["Weapon: ", "Head: ", "Chest: ", "Legs: ", "Boots: "]
 for i in range(0, len(pGear)):
  print(slot[i] + itemTable[pGear[i]][0])

def printHelp():
 print("Commands")
 print("Available anywhere (excluding shop and bank) : wander, look, stats, bag, examine, loot, drop, equip, equipment, gold, craft, recipes")
 print("Available in wilderness: attack, town, loot")
 print("Available in town: rest, shop, smelt, tan")
 print("Available in shop: bag, examine, gold, buy, sell, leave")
 print("Available in bank: bag, examine, gold, deposit, withdraw, leave")
 print("Available in mine: mine")

def generateShopStock():
 global shopStock, shopTable
 shopStock = []
 for i in range(0, 10): shopStock.append(random.choice(shopTable)); i = i

def goShop():
 global inTown
 if not inTown: print("You're not in town"); return
 else: print("Welcome to the shop, what would you like to look at? (General, Weapons, Armor)"); print("Examine, Buy, Sell, Leave"); playerInShop()

def playerInShop():
 global itemTable, shopStock
 cmd = input()
 cmdsplit = cmd.split()

 if cmd == "": playerInShop()
 #lord forgive me for the lazy copy paste
 if cmdsplit[0].lower() == "examine":
  result = ""
  for i in range(1, len(cmdsplit)):
    result += cmdsplit[i]
    if i != (len(cmdsplit) - 1): result += " "
  examineItemShop(result)

 if cmdsplit[0].lower() == "sell":
  result = ""
  for i in range(1, len(cmdsplit)):
    result += cmdsplit[i]
    if i != (len(cmdsplit) - 1): result += " "
  print(sellItem(result))

 if cmdsplit[0].lower() == "buy":
  result = ""
  for i in range(1, len(cmdsplit)):
    result += cmdsplit[i]
    if i != (len(cmdsplit) - 1): result += " "
  print(buyItem(result))

 if cmd.lower() == ("general"): 
  result = ""
  for x in shopStock:
   if itemTable[x][1] < 2: result += itemTable[x][0] + ", "
  if result == "": result = ("There are no " + cmd.lower() + " items in stock")
  print(result)
  print("Examine, Buy, Sell, Leave")

 if cmd.lower() == ("weapons"): 
  result = ""
  for x in shopStock:
   if itemTable[x][1] == 2: result += itemTable[x][0] + ", "
  if result == "": result = ("There are no " + cmd.lower() + " items in stock")
  print(result)
  print("Examine, Buy, Sell, Leave")

 if cmd.lower() == ("armor"): 
  result = ""
  for x in shopStock:
   if itemTable[x][1] > 2: result += itemTable[x][0] + ", "
  if result == "": result = ("There are no " + cmd.lower() + " items in stock")
  print(result)
  print("Examine, Buy, Sell, Leave")

 if cmd.lower() == "help": printHelp()
 if cmd.lower() == "bag": print(getBag())
 if cmd.lower() == "gold": print("You have " + str(pMoney) + " gold")
 if cmd.lower() == "leave": print("You have left the shop"); return()
 playerInShop()

def dropItem(item):
 global pBag, loot, itemTable 
 input = item
 item = getItem(item)
 #(['Orc Tusk', 0, 5, 0, 0, 0], 2)
 for i in range(0, len(pBag)):
  if pBag[i] == item[1]: pBag[i] = 0; loot.append(item[0][0]); return("Dropped " + item[0][0])
 return("You do not have " + selectAorAn(input[0]) + " " + input)

def drinkPotion(item):
 global pBag, loot, itemTable, pHealth, pMaxHealth
 input = item
 item = getItem(item)
 for i in range(0, len(pBag)):
  if pBag[i] == item[1]:
   if item[0][1] != 1: return("You can't drink this!") 
   pBag[i] = 0; pHealth += item[0][3]
   if pHealth > pMaxHealth: pHealth = pMaxHealth
   return("Drank " + selectAorAn(item[0][0][0]) + " " + item[0][0])
 return("You do not have " + selectAorAn(input[0]) + " " + input)

def addItem(id):
 global pBag
 for i in range(0, len(pBag)):
  if pBag[i] == 0: pBag[i] = id; return True
 else: return False

def checkBag():
 global pBag
 for x in pBag:
  if x == 0: return True
 else: return False

def addSkillXp(skill, amount):
 global pSkills
 pSkills[skill][1] += amount
 skillName = ["Magic", "Crafting", "Mining"]
 if pSkills[skill][1] >= pSkills[skill][2]: pSkills[skill][1] = 0; pSkills[skill][0] += 1; newxp = (pSkills[skill][2] * 1.4); pSkills[skill][2] = int(newxp); print("Your " + str(skillName[skill]) + " level is now " + str(pSkills[skill][0]))

def mineOre(ore):
 global pBag, itemTable, ores, oreTable, pSkills, surroundings
 if ore == "": return("You can't mine nothing")
 item = getItem(ore)
 pickaxe = 0
 pickaxeStr = ""
 for x in oreTable:
  if ore.lower() == x[0].lower(): pickaxe = x[3]; pickaxeStr = itemTable[pickaxe]
 hasPick = False
 #Check if any ore is around
 if len(ores) == 0: print("There is no ore around"); return
 #Check if player has pickaxe
 for x in pBag: 
  if x == pickaxe: hasPick = True
 if hasPick == False: print("You need " + selectAorAn(pickaxeStr[0][0]) + " " + pickaxeStr[0] + " to mine this"); return
 levelReq = 0
 xpReward = 0
 mineAmount = 1
 for x in oreTable:
  if x[0].lower() == ore.lower(): levelReq = x[1]; xpReward = x[2]
 for i in range(0, len(ores)): 
  if ores[i].lower() == ore.lower():
   if pSkills[2][0] >= levelReq:
    if addItem(item[1]): temp = ores[i]; ores.pop(i); print("Mined " + str(mineAmount) + " " + temp); addSkillXp(2, xpReward); return
    else: print("Your bag is full"); return
   else: print("You need to be level " + str(levelReq) + " to mine this"); return
 print("There is no " + ore + " around")
#38262313417158783521

def tanHide(hide):
 global itemTable, tanAbles, pBag
 if hide == "": return("You can't tan nothing")
 item = getItem(hide)
 leather = getItem("leather")
 reqAmount = 0
 hasAmount = 0
 if item == "None": return("You do not have this item")
 for x in tanAbles:
  if x[0].lower() == item[0][0].lower():
   reqAmount = x[1]
   #Check if player has req amount
   for i in pBag:
    if i == item[1]: hasAmount += 1
   if hasAmount < reqAmount: return("You need " + str(reqAmount) + " " + item[0][0] + " to tan it into leather")
   else: hasAmount = reqAmount
   for i in range(0, len(pBag)):
    if pBag[i] == item[1]:
     if hasAmount > 0: pBag[i] = 0; hasAmount -= 1
   addItem(leather[1])
   return("Tanned " + str(reqAmount) + " " + item[0][0] + " into 1 leather")
  return("You can't tan this")

def enterMine():
 global ores, wanderLevel, oreTable, surroundings
 print("You enter the mine")
 #Find suitable ore for wanderLevel
 suitableOre = "" 
 for i in range(0, len(oreTable)):
  if oreTable[i][1] > wanderLevel: suitableOre = oreTable[i - 1][0]; break
 for i in range(0, random.randint(1, 5)): ores.append(suitableOre)

def mineStumble():
 cmd = input()
 if cmd.lower() == "enter": enterMine(); return
 if cmd.lower() == "pass": wander(); return
 mineStumble()

def smeltOre(ore):
 global inTown, pBag, oreTable, barTable
 if not inTown: print("You're not in town"); return
 oreCount = 0
 oreIndex = 0
 if ore == "": return("You can't smelt nothing")
 #Check if ore exists, check if player has 3 of them
 if getItem(ore) == "None": return("You do not have " + selectAorAn(ore[0]) + " " + ore)
 #Get ore/bar index
 else: item = getItem(ore)
 for i in range(0, len(oreTable)):
  if oreTable[i][0].lower() == ore: oreIndex = i
 toAdd = (barTable[oreIndex][0])
 toAddInt = (getItem(toAdd)[1])
 for x in pBag:
  if x == item[1]: oreCount += 1
 if oreCount >= 3:
  oreCount = 3
  for i in range(0, len(pBag)):
   if pBag[i] == item[1]:
    if oreCount > 0: pBag[i] = 0; oreCount -= 1
  addItem(toAddInt)
  addSkillXp(1, barTable[oreIndex][1])
  return("Smelted 3 " + item[0][0] + " into " + selectAorAn(ore[0])  + " " + (barTable[oreIndex][0]))
 else: return("You need at least 3 " + item[0][0] + " to smelt")
 
def printItems():
 global itemTable
 for i in range(0, len(itemTable)): print(str(itemTable[i]) + " | " + str(i))

def depositItem(item):
 global pBag, bankStored
 if item == "": return("You can't deposit nothing")
 item = getItem(item)
 if item == "None": return("You do not have this item")
 for i in range(0, len(pBag)):
  if pBag[i] == item[1]: pBag[i] = 0; bankStored.append(item[0][0]); return("Deposited " + item[0][0])
 return("You do not have " + selectAorAn(item[0][0][0]) + " " + item[0][0])

def withdrawItem(item):
 global pBag, bankStored
 if item == "": return("You can't withdraw nothing")
 item = str(item)
 bankIndex = 696969
 bagIndex = 696969
 for i in range(0, len(bankStored)):
  if bankStored[i].lower() == item.lower(): bankIndex = i; break
 if bankIndex == 696969: return("You do not have this stored in the bank")
 for i in range(0, len(pBag)):
  if pBag[i] == 0: bagIndex = i; break
 if bagIndex == 696969: return("Your bag is full")
 item = getItem(item)
 addItem(item[1]); bankStored.pop(bankIndex); return("You withdraw " + selectAorAn(item[0][0][0]) + " " + item[0][0] + " from your storage")

def inBank():
 global pBag, itemTable, bankStored
 cmd = input()
 cmdsplit = cmd.split()
 if cmd.lower() == "view":
  result = ""
  for x in bankStored: result += (x + ", ")
  if result == "": print("You have nothing stored in the bank")
  else: print(result)
 if cmdsplit[0].lower() == "deposit":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   print(depositItem(result)) 
 if cmdsplit[0].lower() == "withdraw":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   print(withdrawItem(result)) 
 if cmdsplit[0].lower() == "examine":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   examineItemBank(result)
 if cmd.lower() == "leave": print("You have left the bank"); return
 if cmd.lower() == "help": printHelp()
 if cmd.lower() == "bag": print(getBag())
 if cmd.lower() == "gold": print("You have " + str(pMoney) + " gold")
 inBank()

def goBank():
 global inTown
 if inTown: print("You have entered the bank"); print("Examine, Deposit, Withdraw, View, Leave"); inBank()
 else: print("You're not in town")

def printRecipes():
 global craftingTable; pSkills, itemTable
 for x in craftingTable:
  result = ""
  if x[1] <= pSkills[1][0]:
   result += x[0] + " | "
   for i in range(3, len(x)):
    toCheck = x[i]
    result += itemTable[toCheck][0] + ", "
   print(result)

def craftItem(item):
 global craftingTable, pBag, pSkills
 #[["Copper Shortsword", 0, 20, 13, 13, 13, 15]]
 #sorry i was drunk when making this
 mats =  []
 matsFixed = []
 levelReq = 0
 xpReward = 0
 found = False
 for x in craftingTable:
  if x[0].lower() == item.lower(): levelReq = x[1]; xpReward = x[2]; found = True
 if not found: return("You can't craft this")
 if levelReq > pSkills[1][0]: return("Your crafting level is too low")
 if item == "": return("You can't craft nothing")
 toAdd = getItem(item)
 if toAdd == "None": return("You can't craft this")
 #Add mats to mats list
 for x in craftingTable:
  if x[0].lower() == item.lower():
   for i in range(3, len(x)):
    mats.append(x[i])
 #Sort into easier format to work with
 for x in mats:
  showsUp = 0
  append = True
  for y in mats:
   if x == y: showsUp += 1
  for i in matsFixed: 
   if i[0] == x: append = False
  if append: matsFixed.append((x, showsUp))
 #Check if player has the materials
 for x in matsFixed:
  hasCount = 0
  for y in pBag:
   if x[0] == y: hasCount += 1
  if hasCount < x[1]: return("You do not have the materials required to craft this")
 for x in range(0, len(matsFixed)):
  toTake = matsFixed[x][1]
  for y in range(0, len(pBag)):
   if pBag[y] == matsFixed[x][0]: 
    if toTake > 0: pBag[y] = 0; toTake -= 1 
 addItem(toAdd[1]); addSkillXp(1, xpReward);  return("You have crafted " + selectAorAn(toAdd[0][0]) +  " " + toAdd[0][0])

def lootAll():
 global pBag, loot
 lootCount = 0
 if len(loot) == 0: print("There is nothing to loot"); return
 for x in range(0, len(loot)):
  item = getItem(loot[x])
  if(addItem(item[1])): print("Looted " + loot[x]); lootCount += 1
  else: print("Your bag is full"); break
 for i in range(0, lootCount): loot.pop(0); i = i

def getCommand():
 global pHealth, pMoney, inShop
 cmd = input()
 cmdsplit = cmd.split()
 if cmd == "": getCommand()
 if (pHealth <= 0): print("Dead people can't " + cmd); return
 if cmd.lower() == "wander": wander()
 if cmd.lower() == "look": look()
 if cmd.lower() == "stats": stats()
 if cmd.lower() == "town": goTown()
 if cmd.lower() == "rest": rest()
 if cmd.lower() == "bag": print(getBag())
 if cmd.lower() == "equipment": printGear()
 if cmd.lower() == "help": printHelp()
 if cmd.lower() == "gold": print("You have " + str(pMoney) + " gold")
 if cmd.lower() == "shop": goShop()
 if cmd.lower() == "bank": goBank()
 if cmd.lower() == "loot": lootAll()
 if cmd.lower() == "recipes": printRecipes()
 if cmdsplit[0].lower() == "examine":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "
   examineItem(result)
 if cmdsplit[0].lower() == "equip":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "
   equipItem(result)
 if cmdsplit[0].lower() == "drop":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   print(dropItem(result)) 
 if cmdsplit[0].lower() == "drink":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   print(drinkPotion(result))         
 if cmdsplit[0].lower() == "loot":
   result = ""
   if len(cmdsplit) == 1: getCommand()
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   print(lootItem(result))  
 if cmdsplit[0].lower() == "mine":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   mineOre(result)   
 if cmdsplit[0].lower() == "smelt":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   print(smeltOre(result))   
 if cmdsplit[0].lower() == "tan":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   print(tanHide(result))  
 if cmdsplit[0].lower() == "craft":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   print(craftItem(result)) 
 if cmdsplit[0].lower() == "attack":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " " 
   if len(cmdsplit) == 1: print("No target selected"); getCommand()    
   attack(result) 
 getCommand()
 
initStats()
pHealth = pMaxHealth
getCommand()