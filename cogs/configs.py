import json

import discord
from discord.ext import commands

DEFAULT_PREFIX = '$'


class Configs(commands.Cog, name='Config Commands'):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    # TODO: check if user has admin perms / is a mod
    def cog_check(self, ctx) -> bool:
        return True

    @commands.hybrid_command(name='prefix')
    async def change_prefix(self, ctx, new_prefix):
        response_message = ''
        try:
            with open('/app/data/prefixes.json', 'r+', encoding='UTF-8') as file:
                prefixes = json.load(file)
                prefixes[str(ctx.guild.id)] = new_prefix

                # overwrite file with new data
                file.seek(0)
                file.truncate()
                json.dump(prefixes, file)
        except IOError:
            response_message = 'Exception when updating prefix'
        else:
            response_message = f'Prefix successfully set to {new_prefix}'

        if ctx.interaction is not None:
            await ctx.interaction.response.send_message(response_message)
        else:
            await ctx.send(response_message)


async def setup(client):
    await client.add_cog(Configs(client))
