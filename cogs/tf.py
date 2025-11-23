import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Tf(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="tf",
        description="convert emoji into picture"
    )
    @app_commands.describe(
        emoji_name='emoji_name'
    )
    async def tf(
        self,
        interaction: discord.Interaction,
        emoji_name: str
    ):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        for emoji in guild.emojis:
            if emoji.name == emoji_name:
                await interaction.followup.send(emoji.url)
                return
        await interaction.followup.send("not found", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Tf(bot))
