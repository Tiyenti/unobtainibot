import discord
import asyncio
import json
import random
import os
import commandhelp
from datetime import datetime

startTime = datetime.now()

client = discord.Client()

with open('config.json', 'r') as f:
    config = json.load(f)

with open('logins.json', 'r') as f:
    logins = json.load(f)

with open('servers.json', 'r') as f:
    servers = json.load(f)

defaultprefix = config['prefix']
botownerid = config['botownerid']
discordtoken = logins['discordtoken']

def add_server_to_config(serverid, servername, serverownerid, prefix):
    print('Adding server to servers.json...')
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    serverjsondata  = { "servername": servername,
                        "serverownerid": serverownerid,
                        "prefix": prefix,
                        "disabledcommands": ["8ball", "tf"],
                        "modrolename": "Moderator",
                        "adminrolename": "Admin",
                        "quotes": [] }

    servers[f'sid{serverid}'] = serverjsondata

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

def update_server_config(serverid, servername, serverownerid):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    try:
        server = servers[f'sid{serverid}']
    except KeyError:
        # server config missing
        add_server_to_config(serverid, servername, serverownerid, defaultprefix)
        return

    server['servername'] = servername
    server['serverownerid'] = serverownerid

    servers[f'sid{serverid}'] = server

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

def set_default_prefix(prefix):
    global defaultprefix

    with open('config.json', 'r') as f:
        config = json.load(f)

    config['prefix'] = prefix
    defaultprefix = prefix

    print(f'Set default prefix to {prefix}. Writing to config file...')
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def set_server_prefix(serverid, prefix):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    server = servers[f'sid{serverid}']
    server['prefix'] = servername
    servers[f'sid{serverid}'] = server

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

def set_userlevel_rolenames(serverid, modrolename, adminrolename):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    server = servers[f'sid{serverid}']
    server['modrolename'] = modrolename
    server['adminrolename'] = adminrolename
    servers[f'sid{serverid}'] = server

    print(f'Set ul rolenames to {modrolename} (mod), {adminrolename} (admin)')

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

def get_userlevel(member, server):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    # there's probably a more efficient way to do this
    roles = []
    for role in member.roles:
        roles.append(str(role))

    if member.id == botownerid:
        return 4
    elif member.id == server.owner.id:
        return 3
    elif servers[f'sid{server.id}']['adminrolename'] in roles:
        return 2
    elif servers[f'sid{server.id}']['modrolename'] in roles:
        return 1
    else:
        return 0

async def random_status_change():
    statuses = config['statuses']
    timeout = int(config['statustimeout'])

    while True:
        randomnum = random.randint(0, len(statuses) - 1)
        print(f'Now playing: {statuses[randomnum]}')
        await client.change_presence(game=discord.Game(name=statuses[randomnum]), afk=False)
        if timeout != 0:
            await asyncio.sleep(timeout)
        else:
            break

@client.event
async def on_ready():
    print(f'Bot ready on {len(client.servers)} server(s).')
    await random_status_change()

@client.event
async def on_server_join(server):
    if not config.has_section(server.id):
        print(f'Server {server} does not have a config entry. Creating one...')
        add_server_to_config(server.id, server.name, server.owner.id, defaultprefix)
        await client.send_message(server.default_channel, '**Unobtainibot is now in your server!**\n' \
                                  + 'The bot has been initlised with the default config:\n' \
                                  + '**Prefix:** !\n' \
                                  + '**Admin Role Name:** Admin\n' \
                                  + '**Moderator Role Name:** Moderator\n' \
                                  + '**Disabled Commands:** !8ball, !tf\n' \
                                  + 'Use `!help` to get PM\'d a list of commands this bot supports.')
    else:
        update_server_config(server.id, server.name, server.owner.id)
        await client.send_message(server.default_channel, '**Unobtainibot is now in your server!**\n' \
                                  + 'Use `!help` to get PM\'d a list of commands this bot supports.')

@client.event
async def on_message(message):
    print(f'[{message.server}#{message.channel}] <{message.author}>: {message.content}')

    if message.server == None:
        return

    update_server_config(message.server.id, message.server.name, message.server.owner.id)

    with open('servers.json', 'r') as f:
        servers = json.load(f)

    disabledcommands = servers[f'sid{message.server.id}']['disabledcommands']
    prefix = servers[f'sid{message.server.id}']['prefix']

    usecounter = 0

    try:
        usecounter = int(config['usecounter'])
    except KeyError:
        print('usecounter key is missing from config.json. Setting use counter to 0.')

    if not message.author.bot:
        if message.content.startswith(prefix):
            # Increase use counter in case command is found
            # (If it's not found, it gets decremented again later.)
            usecounter += 1

            args = message.content.split(' ')
            if args[0] == f'{prefix}test' and 'test' not in disabledcommands:
                messagestr = 'Test command recieved. Arguments:'
                for arg in args[1:]:
                    messagestr += f' {arg}'
                await client.send_message(message.channel, messagestr)
            elif args[0] == f'{prefix}help':
                commandname = None

                if len(args) > 1:
                    commandname = args[1]

                messagestr = commandhelp.get_command_help_string(message.server.id,
                                                                 get_userlevel(message.author,
                                                                               message.server),
                                                                 commandname)

                await client.send_message(message.author, messagestr)
                await client.send_message(message.channel, f'<@{message.author.id}>: Check your PMs')
            elif args[0] == f'{prefix}setprefix':
                if get_userlevel(message.author, message.server) == 4:
                    if len(args) > 1:
                        if not args[1].isspace() or args[1] != '':
                            if len(args) > 2:
                                if args[2] == 'server':
                                    set_server_prefix(message.server.id, args[1])
                                    await client.send_message(message.channel, f'Set server prefix to {args[1]}')
                                else:
                                    set_default_prefix(args[1])
                                    await client.send_message(message.channel, f'Set default prefix to {args[1]}')
                            else:
                                set_default_prefix(args[1])
                                await client.send_message(message.channel, f'Set default prefix to {args[1]}')
                        else:
                            await client.send_message(message.channel,
                                                      f'Prefix cannot be null, whitespace, or empty.')
                    else:
                        await client.send_message(message.channel,
                                                  f'Prefix cannot be null, whitespace, or empty.')
                elif get_userlevel(message.author, message.server) > 1:
                    if len(args) > 1:
                        if not args[1].isspace() or args[1] != '':
                            set_server_prefix(message.server.id, args[1])
                            await client.send_message(message.channel, f'Set server prefix to {args[1]}')
                    else:
                        await client.send_message(message.channel,
                                                  f'Prefix cannot be null, whitespace, or empty.')
                else:
                    await client.send_message(message.channel,
                                              f'The {prefix}setprefix command may only be used by ' + \
                                              'the bot or server owner.' )
            elif args[0] == f'{prefix}8ball' and '8ball' not in disabledcommands:
                if len(args) > 1:
                    randomnum = random.randint(1,20);
                    quote = '';
                    if randomnum == 1:
                        quote = 'It is certain.'
                    elif randomnum == 2:
                        quote = 'It is decidedly so.'
                    elif randomnum == 3:
                        quote = 'Without a doubt, yes.'
                    elif randomnum == 4:
                        quote = 'Yes, definitely.'
                    elif randomnum == 5:
                        quote = 'You may rely on it.'
                    elif randomnum == 6:
                        quote = 'As I see it, yes.'
                    elif randomnum == 7:
                        quote = 'It is most likely.'
                    elif randomnum == 8:
                        quote = 'The outlook is good.'
                    elif randomnum == 9:
                        quote = 'Yes.'
                    elif randomnum == 10:
                        quote = 'Signs point to yes.'
                    elif randomnum == 11:
                        quote = 'Reply hazy. Try again.'
                    elif randomnum == 12:
                        quote = 'Ask again later.'
                    elif randomnum == 13:
                        quote = 'It\'s better not to tell you now.'
                    elif randomnum == 14:
                        quote = 'I cannot predict that now.'
                    elif randomnum == 15:
                        quote = 'Concentrate and ask again.'
                    elif randomnum == 16:
                        quote = 'Don\'t count on it.'
                    elif randomnum == 17:
                        quote = 'My reply is no.'
                    elif randomnum == 18:
                        quote = 'My sources say no.'
                    elif randomnum == 19:
                        quote = 'The outlook is not so good.'
                    elif randomnum == 20:
                        quote = 'It is very doubtful.'

                    await client.send_message(message.channel, f'<@{message.author.id}>: {quote}')
                else:
                    await client.send_message(message.channel, f'<@{message.author.id}>: I cannot answer ' \
                                              + 'a question I have not been asked.')
            elif args[0] == f'{prefix}toggle':
                if get_userlevel(message.author, message.server) >= 1:
                    if len(args) > 1:
                        print (f'Disabled Commands for {message.server.name}: {disabledcommands}')
                        if args[1] not in disabledcommands:
                            print (f'{args[1]} is enabled. Disabling it.')

                            if args[1] != 'enable' and args[1] != 'disable' \
                               and args[1] != 'setprefix' and args[1] != 'help':
                                disabledcommands.append(args[1])
                                print (f'New disabled command array: {disabledcommands}')

                                servers[f'sid{message.server.id}']['disabledcommands'] = disabledcommands

                                with open('servers.json', 'w') as f:
                                    json.dump(servers, f, indent=4)

                                await client.send_message(message.channel, 'Disabled command ' \
                                                          + f'{prefix}{args[1]} on this server.')
                            else:
                                await client.send_message(message.channel, 'You cannot disable that command.')
                        else:
                            print (f'{args[1]} is enabled. Disabling it.')

                            disabledcommands.remove(args[1])
                            print (f'New disabled command array: {disabledcommands}')

                            servers[f'sid{message.server.id}']['disabledcommands'] = disabledcommands

                            with open('servers.json', 'w') as f:
                                json.dump(servers, f, indent=4)

                                await client.send_message(message.channel, 'Enabled command ' \
                                                          + f'{prefix}{args[1]} on this server.')
                    else:
                        await client.send_message(message.channel, 'Specify a command to toggle.')
                else:
                    await client.send_message(message.channel, f'The {prefix}toggle command may ' \
                                              + 'only be used by the server or bot owner.')
            elif args[0] == f'{prefix}quote' and 'quote' not in disabledcommands:
                quotes = servers[f'sid{message.server.id}']['quotes']
                if len(quotes) > 0:
                    quotenum = random.randint(0, len(quotes) - 1)

                    if len(args) > 1:
                        if args[1] == "list":
                            quotestr = ''
                            curindex = 0

                            for quote in quotes:
                                quotestr += f'#{curindex}. {quote}'
                                curindex += 1
                                await client.send_message(message.author, f'```\n{quotestr}```')

                            await client.send_message(message.channel,
                                                      f'<@{message.author.id}>: Check your PMs')
                            return
                        else:
                            try:
                                quotenum = int(args[1])
                            except ValueError:
                                print('Argument given is not an integer, using random digit.')
                            try:
                                await client.send_message(message.channel, quotes[quotenum])
                            except IndexError:
                                print('Index out of range.')
                                await client.send_message(message.channel, f'Quote #{quotenum} does not exist.')
                    else:
                        await client.send_message(message.channel, quotes[quotenum])
                else:
                    await client.send_message(message.channel, 'There are no quotes for this server.')
            elif args[0] == f'{prefix}addquote':
                if get_userlevel(message.author, message.server) > 0:
                    if len(args) > 1:
                        quotestring = ''
                        for arg in args[1:]:
                            quotestring += f'{arg} '
                        if quotestring != '' and not quotestring.isspace():
                            servers[f'sid{message.server.id}']['quotes'].append(quotestring)
                            quotes = servers[f'sid{message.server.id}']['quotes']
                            with open('servers.json', 'w') as f:
                                json.dump(servers, f, indent=4)
                                await client.send_message(message.channel,
                                                          'Added quote #' +
                                                          f'{len(quotes) - 1}: {quotestring}')
                        else:
                            await client.send_message(message.channel, 'Quote cannot be empty')
            elif args[0] == f'{prefix}delquote':
                if get_userlevel(message.author, message.server) > 0:
                    if len(args) > 1:
                        if args[1] == "all":
                            if get_userlevel(message.author, message.server) > 1:
                                await client.send_message(message.channel,
                                                          '**Hold it!** ' +
                                                          'This will remove every quote on this server. ' +
                                                          'Continue? [y/N]')
                                msg = await client.wait_for_message(author=message.author)
                                if msg.content == 'y':
                                    servers[f'sid{message.server.id}']['quotes'] = []
                                    with open('servers.json', 'w') as f:
                                        json.dump(servers, f, indent=4)
                                        await client.send_message(message.channel, 'Removed all quotes.')
                            else:
                                await client.send_message(message.channel,
                                                          'Only admins have the ability to delete all ' +
                                                          'quotes.')
                        else:
                            quotenum = 0
                            try:
                                quotenum = int(args[1])
                            except ValueError:
                                await client.send_message(message.channel,
                                                          'Couldn\'t delete quote; ' +
                                                          'Argument given was not an integer.')
                            try:
                                quote = servers[f'sid{message.server.id}']['quotes'][quotenum]
                                servers[f'sid{message.server.id}']['quotes'].pop(quotenum)

                                with open('servers.json', 'w') as f:
                                    json.dump(servers, f, indent=4)
                                    await client.send_message(message.channel,
                                                              f'Removed quote #{quotenum}: {quote}')

                            except IndexError:
                                await client.send_message(message.channel, 'Couldn\'t delete quote; ' +
                                                          'Index was out of range.')
                    else:
                        await client.send_message(message.channel, 'Couldn\'t delete quote; ' +
                                                      'No index given.')
                else:
                    await client.send_message(message.channel, 'Permission denied.')
            elif args[0] == f'{prefix}setulrolenames':
                if get_userlevel(message.author, message.server) > 1:
                    if len(args) > 2:
                        set_userlevel_rolenames(message.server.id, args[1], args[2])
                        await client.send_message(message.channel,
                                                  f'Set userlevel rolenames to {args[1]} (mod), ' +
                                                  f'{args[2]} (admin).')
                    elif len(args) > 1:
                        set_userlevel_rolenames(message.server.id, args[1],
                                                servers[f'sid{message.server.id}']['adminrolename'])
                        await client.send_message(message.channel,
                                                  f'Set userlevel rolenames to {args[1]} (mod), ' +
                                                  f'{args[2]} (admin).')
                    else:
                        await client.send_message(message.channel,
                                                  'Please specify the moderator and admin role names ' \
                                                  + '(mod first, admin second).')
                else:
                    await client.send_message(message.channel, \
                                              f'The {prefix}setulrolenames command may only be used by ' \
                                              + 'admins, the server owner, or the bot owner.')
            elif args[0] == f'{prefix}tf' and 'tf' not in disabledcommands:
                await client.send_message(message.channel, \
                                    '(╯°□°）╯︵ ┻━┻ FLIP THIS TABLE\n' \
                                    + '┻━┻ ︵ ヽ(°□°ヽ) FLIP THAT TABLE\n' \
                                    + '┻━┻ ︵ \\\\(°□°)/ ︵ ┻━┻ FLIP **ALL** THE TABLES')
            elif args[0] == f'{prefix}addcom':
                if get_userlevel(message.author, message.server) > 1:
                    if len(args) > 4:
                        # args[1] = command name
                        # args[2] = userlevel
                        # args[3] = reply in pm? 0/1
                        # args[4:] = content

                        content = ''

                        for arg in args[4:]:
                            content += f'{arg} '

                        jsondata = {
                            'name': args[1],
                            'userlevel': int(args[2]),
                            'replyinpm': int(args[3]),
                            'content': content
                        }

                        try:
                            servers[f'sid{message.server.id}']['customcommands'].append(jsondata)
                        except KeyError:
                            servers[f'sid{message.server.id}']['customcommands'] = []
                            servers[f'sid{message.server.id}']['customcommands'].append(jsondata)

                        with open('servers.json', 'w') as f:
                            json.dump(servers, f, indent=4)
                            await client.send_message(message.channel,
                                                      f'Successfully added custom command.')
                    else:
                         await client.send_message(message.channel,
                                                   f'Usage: `{prefix}addcom [name] ' +
                                                   '[userlevel] [reply-in-pm] [content]`')
                else:
                     await client.send_message(message.channel,
                                               f'You do not have permission to use that command.')
            elif args[0] == f'{prefix}delcom':
                if get_userlevel(message.author, message.server) > 1:
                    if len(args) > 1:
                        customcommands = servers[f'sid{message.server.id}']['customcommands']

                        for command in customcommands:
                            if command['name'] == args[1]:
                                servers[f'sid{message.server.id}']['customcommands'].remove(command)

                                with open('servers.json', 'w') as f:
                                    json.dump(servers, f, indent=4)
                                    await client.send_message(message.channel,
                                                              'Successfully removed command.')
                                return

                        # If command isn't found, fallback to this.
                        await client.send_message(message.channel,
                                                  'That command does not exist.')
                    else:
                        await client.send_message(message.channel,
                                                  f'Usage: `{prefix}delcom [name]`')
                else:
                     await client.send_message(message.channel,
                                               f'You do not have permission to use that command.')
            elif args[0] == f'{prefix}eval':
                if get_userlevel(message.author, message.server) == 4:
                    if len(args) > 1:
                        code = ''

                        for arg in args[1:]:
                            code += f'{arg} '

                        output = eval(code)
                        await client.send_message(message.channel, f'```\n{output}```')
                    else:
                        await client.send_message(message.channel,
                                                  f'Usage: `{prefix}eval [code ... ]`')
                else:
                    await client.send_message(message.channel,
                                              'You do not have permission to use that command.')
            elif args[0] == f'{prefix}exec':
                if get_userlevel(message.author, message.server) == 4:
                    if len(args) > 1:
                        code = ''

                        for arg in args[1:]:
                            code += f'{arg} '

                        output = exec(code)
                        await client.send_message(message.channel, f'```\n{output}```')
                    else:
                        await client.send_message(message.channel,
                                                  f'Usage: `{prefix}exec [code ... ]`')
                else:
                    await client.send_message(message.channel,
                                              'You do not have permission to use that command.')
            elif args[0] == f'{prefix}userlevel' and 'userlevel' not in disabledcommands:
                userlevel = get_userlevel(message.author, message.server)
                await client.send_message(message.channel,
                                          f'<@{message.author.id}>: You have userlevel {userlevel}.')
            elif args[0] == f'{prefix}stats' and 'stats' not in disabledcommands:
                servercount = len(client.servers)
                users = client.get_all_members()
                onlineuserids = []
                for user in users:
                    if not user.status == discord.Status.offline or \
                       user.status == discord.Status.invisible:
                       if user.id not in onlineuserids and \
                          user.id != client.user.id:
                          onlineuserids.append(user.id)

                onlinecount = len(onlineuserids)
                print(onlineuserids)
                uptime = datetime.now() - startTime

                await client.send_message(message.channel,
                                          '```' +
                                          f'Currently in {servercount} server(s), ' +
                                          f'with {onlinecount} user(s) online (excluding ' +
                                          'invisible users and myself).\n' +
                                          f'Bot command use counter: {usecounter}\n' +
                                          f'Bot uptime: {uptime}```')

            else:
                customcommands = servers[f'sid{message.server.id}']['customcommands']

                for command in customcommands:
                    if args[0][len(prefix):] == command['name'] and command['name'] not in disabledcommands:
                        if get_userlevel(message.author, message.server) >= int(command['userlevel']):
                            if command['replyinpm'] == 1:
                                await client.send_message(message.author, command['content'])
                                await client.send_message(message.channel,
                                                          f'<@{message.author.id}>: Check your PMs')
                            else:
                                await client.send_message(message.channel, command['content'])
                        else:
                            await client.send_message('You do not have permission to use that command.')
                        return

                # By this point in the code, the command has not been found, so we the decrease the use
                # counter.
                usecounter -= 1

            # And now we save the new usecounter to the json.
            config['usecounter'] = usecounter

            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)


@client.event
async def on_message_delete(message):
    print(f'Message deleted: [{message.server}#{message.channel}] <{message.author}>: {message.content}')


client.run(discordtoken)
