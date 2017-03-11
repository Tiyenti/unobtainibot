import json
import errors

def add_command(serverid, jsondata):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    try:
        servers[f'sid{serverid}']['customcommands'].append(jsondata)
    except KeyError:
        servers[f'sid{serverid}']['customcommands'] = []
        servers[f'sid{serverid}']['customcommands'].append(jsondata)

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

def get_custom_command_names(serverid):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    customcommandnames = []
    try:
        for command in servers[f'sid{serverid}']['customcommands']:
            customcommandnames.append(command['name'])
    except KeyError:
        customcommandnames = []

    return customcommandnames

def add_simple_command(serverid, name, userlevel, replyinpm, content):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    customcommandnames = get_custom_command_names(serverid)

    if name in customcommandnames:
        raise errors.CustomCommandNameError('a custom command with that name already exists')
    else:
        jsondata = {
            'type': 'simple',
            'name': name,
            'userlevel': userlevel,
            'replyinpm': replyinpm,
            'content': content
        }
        add_command(serverid, jsondata)

def add_quotesys_command(serverid, name, userlevel):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    customcommandnames = get_custom_command_names(serverid)

    if name in customcommandnames:
        raise errors.CustomCommandNameError('a custom command with that name already exists')
    else:
        jsondata = {
            'type': 'quotesys',
            'name': name,
            'userlevel': userlevel,
            'content': []
        }
        add_command(serverid, jsondata)

def add_addquote_command(serverid, name, userlevel, quotesys):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    customcommandnames = get_custom_command_names(serverid)

    if name in customcommandnames:
        raise errors.CustomCommandNameError('a custom command with that name already exists')
    else:
        jsondata = {
            'type': 'addquote',
            'name': name,
            'userlevel': userlevel,
            'content': quotesys
        }

        add_command(serverid, jsondata)

def add_delquote_command(serverid, name, userlevel, quotesys):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    customcommandnames = get_custom_command_names(serverid)

    if name in customcommandnames:
        raise errors.CustomCommandNameError('a custom command with that name already exists')
    else:
        jsondata = {
            'type': 'delquote',
            'name': name,
            'userlevel': userlevel,
            'content': quotesys
        }

        add_command(serverid, jsondata)
