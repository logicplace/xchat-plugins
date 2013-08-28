fauxchat - Preliminary
    Note: this is NOT a plugin
    fauxchat is a small xchat emulator that allows you to test plugins
    without doing it through xchat (because xchat likes to crash for certain
    errors)
    Link this file in /usr/lib/python*
    Instead of using  import xchat  use  import fauxchat as xchat
    It works the same way! Eventually, I may add some extra features.

autoghost 0.4 - Nearly Complete - Needs to switch from using whois to who
    Ghosts your nick via nickserv if it can
    Otherwise will wait till your prefered nick disconnects
    either by waiting for the quit in current channels or polling whois

betterkb 0.5 - Nearly complete
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
    /ban [FLAGS] NICK [TYPE] [TIME]
    /ban [FLAGS] MASK [TIME]
    /kick NICK [MESSAGE]
    /kickban [FLAGS] NICK [TYPE] [TIME] [MESSAGE]
    /unban NICK
    /unban MASK
    /b is an alias of /ban
    /k is an alias of /kick
    /kb and /bk are aliases of /kickban
    /ub and /-b are aliases of /unban

    Flags are:
    -k = Kick also
    -u = Time in seconds (eg. -u9001)
    To use both, u must be last (eg -ku9001)

    TODO:
    Unban by nick when someone else banned the person.
    Set a time for a ban not set by you via /unban NICK|MASK TIME

ctcp 1.1 - Complete
    Send text files and avatars via CTCP. Conditionalize CTCP responses.
    Includes spam protection.
    Set up ctcp responses in XChat settings.
    Commands are:
    /dump NICK TEXTFILE
    /face NICK
    /face NICK ascii
    /offtime NICK OFFSET [FORMAT]
    /ifuser USER COMMAND
    /ifnotuser USER COMMAND
    /vercond CONDITION [ARGUMENTS]
    NICK is who to send the response to.
    TEXTFILE is relative to %xchatdir%/settings/ctcp and .txt is appended.
    Avatar should be saved as face.png or face.txt in the above directory.
    OFFSET is of the format #d#h#m#s where each is optional, and negatives are
    allowed. For example, /offtime Person 2h replies to Person's time request
    with your local time + 2 hours.
    FORMAT is optional and uses Python's datetime.strftime to print. Default is
    XChat's format (at least, my version of XChat).
    Conditionals work by checking the condition before processing the command.
    It should be pretty obvious but an example is:
        ifnotuser Anonymous dump %s my-personal-info
    Condition "user" refers to your username in the context requested. Case
    sensitive.
    /vercond allows you to set the condition on which you reply to version
    requests, since it's internal. For example:
        /vercond ifnotuser Anonymous
    To prevent version requests always, use /vercond false
    To always reply to version requests, use /vercond true

delayedmsg 1.0 - Complete
    Sends a message after so many milliseconds to people who join the room
    for the first time.
    Use /dlm for help

h-tan 1.2 - Complete
    A script for #japanese, see http://www.japanese-irc.net/
    Proxies H-tan/U-tan's messages through emit_print and /recv as needed.
    This makes the join/part/etc not highlight the channel as if a message was
    sent, but it does for regular channel messages and actions. Those are also
    sent as the original sender, rather than H-tan.
    このスクリプトは#japaneseのためのものだ。http://www.japanese-irc.net/ を見てください。
    emit_printと/recvはH-tanかU-tanのメッセージの代理をする。
    それから、joinやpartがメッセージの通知のように見えないけど、本当のメッセージの通知が
    正しく見える。そのメッセージは発信人から送信して見えた、H-tanからない。

nosajoin 1.0 - Complete
    If you're forcibly joined to a channel, this sends a part message and
    never lets xchat know it happened (ie. a tab for the channel does not open).

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

youtubeinfo 0.8 - Nearly Complete
    Shows formatted information for youtube links
    Able to ignore channels (manually) in case there's a bot there that does it.
    Able to tell the channel the printed info.
    /yti say LINK
    /yti ignore CHANNEL
    /yti unignore CHANNEL
    TODO:
    Support more than # prefixed channels in un/ignore
    Default un/ignore channel to selected channel
    Support /yti ignore NICK [CHANNEL] to ignore a channel when a certain nick is there

