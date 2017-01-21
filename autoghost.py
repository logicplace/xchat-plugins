__module_name__ = "AutoGhost"
__module_author__ = "Sapphire Becker (logicplace.com)"
__module_version__ = "0.4"
__module_description__ = "Ensures you have the nick you want by any means available."

import xchat
import string

try: hF=open(xchat.get_info("xchatdir")+"/servlist_.conf")
except IOError as err:
	if err.errno == 2: hF=open(xchat.get_info("xchatdir")+"/servlist.conf")
	else: raise
#endtry
lSL=hF.readlines()
hF.close()

dInfo = {}

def GhostThatFucker(word,word_eol,userdata):
	global dInfo
	hContext = xchat.get_context()
	sServ=hContext.get_info("network")
	if sServ != None:
		sNick=hContext.get_info("nick")
		sTmp="N="+sServ
		bFnd=False
		sPNick=None
		sPass=None
		iFlags=None
		for sI in lSL:
			sI = sI.rstrip()
			if bFnd and sI:
				if sI[0] == 'N': break
				elif sI[0] == 'I': sPNick=sI[2:]
				elif sI[0] == 'B': sPass=sI[2:]
				elif sI[0] == 'F': iFlags=int(sI[2:])
			elif sI == sTmp:
				bFnd=True
			#endif
		#endfor
		if iFlags == None: iFlags=0
		if iFlags&0x2: sPNick=None
		if sPNick == None: sPNick=xchat.get_prefs("irc_nick1")
		if sNick != sPNick:
			xchat.prnt("%s: Incorrect nick %s (should be %s)" % (__module_name__,sNick,sPNick))
			if sPass != None:
				dInfo[sServ] = {
					"on": 1,
					"nick": sPNick,
					"pass": sPass
				}
				hContext.command("nickserv GHOST %s %s" % (sPNick,sPass))
				xchat.prnt("%s: Ghosting.." % __module_name__)
				return xchat.EAT_NONE
			elif userdata:
				dInfo[sServ] = {
					"on": 3, # Listen for user lists, see if the nick you want is in the room
					"nick": sPNick
				}
			#endif
		#endif
	#endif
	return xchat.EAT_NONE
#enddef

def DoNick(word,word_eol,userdata):
	global dInfo
	#xchat.prnt("Received Notice from %s." % word[0])
	if word[0] == "NickServ": # Maybe this needs to be more variable, idk
		sServ=xchat.get_info("network")
		if sServ in dInfo and dInfo[sServ]["on"] == 1:
			dInfo[sServ]["on"] = 2
			xchat.command("nick %s" % dInfo[sServ]["nick"])
			xchat.prnt("%s: Changing nick.." % __module_name__)
		#endif
	#endif
	return xchat.EAT_NONE
#enddef

def DoIdentify(word,word_eol,userdata):
	global dInfo
	sServ=xchat.get_info("network")
	if sServ in dInfo and dInfo[sServ]["on"] == 2:
		xchat.command("nickserv IDENTIFY %s" % dInfo[sServ]["pass"])
		del dInfo[sServ]
		xchat.prnt("%s: Identifying.." % __module_name__)
	#endif
	return xchat.EAT_NONE
#enddef

def CheckQuit(word,word_eol,userdata):
	global dInfo
	sServ=xchat.get_info("network")
	if sServ in dInfo and word[0] == dInfo[sServ]["nick"]:
		xchat.command("nick %s" % dInfo[sServ]["nick"])
		if "timer" in dInfo[sServ]:
			xchat.unhook(dInfo[sServ]["timer"])
		#endif
		del dInfo[sServ]
	#endif
#enddef

def CheckPart(word,word_eol,userdata):
	global dInfo
	sServ=xchat.get_info("network")
	if sServ in dInfo and word[0] == dInfo[sServ]["nick"]: WhoLoopStart()
#enddef

def CheckJoin(word,word_eol,userdata):
	global dInfo
	sServ=xchat.get_info("network")
	if sServ in dInfo and word[0] == dInfo[sServ]["nick"]:
		dInfo[sServ]["on"] = 5
		if "timer" in dInfo[sServ]:
			xchat.unhook(dInfo[sServ]["timer"])
			del dInfo[sServ]["timer"]
		#endif
	#endif
#enddef

def WhoLoopStart():
	global dInfo
	sServ=xchat.get_info("network")
	if sServ in dInfo:
		dInfo[sServ]["on"] = 4
		dInfo[sServ]["timer"] = xchat.hook_timer(300000, WhoStoleIt) #Check every five minutes
	#endif
#enddef

def WhoStoleIt(userdata):
	global dInfo
	sServ=xchat.get_info("network")
	if sServ in dInfo:
		xchat.command("whois %s" % dInfo[sServ]["nick"])
		dInfo[sServ]["who1"] = xchat.hook_print("Generic Message", Test)
		dInfo[sServ]["who2"] = xchat.hook_print("WhoIs End", WhoEnd)
	#endif
#endif

def Test(word,word_eol,userdata):
	global dInfo
	sServ=xchat.get_info("network")
	xchat.prnt(' '.join(word))
#enddef

def WhoEnd(word,word_eol,userdata):
	global dInfo
	sServ=xchat.get_info("network")
	if sServ in dInfo:
		xchat.unhook(dInfo[sServ]["who1"])
		xchat.unhook(dInfo[sServ]["who2"])
	#endif
#enddef

def CheckUserList(word,word_eol,userdata):
	global dInfo
	sServ=xchat.get_info("network")
	if sServ in dInfo and dInfo[sServ]["on"] == 3:
		lChannels = xchat.get_list("channels")
		for i in lChannels:
			if i.type == 2:
				lUsers = i.context.get_list("users")
				for j in lUsers:
					if j.nick == dInfo[sServ]["nick"]:
						dInfo[sServ]["on"] = 5 # Wait for quit
						return
					#endif
				#endfor
			#endif
		#endfor
		WhoLoopStart()
	#endif
#enddef

xchat.hook_print("Notice", DoNick)
xchat.hook_print("Your Nick Changing", DoIdentify)
xchat.hook_print("Join", CheckJoin)
xchat.hook_print("Quit", CheckQuit)
xchat.hook_print("Part", CheckPart)
xchat.hook_print("You Join", CheckUserList)

xchat.hook_server("376",GhostThatFucker,True) #MOTD End
xchat.hook_server("422",GhostThatFucker,True) #MOTD Missing
xchat.hook_command("gnick",GhostThatFucker,False)
xchat.prnt("Loaded %s version %s." % (__module_name__,__module_version__))
