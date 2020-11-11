#Welcome to the Urgovaan easy-mod script
#This will replace all vanilla content with custom content
loadModded = False #Set to True to load Urgovaan with mods

#NPC
npcTable = ["Rat", "Boar", "Orc", "Large Boar"] #Npc names
npcBase = [[17, 10, 5], [32, 30, 8], [50, 20, 10], [50, 35, 12]] #Npc stats
#IMPORTANT-
#NPC NAMES NEED TO HAVE SAME INDEX AS STATS
npcDropTable = [[2, 1, 3], [2, 2, 50], [3, 12, 30], [1, 12, 15]] #Npc Index, Item to drop, Drop chance (%)
#Minimum drop chance is 1, don't go lower.

#Items
itemTable = [["Nothing", 0, 0, 0, 0, 0,], ["Wooden Club", 2, 10, 3, 0, 0,], ["Orc Tusk", 0, 5, 0, 0, 0,], ["Spiked Wooden Club", 2, 50, 5, 0, 0,], ["Rough Leather Vest", 4, 30, 0, 0, 3,], ["Minor Healing Potion", 1, 15, 30, 0, 0,], ["Wool Cap", 3, 15, 0, 0, 1,], ["Torn Leather Pants", 5, 20, 0, 0, 2,], ["Leather Boots", 6, 15, 0, 0, 1,], ["Pickaxe", 0, 30, 0, 0, 0,], ["Copper Ore", 0, 20, 0, 0, 0], ["Iron Ore", 0, 40, 0, 0, 0], ["Boar Hide", 0, 5, 0, 0, 0], ["Copper Bar", 0, 60, 0, 0, 0], ["Iron Bar", 0, 120, 0, 0, 0], ["Leather", 0, 10, 0, 0, 0], ["Copper Shortsword", 2, 40, 7, 0, 0,]]
#Example: ["Copper Shortsword", 2, 40, 7, 0, 0,]
#Copper Shortsword, type 2 (Weapon), value 40, strength 7, agility 0, stamina 0
#Look below for additional help on itemTable layout
shopTable = [1, 3, 4, 5, 6, 7, 8, 9] #Items which can appear in the shop
shopStock = [3, 1, 6, 5, 5, 1, 3, 4, 3, 9] #First shop stock on game launch

#Skill stuff
oreTable = [["Copper Ore", 0, 7, 9], ["Iron Ore", 2, 18, 9]] #Ore name, mining req, xp reward, pickaxe (item) required
barTable = [["Copper Bar", 14], ["Iron Bar", 36]] #Bar name, crafting xp reward on smelt
#-IMPORTANT-
#ORE NEEDS TO HAVE SAME INDEX AS THE BAR IT SMELTS INTO
craftingTable = [["Copper Shortsword", 0, 20, 13, 13, 13, 15]] #Item, levelreq, xp, materials required (add as many materials as you wish)
tanAbles = [["Boar Hide", 3]] #Items which you can tan into leather & required amount
#Name, type, value, str, agi, stam
#Types:
#0 = Vendor
#1 = Consumable
#2 = Weapon
#3 = Head
#4 = Chest
#5 = Legs
#6 = Feet

def activateContent():
 if loadModded: print("Custom content loaded"); return(npcTable, npcBase, npcDropTable, itemTable, shopTable, shopStock, oreTable, barTable, craftingTable, tanAbles)
 else: return(False)