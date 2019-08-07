#!/usr/bin/env python3

CFG_FILE = "/etc/redViper/redViperAccounts.cfg"
ALIVE_ID = #SEND_ALIVE_ID
CMD_REQ_ID= #COMMAND_REQUEST_ID
SERVER_BEACON_ID = #SERVER_ALIVE_ID

CHANNEL_VERIFY = #CHANNEL_VERIFY


# If there's some alias you're more comfortable with, prefer to use for any of the
# available commands, you can append them to the lists below.
EXIT_COMMANDS = [ "exit", "quit", "wq", "q" ]
LIST_COMMANDS = [ "zombies", "list", "show", "zombs", "z" ]
CONTROL_COMMANDS = [ "control", "use", "interact", "c" ]
CMD_COMMANDS = [ "execute", "run", "cmd", "exec", "e" ]
BACK_COMMANDS = [ "back", "b", "main", "return" ]
INFO_COMMANDS = [ "info", "getinfo", "i" ]
KILL_COMMANDS = [ "kill", "terminate", "die" ]
HELP_COMMANDS = [ "help", "?", "h" ]


zombieCount = 0
