import json

import discord
from discord.ext import commands

DEFAULT_PREFIX = '$'


class Configs(commands.Cog, name = 'Config Commands'):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def cog_check(self, ctx) -> bool:
        with open('/app/data/mod_roles.json', 'r', encoding = 'UTF-8') as infile:
            mod_roles = json.load(infile)

            # get the intersection of mod_roles and ctx.author.roles
            if ctx.guild.id in mod_roles:
                intersection = [role for role in ctx.author.roles if str(role.id) in mod_roles[str(ctx.guild.id)]]
            else:
                intersection = []
            return len(intersection) > 0 or ctx.author.guild_permissions.administrator

    @commands.hybrid_command(name = 'prefix')
    async def change_prefix(self, ctx, new_prefix):
        response_message = ''
        try:
            with open('/app/data/prefixes.json', 'r+', encoding = 'UTF-8') as file:
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

    @commands.hybrid_command(name = 'addmodrole')
    async def add_mod_role(self, ctx):
        selection = discord.ui.RoleSelect()
        view = discord.ui.View()

        async def callback(interaction):
            try:
                with open('/app/data/mod_roles.json', 'r+', encoding = 'UTF-8') as file:
                    role_list = json.load(file)

                    # create list if it doesn't exist
                    if str(interaction.guild_id) not in role_list:
                        role_list[str(interaction.guild_id)] = []

                    if str(selection.values[0].id) not in role_list[str(interaction.guild_id)]:
                        role_list[str(interaction.guild_id)].append(str(selection.values[0].id))
                        await interaction.response.send_message(f'Successfully added {selection.values[0].name} to mod roles')
                    else:
                        await interaction.response.send_message(f'{selection.values[0].name} already added')

                    # overwrite file with new data
                    file.seek(0)
                    file.truncate()
                    json.dump(role_list, file)
            except IOError:
                await interaction.response.send_message('Exception when updating mod roles')

        selection.callback = callback
        view.add_item(selection)

        if ctx.interaction is not None:
            await ctx.interaction.response.send_message('Choose a role to add to the list of mod roles', view = view)
        else:
            await ctx.send('Choose a role to add to the list of mod roles', view = view)

    @commands.hybrid_command(name = 'modroles')
    async def mod_roles(self, ctx):
        embed = discord.Embed()

        with open('/app/data/mod_roles.json', 'r', encoding = 'UTF-8') as infile:
            role_list = json.load(infile)

            # get mention strings of roles, separated by newline
            if str(ctx.guild.id) not in role_list:
                role_mentions = ''
            else:
                role_mentions = '\n'.join([role.mention for role in [discord.utils.get(ctx.guild.roles, id = int(id)) for id in role_list[str(ctx.guild.id)]]])
            embed.add_field(name = 'Roles', value = role_mentions)
        await ctx.send(embed = embed, allowed_mentions = discord.AllowedMentions.all())

async def setup(client):
    await client.add_cog(Configs(client))
