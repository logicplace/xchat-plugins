autoghost 0.3 - Nearly Complete - Needs to switch from using whois to who
	Ghosts your nick via nickserv if it can
	Otherwise will wait till your prefered nick disconnects
	either by waiting for the quit in current channels or polling whois

betterkb 0.1 - Nearly complete
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

