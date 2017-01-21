__module_name__ = "YouTubeInfo"
__module_author__ = "Sapphire Becker (logicplace.com)"
__module_version__ = "0.9"
__module_description__ = "Display YouTube video's info when a link is given."

import os
import sys
import xchat
#import fauxchat as xchat
import re
import string
import math
import json
import urllib2

# pip install isodate
import isodate

sPathToSettings = xchat.get_info("xchatdir")
warnedv3key = False
YTCategories = {}

class StopExecution(Exception): pass
class YTIError(Exception):
   def __init__(self, err, sel, chl):
       self.error = err
       self.selector = sel
       self.child = chl
   def __str__(self):
       return "YTI Error: %s. In Format String: Selector %i, Child %i." % (self.selector, self.child)

dSettings = {
	"string": "\x0306(%id%)\x0f \"\x0303%+snippet.title%\x0f\" by \"\x0302%+snippet.channelTitle%\x0f\" is \"\x0303%category%\x0f\" - Length: \x0305%hr%:%mn%:%sc%\x0f",
	"showdesc": '0',
	"chanignores[]": [],
	"v3key": None,
	"regionCode": "US",
}

if not os.path.isdir(sPathToSettings + "/settings"):
	os.mkdir(sPathToSettings + "/settings")

if os.path.isfile(sPathToSettings + "/settings/youtubeinfo"):
	hF = open(sPathToSettings + "/settings/youtubeinfo", "r")
	lSetLines = hF.readlines()
	hF.close()
	for sI in lSetLines:
		lI = sI.rstrip().split('=', 1)
		if len(lI) == 2:
			if lI[0][-2:] == "[]":
				lI[1] = lI[1].split(", ")
			#endif
			dSettings[lI[0]] = lI[1]
		#endif
	#endfor
#endif

def SaveSettings():
	global sPathToSettings
	hF = open(sPathToSettings + "/settings/youtubeinfo", "w")
	for sI, sV in dSettings.iteritems():
		if sI[-2:] == "[]":
			sV = ','.join(sV)
		#endif
		hF.write("%s=%s\n" % (sI, sV))
	hF.close()
#enddef

def YTv3fetch(command, args, raiseStopExecution=False):
	global dSettings
	url = "https://www.googleapis.com/youtube/v3/" + command + "?"
	if dSettings["v3key"]: url += "key=" + dSettings["v3key"] + "&"

	for arg, val in args.items(): url += arg + "=" + val + "&"
	
	hInfo = urllib2.urlopen(url[:-1])
	sInfo = hInfo.read()
	if sInfo:
		dJSON = json.loads(sInfo)
		if "error" in dJSON:
			if dJSON["error"]["errors"][0]["reason"] == "dailyLimitExceededUnreg":
				if not warnedv3key:
					xchat.prnt("Unregistered usage exceeded. Set your YouTube API v3 key with: /yti v3key YOUR_KEY")
				#endif
				if raiseStopExecution: raise StopExecution()
				else: return None
			else:
				errors = [e["message"] for e in dJSON["error"]["errors"]]
				if len(errors) == 1:
					xchat.prnt("Encountered error while retrieving YTI for %s: %s" % (sI, errors[0]))
				else:
					xchat.prnt("Encountered multiple errors while retrieving YTI for %i:" % sI)
					for e in errors: xchat.prnt("  " + e)
				#endif
			#endif
			return None
		#endif

		return dJSON
	#endif
#enddef

dAntiSpam = {}
reFindyt = re.compile(r'https?://(?:[^.]*\.?youtube\.com/watch\?.*v=|youtu.be/)([a-zA-Z0-9_\-]+)')
reSelector = re.compile(r'^([a-zA-Z][a-zA-Z0-9]*)(?:\(([0-9]+)\))?$')
def LookForLink(word, word_eol, userdata, alt = 0):
	global reFindyt, reSelector, YTCategories
	if alt == 0 and xchat.get_info("channel") in dSettings["chanignores[]"]: return
	lLinks = reFindyt.findall(word_eol[1])
	for sI in lLinks:
		if alt != 0 or sI not in dAntiSpam:
			dAntiSpam[sI] = True
			try:
				try: 
					dJSON = YTv3fetch("videos", {
						"part": "snippet,contentDetails",
						"id": sI,
					}, True)
				except StopExecution: return
				
				if dJSON:
					dJSON = dJSON["items"][0]

					# Get the duration information.
					tdDuration = isodate.parse_duration(dJSON["contentDetails"]["duration"])
					iVidSecs = tdDuration.seconds
					iVidMins = int(math.floor(iVidSecs / 60));
					iVidSecs -= iVidMins * 60
					iVidHrs = int(math.floor(iVidMins / 60));
					iVidMins -= iVidHrs * 60

					# Format the output string
					lFmt = dSettings['string'].split("%")
					prnt = u""
					for iI, sV in enumerate(lFmt):
						if iI % 2 == 0: prnt += sV
						else:
							if sV[0] == '+':
								sV = sV[1:]
								## First check backwards compatibility stuff
								backwardsCompat = {
									"title": "snippet.title",
									"author>name": "snippet.channelTitle",
								}

								if sV == "media:category":
									prnt += GetCategory(dJSON)
									continue
								else:
									for sBCK, sBCV in backwardsCompat.items():
										if sV == sBCK:
											sV = sBCV
											break
										#endif
									#endfor
								#endif

								## sV is now a basic, JSON selector to a string or number
								lV = sV.split(".") ## Split children
								hPar = dJSON
								bDidAttr = False
								for iId, sX in enumerate(lV):
									## Get what result we're reading
									hSel = reSelector.match(sX)
									if hSel:
										sTag = hSel.group(1)
										sRes = hSel.group(2)

										try:
											hPar = hPar[sTag]
											if sRes is not None: hPar = hPar[int(sRes)]
										except (AttributeError, KeyError):
											raise YTIError('Invalid selector "%s", entry not found.' % sX, math.floor(iI / 2), iId)
										#endtry
									else:
										raise YTIError('Invalid selector "%s".' % sX, math.floor(iI / 2), iId)
									#endif
								#endfor
								if type(hPar) not in [list, dict]:
									prnt += unicode(hPar)
								#endif
							elif sV == "id": prnt += sI
							elif sV == "hr": prnt += str(iVidHrs)
							elif sV == "mn": prnt += u"%02i" % iVidMins
							elif sV == "sc": prnt += u"%02i" % iVidSecs
							elif sV == "category": prnt += GetCategory(dJSON)
							#endif
						#endif
					#endfor

					if alt == 1:
						xchat.command(("say " + prnt).encode('utf-8'))
					else:
						xchat.emit_print(userdata, *word)
						xchat.prnt(prnt.encode('utf-8'))
					#endif

					if dSettings['showdesc'] != '0':
						sDesc = dJSON["snippet"]["description"]
						sDesc = sDesc.replace("\n", " ")
						if alt == 1: xchat.command(("say " + sDesc[0:100]).encode('utf-8'))
						else: xchat.prnt(sDesc[0:100].encode('utf-8'))
						#endif
					#endif

					return xchat.EAT_XCHAT
				else:
					xchat.prnt("No data returned")
				#endif

			except urllib2.HTTPError as e:
				xchat.prnt("Server error, code %i." % e.code)
				for i in e:
					 xchat.prnt("Error: " + i)
			except urllib2.URLError as e:
				xchat.prnt("Error connecting to server: %s" % e.reason)
			except YTIError as e:
				xchat.prnt(str(e))
			except:
				print("Unexpected error:", sys.exc_info()[0])
				raise
			#endtry
		#endif
	#endfor

	return xchat.EAT_NONE
#enddef

def GetCategories():
	global dSettings, YTCategories
	dJSON = YTv3fetch("videoCategories", {
		"part": "snippet",
		"regionCode": dSettings["regionCode"],
	})

	if dJSON:
		YTCategories = {}
		for dItem in dJSON["items"]:
			YTCategories[dItem["id"]] = dItem["snippet"]["title"]
		#endfor
	else:
		xchat.prnt("Failure fetching YT categories.")
	#endif
#enddef

def GetCategory(dJSON):
	try: return YTCategories[dJSON["snippet"]["categoryId"]]
	except KeyError:
		return "Unknown (%s)" % dJSON["snippet"]["categoryId"]
	#endtry
#endif

def Settings(word, word_eol, userdata):
	global dSettings
	if len(word) >= 3:
		if word[1] == 'say':
			LookForLink(['', word[2], ''], ['', word[2], ''], None, 1)
			return
		elif word[1] == 'ignore':
			if word[2][0] == '#': 
				if word[2] not in dSettings["chanignores[]"]:
					dSettings["chanignores[]"].append(word[2])
				#endif
				xchat.prnt("Ignoring links in " + word[2])
			else:
				xchat.prnt("Ignore what?")
			#endif
		elif word[1] == 'unignore':
			if word[2][0] == '#': 
				if word[2] in dSettings["chanignores[]"]:
					dSettings["chanignores[]"].remove(word[2])
				#endif
				xchat.prnt("Monitoring links in " + word[2])
			else:
				xchat.prnt("Unignore what?")
			#endif
		else:
			dSettings[word[1]] = word_eol[2]
			xchat.prnt("Set \"%s\"" % word[1])
			if word[1] == "regionCode": GetCategories()
		#endif
		SaveSettings()
	elif len(word) == 2:
		iTmp = LookForLink(['YTI: ', word[1], ''], ['', '', ''], None, 2)
		if iTmp == xchat.EAT_NONE and word[1] in dSettings:
			sDots = '.'*(29 - len(word[1]))
			sTmpStr = "%s\x0312%s\x0f\x0311:\x0f %s" % (word[1], sDots, dSettings[word[1]])
			xchat.prnt(sTmpStr)
		#endif
	else:
		for sI, sV in dSettings.iteritems():
			sDots = '.'*(29 - len(sI))
			sTmpStr = "%s\x0312%s\x0f\x0311:\x0f %s" % (sI, sDots, sV)
			xchat.prnt(sTmpStr)
		#endfor
	#endif

	return xchat.EAT_ALL
#enddef

lEvents4L4l = [
	  "Channel Action"
	, "Channel Action Hilight"
	, "Channel Message"
	, "Channel Msg Hilight"
]

for sI in lEvents4L4l:
	xchat.hook_print(sI, LookForLink, sI)
#endfor

xchat.hook_command("yti", Settings)
xchat.prnt("Loaded %s version %s." % (__module_name__, __module_version__))

GetCategories()

import sys
if len(sys.argv) > 1:
	LookForLink(['', sys.argv[1], ''], ['', sys.argv[1], ''], None)
