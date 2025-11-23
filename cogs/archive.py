import os
import re
import datetime
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()

TOKEN = os.environ["TOKEN"]

ID_MY_SERVER = int(os.environ['MY_SERVER'])

ARCHIVE_CHANNEL = int(os.environ['ARCHIVE_CHANNEL'])

TEMP_CHANNEL = int(os.environ['TEMP_CHANNEL'])

ARCHIVE_CRITERION = int(os.environ['ARCHIVE_CRITERION'])

COLOR_EMBED = int(os.environ['COLOR_EMBED'], 0)
COLOR_ARCHIVE = int(os.environ['COLOR_ARCHIVE'], 0)

ARCHIVE_EMOJI = os.environ['ARCHIVE_EMOJI']

URL_REGEX = r"https://discord.com/channels/(?P<guild>[0-9]{17,20})/(?P<channel>[0-9]{17,20})/(?P<message>[0-9]{17,20})"

class Archive(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="archive",
        description="archive message"
    )
    @app_commands.describe(
        message_url='url'
    )
    async def archive(
        self,
        interaction: discord.Interaction,
        message_url:str
    ):

        await interaction.response.defer(ephemeral=True)
        channel = self.bot.get_channel(ARCHIVE_CHANNEL)
        messages = []
        for idx in re.finditer(URL_REGEX, message_url):
            try:
                ms = await self.bot.get_channel(int(idx["channel"])).fetch_message(int(idx["message"]))
                messages.append(ms)
            except:
                pass
        for message in messages:
            embed = await make_embed(self.bot, message, COLOR_ARCHIVE)
            await channel.send(embed=embed)
        await interaction.followup.send("完了", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Archive(bot),guilds = [discord.Object(id=ID_MY_SERVER)])

async def make_embed(bot, message, color_code):
    embed = discord.Embed(
        color=color_code, description=message.clean_content)
    embed.set_author(name=message.author.display_name,
                        icon_url=message.author.display_avatar.url, url=message.jump_url)
    time = (message.created_at + datetime.timedelta(hours=9)
            ).strftime("%Y/%m/%d %H:%M")
    name = message.channel.name
    embed.set_footer(text=f"{name}   {time}   {message.id}")
    for attachment in message.attachments:
        f = await attachment.to_file(filename="image.png")
        tmpmsg = await bot.get_channel(TEMP_CHANNEL).send(file=f)
        embed.set_image(url=tmpmsg.attachments[0].proxy_url)
    return embed
