"""
Gets server specific prefix for bot
"""
import json

import discord
from discord.ext import commands

DEFAULT_PREFIX = '$'

def get_prefix(_: commands.Bot, message: discord.Message) -> str:
    """
    Gets server specific prefix for bot.
    
    This is automatically called whenever a user sends a message and **is not meant to be called directly**.

    Args:
        _ (commands.Bot): The bot to get the prefix for. This is unused in the function.
        message (discord.Message): The message that was sent in the server.

    Returns:
        str: The prefix for the given server.
    """
    with open('/app/data/prefixes.json', 'r', encoding='UTF-8') as infile:
        prefixes = json.load(infile)
        if str(message.guild.id) in prefixes:
            return prefixes[str(message.guild.id)]
        else:
            return DEFAULT_PREFIX
