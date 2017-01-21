__module_name__ = "No SAJoin"
__module_author__ = "Sapphire Becker"
__module_version__ = "1.0"
__module_description__ = "Prevents being /sajoin'd by an IRCOp"

import xchat

didJoin = {}
def DidJoin(word,word_eol,userdata):
	global didJoin
	didJoin[xchat.get_info("server") + "/" + word[1]] = True
#enddef

def fc(word): return word[1:] if word[0] == ":" else word

def OrDidI(word,word_eol,userdata):
	global didJoin
	nick = word[0]
	nick = nick[1:nick.find("!")]
	if nick == xchat.get_info("nick"):
		chan = fc(word[2])
		if chan[0] == ":": chan = chan[1:]
		servChan = xchat.get_info("server") + "/" + chan
		if servChan not in didJoin:
			xchat.command("part " + chan)
			return xchat.EAT_ALL
		else:
			del didJoin[servChan]
		#endif
	#endif
#enddef

xchat.hook_server("JOIN",OrDidI)
xchat.hook_command("join",DidJoin)
xchat.prnt("Loaded %s version %s." % (__module_name__,__module_version__))
