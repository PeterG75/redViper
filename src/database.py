#!/usr/bin/env python3

import mysql.connector
import globals
import ui
import engine
import sys
from datetime import datetime, timedelta


def dbconnect():

	cfg = engine.parseDbConfig()

	try:
		databaseConnect = mysql.connector.connect(
						  host = cfg["MYSQL_HOST"],
						  user = cfg["MYSQL_USER"],
						  passwd = cfg["MYSQL_PASS"],
						  database = cfg["MYSQL_DB"]
				     	 )

		return databaseConnect

	except:
		
		print(f"{ui.RED_MINUS} Unable to contact mySQL Database. Is it running?")
		sys.exit(1)


def checkIfZombieExists(zid):

	db = dbconnect()


def getZombieCount():

	db = dbconnect()
	csr = db.cursor()
	query = "SELECT COUNT(*) FROM zombies;"
	csr.execute(query)
	count = csr.fetchall()[0][0]
	csr.close()
	db.close()
	return count

def pushZombieToDb(zombie):

	db = dbconnect()
	csr = db.cursor()
	query = "INSERT INTO zombies (zid, subreddit, reddit_account, aes_key, implant_id, hostname, pub_ip, priv_ip, platform ) "
	query += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
	val = ( zombie.zid, zombie.channel, zombie.associated_account, zombie.aes_key, zombie.implant_id, zombie.hostname, zombie.pub_ip, zombie.priv_ip, zombie.platform, )

	csr.execute(query, val)
	db.commit()
	csr.close()
	db.close()


def getZombieDataByZid(zid):

	db = dbconnect()
	csr = db.cursor()

	query = "SELECT * FROM zombies WHERE zid = '" + zid + "';"
	csr.execute(query)
	resp = csr.fetchall()
	csr.close()
	db.close()
	
	return resp[0]

def listZombiesSummary():

	db = dbconnect()
	csr = db.cursor()

	query = "SELECT db_id, zid, subreddit, pub_ip, last_check FROM zombies;"
	csr.execute(query)
	resp = csr.fetchall()
	csr.close()
	db.close()
	
	return resp

def wipeZombieDb():

	db = dbconnect()
	csr = db.cursor()
	
	sqlCmds = []
	sqlCmds.append("DELETE FROM zombies WHERE 1=1;")
	sqlCmds.append("ALTER TABLE zombies AUTO_INCREMENT = 1;")
	for cmd in sqlCmds:
		csr.execute(cmd)

	db.commit()
	csr.close()
	db.close()

def getZombieByDbID(db_id):

	db = dbconnect()
	csr = db.cursor()

	query = "SELECT * FROM zombies WHERE db_id = " + str(db_id) + ";"
	csr.execute(query)
	resp = csr.fetchall()
	if len(resp) == 0:
		return None
	else:
		return resp[0]

def updateZombieTimestamp(zid):

	db = dbconnect()
	csr = db.cursor()

	query = "UPDATE zombies SET last_check = current_timestamp WHERE zid = '" + zid + "';"
	csr.execute(query)
	db.commit()
	csr.close()
	db.close()


def checkCheckInTimes():

	db = dbconnect()
	csr = db.cursor()

	query = "SELECT zid FROM zombies WHERE last_check < (NOW() - INTERVAL 5 MINUTE);"
	csr.execute(query)
	resp = csr.fetchall()
	csr.close()
	db.close()

	for result in resp:
		zid = result[0]
		print(f"\n{ui.notif_yellow()} Zombie {ui.WHITE_B}{zid}{ui.RESET} has not checked in for 5 minutes. Dropping zombie until a call has been received...")
		deleteZombieByZid(zid)


def deleteZombieByZid(zid):

	db = dbconnect()
	csr = db.cursor()

	query = "DELETE FROM zombies WHERE  zid = '" + zid + "';"
	csr.execute(query)
	db.commit()
	csr.close()
	db.close()

def getImplantKeyByID(implant_id):

	db = dbconnect()
	csr = db.cursor()

	query = "SELECT implant_key FROM implants WHERE implant_id = '" + implant_id + "';"
	csr.execute(query)
	resp = csr.fetchall()
	if len(resp) == 0:
		return None
	else:
		return resp[0][0]





		





	


	
	




