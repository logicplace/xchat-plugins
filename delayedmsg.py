__module_name__ = "DelayedMessage"
__module_author__ = "Wa (logicplace.com)"
__module_version__ = "1.0"
__module_description__ = "Delayed message for people that don't read the topic (everyone)"

import xchat

sSettings = xchat.get_info("xchatdir")+"/settings/delayedmsg.txt"
dSettings = {}

try:
	hSet = open(sSettings,"r")
	lSettings = map(str.strip,hSet.readlines())
	for i in range(0,len(lSettings),4):
		sHost,sChan = tuple(lSettings[i].split("|"))
		if sHost not in dSettings: dSettings[sHost] = {}
		dSettings[sHost][sChan] = [
			lSettings[i+1],
			int(lSettings[i+2]),
			lSettings[i+3]
		]
	#endfor
	hSet.close()
except: pass

dTimers = {}
def ReadySend(word,word_eol,userdata):
	global dTimers
	if GetOpt(0) != "none" and GetOpt(2):
		#xchat.prnt("%s joined channel..prepping for message." % word[0])
		dTimers[word[0]] = xchat.hook_timer(GetOpt(1), SendMessage, [word[0],xchat.get_context()])
	#endif
	return xchat.EAT_NONE
#enddef

lSent = []
def SendMessage(userdata):
	global dTimers,lSent
	# Is user still around?
	if userdata[0] in map((lambda x: x.nick),userdata[1].get_list("users")):
		method = GetOpt(0,userdata[1])
		if method != "say": lSent.append(userdata[0])
		xchat.command("%s %s %s" % (method,userdata[0],GetOpt(2,userdata[1])))
		#xchat.prnt("Sent %s the message." % userdata[0])
	#else:
		#xchat.prnt("%s left early." % userdata[0])
	#endif
	xchat.unhook(dTimers[userdata[0]])
#enddef

def BlockSelf(word,word_eol,userdata):
	if word[0] in lSent:
		lSent.remove(word[0])
		return xchat.EAT_XCHAT
	#endif
	return xchat.EAT_NONE
#enddef

def SaveSettings(userdata):
	global dSettings
	hSet = open(sSettings,"w")
	for sHost in dSettings:
		for sChan in dSettings[sHost]:
			hSet.write(sHost+"|"+sChan+"\r\n")
			hSet.writelines(map((lambda x: str(x)+"\r\n"),dSettings[sHost][sChan]))
		#endfor
	#endfor
	hSet.close()
#enddef

def AssureOpts(context=xchat):
	global dSettings
	sHost,sChan = context.get_info("host"),context.get_info("channel")
	if sHost not in dSettings:
		dSettings[sHost] = {
			sChan: ["none",5000,""]
		}
	elif sChan not in dSettings[sHost]:
		dSettings[sHost][sChan] = ["none",5000,""]
	#endif
	return sHost,sChan
#enddef

def SetOpt(opt,val):
	global dSettings
	sHost,sChan = AssureOpts()
	dSettings[sHost][sChan][opt] = val
#enddef

def GetOpt(opt,context=xchat):
	global dSettings
	sHost,sChan = AssureOpts(context)
	return dSettings[sHost][sChan][opt]
#enddef

def Settings(word,word_eol,userdata):
	sChan = xchat.get_info("channel")
	if len(word) >= 3:
		if word[1] == 'msg':
			SetOpt(2,word_eol[2])
			xchat.prnt("Set message for %s to: %s" % (sChan,word_eol[2]))
		if word[1] == 'delay':
			try:
				SetOpt(1,int(word[2]))
				xchat.prnt("Set delay for %s to: %s" % (sChan,word[2]))
			except: xchat.prnt("Pass delay time in milliseconds")
		elif word[1] == 'method':
			if word[2] in ["notice","msg","say","none"]:
				SetOpt(0,word[2])
				xchat.prnt("Set method for %s to: %s" % (sChan,word[2]))
			else:
				xchat.prnt("Method options: notice, msg, say, none")
			#end
		#endif
	elif len(word) == 2:
		if word[1] == 'msg':
			xchat.prnt("/dlm msg Message to send to people here")
		if word[1] == 'msg':
			xchat.prnt("/dlm delay milliseconds")
		elif word[1] == 'method':
			xchat.prnt("/dlm method notice|msg|say|none")
		elif word[1] == 'show':
			xchat.prnt("Settings for %s:" % sChan)
			xchat.prnt("Message: "+GetOpt(2))
			xchat.prnt("Delay: "+str(GetOpt(1)))
			xchat.prnt("Method: "+GetOpt(0))
		#endif
	else:
		xchat.prnt("/dlm msg|method|delay arguments")
	#endif
	return xchat.EAT_ALL
#enddef

xchat.hook_command("dlm",Settings)
xchat.hook_print("Join",ReadySend)

for x in ["Notice Send","Message Send"]:
	xchat.hook_print(x,BlockSelf)
#endfor

xchat.hook_unload(SaveSettings)

xchat.prnt("Loaded %s version %s." % (__module_name__,__module_version__))

