import os

import discord
from discord.ext import commands

import clickergame

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = '$', intents = intents)

@client.event
async def on_ready():
    print(f'{client.user} up and running')

@client.command(name = 'clicker')
async def _test(ctx):
    await clickergame.command(ctx = ctx)

client.run(os.environ['TOKEN'], reconnect = True)