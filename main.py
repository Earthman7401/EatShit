import os
import sys

import discord
from discord.ext import commands

import clickergame
import prefix

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix=prefix.get_prefix, intents=intents)


@client.event
async def on_ready():
    print('Adding cogs...')
    with open('/app/cogs/coglist.txt', 'r', encoding = 'UTF-8') as infile:
        cog_list = infile.readlines()
        for item in cog_list:
            item = item[:-1]
            try:
                await client.load_extension(f'cogs.{item}')
            except commands.ExtensionAlreadyLoaded:
                print(f'Cog {item} is already loaded')
            except commands.ExtensionNotFound:
                print(f'Cog {item} not found')

    print(f'{client.user} up and running')


@client.hybrid_command(name='clicker')
async def _clicker(ctx):
    await clickergame.command(ctx)


client.run(os.environ['TOKEN'], reconnect=True)
