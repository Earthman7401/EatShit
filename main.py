"""
This is the script executed by docker when the container starts.

To start the program in docker, run:

    $ docker compose up --build

"""
import os

import discord
from discord.ext import commands

import prefix

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix=prefix.get_prefix, intents=intents)


@client.event
async def on_ready():
    """
    This is automatically called when the bot has connected to discord.

    Loads cogs for the bot.
    """
    print('Adding cogs...')

    # theres a __pycache__ file in there for some reason???
    # anyways that slice is to exclude that file
    for filename in os.listdir('./cogs')[1:]:
        try:
            # excluding last 3 characters because it's '.py'
            print(f'Loading cog: {filename}')
            await client.load_extension(f'cogs.{filename}'[:-3])
        except commands.ExtensionAlreadyLoaded:
            print(f'Cog {filename} is already loaded')
        except commands.ExtensionNotFound:
            print(f'Cog {filename} not found')

    print(f'{client.user} up and running')

def main():
    """
    Main entry point of program.

    Starts up the bot.
    """
    client.run(os.environ['TOKEN'], reconnect=True)


if __name__ == '__main__':
    main()
