__module_name__ = "VoiceOnce"
__module_author__ = "Sapphire Becker (logicplace.com)"
__module_version__ = "0.1"
__module_description__ = "Voices entrants on their first join"

import xchat

hostsThatJoined = {}
okChannels = {}

def CheckJoin(word,word_eol,userdata):
	global hostsThatJoined,okChannels
	context = xchat.get_context()
	if context.get_info("channel") in okChannels:
		host = word[2].split("@")[1]
		if host not in hostsThatJoined:
			hostsThatJoined[host] = True
			context.command("mode +v "+word[0])
		#endif
	#endif
	return xchat.EAT_NONE
#enddef

def VoiceChannel(word,word_eol,userdata):
	global okChannels
	context = xchat.get_context()
	cn = context.get_info("channel")
	okChannels[cn] = True
	xchat.prnt("Automatically voicing newcomers in "+cn)
	return xchat.EAT_ALL
#enddef

def UnVoiceChannel(word,word_eol,userdata):
	global okChannels
	context = xchat.get_context()
	cn = context.get_info("channel")
	del okChannels[cn]
	xchat.prnt("No longer automatically voicing newcomers in "+cn)
	return xchat.EAT_ALL
#enddef

def ResetChannel(word,word_eol,userdata):
	global hostsThatJoined
	context = xchat.get_context()
	del hostsThatJoined
	hostsThatJoined = {}
	cn = context.get_info("channel")
	xchat.prnt("Everyone is now a newcomer in "+cn)
	return xchat.EAT_ALL
#enddef

xchat.hook_print("Join", CheckJoin)
xchat.hook_command("autovoice",VoiceChannel,False)
xchat.hook_command("unautovoice",UnVoiceChannel,False)
xchat.hook_command("resetvoice",ResetChannel,False)
xchat.prnt("Loaded %s version %s." % (__module_name__,__module_version__))
