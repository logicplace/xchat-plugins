__module_name__ = "YouTubeInfo"
__module_author__ = "Sapphire Becker (logicplace.com)"
__module_version__ = "0.8.1"
__module_description__ = "Display YouTube video's info when a link is given."

import os
import sys
import xchat
#sys.path.append("%s/.python"%(os.environ['HOME'] or os.environ['USERPROFILE']))
#from fauxchat import *
import re
import string
import math
from xml.dom.minidom import parseString
import urllib2

sPathToSettings = xchat.get_info("xchatdir")

class YTIError(Exception):
   def __init__(self, err, sel,chl):
       self.error = err
       self.selector = sel
       self.child = chl
   def __str__(self):
       return "YTI Error: %s. In Format String: Selector %i, Child %i."%(self.selector,self.child)

dSettings={
	"string":"\x0306(%id%)\x0f \"\x0303%+title%\x0f\" by \"\x0302%+author>name%\x0f\" is \"\x0303%+media:category%\x0f\" - Length: \x0305%hr%:%mn%:%sc%\x0f",
	"showdesc":'0',
	"chanignores[]":[]
}
if not os.path.isdir(sPathToSettings+"/settings"):
	os.mkdir(sPathToSettings+"/settings")
if os.path.isfile(sPathToSettings+"/settings/youtubeinfo"):
	hF=open(sPathToSettings+"/settings/youtubeinfo","r")
	lSetLines=hF.readlines()
	hF.close()
	for sI in lSetLines:
		lI=sI.rstrip().split('=',1)
		if len(lI) == 2:
			if lI[0][-2:] == "[]":
				lI[1] = lI[1].split(",")
			#endif
			dSettings[lI[0]]=lI[1]
		#endif
	#endfor
#endif

def SaveSettings():
	global sPathToSettings
	hF=open(sPathToSettings+"/settings/youtubeinfo","w")
	for sI,sV in dSettings.iteritems():
		if sI[-2:] == "[]":
			sV = ','.join(sV)
		#endif
		hF.write("%s=%s\n"%(sI,sV))
	hF.close()
#enddef

dAntiSpam={}
reFindyt=re.compile(r'https?://(?:[^.]*\.?youtube\.com/watch\?.*v=|youtu.be/)([a-zA-Z0-9_\-]+)')
reSelector=re.compile(r'^([a-zA-Z_][a-zA-Z0-9_:]*)?(?:\(([0-9]+)\))?(?:\[([a-zA-Z_][a-zA-Z0-9_:]*])\])?$')
def LookForLink(word,word_eol,userdata,alt=0):
	global reFindyt,reSelector
	if alt == 0 and xchat.get_info("channel") in dSettings["chanignores[]"]: return
	lLinks=reFindyt.findall(word_eol[1])
	for sI in lLinks:
		if alt != 0 or sI not in dAntiSpam:
			dAntiSpam[sI]=True
			try:
				#xchat.prnt("http://gdata.youtube.com/feeds/api/videos/"+lI)
				hInfoXML = urllib2.urlopen("http://gdata.youtube.com/feeds/api/videos/"+sI)
				sInfoXML = hInfoXML.read()
				if sInfoXML:
					hXMLDom = parseString(sInfoXML)
					iVidSecs = int(hXMLDom.getElementsByTagName("media:content")[0].attributes['duration'].value)
					iVidMins = int(math.floor(iVidSecs/60));
					iVidSecs -= iVidMins*60
					iVidHrs = int(math.floor(iVidMins/60));
					iVidMins -= iVidHrs*60
					lFmt = dSettings['string'].split("%")
					prnt=""
					for iI,sV in enumerate(lFmt):
						if iI%2==0:prnt+=sV
						else:
							if sV[0]=='+':
								sV=sV[1:]
								## sV is now a basic, XML-capable CSS selector that will only find ONE element
								lV=sV.split(">") ## Split children
								## Shouldn't need # or . in a XML doc, assume tag
								hPar=hXMLDom
								bDidAttr=False
								for iId,sX in enumerate(lV):
									## Get what result we're reading, default to 0
									## Also look if we're looking at attributes
									hSel=reSelector.match(sX)
									if hSel:
										sTag=hSel.group(1)
										sRes=hSel.group(2)
										iRes=0
										if sRes!=None:
											try:
												iRes=int(sRes)
											except:
												xchat.prnt("YTI Warning: Result selector must be a number. In Format String: Selector %i, Child %i."%(math.floor(iI/2),iId))
											#endtry
										#endif
										sAttr=hSel.group(3)
										if sTag is None:
											hPar=hPar.childNodes[iRes]
										else:
											hPar=hPar.getElementsByTagName(sTag)[iRes]
										#endif
										if sAttr!=None:
											bDidAttr=True
											prnt+=hPar.attributes[sAttr].value
											break ## No more children necessary
										#endif
									else:
										raise YTIError("Invalid selector \"%s\"."%sX,math.floor(iI/2),iId)
									#endif
								#endfor
								if not bDidAttr:
									prnt += hPar.childNodes[0].data
								#endif
							elif sV=="id": prnt+=sI
							elif sV=="hr": prnt+=str(iVidHrs)
							elif sV=="mn": prnt+="%02i" % iVidMins
							elif sV=="sc": prnt+="%02i" % iVidSecs
							#endif
						#endif
					#endfor
					if alt == 1:
						xchat.command(("say "+prnt).encode('utf-8'))
					else:
						xchat.emit_print(userdata, *word)
						xchat.prnt(prnt.encode('utf-8'))
					#endif
					if dSettings['showdesc']!='0':
						sDesc=hXMLDom.getElementsByTagName('content')[0].childNodes[0].data
						sDesc=sDesc.replace("\n"," ")
						if alt == 1: xchat.command(("say "+sDesc[0:100]).encode('utf-8'))
						else: xchat.prnt(sDesc[0:100].encode('utf-8'))
						#endif
					#endif
					return xchat.EAT_XCHAT
				else:
					xchat.prnt("No data returned")
				#endif
			except urllib2.HTTPError as e:
				xchat.prnt("Server error, code %i."%e.code)
				for i in e:
					 xchat.prnt("Error: "+i)
			except urllib2.URLError as e:
				xchat.prnt("Error connecting to server: %s"%e.reason)
			except YTIError as e:
				xchat.prnt(str(e))
			except:
				print "Unexpected error:", sys.exc_info()[0]
				raise
			#endtry
		#endif
	#endfor
	return xchat.EAT_NONE
#enddef

def Settings(word,word_eol,userdata):
	global dSettings
	if len(word) >= 3:
		if word[1]=='say':
			LookForLink(['',word[2],''],['',word[2],''],None,1)
			return
		elif word[1]=='ignore':
			if word[2][0] == '#': 
				if word[2] not in dSettings["chanignores[]"]:
					dSettings["chanignores[]"].append(word[2])
				#endif
				xchat.prnt("Ignoring links in "+word[2])
			else:
				xchat.prnt("Ignore what?")
			#endif
		elif word[1]=='unignore':
			if word[2][0] == '#': 
				if word[2] in dSettings["chanignores[]"]:
					dSettings["chanignores[]"].remove(word[2])
				#endif
				xchat.prnt("Monitoring links in "+word[2])
			else:
				xchat.prnt("Unignore what?")
			#endif
		else:
			dSettings[word[1]]=word_eol[2]
			xchat.prnt("Set \"%s\""%word[1])
		#endif
		SaveSettings()
	elif len(word) == 2:
		iTmp=LookForLink(['YTI: ',word[1],''],['','',''],None,2)
		if iTmp == xchat.EAT_NONE and word[1] in dSettings:
			sDots='.'*(29-len(word[1]))
			sTmpStr="%s\x0312%s\x0f\x0311:\x0f %s"%(word[1],sDots,dSettings[word[1]])
			xchat.prnt(sTmpStr)
		#endif
	else:
		for sI,sV in dSettings.iteritems():
			sDots='.'*(29-len(sI))
			sTmpStr="%s\x0312%s\x0f\x0311:\x0f %s"%(sI,sDots,sV)
			xchat.prnt(sTmpStr)
		#endfor
	#endif
	return xchat.EAT_ALL
#enddef

lEvents4L4l = [
	 "Channel Action"
	,"Channel Action Hilight"
	,"Channel Message"
	,"Channel Msg Hilight"
]

for sI in lEvents4L4l:
	xchat.hook_print(sI,LookForLink,sI)
#endfor
xchat.hook_command("yti",Settings)
xchat.prnt("Loaded %s version %s." % (__module_name__,__module_version__))
#import sys
#if len(sys.argv) > 1:
#	LookForLink(['',sys.argv[1],''],['','',''],None)
