from colors import *
from ParseConfig import *
import commands
import thread
import os
import sys
import signal
import traceback
import subprocess
import sqlalchemy
def pm(s,p,m):
	try:
		print yellow+"PM To:%s, Message: %s" %(p,m) + normal
		s.send("SAYPRIVATE %s %s\n" %(p,m))
	except:
		pass
def saychannel( socket, channel, message ):
		socket.send("SAY " + channel + " " + message + "\n")
class OptionEntry:
	 def __init__(self):
	 	self.valuelist = []
class LadderOptions:
	 def __init__(self):
	 	self.modname = ""
	 	self.controlteamminsize = 1
	 	self.controlteammaxsize = 1
	 	self.allymaxsize = 1
	 	self.allyminsize = 1
	 	self.allowedoptions = dict() # option path -> list of allowed values
	 	self.restrictedoptions = dict() # option path -> list of denied value
	 	self.allowedmaps = [] # list of allowed map names
	 	self.restrictedmaps = [] # list of denied map names
class LadderMatch:
	def __init__(self):
		self.timestamp = 0
		self.winnerid = -1
		self.playerids = []
		self.teams
class LadderScores:
	def __init__(self):
		self.playerscores = [] # player id -> score
class Main:
	botpid = dict() # slot -> bot pid
	botstatus = dict() # slot -> bot already spawned
	battleswithbots = dict() # battle id -> bot already in
	ladderlist = dict() # id -> ladder name
	ladderoptions = dict() # id -> ladder options
	
	sql = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)
	def botthread(self,slot,battleid,ladderid,ist):
		try:
			d = dict()
			d.update([("serveraddr",self.app.config["serveraddr"])])
			d.update([("serverport",self.app.config["serverport"])])
			d.update([("admins",self.app.config["admins"])])
			d.update([("nick",self.app.config["nick"]) + str(slot) )])
			d.update([("password",self.app.config["password"])])])
			d.update([("plugins","channels,ladderbot,help")])
			d.update([("bans",self.app.config["bans"])])
			d.update([("battleid",str(battleid))])
			d.update([("ladderid",str(ladderid))])
			writeconfigfile(nick+".cfg",d)
			p = subprocess.Popen(("python","Main.py","-c", "%s" % (nick+".cfg")),stdout=sys.stdout)
			self.bots[slot] = p.pid
			#print self.bots
			p.wait()
			self.ul.remove(r)
		except:
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60
	def onload(self,tasc):
		self.tsc = tasc
		self.bans = []
		self.app = tasc.main
	def queryladderidexists(ladderid):
	def notifyuser( socket, fromwho, fromwhere, ispm, message ):
		if fromwhere == "main":
			ispm = true
		if not ispm:
			saychannel( socket, fromwhere, message )
		else:
			pm( socket, fromwho, message )
	def spawnbot( self,  socket, battleid, ladderid ):	
		slot = len(botstatus)
		self.threads.append(thread.start_new_thread(self.botthread,(slot,socket,battleid,ladderid,self)))
		self.botstatus[slot] = True
	def oncommandfromuser(self,fromwho,fromwhere,ispm,command,args,socket):
		if command == "!ladder":
			ladderid = -1
			if len(args) > 1:
				notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax or command not found, use !help for a list of available commands and their usage." )
			else:
				if ( args[0].isdigit() ):
					ladderid = int(args[0])
				try:
					battleid = self.users[self.args[0]].battleid
					if ( battleid == -1 ):
						notifyuser( socket, fromwho, fromwhere, ispm, "You are not in a battle." )
					else:
						if ( battleswithbots[battleid] == True ):
							notifyuser( socket, fromwho, fromwhere, ispm, "A ladder bot is already present in your battle." )
						else:
							if ( laderid == -1 or queryladderidexists(ladderid) ):
								spawnbot( self, socket, battleid, ladderid )
							else:
								notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )
				except:
					pass
		if command == "!ladderlist":
			notifyuser( socket, fromwho, fromwhere, ispm, "Available ladders, format name: ID:" )
			for i in self.ladderlist:
				notifyuser( socket, fromwho, fromwhere, ispm, ladderlist[i] + ": " + str(i) )
		if command == "!addladder":
			if ( fromwho in self.app.config["admins"]) ):
				if len(args) < 1:
					notifyuser( socket, fromwho, fromwhere, ispm, "Ladder name can't be empty." )
				else:
					ladderid = len(self.ladderlist)
					self.ladderlist[ladderid] = " ".join(args[0:])
					self.ladderoptions[ladderid] = LadderOptions()
					notifyuser( socket, fromwho, fromwhere, ispm, "New ladder created, ID: " + str(ladderid) )
		if command == "!deleteladder":
			if ( fromwho in self.app.config["admins"]) ):
				if len(args) != 1 or not args[0].isdigit():
					notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
				else:
					ladderid = int(args[0])
					if ( queryladderidexists(ladderid) ):
					else:
						notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )
		if command == "!changeladdermod":
			if ( fromwho in self.app.config["admins"]) ):
				if len(args) < 2 or not args[0].isdigit():
					notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
				else:
					ladderid = int(args[0])
					if ( queryladderidexists(ladderid) ):
						ladderoptions[ladderid].modname = " ".join(args[1:])
					else:
						notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )
		if command == "!changeladdercontrolteamsize":
			if ( fromwho in self.app.config["admins"]) ):
				if len(args) > 3 or not args[0].isdigit() or not args[1].isdigit():
					notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
				else:
					ladderid = int(args[0])
					if ( queryladderidexists(ladderid) ):
						if len(args) == 2: # min = max
							ladderoptions[ladderid].controlteamminsize = int(args[1])
							ladderoptions[ladderid].controlteamminsize = int(args[1])
						else if len(args) == 3: # separate min & max
							if ( not args[2].isdigit() ):
								notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )							
							else:
								ladderoptions[ladderid].controlteamminsize = int(args[1])
								ladderoptions[ladderid].controlteamminsize = int(args[2])
					else:
						notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )
		if command == "!changeladderallysize":
			if ( fromwho in self.app.config["admins"]) ):
				if len(args) > 3 or not args[0].isdigit() or not args[1].isdigit():
					notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
				else:
					ladderid = int(args[0])
					if ( queryladderidexists(ladderid) ):
						if len(args) == 2: # min = max
							ladderoptions[ladderid].allyminsize = int(args[1])
							ladderoptions[ladderid].allymaxsize = int(args[1])
						else if len(args) == 3: # separate min & max
							if ( not args[2].isdigit() ):
								notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )							
							else:
								ladderoptions[ladderid].allyminsize = int(args[1])
								ladderoptions[ladderid].allymaxsize = int(args[2])
					else:
						notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )						
		if command == "!addladderoption":
			if ( fromwho in self.app.config["admins"]) ):
				if len(args) != 4 or not args[0].isdigit() or not args[1].isdigit():
					notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
				else:
					ladderid = int(args[0])
					if ( queryladderidexists(ladderid) ):
						whitelist = bool(args[1])
						keyname = args[2]
						value = args[3]
						if whitelist:
							if ( keyname in self.ladderoptions[ladderid].restrictedoptions ):
								notifyuser( socket, fromwho, fromwhere, ispm, "You cannot use blacklist and whitelist at the same time for the same option key." )
							else:
								currentvalues = self.ladderoptions[ladderid].allowedoptions[keyname]
								if ( not value in currentvalues ):
									currentvalues.append(value)
									self.ladderoptions[ladderid].allowedoptions.Update([keyname,currentvalues])
									notifyuser( socket, fromwho, fromwhere, ispm, "Option added to the whitelist." )
						else:
							if( keyname in self.ladderoptions[ladderid].allowedoptions ):
								notifyuser( socket, fromwho, fromwhere, ispm, "You cannot use blacklist and whitelist at the same time for the same option key." )
							else:
								currentvalues = self.ladderoptions[ladderid].restrictedoptions[keyname]
								if ( not value in currentvalues ):
									currentvalues.append(value)
									self.ladderoptions[ladderid].restrictedoptions.Update([keyname,currentvalues])
									notifyuser( socket, fromwho, fromwhere, ispm, "Option added to the blacklist." )
					else:
						notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )
		if command == "!removeladderoption":
			if ( fromwho in self.app.config["admins"]) ):
				if len(args) != 3 or not args[0].isdigit():
					notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
				else:
					ladderid = int(args[0])
					if ( queryladderidexists(ladderid) ):
						keyname = args[1]
						value = args[2]
						indisableoptions = False
						indenableoptions = False
						if keyname in self.ladderoptions[ladderid].restrictedoptions:
							indisableoptions = True
						if keyname in self.ladderoptions[ladderid].allowedoptions ):
							inenabledoptions = True
						if not indisableoptions and not indenableoptions:
							notifyuser( socket, fromwho, fromwhere, ispm, "Key doesn't exist in both whitelist and blackist." )
						else:
							currentvalues = dict()
							if indisableoptions:
								currentvalues = self.ladderoptions[ladderid].restrictedoptions[keyname]
							else:
								currentvalues = self.ladderoptions[ladderid].allowedoptions[keyname]
							if not value in currentvalues:
								message = "blacklisted"
								if inenabledoptions:
									message = "whitelisted"
								notifyuser( socket, fromwho, fromwhere, ispm, "Value doesn't exist in " + message + " options" )
							else:
								currentvalues.remove(value)
								if inenabledoptions:
									if len(currentvalues) == 0:
										self.ladderoptions[ladderid].allowedoptions.remove(keyname)
									else:
										self.ladderoptions[ladderid].allowedoptions.Update([keyname,currentvalues])
									notifyuser( socket, fromwho, fromwhere, ispm, "Option removed from the whitelist." )
								else:
									if len(currentvalues) == 0:
										self.ladderoptions[ladderid].restrictedoptions.remove(keyname)
									else:
										self.ladderoptions[ladderid].restrictedoptions.Update([keyname,currentvalues])
									notifyuser( socket, fromwho, fromwhere, ispm, "Option removed from the blacklist." )
					else:
						notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )
		if command == "!listladderoptions":
				if len(args) != 1 or not args[0].isdigit():
					notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
				else:
					ladderid = int(args[0])
					if ( queryladderidexists(ladderid) ):
						whitelist = self.ladderoptions[ladderid].allowedoptions
						blacklist = self.ladderoptions[ladderid].restrictedoptions
						notifyuser( socket, fromwho, fromwhere, ispm, "Ladder :" + self.ladderlist[ladderid] )
						notifyuser( socket, fromwho, fromwhere, ispm, "Whitelisted options ( if a key is present, no other value except for those listed will be allowed for such key ):" )
						for key in whitelist:
							allowedvalues = whitelist[key]
							for valueindex in allowedvalues:
								notifyuser( socket, fromwho, fromwhere, ispm, key + ": " + allowedvalues[valueindex] )
						notifyuser( socket, fromwho, fromwhere, ispm, "Blacklisted options ( if a value is present for a key, such value won't be allowed ):" )
						for key in blacklist:
							disabledvalues = blacklist[key]
							for valueindex in disabledvalues:
								notifyuser( socket, fromwho, fromwhere, ispm, key + ": " + disabledvalues[valueindex] )						
					else:
						notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )
		if command == "!addladdermap":
			if ( fromwho in self.app.config["admins"]) ):
				if len(args) != 3 or not args[0].isdigit() or not args[1].isdigit():
					notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
				else:
					ladderid = int(args[0])
					if ( queryladderidexists(ladderid) ):
						whitelist = bool(args[1])
						mapname = args[2]
						if whitelist:
							if (len(self.ladderoptions[ladderid].restrictedmaps) != 0 ):
								notifyuser( socket, fromwho, fromwhere, ispm, "You cannot use blacklist and whitelist at the same time for maps." )
							else:
								if ( not value in self.ladderoptions[ladderid].allowedmaps ):
									self.ladderoptions[ladderid].allowedmaps.append(mapname)
									notifyuser( socket, fromwho, fromwhere, ispm, "Map added to the whitelist." )
						else:
							if( len(self.ladderoptions[ladderid].restrictedoptions) != 0 ):
								notifyuser( socket, fromwho, fromwhere, ispm, "You cannot use blacklist and whitelist at the same time for maps." )
							else:
								if ( not value in self.ladderoptions[ladderid].restrictedmaps ):
									self.ladderoptions[ladderid].restrictedmaps.append(mapname)
									notifyuser( socket, fromwho, fromwhere, ispm, "Map added to the blacklist." )
					else:
						notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )
		if command == "!removeladdermap":
			if ( fromwho in self.app.config["admins"]) ):
				if len(args) != 2 or not args[0].isdigit():
					notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
				else:
					ladderid = int(args[0])
					if ( queryladderidexists(ladderid) ):
						mapname = args[1]
						indisableoptions = False
						indenableoptions = False
						if mapname in self.ladderoptions[ladderid].restrictedmaps:
							indisableoptions = True
						if mapname in self.ladderoptions[ladderid].allowedmaps ):
							inenabledoptions = True
						if not indisableoptions and not indenableoptions:
							notifyuser( socket, fromwho, fromwhere, ispm, "Map doesn't exist in both whitelist and blackist." )
						else:
							if indisableoptions:
								self.ladderoptions[ladderid].restrictedmaps.remove(mapname)
								notifyuser( socket, fromwho, fromwhere, ispm, "Map removed rom blacklist." )
							else:
								self.ladderoptions[ladderid].allowedmaps.remove(mapname)
								notifyuser( socket, fromwho, fromwhere, ispm, "Map removed from whitelist." )
					else:
						notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )
		if command == "!listladdermaps":
			if len(args) != 1 or not args[0].isdigit():
				notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
			else:
				ladderid = int(args[0])
				if ( queryladderidexists(ladderid) )
					indisableoptions = False
					indenableoptions = False
					if len(self.ladderoptions[ladderid].restrictedmaps) > 0:
						indisableoptions = True
					if len(self.ladderoptions[ladderid].allowedmaps) > 0:
						inenabledoptions = True
					notifyuser( socket, fromwho, fromwhere, ispm, "Ladder :" + self.ladderlist[ladderid] )
					if not indisableoptions and not indenableoptions:
						notifyuser( socket, fromwho, fromwhere, ispm, "No map restrictions are in place." )
					else:
						maplist = []
						if indisableoptions:
							notifyuser( socket, fromwho, fromwhere, ispm, "Blacklisted maps:" )
							maplist = self.ladderoptions[ladderid].restrictedmaps
						else:
							notifyuser( socket, fromwho, fromwhere, ispm, "Whitelisted maps:" )
							maplist = self.ladderoptions[ladderid].allowedmaps
						for mapindex in maplist:
							notifyuser( socket, fromwho, fromwhere, ispm, maplist[mapindex] )
				else:
					notifyuser( socket, fromwho, fromwhere, ispm, "Invalid ladder ID." )
		if command == "!score":
			if len(args) > 2:
				notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
			else:
				ladderid = -1
				playername = ""
				if len(args) == 1:
					if args[0].isdigit():
						ladderid = int(args[0])
					else:
						playername = args[0]
				if len(args) == 2:
					if not args[0].isdigit():
						notifyuser( socket, fromwho, fromwhere, ispm, "Invalid command syntax, check !help for usage." )
					else:
						ladderid = int(args[0])
						plaeryname = args[1]
				if ladderid != -1 or len(playername) != 0:
					if ladderid != -1 and len(playername) == 0: # print full ladder scores
						notifyuser( socket, fromwho, fromwhere, ispm, "Stub" )
					if ladderid == -1 and len(playername) != 0: # print player's scores for all ladders
						notifyuser( socket, fromwho, fromwhere, ispm, "Stub" )
					if ladderid != -1 and len(playername) != 0: # print player's score for given ladder
						notifyuser( socket, fromwho, fromwhere, ispm, "Stub" )
	def oncommandfromserver(self,command,args,socket):
		if command == "SAID" and len(args) > 2 and args[2].startswith("!"):
			oncommandfromuser(self,args[1],args[0],False,args[2:],socket)
		if command == "SAIDPRIVATE" and len(args) > 1 and args[1].startswith("!"):
			oncommandfromuser(self,args[0],"PM",True,args[1:],socket)
	def updatestatus(self,socket):
		socket.send("MYSTATUS %i\n" % int(int(0)+int(0)*2))	
	def onloggedin(self,socket):
		self.updatestatus(socket)	
