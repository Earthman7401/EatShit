import json

import discord
from discord.ext import commands

DEFAULT_PREFIX = '$'


def get_prefix(bot, message):
    with open('/app/data/prefixes.json', 'r', encoding='UTF-8') as infile:
        prefixes = json.load(infile)
        if str(message.guild.id) in prefixes:
            return prefixes[str(message.guild.id)]
        else:
            return DEFAULT_PREFIX
