import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()
ID_MY_SERVER = os.environ["MY_SERVER"]

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="使い方"
    )
    async def help(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer()
        with open("./help.md", "r", encoding="utf-8") as file:
            message = file.read()
        await interaction.followup.send(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot),guilds = [discord.Object(id=ID_MY_SERVER)])
