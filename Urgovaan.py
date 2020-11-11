import random

wanderLevel = 0
inTown = True
inShop = False
surroundings = []
surroundingsStats = []
loot = []

#NPC
npcTable = ["Orc", "Boar", "Rat"]
npcBase = [[50, 20, 10], [32, 30, 8], [17, 10, 5]]
npcDropTable = [[0, 1, 3], [0, 2, 50]]

#Items
itemTable = [["Nothing", 0, 0, 0, 0, 0,], ["Wooden Club", 2, 10, 3, 0, 0,], ["Orc Tusk", 0, 5, 0, 0, 0,], ["Spiked Wooden Club", 2, 50, 5, 0, 0,], ["Rough Leather Vest", 4, 10, 0, 0, 3,], ["Minor Healing Potion", 1, 15, 30, 0, 0,]]
shopTable = [1, 2, 3, 4, 5]
shopStock = [3, 1, 2, 1, 5, 5, 1, 3, 4, 3]

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
pBag = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
 global wanderLevel, surroundings, surroundingsStats, inTown, loot
 surroundings = []
 surroundingsStats = []
 loot = []
 if inTown: print("You wander into the forest"); inTown = False
 else:
  print("You wander further into the forest")
  print("You feel the danger increase")
 
 rng = random.randint(0, 3)
 
 for i in range(0, rng):
  i = i
  rng2 = random.randint(0, 2)
  surroundings.append(rng2)
  surroundingsStats.append(npcBase[rng2][0])

 wanderLevel += 1
 
def translateSurroundings():
 global surroundings, npcTable, surroundingsStats
 if len(surroundings) == 0: return "No hostile creatures"
 returnString = ""
 for i in range(0, len(surroundings)):
  if npcTable[surroundings[i]][0] == "B" or npcTable[surroundings[i]][0] == "R": returnString += "a "
  else: returnString += "an "
  returnString += (npcTable[surroundings[i]] + "(" + str(surroundingsStats[i]) + "), ")
 return returnString
 
def translateTarget(target):
 global npcTable
 for i in range(0, len(npcTable)):
  if npcTable[i].lower() == target.lower(): return(i)
  
def look():
 global surroundings, loot
 print("You look around and see:")
 print(translateSurroundings())
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
  global pHealth, pDamage, pMaxHealth, pLevel, pAttributes, pGearAttributes
  print("Level: " + str(pLevel[0]))
  print("XP: " + str(pLevel[1]) + "/" + str(pLevel[2]))
  print("Health: " + str(pHealth) + "/" + str(pMaxHealth))
  print("Damage: " + str(pDamage))
  print("Strength: " + str(pAttributes[0]) + " (+" + str(pGearAttributes[0]) + ")")
  print("Agility: " + str(pAttributes[1]) + " (+" + str(pGearAttributes[1]) + ")")
  print("Stamina: " + str(pAttributes[2]) + " (+" + str(pGearAttributes[2]) + ")")

def goTown():
 global wanderLevel, surroundings, surroundingsStats, inTown, loot
 loot = []
 surroundings = []
 surroundingsStats = []
 wanderLevel = 0

 inTown = True
 print("You wander to the town")

def rest():
 global inTown, pHealth, pMaxHealth
 if inTown: print("You rest until you feel healthy again"); pHealth = pMaxHealth
 else: print("You can only rest in town")

def printBag():
 global pBag, itemTable
 result = ""
 for i in pBag:
  if (i > 0): result += itemTable[i][0] + ", "
 print(result)

def getItem(item): #Gets item from string
 global pBag, itemTable
 for i in range(0, len(itemTable)): 
   if item.lower() == itemTable[i][0].lower(): return(itemTable[i], i)
 return("None")

def buyItem(item):
  global pBag, itemTable, shopStock, pMoney
  item = getItem(item)
  if item == "None": return("This item does not exist")
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
  if item == "None": return("This item does not exist")
  for i in range(0, len(pBag)):
   if pBag[i] == item[1]: pBag.pop(i); pMoney += item[0][2]; shopStock.append(item[1]); return("Sold " + item[0][0] + " for " + str(item[0][2]) + " gold")
  return("You do not have a " + item[0][0])

def lootItem(item):
  global pBag, itemTable, loot
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
 print("The shop doesn't have a " + item) 

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
 print("You don't have a " + item) 

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
 print("You don't have a " + item)

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
 print("Available anywhere (excluding shop) : wander, look, stats, bag, examine, loot, equip, equipment, gold")
 print("Available in wilderness: attack, town, loot")
 print("Available in town: rest")
 print("Available in shop: bag, examine, gold, buy, sell, leave")

def generateShopStock():
 global shopStock, shopTable
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
 if cmd.lower() == "bag": printBag()
 if cmd.lower() == "gold": print("You have " + str(pMoney) + " gold")
 if cmd.lower() == "leave": print("You have left the shop"); return()
 playerInShop()
 
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
 if cmd.lower() == "bag": printBag()
 if cmd.lower() == "equipment": printGear()
 if cmd.lower() == "help": printHelp()
 if cmd.lower() == "gold": print("You have " + str(pMoney) + " gold")
 if cmd.lower() == "shop": goShop()
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
 if cmdsplit[0].lower() == "loot":
   result = ""
   for i in range(1, len(cmdsplit)):
     result += cmdsplit[i]
     if i != (len(cmdsplit) - 1): result += " "     
   print(lootItem(result))   
 if cmdsplit[0].lower() == "attack": 
   if (len(cmdsplit) == 1): print("No target selected"); getCommand()
   else: attack(cmdsplit[1])
 getCommand()
 
initStats()
pHealth = pMaxHealth
getCommand()