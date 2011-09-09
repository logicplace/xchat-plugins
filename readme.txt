fauxchat - Preliminary
	Note: this is NOT a plugin
	fauxchat is a small xchat emulator that allows you to test plugins
	without doing it through xchat (because xchat likes to crash for certain
	errors)
	Link this file in /usr/lib/python*
	Instead of using  import xchat  use  import fauxchat as xchat
	It works the same way! Eventually, I may add some extra features.

autoghost 0.3 - Nearly Complete - Needs to switch from using whois to who
	Ghosts your nick via nickserv if it can
	Otherwise will wait till your prefered nick disconnects
	either by waiting for the quit in current channels or polling whois

betterkb 0.3 - Nearly complete
	Allows you to kick and ban in more robust ways.
	Set a default kick message via /set irc_kick_message MESSAGE
	Can set a timer to remove bans, these are saved between sessions.
	Can ban/unban by nick when said nick is no longer in the channel.
	If you kickban with a time, it will append the time to the kick message.
	Set a default numeric ban mask via /set irc_ban_type
	0) *!*@*.host
	1) *!*@host
	2) *!*user@*.host
	3) *!*user@host
	4) *!*user@*
	5) nick!*@*
	Commands are:
	/ban NICK [TYPE] [TIME]
	/ban MASK [TIME]
	/kick NICK [MESSAGE]
	/kickban NICK [TYPE] [TIME] [MESSAGE]
	/unban NICK
	/unban MASK
	/b is an alias of /ban
	/k is an alias of /kick
	/kb and /bk are aliases of /kickban
	/ub and /-b are aliases of /unban
	
	TODO:
	Unban by nick when someone else banned the person.
	Set a time for a ban not set by you via /unban NICK|MASK TIME

ctcp 1.0 - Complete
	Send text files and avatars via ctcp.
	Includes spam protection.
	Set up ctcp responses in xchat settings.
	Commands are:
	/dump TEXTFILE
	/face
	/face exist
	/face ascii
	TEXTFILE is relative to %xchatdir%/settings/ctcp
	Avatar should be saved as face.png or face.txt in the above directory.

delayedmsg 1.0 - Complete
	Sends a message after so many milliseconds to people who join the room
	for the first time.
	Use /dlm for help

nosajoin 0.0 - Experimental
	GOAL: Automatically part rooms that you were forced to join.

nowplaying 0.1 - In Progress
	Simple NowPlaying script to show what's now playing on your system
	Currently only for Linux
	Use /np to display now playing script, and set your message with
	/set now_playing_message COMMAND ARGS
	Suggested commands are: me, say, echo
	You may override the command for one report with /np COMMAND
	Syntax is currently very basic. Use:
	*) %(NAME)  to replace with that argument
	*) %{etc %(NAME) etc}  to only show etc if NAME exists
	Note %{} forms cannot be nested, currently, but you may have multiple
	%() in them. For example:
		say %(title) %{- Length: %(length)}
	If return from the program is {"title": "Hi", "length": "8:00"} result is:
		say Hi - Length: 8:00
	If return from the program is {"title": "Hi"} result is:
		say Hi 
	If return from the program is {"length": "8:00"} result is:
		say  - Length: 8:00
	Currently supports:
	*) Pithos
	*) Audacious (partially, untested)
	And I wish to support:
	*) mpris
	*) YouTube somehow

voiceonce 0.1 - Semi-experimental
	Voice people the first time they join the room.

youtubeinfo 0.7 - Nearly Complete
	Shows formatted information for youtube links
	Able to ignore channels (manually) in case there's a bot there that does it.
	Able to tell the channel the printed info.
	/yti say LINK
	/yti ignore CHANNEL
	/yti unignore CHANNEL
	TODO:
	Support youtu.be links
	Support more than # prefixed channels in un/ignore
	Default un/ignore channel to selected channel
	Support /yti ignore NICK [CHANNEL] to ignore a channel when a certain nick is there

