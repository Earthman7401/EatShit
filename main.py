import os

import discord
from discord.ext import commands

import clickergame
import prefix

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = prefix.get_prefix, intents = intents)

@client.event
async def on_ready():
    print(f'{client.user} up and running')

@client.command(name = 'clicker')
async def _clicker(ctx):
    await clickergame.command(ctx)

@client.command(name = 'prefix')
async def _prefix(ctx, arg):
    await prefix.change_prefix(ctx, arg)

client.run(os.environ['TOKEN'], reconnect = True)