"""
Contains the cog for developer commands and a setup function to load the extension.
"""
import os

import discord
from discord.ext import commands


class DevCommands(commands.Cog, name='Developer Commands'):
    """
    Commands intended only for developer use.
    These commands should not be accessible to anyone but the developer.
    """
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        self.client = client

    def cog_check(self, ctx: commands.Context) -> bool:
        """
        Checks if user has permission to use commands in this cog.

        In this case, the condition is only met when the user is the developer.

        Args:
            ctx (commands.Context): The commands.Context provided by command invocation.

        Returns:
            bool: Whether the user meets the requirements to use the commands.
        """
        return str(ctx.author.id) == os.environ['DEVELOPER_ID']

    @commands.hybrid_command(name='sync')
    async def _sync(self, ctx: commands.Context) -> None:
        """
        Syncs the appCommands in the command tree.

        Args:
            ctx (commands.Context): The commands.Context provided by command invocation.
        """
        if ctx.interaction is not None:
            await ctx.interaction.response.send_message('Syncing...')
        else:
            await ctx.send('Syncing...')

        try:
            synced_commands = await self.client.tree.sync()
            await ctx.send(f'{len(synced_commands)} commands synced: {[command.name for command in synced_commands]}')
        except (discord.HTTPException, discord.DiscordException):
            await ctx.send('Error when syncing commands')


async def setup(client):
    """
    Loads the cog DevCommands into the bot.

    This is automatically called by commands.Bot.load_extension() and **is not meant to be called directly**.

    Args:
        client (commands.Bot): The bot to load the cog into.
    """
    await client.add_cog(DevCommands(client))
