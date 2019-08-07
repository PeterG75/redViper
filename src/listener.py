#!/usr/bin/env python3

import praw


class listener:

	def __init__(self, username, password, api_secret, client_id, user_agent, subreddit):
	
		self.username = username
		self.password = password
		self.api_secret = api_secret
		self.client_id = client_id
		self.user_agent = user_agent
		self.subreddit = subreddit

	
	def catchAlives(self):
		None


	def expectCmdResponse(self, zombie, cmd_id):
		None


