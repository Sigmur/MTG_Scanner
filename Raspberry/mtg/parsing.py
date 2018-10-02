#!/usr/bin/python
'''
MIT License

Copyright (c) 2018 Sigmur

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import re

MTG_EXTENTIONS = {
	"CHR": ["CHR", "Chronicles", "01/07/95", 125],
	"HOP": ["HOP", "Planechase10", "04/09/09", 0],
	"ARC": ["ARC", "Archenemy11", "18/06/10", 0],
	"COM": ["COM", "Magic The Gathering Commander", "17/06/11", 0],
	"PC2": ["PC2", "Planechase 2012", "01/05/12", 0],
	"CMA": ["CMA", "Commander's Arsenal", "02/11/12", 0],
	"C13": ["C13", "Magic Commander 2013", "01/11/13", 0],
	"CNS": ["CNS", "Conspiracy", "06/06/14", 210],
	"C14": ["C14", "Magic Commander 2014", "07/11/14", 0],
	"C15": ["C15", "Magic Commander 2015", "13/11/15", 0],
	"CN2": ["CN2", "Conspiracy: Take the Crown", "26/08/16", 221],
	"C16": ["C16", "Magic Commander 2016", "11/11/16", 0],
	"E01": ["E01", "Archenemy: Nicol Bolas", "16/06/17", 0],
	"C17": ["C17", "Magic Commander 2017", "25/08/17", 0],
	"EXL": ["EXL", "Explorers of Ixalan", "24/11/17", 47],
	"BBD": ["BBD", "Battlebond", "08/06/18", 256],
	"C18": ["C18", "Magic Commander 2018", "10/08/18", 0],
	"EVG": ["EVG", "Duel Decks : Elves vs. Goblins", "01/11/07", 0],
	"JVC": ["JVC", "Duel Decks : Jace vs. Chandra", "01/11/08", 0],
	"DVD": ["DVD", "Duel Decks : Divine vs. Demonic", "01/04/09", 0],
	"GVL": ["GVL", "Duel Decks : Garruk vs. Liliana", "01/10/09", 0],
	"PVC": ["PVC", "Duel Decks: Phyrexia vs. The Coalition12", "01/03/10", 0],
	"DDF": ["DDF", "Duel Decks: Elspeth vs. Tezzeret", "01/09/10", 0],
	"TBA": ["TBA", "Duel Decks: Knights vs. Dragons", "01/04/11", 0],
	"DDG": ["DDG", "Duel Decks : Ajani vs. Nicol Bolas", "02/09/11", 0],
	"DDI": ["DDI", "Duel Decks : Venser vs. Koth", "30/03/12", 0],
	"DDJ": ["DDJ", "Duel Decks : Izzet vs. Golgari", "07/09/12", 0],
	"DDK": ["DDK", "Duel Decks : Sorin vs. Tibalt", "15/03/12", 0],
	"DDL": ["DDL", "Duel Decks : Heroes vs. Monsters", "06/09/13", 0],
	"DDM": ["DDM", "Duel Decks : Jace vs. Vraska", "14/03/14", 0],
	"DDN": ["DDN", "Duel Decks : Speed vs. Cunning", "05/09/14", 0],
	"DD3": ["DD3", "Duel Decks : Anthology", "05/12/14", 0],
	"DDO": ["DDO", "Duel Decks : Elspeth vs. Kiora", "27/02/15", 0],
	"DDP": ["DDP", "Duel Decks : Zendikar vs. Eldrazi", "28 aout 2015", 0],
	"DDQ": ["DDQ", "Duel Decks : Blessed vs. Cursed", "26/02/16", 0],
	"DDR": ["DDR", "Duel Decks : Nissa vs. Ob Nixilis", "02/09/16", 0],
	"DDS": ["DDS", "Duel Decks : Mind vs. Might", "31/03/17", 0],
	"DDT": ["DDT", "Duel Decks : Merfolk vs. Goblins", "10/11/17", 0],
	"GS1": ["GS1", "Global Series Jiang Yanggu & Mu Yanling", "22/06/18", 0],
	"DRB": ["DRB", "From the Vault : Dragons", "01/08/08", 15],
	"V09": ["V09", "From the Vault : Exiled", "01/08/09", 15],
	"V10": ["V10", "From the Vault : Relics13", "27/08/10", 15],
	"V11": ["V11", "From the Vault : Legends", "26/08/11", 15],
	"V12": ["V12", "From the Vault : Realms", "31/08/12", 15],
	"V13": ["V13", "From the Vault : Twenty", "23/08/13", 20],
	"V14": ["V14", "From the Vault : Annihilation", "22/08/14", 15],
	"V15": ["V15", "From the Vault : Angels", "21/08/15", 15],
	"V16": ["V16", "From the Vault : Lore", "19/08/16", 15],
	"V17": ["V17", "From the Vault : Transform", "24/11/17", 15],
	"PDS": ["PDS", "Premium Deck Series : Slivers", "01/11/09", 60],
	"FAL": ["FAL", "Premium Deck Series : Fire & Lightning", "01/11/10", 60],
	"POR": ["POR", "Portal", "1er mai 1997", 228],
	"P02": ["P02", "Portal Second Age", "24 juin 1998", 165],
	"PTK": ["PTK", "Portal Three Kingdoms", "6 juillet 1999", 180],
	"S99": ["S99", "Starter 1999", "juillet 1999", 173],
	"S00": ["S00", "Starter 2000", "juillet 2000", 57],
	"ARN": ["ARN", "Arabian Nights", "décembre 1993", 78],
	"ATQ": ["ATQ", "Antiquities", "mars 1994", 100],
	"LEG": ["LEG", "Legends", "juin 1994", 310],
	"DRK": ["DRK", "The Dark", "août 1994", 119],
	"FEM": ["FEM", "Fallen Empires", "novembre 1994", 187],
	"HML": ["HML", "Homelands", "octobre 1995", 140],
	"ICE": ["ICE", "Ice Age", "juin 1995", 383],
	"ALL": ["ALL", "Alliances", "10 juin 1996", 199],
	"CSP": ["CSP", "Coldsnap", "21 juillet 2006", 155],
	"MIR": ["MIR", "Mirage", "7 octobre 1996", 350],
	"VIS": ["VIS", "Visions", "2 février 1997", 167],
	"WTH": ["WTH", "Weatherlight", "9 juin 1997", 167],
	"TMP": ["TMP", "Tempest", "4 octobre 1997", 350],
	"STH": ["STH", "Stronghold", "5 mars 1998", 143],
	"EXO": ["EXO", "Exodus", "16 juin 1998", 143],
	"USG": ["USG", "Urza's Saga", "8 octobre 1998", 350],
	"ULG": ["ULG", "Urza's Legacy", "16 février 1999", 143],
	"UDS": ["UDS", "Urza's Destiny", "7 juin 1999", 143],
	"MMQ": ["MMQ", "Mercadian Masques", "4 octobre 1999", 350],
	"NMS": ["NMS", "Nemesis", "14 février 2000", 143],
	"PCY": ["PCY", "Prophecy", "6 juin 2000", 143],
	"INV": ["INV", "Invasion", "3 octobre 2000", 350],
	"PLS": ["PLS", "Planeshift", "5 février 2001", 143],
	"APC": ["APC", "Apocalypse", "4 juin 2001", 143],
	"ODY": ["ODY", "Odyssey", "21 septembre 2001", 350],
	"TOR": ["TOR", "Torment", "4 février 2002", 143],
	"JUD": ["JUD", "Judgment", "27 mai 2002", 143],
	"ONS": ["ONS", "Onslaught", "7 octobre 2002", 350],
	"LGN": ["LGN", "Legions", "4 février 2003", 145],
	"SCG": ["SCG", "Scourge", "27 mai 2003", 143],
	"MRD": ["MRD", "Mirrodin", "3 octobre 2003", 306],
	"DST": ["DST", "Darksteel", "6 février 2004", 165],
	"5DN": ["5DN", "5th Dawn", "4 juin 2004", 165],
	"CHK": ["CHK", "Champions of Kamigawa", "1er octobre 2004", 306],
	"BOK": ["BOK", "Betrayers of Kamigawa", "4 février 2005", 165],
	"SOK": ["SOK", "Saviors of Kamigawa", "3 juin 2005", 165],
	"RAV": ["RAV", "Ravnica: the City of Guilds", "7 octobre 2005", 306],
	"GPT": ["GPT", "Guildpact", "3 février 2006", 165],
	"DIS": ["DIS", "Dissension", "5 mai 2006", 180],
	"TSB": ["TSB", "Time Spiral", "6 octobre 2006", 121],
	"TSP": ["TSP", "Time Spiral", "6 octobre 2006", 301],
	"PLC": ["PLC", "Planar Chaos", "2 février 2007", 165],
	"FUT": ["FUT", "Future Sight", "4 mai 2007", 180],
	"LRW": ["LRW", "Lorwyn", "12 octobre 2007", 301],
	"MOR": ["MOR", "Morningtide", "1er février 2008", 165],
	"SHM": ["SHM", "Shadowmoor", "2 mai 2008", 301],
	"EVE": ["EVE", "Eventide", "25 juillet 2008", 180],
	"ALA": ["ALA", "Shards of Alara", "3 octobre 2008", 249],
	"CFX": ["CFX", "Conflux", "6 février 2009", 145],
	"ARB": ["ARB", "Alara Reborn", "30 avril 2009", 145],
	"ZEN": ["ZEN", "Zendikar", "2 octobre 2009", 249],
	"WWK": ["WWK", "Worldwake", "5 février 2010", 145],
	"ROE": ["ROE", "Rise of the Eldrazi", "23 avril 2010", 248],
	"SOM": ["SOM", "Scars of Mirrodin3", "1er octobre 2010", 249],
	"MBS": ["MBS", "Mirrodin Besieged4", "4 février 20114", 155],
	"NPH": ["NPH", "New Phyrexia", "13 mai 2011", 175],
	"ISD": ["ISD", "Innistrad", "30 septembre 2011", 264],
	"DKA": ["DKA", "Dark Ascension7", "3 février 2012", 158],
	"AVR": ["AVR", "Avacyn Restored8", "4 mai 2012", 244],
	"RTR": ["RTR", "Return to Ravnica", "5 octobre 2012", 274],
	"GTC": ["GTC", "Gatecrash", "26 janvier 2013", 249],
	"DGM": ["DGM", "Dragon's Maze", "3 mai 2013", 156],
	"THS": ["THS", "Theros", "27 septembre 2013", 249],
	"BNG": ["BNG", "Born of The Gods", "7 février 2014", 165],
	"JOU": ["JOU", "Journey into Nyx", "2 mai 2014", 165],
	"KTK": ["KTK", "Khans of Tarkir", "26 septembre 2014", 269],
	"FRF": ["FRF", "Fate Reforged", "23 janvier 2015", 185],
	"DTK": ["DTK", "Dragons of Tarkir", "27 mars 2015", 264],
	"BFZ": ["BFZ", "Battle for Zendikar", "2 octobre 2015", 274],
	"OGW": ["OGW", "Oath of the Gatewatch", "22 janvier 2016", 184],
	"SOI": ["SOI", "Shadows over Innistrad", "8 avril 2016", 297],
	"EMN": ["EMN", "Eldritch Moon", "22 juillet 2016", 205],
	"KLD": ["KLD", "Kaladesh", "30 septembre 2016", 264],
	"AER": ["AER", "Aether Revolt", "20 janvier 2017", 184],
	"AKH": ["AKH", "Amonkhet", "28 avril 2017", 269],
	"HOU": ["HOU", "Hour of Devastation", "14 juillet 2017", 184],
	"XLN": ["XLN", "Ixalan", "29 septembre 2017", 279],
	"RIX": ["RIX", "Rivals of Ixalan", "19 janvier 2018", 196],
	"DOM": ["DOM", "Dominaria", "27 avril 2018", 269],
	"LEA": ["LEA", "Alpha", "5 août 1993", 295],
	"LEB": ["LEB", "Beta", "octobre 1993", 302],
	"2ED": ["2ED", "Unlimited", "décembre 1993", 302],
	"3ED": ["3ED", "Revised", "avril 1994", 306],
	"4ED": ["4ED", "4th Edition", "mai 1995", 378],
	"5ED": ["5ED", "5th Édition", "24 mars 1997", 449],
	"6ED": ["6ED", "Classic 6th Edition", "27 avril 1999", 350],
	"7ED": ["7ED", "7th Edition", "2 avril 2001", 350],
	"8ED": ["8ED", "8th Edition", "28 juillet 2003", 350],
	"9ED": ["9ED", "9th Edition", "29 août 2005", 350],
	"10E": ["10E", "10th Edition", "13 juillet 2007", 383],
	"M10": ["M10", "Edition 2010", "17 juillet 2009", 249],
	"M11": ["M11", "Edition 2011", "16 juillet 2010", 249],
	"M12": ["M12", "Edition 2012", "15 juillet 2011", 249],
	"M13": ["M13", "Edition 2013", "13 juillet 2012", 249],
	"M14": ["M14", "Edition 2014", "19 juillet 2013", 249],
	"M15": ["M15", "Edition 2015", "18 juillet 2014", 269],
	"ORI": ["ORI", "Magic Origins", "17 juillet 2015", 272],
	"M19": ["M19", "Magic 2019", "20 juillet 2018", 269],
	"MMA": ["MMA", "Modern Masters", "7 juin 2013", 229],
	"MM2": ["MM2", "Modern Masters 2015 edition", "22 mai 2015", 249],
	"EMA": ["EMA", "Eternal Masters", "10 juin 2016", 249],
	"MM3": ["MM3", "Modern Masters 2017 edition", "17 mars  2017", 249],
	"IMA": ["IMA", "Iconic Masters", "17 novembre 2017", 249],
	"A25": ["A25", "Masters 25", "16 mars 2018", 249],
}

MTG_CARD_TYPES = {
	'C': 'common',
	'U': 'uncommon',
	'R': 'rare',
	'M': 'mythic rare',
	'L': 'land',
	'T': 'token',
	'S': 'special',
	'E': 'emblem'
}

def parse(string):
	string = string.upper()
	string = string.replace('I', '!')
	#Parse Tesseract string datas
	#1) Card number
	number_and_type = getCardNumberAndType(string)
	number = number_and_type[0]
	type = number_and_type[1]
	#2) Extention
	extention_and_lang = getCardExtentionAndLang(string)
	extention = extention_and_lang[0]
	lang = extention_and_lang[1]
	
	return {'number': number, 'extention': extention, 'lang': lang, 'type': type}
	
def getCardNumberAndType(string):
	result = re.search(r'(\d{2,}\/\d{2,}).{0,}(C|U|R|M|L|T|S|E)', string)
	type = ''
	number = ''
	
	if result is None:
		return (number, type)
		
	for i in range(0, len(result.groups()) + 1):
		text = result.group(i)
		if type == '' and len(text) == 1 and isValidCardType(text):
			type = text
		elif number == '' and len(text) > 1 and re.search(r'\d{2,}\/\d{2,}', text) != None:
			splitted = text.split('/')
			number = splitted[0]
			
	return (number, type)
	
def getCardExtentionAndLang(string):
	result = re.search(r'(\w{3}).{0,}(EN|FR)', string)
	extention = ''
	lang = ''
	
	if result is None:
		return (extention, lang)
	
	for i in range(0, len(result.groups()) + 1):
		text = result.group(i)
		if len(text) == 3 and isValidExtention(text):
			extention = text
		elif len(text) == 2 and (text == 'FR' or text == 'EN'):
			lang = text
	return (extention, lang)
	
def isValidExtention(trigram):
	return trigram in MTG_EXTENTIONS
	
def isValidCardType(type):
	return type in MTG_CARD_TYPES
