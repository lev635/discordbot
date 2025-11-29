import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.environ["TOKEN"]

INITIAL_EXTENSIONS = [
    "cogs.help",
    "cogs.archive",
    "cogs.tf",
    "cogs.back"
]

class yukari(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix="/",
            intents=intents,
        )

    async def setup_hook(self):
        for cog in INITIAL_EXTENSIONS:
            await self.load_extension(cog)
        await self.tree.sync()

yukari().run(TOKEN)
