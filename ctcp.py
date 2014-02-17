__module_name__ = "CTCP"
__module_author__ = "Wa (logicplace.com)"
__module_version__ = "1.1"
__module_description__ = "Handles some extra ctcp functionality"

import xchat
from PIL import Image
import os, re, datetime

pathToVercond = xchat.get_info("xchatdir") + "/settings/vercond.txt"
pathToSettings = xchat.get_info("xchatdir") + "/settings/ctcp"

try:
	verFile = open(pathToVercond, "r")
	verCond = verFile.read().split()
	verFile.close()
except IOError: verCond = ["true"]

def SetVerCond(word, word_eol, userdata):
	global verCond
	# Set
	verCond = (word + [None])[1:3]

	# Test
	xchat.prnt("Set vercond. Condition is %s here." % (
		"true" if CheckCondition(*verCond) else "false"
	))
	return xchat.EAT_ALL
#enddef

def SaveVerCond(userdata):
	verFile = open(pathToVercond, "w")
	verFile.write(" ".join(verCond))
	verFile.close()
#enddef

def VersionCond(word, word_eol, userdata):
	if word_eol[3] != ":\x01VERSION\x01": return xchat.EAT_NONE
	if CheckCondition(*verCond): return xchat.EAT_NONE
	xchat.prnt("Prevented version request by %s" % word[0].split("!")[0].lstrip(":"))
	return xchat.EAT_ALL
#enddef

def CheckCondition(cond, arg):
	if cond in ["ifuser", "ifnotuser"]:
		# EVERY CHANNEL LIKE A RETARD, XCHAT
		# WHY NOT JUST HAVE xchat.get_info("user") HUH? FUCK YOU
		username = None
		serv = xchat.get_info("server")
		for ch in xchat.get_list("channels"):
			if ch.server == serv:
				nick = xchat.get_info("nick")
				for user in ch.context.get_list("users"):
					if user.nick == nick:
						# FURTHER TROLLING?
						username = user.host.split("@")[0].lstrip("~")
						break
					#endif
				#endfor
			#endif
		#endfor
		if not username: return False
		if "not" in cond: return arg != username
		else: return arg == username
	elif cond == "true": return True
	return False
#enddef

def IfCondition(word, word_eol, userdata):
	if CheckCondition(userdata, word[1]): xchat.command(word_eol[2])
	return xchat.EAT_XCHAT
#enddef

def FaceExists():
	if os.path.isfile(pathToSettings + "/face.png"): return "YES"
	if os.path.isfile(pathToSettings + "/face.txt"): return "ASCII"
	return "NO"
#enddef

def Face2ASCII(flat):
	#try:
		img = Image.open(pathToSettings + "/face.png")
		img = img.resize((32, 16), Image.BICUBIC)

		text = ["+--------------------------------+"]
		tidx = 1
		bgcolor = 0 #temporarily static
		irccols = [
			[0xFF, 0xFF, 0xFF], [0x00, 0x00, 0x00], [0x36, 0x36, 0xB2], [0x2A, 0x8C, 0x2A], [0xC3, 0x3B, 0x3B], 
			[0xC7, 0x32, 0x32], [0x80, 0x26, 0x7F], [0x66, 0x36, 0x1F], [0xD9, 0xA6, 0x41], [0x3D, 0xCC, 0x3D], 
			[0x1A, 0x55, 0x55], [0x2F, 0x8C, 0x74], [0x45, 0x45, 0xE6], [0xB0, 0x37, 0xB0], [0x4C, 0x4C, 0x4C], 
			[0x95, 0x95, 0x95]
		]
		chars = "#@8&$WM0QO2C1|/\\mxzvc;:=~- "
		clen = len(chars)-1
		calc = 255/clen
		#xchat.prnt("calc: %i"%calc)
		for y in range(16):
			if flat: text.append("|")
			else: text.append("|01, %02i" % bgcolor)
			#derp = ""
			for x in range(32):
				color = img.getpixel((x, y))
				light = (color[0] + color[1] + color[2]) / 3
				#derp += "%i, "%light
				irccc = 0
				irccm = 1000
				if not flat:
					for c in range(len(irccols)):
						rcomp = abs(irccols[c][0] - color[0])
						gcomp = abs(irccols[c][1] - color[1])
						bcomp = abs(irccols[c][2] - color[2])
						lcomp = (rcomp + gcomp + bcomp) / 3
						if lcomp < irccm:
							irccm = lcomp
							irccc = c
							if irccm == 0: break
						#endif
					#endfor
					text[tidx] += "%02i" % irccc
				text[tidx] += chars[min(light/calc, clen)]
			#endfor
			if not flat: text[tidx] += ""
			text[tidx] += "|"
			tidx += 1
			#xchat.prnt(derp)
		#endfor
		text.append(text[0])
		return text
	#except:
		#return None
	#endtry
#enddef

def StripColor(text):
	for i in range(len(text)):
		pass
#enddef

alreadysentpic={}
alreadysentascii={}

def DoFace(word, word_eol, userdata):
	if len(word) > 2:
		word[2] = word[2].lower()
		if word[2] == "exist":
			xchat.command("nctcp %s %s" % (word[1], FaceExists()))
			return xchat.EAT_ALL
		elif word[2] == "ascii":
			if word[1] in alreadysentascii: return xchat.EAT_ALL
			alreadysentascii[word[1]] = True;
			img = None
			try:
				img = open(pathToSettings+"/face.txt").readlines()
				if len(word) > 3 and word[3] == "flat": img=StripColor(img)
			except:
				if len(word) > 3 and word[3] == "flat": img=Face2ASCII(True)
				else: img=Face2ASCII(False)
			#endtry
			if img is not None:
				for i in img:
					xchat.command("nctcp %s %s" % (word[1], i))
				#endfor
			else:
				xchat.command("nctcp %s ERRMSG Unable to load/parse/send file." % word[1])
			#endif
			return xchat.EAT_ALL
		#endif
	if word[1] in alreadysentpic: return xchat.EAT_ALL
	alreadysentpic[word[1]] = True;
	if os.path.isfile(pathToSettings+"/face.png"):
		xchat.command("dcc send %s %s/.xchat2/settings/ctcp/face.png" % (word[1], os.getcwd()))
		#should be sendface I guess but xchat doesn't support that
	#endif
	return xchat.EAT_ALL
#enddef

def DumpFile(word, word_eol, userdata):
	try:
		text = open(pathToSettings+"/%s.txt" % word[2]).readlines()
		for i in text:
			xchat.command("nctcp %s %s" % (word[1], i))
	except:
		xchat.command("nctcp %s ERRMSG Unable to load/parse/send file." % word[1])
	#endtry
	return xchat.EAT_ALL
#enddef

retime = re.compile("(?:(-?\d+)d)?(?:(-?\d+)h)?(?:(-?\d+)m)?(?:(-?\d+)s)?")
def OffsetTime(word, word_eol, userdata):
	d, h, m, s = tuple(map(lambda x: int(x) if x else 0, retime.match(word[2]).groups()))
	# XChat's format example: Sat Dec 15 19:38:08
	form = word_eol[3] if len(word_eol) > 3 else "%a %b %d %H:%M:%S"
	time = datetime.datetime.now() + datetime.timedelta(days=d, hours=h, minutes=m, seconds=s)
	xchat.command("nctcp %s TIME %s" % (word[1], time.strftime(form)))
	return xchat.EAT_XCHAT
#enddef

xchat.hook_command("face", DoFace)
xchat.hook_command("dump", DumpFile)
xchat.hook_command("vercond", SetVerCond)
xchat.hook_command("offtime", OffsetTime)
xchat.hook_server("privmsg", VersionCond)
for x in ["ifuser", "ifnotuser"]:
	xchat.hook_command(x, IfCondition, x)
#endfor
xchat.hook_unload(SaveVerCond)

xchat.prnt("Loaded %s version %s." % (__module_name__,__module_version__))
