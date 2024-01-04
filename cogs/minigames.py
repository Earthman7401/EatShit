"""
Contains the cog for minigame commands and a setup function to load the extension.
"""
import json
import random

import discord
from discord.ext import commands


class Minigames(commands.Cog, name='Minigames'):
    """
    All sorts of minigame commands.
    """
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        self.client = client

    async def handle_button_press(self, interaction: discord.Interaction, correct: bool) -> None:
        """
        Handles user pressing the buttons in the interaction.

        If the user presses the correct button, increment their score.
        If not, reset their score.

        Args:
            interaction (discord.Interaction): The interaction for the minigame.
            correct (bool): Whether the button pressed was the correct one.
        """
        with open('/app/data/clickergame_score.json', 'r+', encoding = 'UTF-8') as file:
            json_object = json.load(file)

            # update score
            if correct:
                if str(interaction.guild_id) not in json_object:
                    json_object[str(interaction.guild_id)] = 1
                else:
                    json_object[str(interaction.guild_id)] += 1
            else:
                json_object[str(interaction.guild_id)] = 0

            # overwrite file with new data
            file.seek(0)
            file.truncate()
            json.dump(json_object, file)

            # disable buttons and send response
            if interaction.message is not None:
                view = discord.ui.View.from_message(interaction.message)
            for child in view.children:
                child.disabled = True
            await interaction.response.edit_message(view = view)

            if correct:
                await interaction.followup.send(f'current streak: {json_object[str(interaction.guild_id)]}')
                await self.clicker(interaction = interaction)
            else:
                await interaction.followup.send(f'and there we go {interaction.user.mention} fucked it up\nscore has been reset')

    async def correct_pressed(self, interaction: discord.Interaction) -> None:
        """
        Callback function for when the user presses the correct button.

        Args:
            interaction (discord.Interaction): The interaction containing the button.
        """
        await self.handle_button_press(interaction, True)

    async def incorrect_pressed(self, interaction: discord.Interaction) -> None:
        """
        Callback function for when the user presses the incorrect button.

        Args:
            interaction (discord.Interaction): The interaction containing the button.
        """
        await self.handle_button_press(interaction, False)

    class ButtonList(discord.ui.View):
        """
        The button list for clickergame.
        """
        def __init__(self, *, timeout: float = None, correct: bool, clicker) -> None:
            super().__init__(timeout = timeout)

            #create buttons
            for i in range(5):
                button = discord.ui.Button(style = discord.ButtonStyle.green if i == correct else discord.ButtonStyle.gray, label = str(i))
                button.callback = clicker.correct_pressed if i == correct else clicker.incorrect_pressed
                self.add_item(button)

    async def clicker(self, ctx: commands.Context = None, interaction: discord.Interaction = None) -> None:
        """
        Starts the minigame "clicker".

        Args:
            ctx (commands.Context, optional): The commands.Context provided by command invocation. Defaults to None.
            interaction (discord.Interaction, optional): The last discord.Interaction from the command invocation. Defaults to None.
        """
        view = self.ButtonList(correct = random.randint(0, 4), clicker = self)
        if ctx is not None:
            await ctx.send('Press the green button', view = view)
        elif interaction is not None:
            await interaction.message.channel.send('Press the green button', view = view)

    @commands.hybrid_command(name='clicker')
    async def _clicker(self, ctx: commands.Context) -> None:
        await self.clicker(ctx)


async def setup(client: commands.Bot) -> None:
    """
    Loads the cog Minigames into the bot.

    This is automatically called by commands.Bot.load_extension() and **is not meant to be called directly**.

    Args:
        client (commands.Bot): The bot to load the cog into.
    """
    await client.add_cog(Minigames(client))
