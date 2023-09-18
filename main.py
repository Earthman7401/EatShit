import os

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = '$', intents = intents)

@client.event
async def on_ready():
	print(f'{client.user} up and running')

@client.command(name = 'test')
async def _test(ctx):
	view = discord.ui.View()
	item = discord.ui.Button(style = discord.ButtonStyle.green, label = 'hi', url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')
	view.add_item(item = item)
	await ctx.send('i made a button lmao', view = view)

client.run(os.environ['TOKEN'], reconnect = True)