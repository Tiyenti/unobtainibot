import json

def get_command_help_string(serverid, userlevel, commandname):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    servername = servers[f'sid{serverid}']['servername']
    disabledcommands = servers[f'sid{serverid}']['disabledcommands']
    customcommands = servers[f'sid{serverid}']['customcommands']
    prefix = servers[f'sid{serverid}']['prefix']

    # 0 = Everyone
    # 1 = Mod
    # 2 = Admin
    # 3 = Server Owner
    # 4 = Bot Owner

    # setprefix
    if commandname == 'setprefix':
        messagestr = f'`{prefix}setprefix [prefix] <server|default>`: ' + \
                      'Changes the bot command prefix. (userlevel: 2)\n' + \
                      '`[prefix]`: What to change the prefix to.\n' + \
                      '`<server|default>`: Specify whether or not to change the ' + \
                      'server\'s command prefix, or the default prefix. If omitted, ' + \
                      'defaults to `server`. (userlevel: 4)'
    elif commandname == 'setulrolenames':
        messagestr = f'`{prefix}setulrolenames [modrole] <adminrole>`: ' + \
                      'Changes the moderator/admin role names. (userlevel: 2)\n' + \
                      '`[modrole]`: The moderator rolename.\n' + \
                      '`<adminrole>`: The admin role name. If omitted, ' + \
                      'defaults to whatever the current admin role name is.'
    elif commandname == 'addquote':
        messagestr = f'`{prefix}addquote [quote ... ]`: ' + \
                      'Adds a quote to the list. (userlevel: 1)\n' + \
                      '`[quote ... ]`: The quote to add.'
    elif commandname == 'delquote':
        messagestr = f'`{prefix}delquote [index|all]`: ' + \
                      'Removes a quote from the list. (userlevel: 1)\n' + \
                      '`[index|all]`: Either a number corrosponding to the index ' + \
                      'of the quote to be removed, or `all` (which deletes all quotes). ' + \
                      'Using `all` requires userlevel 2.'
    elif commandname == 'quote':
        messagestr = f'`{prefix}quote <index|list>`: Prints a quote from the list. (userlevel: 0)\n' + \
                      '`<index|list>: Either a number corrosponding to the index of ' + \
                      'the quote to be printed, or `list` (which PMs the user the quote list). ' + \
                      'If ommitted, choses a random quote.'
    elif commandname == '8ball':
        messagestr = f'`{prefix}8ball [question ... ]`: ' + \
                      'Prints out a random Magic 8-Ball response. (userlevel: 0)\n' + \
                      '`[question ... ]`: The question to ask the Magic 8-Ball.'
    elif commandname == 'help':
        messagestr = f'`{prefix}help <command>`: ' + \
                      'PMs the user information about the commands this bot supports. (userlevel: 0)\n' + \
                      '`<command>`: A command to view information about. If ommitted, ' + \
                      'PMs the user a list of commands that they can use.'
    elif commandname == 'toggle':
        messagestr = f'`{prefix}toggle [command]`: ' + \
                      'Toggles on/off the specified command on the server. (userlevel: 2)\n' + \
                      '`[command]`: The command to toggle, without the prefix.'
    elif commandname == 'addcom':
        messagestr = f'`{prefix}addcom [name] [userlevel] [reply-in-pm] [content ... ]`: ' + \
                      'Adds a simple custom command to the server. (userlevel: 2)\n' + \
                      '`[name]`: The name of the command, without prefix.\n' + \
                      '`[userlevel]`: An integer corrosponding to the minimum userlevel ' + \
                      'required to use the command. `0` for everyone, `1` for mod, `2` for admin, ' + \
                      '`3` for server owner, and `4` for bot owner.\n' + \
                      '`[reply-in-pm]`: Either `1` or `0`. If `1`, the command will reply to the user ' + \
                      'in a PM rather than in the channel the command was used.\n' + \
                      '`[content ... ]`: The content the command will print when used.'
    elif commandname == 'delcom':
        messagestr = f'`{prefix}delcom [command]`: ' + \
                      'Removes a custom command from the server. (userlevel: 2)\n' + \
                      '`[command]`: The command to remove, without the prefix.'
    elif commandname == 'test':
        messagestr = f'`{prefix}test <args ... >`: Prints the arguments specified. (userlevel: 0)\n' + \
                      '`<args ... >`: The args to print.'
    elif commandname == 'tf':
        messagestr = f'`{prefix}tf`: Flip some tables. (╯°□°）╯︵ ┻━┻ (userlevel: 0)'
    elif commandname == 'eval':
        messagestr = f'`{prefix}eval [expression ... ]`: \n' + \
                      'Takes the provided Python expression, `eval`s it, and shows the output. ' + \
                      '(userlevel: 4)' + \
                      '`[expression ... ]`: The expression to evaluate.'
    elif commandname == 'exec':
        messagestr = f'`{prefix}exec [code ... ]`: \n' + \
                      'Takes the provided Python code, `exec`s it, and shows the output. (userlevel: 4)' + \
                      '`[code ... ]`: The code to execute.'
    elif commandname == 'userlevel':
        messagestr = f'`{prefix}userlevel`: Shows your userlevel.\n'
    elif commandname == None:
        messagestr = f'**Unobtainibot commands available to you in {servername}**\n' + \
                     f'For more information on these commands, use `{prefix}help <command>`\n\n'

        if userlevel >= 4:
            messagestr += f'`{prefix}eval`: Takes the provided Python expression and `eval`s it.\n'
            messagestr += f'`{prefix}exec`: Takes the provided Python code, and `exec`s it.\n'
        if userlevel >= 2:
            messagestr += f'`{prefix}changeprefix`: Changes the bot command prefix.\n'
            messagestr += f'`{prefix}setulrolenames`: Changes the admin/mod role names.\n'
            messagestr += f'`{prefix}toggle`: Toggles a command on or off.\n'
            messagestr += f'`{prefix}addcom`: Adds a custom command to the server.\n'
            messagestr += f'`{prefix}delcom`: Removes a custom command from the server.\n'
        if userlevel >= 1:
            messagestr += f'`{prefix}addquote`: Adds a quote to the quote list.\n'
            messagestr += f'`{prefix}delquote`: Removes a quote from the quote list.\n'
        if userlevel >= 0:
            messagestr += f'`{prefix}help`: PMs the user info about the commands this bot supports.\n'
            messagestr += f'`{prefix}quote`: Prints a quote from the list.\n'
            messagestr += f'`{prefix}8ball`: Prints a random Magic 8-Ball response.\n'
            messagestr += f'`{prefix}test`: Prints the arguments specfied..\n'
            messagestr += f'`{prefix}tf`: Flips some tables. (╯°□°）╯︵ ┻━┻\n'
            messagestr += f'`{prefix}userlevel`: Shows your userlevel.\n'

        # custom commands
        for command in customcommands:
            if command['name'] not in disabledcommands:
                if userlevel >= int(command['userlevel']):
                    messagestr += f'`{prefix}{command["name"]}`: Custom command.\n'

    return messagestr
