try:
	from xchat import *
	FAUX = False
except ImportError:
	import sys
	import os
	
	FAUX = True
	EAT_NONE = 0
	EAT_XCHAT = 1
	EAT_PLUGIN = 2
	EAT_ALL = 3
	
	PRI_HIGHEST = 127
	PRI_HIGH = 64
	PRI_NORM = 0
	PRI_LOW = -64
	PRI_LOWEST = -128
	
	_hooks = []
	_commandHooks = {}
	_printHooks = {}
	_serverHooks = {}
	_timerHooks = {}
	_unloadHooks = []
	_prefs = {}
	
	def set_pref(name,data): #Non-standard
		_prefs[name] = data
	#enddef
	
	def prnt(*args):
		for x in args: print x,
		print ""
	#enddef
	
	def get_info(name):
		if name == "xchatdir":
			for x in [".xchat2", ".config/hexchat"]:
				path = os.path.join(os.environ['HOME'], x)
				if os.path.isdir(path): return path
			#endfor
		#endif
	#enddef
	
	def get_prefs(name):
		# TODO: Handle properly
		if name in _prefs: return _prefs[name]
		else: return None
	#enddef
	
	def _handle(group,com,txt):
		words = txt.split(" ")
		word_eols = []
		for i in range(len(words)): word_eols.append(txt.split(" ",i)[i])
		ret = 0
		if com in _commandHooks:
			for x in _commandHooks[com]:
				ret |= x[0](words[:],word_eols[:],x[1])
				if ret & EAT_PLUGIN: break
			#endfor
		#endif
		return (ret,words, word_eols)
	#enddef
	
	def _server(txt):
		pass
	#enddef
	
	def command(comstr):
		com = comstr.split(" ",1)[0]
		#txt = comstr[1] if len(comstr) > 1 else ""
		
		ret, words, word_eols = _handle(_commands,com,comstr)
		
		if ret & EAT_XCHAT == 0:
			if com in _commands: print _commands[com](words,word_eols)
			else: print ">",com,txt
		#endif
	#enddef
	
	def hook_command(name, callback, userdata=None, priority=PRI_NORM, help=None):
		#TODO: priority,help
		#TODO: Verify that it doesn't exist already
		if name not in _commandHooks: _commandHooks[name] = []
		_commandHooks[name].append([callback,userdata])
		_hooks.append([_commandHooks,name,callback])
		return len(_hooks)-1
	#enddef
	
	def hook_unload(callback, userdata=None):
		#TODO: Verify that it doesn't exist already
		_unloadHooks.append([callback,userdata])
		_hooks.append([_unloadHooks,callback])
		return len(_hooks)-1
	#enddef

	def hook_print(event, callback, userdata=None):
		# TODO: Do something
		pass
	#enddef

	def emit_print(pevent, *words):
		# TODO: Load pevents.conf and deal with that.
		print("PrintEvent %s: %s" % (pevent, ", ".join(words)))
	#enddef
	
	def _line(txt):
		what = txt[0]
		txt = txt[1:]
		if what == "/": command(txt)
		elif what == ">": pass
		elif what == "<": _server(txt)
		else: command("say "+txt)
	#enddef
	
	def loop():
		if len(sys.argv) > 1:
			_line(" ".join(sys.argv[1:]))
		else:
			try:
				while True:
					txt = raw_input("")
					_line(txt)
				#endwhile
			except KeyboardInterrupt: pass
		#endif
		
		# Unloads
		for x in _unloadHooks: x[0](x[1])
	#enddef
	
	_commands = {
		"me": (lambda x,y: "> PRIVMSG #curchan :\1ACTION %s\1" % y[1]),
		"say": (lambda x,y: "> PRIVMSG #curchan :"+y[1]),
		"echo": (lambda x,y: y[1]),
		"set": (lambda x,y: set_pref(x[1],y[2]))
	}
#endtry
