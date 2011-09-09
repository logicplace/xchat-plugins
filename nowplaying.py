import fauxchat as xchat
import sys
import os
import re
import dbus

__module_name__ = "NowPlaying"
__module_author__ = "Wa (logicplace.com)"
__module_version__ = "0.1"
__module_description__ = "Announce what's now playing on your [linux] system"

#TODO: Why does this crash xchat on exit?

bus = dbus.SessionBus()
players = []

settingsLoc = os.path.join(xchat.get_info("xchatdir"),"settings")
try: os.mkdir(settingsLoc)
except OSError: pass
settingsLoc = os.path.join(settingsLoc,"nowplaying")

try:
	f = open(settingsLoc,"r")
	now_playing_message = f.read() 
	f.close()
except IOError: now_playing_message = "me is listening to %(title) - %(artist)"

class Player:
	def __init__(self,name,dbusInfo,playing,song):
		global bus
		self.name = name
		
		self.interface = []
		nolist = False
		if type(dbusInfo) is not list:
			nolist = True
			dbusInfo = [dbusInfo]
		#endif
		for x in dbusInfo:
			try:
				self.interface.append(dbus.Interface(
					bus.get_object(x["sender"],x["path"]),
					x["interface"] if "interface" in x else x["sender"]
				))
			except dbus.exceptions.DBusException:
				self.interface = None
				nolist = False
				break
			except x:
				self.interface = None
				nolist = False
				break
				xchat.prnt(x)
			#endtry
		#endfor
		if nolist: self.interface = self.interface[0]
		
		# Function that returns true (player is playing music) or false (player is off)
		self._playing = playing
		# Function that returns song info: {
		# 	title:  Title of the song
		# 	artist: Artists' names
		# 	album:  Album title
		# 	url:    URL related to the song
		# 	length: Total length of the song in seconds
		# 	time:   Current place in the song in seconds
		# 	player: Name of the program playing the song # Added by this class! 
		# }
		self._song = song
	#enddef
	
	def playing(self):
		if self.interface is None: return False
		return self._playing(self.interface)
	#endif
	
	def song(self):
		if self.interface is None: return {}
		ret = self._song(self.interface)
		ret["player"] = self.name
		return ret
	#enddef
#endclass

### Pithos ###
def pithosGetCurrentSong(self):
	data = self.GetCurrentSong()
	return {
		"album": unicode(data["album"]),
		"artist": unicode(data["artist"]),
		"title": unicode(data["title"]),
		"url": unicode(data["songDetailURL"]),
	}
#enddef

players.append(Player(
	"Pithos (Pandora)",{
		"sender": "net.kevinmehall.Pithos",
		"path": "/net/kevinmehall/Pithos"
	},
	(lambda self: bool(self.IsPlaying())),
	pithosGetCurrentSong
))

### Audacious ###
def audGetCurrentTrack(self):
	curTrack = self[0].GetCurrentTrack()
	return {
		"title": self[1].SongTitle(curTrack)
		#TODO: More data
	}
#enddef

players.append(Player(
	"Audacious",[{
		"sender": "org.mpris.audacious",
		"path": "/TrackList",
		"interface": "org.freedesktop.MediaPlayer",
	},{
		"sender": "org.mpris.audacious",
		"path": "/org/atheme/audacious",
		"interface": "org.atheme.audacious"
	}],
	(lambda self: True), #TODO: Fix
	audGetCurrentTrack
))

### XChat Stuff ###
bsection = re.compile("%\{([^}]+)\}")
psection = re.compile("(%\(([a-z]+)\))")
def NowPlaying(word,word_eol,userdata):
	msg = now_playing_message
	if len(word) > 1: msg = word[1]+" "+msg.split(" ",1)[1]
	
	songData = None
	for x in players:
		if x.playing(): 
			songData = x.song()
			break
		#endif
	#endfor
	
	if songData:
		msgs = bsection.split(msg)
		msg = ""
		for i in range(len(msgs)):
			if i%2 == 0: # replace with "" if non existent
				msg += psection.sub((lambda m: songData[m.group(2)] if m.group(2) in songData else ""),msgs[i])
			else:
				try: msg += psection.sub(r'\1s',msgs[i]) % songData
				except KeyError: pass
			#endif
		#endfor
		xchat.command(msg)
	else:
		xchat.prnt("Not playing anything")
	#endif
	
	return xchat.EAT_XCHAT
#enddef

def SetMessage(word,word_eol,userdata):
	global now_playing_message
	if word[1] == "now_playing_message":
		if len(word_eol) > 2: # Set
			now_playing_message = word_eol[2]
			xchat.prnt("%s set to: %s" % (word[1],word_eol[2]))
		else:
			dots = 29-len(word[1])
			xchat.prnt(word[1]+"\00318"+("."*dots)+"\00319:\x0f "+now_playing_message)
		#endif
		return xchat.EAT_XCHAT
	#endif
	
	return xchat.EAT_NONE
#enddef

def SaveMessage(userdata):
	f = open(settingsLoc,"w")
	f.write(now_playing_message) 
	f.close()
#enddef

xchat.hook_command("np",NowPlaying)
xchat.hook_command("set",SetMessage)
xchat.hook_unload(SaveMessage)
xchat.prnt("Loaded %s version %s." % (__module_name__,__module_version__))
if xchat.FAUX: xchat.loop()
