import os

import discord
from discord.ext import commands


class DevCommands(commands.Cog, name='Developer Commands'):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    # check if command sender is me
    def cog_check(self, ctx) -> bool:
        return str(ctx.author.id) == os.environ['DEVELOPER_ID']

    @commands.hybrid_command(name='sync')
    async def _sync(self, ctx):
        if ctx.interaction is not None:
            await ctx.interaction.response.send_message('Syncing...')
        else:
            await ctx.send('Syncing...')

        try:
            synced_commands = await self.client.tree.sync()
            await ctx.send(f'{len(synced_commands)} commands synced: {synced_commands}')
        except Exception as e:
            await ctx.send('Error when syncing commands')
            


async def setup(client):
    await client.add_cog(DevCommands(client))
