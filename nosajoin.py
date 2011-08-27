__module_name__ = "No SaJoin"
__module_author__ = "Wa"
__module_version__ = "0.0"
__module_description__ = "Autopart rooms that you don't join yourself"

import xchat

dDidJoin = {}
def DidJoin(word,word_eol,userdata):
	global dDidJoin
	dDidJoin[word[1]] = True
#enddef

def OrDidI(word,word_eol,userdata):
	global dDidJoin
	sName = word[0]
	sName = sName[1:sName.find("!")]
	if sName == xchat.get_info("nick"):
		sChan = word[2]
		if sChan[0] == ":": sChan = sChan[1:]
		if sChan not in dDidJoin:
			xchat.command("part " + sChan)
		else:
			del dDidJoin[sChan]
		#endif
	#endif
#enddef

xchat.hook_server("JOIN",OrDidI)
xchat.hook_command("join",DidJoin)
