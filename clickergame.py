import json
import random

import discord
from discord.ext import commands


async def correct_pressed(interaction: discord.Interaction):
    with open('./data/clickergame_score.json', 'r+') as file:
        json_object = json.load(file)
        
        # update score
        if str(interaction.guild_id) not in json_object:
            json_object[str(interaction.guild_id)] = 1
        else:
            json_object[str(interaction.guild_id)] += 1
        await interaction.response.send_message(f'current streak: {json_object[str(interaction.guild_id)]}')

        # overwrite file with new data
        file.seek(0)
        file.truncate()
        json.dump(json_object, file)

    # restart command
    await command(interaction = interaction)
async def incorrect_pressed(interaction: discord.Interaction):
    with open('./data/clickergame_score.json', 'r+') as file:
        json_object = json.load(file)

        #update score
        json_object[str(interaction.guild_id)] = 0
        await interaction.response.send_message(f'and there we go {interaction.user.mention} fucked it up\nscore has been reset')

        # overwrite file with new data
        file.seek(0)
        file.truncate()
        json.dump(json_object, file)

class ButtonList(discord.ui.View):
    def __init__(self, *, timeout = None, correct):
        super().__init__(timeout = timeout)
        for i in range(5):
            button = discord.ui.Button(style = discord.ButtonStyle.green if i == correct else discord.ButtonStyle.gray, label = str(i))
            button.callback = correct_pressed if i == correct else incorrect_pressed
            self.add_item(button)
            

async def command(ctx = None, interaction = None):
    view = ButtonList(correct = random.randint(0, 4))
    if ctx is not None:
        await ctx.send('Press the green button', view = view)
    elif interaction is not None:
        await interaction.message.channel.send('Press the green button', view = view)
    