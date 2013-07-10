__module_name__ = "H-tan"
__module_author__ = "Muma (logicplace.com)"
__module_version__ = "1.0"
__module_description__ = "#japanese interchannl bot (H-tan) to emit_print"

import xchat, re

def Host(nick, network): return S(nick + "!~linked@" + network)
def S(arg): return arg.replace("\x02", "").replace("\x0f", "")

def Join(args): return (S(args[0]), S(args[1]), Host(args[0], args[2]))
def Part(args): return (S(args[0]), Host(args[0], args[2]), S(args[1]), args[3])
def Quit(args): return (S(args[0]), args[2], Host(args[0], args[1]))
def Nick(args): return (S(args[0] + "@" + args[2]), S(args[1]))
def Message(args): return (S(args[0]), args[1])
def Action(args): return (S(args[0]), args[1])

messages = {
	"Join": (Join, re.compile(r'- Join ([^ ]+) to ([^ ]+) on ([^ ]+)')),
	"Part": (Part, re.compile(r'- Part ([^ ]+) from ([^ ]+) on ([^:]+)(?::[\x02\x0f]? (.+))?')),
	"Quit": (Quit, re.compile(r'- Quit ([^ ]+) from ([^:]+)(?::[\x02\x0f]? (.+))?')),
	"Change Nick": (Nick, re.compile(r'- ([^ ]+) is now known as ([^ ]+) on (.+)')),
	"Message": (Message, re.compile(r'<\x02?[~&@%+]?([^>]+)> (.+)')),
	"Action": (Action, re.compile(r'\* \x02?[~&@%+]?([^ ]+) (.+)')),
}

def ProxyMessage(word, word_eol, userdata):
	# Only care if it's on a proper channel.
	if word[2] in ("#japanese", "#japanese.utf8"):
		nick = word[0][1:word[0].find("!")]
		# Only care if it's the bot.
		if nick not in ["H-tan", "U-tan"]: return xchat.EAT_NONE

		msg = word_eol[3][1:]

		# Check messages.
		for k, x in messages.iteritems():
			# Check against regex.
			mo = x[1].search(msg)
			if mo:
				# Run argument structuring function.
				args = x[0](mo.groups(""))

				# There are two options for part.
				if k == "Part":
					if args[3]: msgid = "Part with Reason"
					else: msgid = "Part"
				# We want to keep if it's a highlight intact, so pass the event along.
				elif k == "Message" or k == "Action":
					if k == "Action": msg = "\x01ACTION " + args[1] + "\x01"
					else: msg = args[1]
					# Emulate the message so that it will promote the channel status appropriately.
					xchat.command("RECV :%s PRIVMSG %s :%s" % (
						Host(*args[0].split("@")), word[2], msg
					))
					return xchat.EAT_XCHAT
				# Otherwise use the key.
				else: msgid = k

				# Emit the actual message.
				xchat.emit_print(msgid, *args)

				# Tell xchat not to print H-tan's Channel Message.
				return xchat.EAT_XCHAT
			#endif
		#endfor

		return xchat.EAT_NONE
#enddef

xchat.hook_server("PRIVMSG", ProxyMessage)

xchat.prnt("Loaded %s version %s." % (__module_name__,__module_version__))
