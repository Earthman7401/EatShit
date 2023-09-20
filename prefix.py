import json

import discord
from discord.ext import commands

DEFAULT_PREFIX = '$'

async def get_prefix(bot, message):
    with open('data.json', 'r', encoding = 'UTF-8') as infile:
        prefixes = json.load(infile)
        if prefixes[str(message.guild.id)] is not None:
            return commands.when_mentioned_or(prefixes[str(message.guild.id)])
        else:
            commands.when_mentioned_or(DEFAULT_PREFIX)

async def change_prefix(ctx, new_prefix: str):
    try:
        with open('data.json', 'r+', encoding = 'UTF-8') as file:
            prefixes = json.load(file)
            prefixes[str(ctx.guild.id)] = new_prefix

            # overwrite file with new data
            file.seek(0)
            file.truncate()
            json.dump(prefixes, file)
    except IOError as error:
        ctx.send(f'Exception when updating prefix {error}')
    else:
        ctx.send(f'Prefix successfully set to {new_prefix}')
