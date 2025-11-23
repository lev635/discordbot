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
        super().__init__(
            command_prefix="/",
            intents=discord.Intents.all(),
        )

    async def setup_hook(self):
        for cog in INITIAL_EXTENSIONS:
            await self.load_extension(cog)
        await self.tree.sync()

    async def on_ready(self):
        await self.change_presence(
            status=discord.Status.idle
        )

yukari().run(TOKEN)