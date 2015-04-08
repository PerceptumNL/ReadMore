import random

def generate_password():
	adjective_list = [
	"rode", 
	"gele", 
	"paarse",
	"groene",
	"roze",
	"boze", 
	"blije", 
	"slimme",
	"flauwe",
	"coole",
	"zachte",
	"snelle",
	"brave",
	]
	noun_list = [
	"draak",
	"kat",
	"hond",
	"haas",
	"aap",
	"kip",
	"pauw",
	"bij",
	"kikker",
	"slang",
	"leeuw",
	"tijger",
	"mier",
	"zebra",
	"beer"
	]
	adjective = random.choice(adjective_list)
	noun = random.choice(noun_list)
	return adjective+noun