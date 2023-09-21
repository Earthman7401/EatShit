import json

import discord
from discord.ext import commands

DEFAULT_PREFIX = '$'

def get_prefix(bot, message):
    with open('./data/prefixes.json', 'r', encoding = 'UTF-8') as infile:
        prefixes = json.load(infile)
        if str(message.guild.id) in prefixes:
            return prefixes[str(message.guild.id)]
        else:
            return DEFAULT_PREFIX

async def change_prefix(ctx, new_prefix: str):
    try:
        with open('./data/prefixes.json', 'r+', encoding = 'UTF-8') as file:
            prefixes = json.load(file)
            prefixes[str(ctx.guild.id)] = new_prefix

            # overwrite file with new data
            file.seek(0)
            file.truncate()
            json.dump(prefixes, file)
    except IOError as error:
        await ctx.send(f'Exception when updating prefix {error}')
    else:
        await ctx.send(f'Prefix successfully set to {new_prefix}')
