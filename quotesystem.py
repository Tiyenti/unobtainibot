import random
import json

def get_quote(serverid, index, customcommandname=None):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    try:
        if customcommandname == None:
            quotes = servers[f'sid{serverid}']['quotes']
        else:
            for command in servers[f'sid{serverid}']['customcommands']:
                if command['name'] == customcommandname:
                   if command['type'] == 'quote' or command['type'] == 'quotesys':
                       quotes = command['content']
                       break
                else:
                    quotes = []
    except KeyError:
        quotes = []

    if len(quotes) > 0:
        if index == None:
            quotenum = random.randint(0, len(quotes) - 1)
        else:
            quotenum = index

        try:
            return quotes[quotenum]
        except IndexError:
            print('Index out of range.')
            return f'Quote #{quotenum} does not exist.'
    else:
        return 'There are no quotes for this server.'

def list_quotes(serverid, customcommandname=None):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    try:
        if customcommandname == None:
            quotes = servers[f'sid{serverid}']['quotes']
        else:
            for command in servers[f'sid{serverid}']['customcommands']:
                if command['name'] == customcommandname:
                   if command['type'] == 'quote' or command['type'] == 'quotesys':
                       quotes = command['content']
                       break
                else:
                    quotes = []
    except KeyError:
        quotes = []

    if len(quotes) > 0:
        messagestr = '```\n'
        counter = 0
        for quote in quotes:
            messagestr += f'#{counter}. {quote}\n'
            counter += 1
        messagestr += '```'
        return messagestr
    else:
        return None

def add_quote(serverid, quote, customcommandname=None):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    if quote != '' and not quote.isspace():
        if customcommandname == None:
            servers[f'sid{serverid}']['quotes'].append(quote)
            quotes = servers[f'sid{serverid}']['quotes']
        else:
            counter = 0
            for command in servers[f'sid{serverid}']['customcommands']:
                if command['name'] == customcommandname:
                   if command['type'] == 'quote' or command['type'] == 'quotesys':
                       customcommandindex = counter
                       break
                counter += 1

            servers[f'sid{serverid}']['customcommands'][customcommandindex]['content'].append(quote)
            quotes = servers[f'sid{serverid}']['customcommands'][customcommandindex]['content']

        with open('servers.json', 'w') as f:
            json.dump(servers, f, indent=4)
        return f'Added quote #{len(quotes) - 1}: {quote}'
    else:
        return 'Quote cannot be whitespace or empty.'

def remove_quote(serverid, index, customcommandname=None):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    try:
        if customcommandname == None:
            quotes = servers[f'sid{serverid}']['quotes']
        else:
            for command in servers[f'sid{serverid}']['customcommands']:
                if command['name'] == customcommandname:
                   if command['type'] == 'quote' or command['type'] == 'quotesys':
                    quotes = command['content']
                    break
                else:
                    quotes = []
    except KeyError:
        quotes = []

    if len(quotes) > 0:
        if index == None:
            return 'Couldn\'t delete quote; no index given.'
        else:
            quotenum = index

            try:
                quote = quotes[quotenum]
                if customcommandname == None:
                    servers[f'sid{serverid}']['quotes'].pop(quotenum)
                else:
                    counter = 0
                    for command in servers[f'sid{serverid}']['customcommands']:
                        if command['name'] == customcommandname:
                            if command['type'] == 'quote' or command['type'] == 'quotesys':
                                customcommandindex = counter
                                break
                        counter += 1

                    servers[f'sid{serverid}']['customcommands'][customcommandindex]['content'].pop(quotenum)

                with open('servers.json', 'w') as f:
                    json.dump(servers, f, indent=4)

                return f'Removed quote #{quotenum}: {quote}'
            except IndexError:
                print('Index out of range.')
                return f'Quote #{quotenum} does not exist.'
    else:
        return 'There are no quotes to remove.'

def remove_all_quotes(serverid, customcommandname=None):
    with open('servers.json', 'r') as f:
        servers = json.load(f)

    try:
        if customcommandname == None:
            del servers[f'sid{serverid}']['quotes'][:]
        else:
            counter = 0
            for command in servers[f'sid{serverid}']['customcommands']:
                if command['name'] == customcommandname:
                   if command['type'] == 'quote' or command['type'] == 'quotesys':
                       customcommandindex = counter
                       break
                counter += 1

            del servers[f'sid{serverid}']['customcommands'][customcommandindex]['content'][:]

        with open('servers.json', 'w') as f:
            json.dump(servers, f, indent=4)

        return 'Removed all quotes.'
    except KeyError:
        return 'There are no quotes to remove.'
